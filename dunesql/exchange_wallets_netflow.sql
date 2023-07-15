with wallet_addresses AS (
SELECT *
FROM cex.addresses
WHERE cex_name IN ('Binance','Bybit','Coinbase','Bitget','Bitmart','Gate.io','OKX','Kucoin','Kraken')
limit 50
),
  eth_transfer_raw AS (
    SELECT
      "from" AS address,
      -1 * CAST(value AS DOUBLE) as amount,
      block_time
    FROM
      ethereum.traces
    WHERE
      call_type = 'call'
      AND block_time >= DATE_ADD('month', -1, DATE_TRUNC('day', now())) 
      AND success = true
      AND value > uint256 '0'
      AND "from" is NOT NULL
      AND "to" is NOT NULL
      AND "from" IN (
        SELECT
          address
        FROM
          wallet_addresses
      )
    UNION ALL
    SELECT
      "to" AS address,
      CAST(value AS DOUBLE) as amount,
      block_time
    FROM
      ethereum.traces
    WHERE
      call_type = 'call'
      AND block_time >= DATE_ADD('month', -1, DATE_TRUNC('day', now())) 
      AND success = true
      AND value > uint256 '0'
      AND "from" is NOT NULL
      AND "to" is NOT NULL
      AND "to" IN (
        SELECT
          address
        FROM
          wallet_addresses
      )
    UNION ALL
    SELECT
      "from" AS address,
      -1 * CAST(gas_price AS DOUBLE) * gas_used AS amount,
      block_time
    FROM
      ethereum.transactions
    WHERE
      success = true
      AND block_time >= DATE_ADD('month', -1, DATE_TRUNC('day', now())) 
      AND "from" IN (
        SELECT
          address
        FROM
          wallet_addresses
      )
  ),
  eth_price as (
    SELECT
      price
    FROM
      prices.usd_latest
    WHERE
      blockchain = 'ethereum'
      AND symbol = 'WETH'
  ),
transfers_with_flow as(
SELECT
  w.address,
  t.amount,
  w.cex_name,
  DATE_TRUNC('day',t.block_time) as date_txn,
  t.usd_value,
  CASE
    WHEN t.amount < 0 THEN 'outflow'
    WHEN t.amount > 0 THEN 'inflow'
    ELSE 'zero'
  END as flow
FROM
  (
    SELECT
      address,
      block_time,
      amount / 1e18 AS amount,
      amount * (SELECT
            price
          FROM
            eth_price
        ) / 1e18 as usd_value
    FROM
      eth_transfer_raw
  ) t
JOIN
  wallet_addresses w
ON
  t.address = w.address
)
SELECT
  address,
  date_txn,
  flow,
  cex_name,
  SUM(amount) as netflow,
  SUM(usd_value) as usd_value
FROM
  transfers_with_flow
GROUP BY
  address, date_txn, flow ,cex_name
