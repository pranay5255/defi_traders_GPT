# Wallet Transactions Analysis

This document presents an analysis of wallet transactions, providing insights into wallet segmentation, transaction patterns, and characteristics of abandoned wallets.

## Overview

- **Total Wallets Analyzed:** 468
- **Total Transactions:** 115,000 individual transactions from 468 wallets
- **Key Observation:** Wallets are often abandoned, and identity is often tied to a cluster of wallets.

## Wallet Segmentation

Wallets are categorized into different segments based on their transaction patterns and characteristics.

### Criteria for Identifying Abandoned Wallets:

1. **All Funds Transferred Out:** A wallet is considered abandoned if all funds are transferred out.
2. **Zero Transaction Frequency:** If the frequency of transactions drops to zero over a certain period.
3. **Non-Smart Contract Transfers:** A high number of non-smart contract transfers is another indicator of abandonment.

## Base Insights

- **46% of Transactions Lack a Function Selector:** This suggests a significant portion of the transactions are simple ether or ERC20 transfers.
- **Unique Gas Usage Patterns:** 21,000 gas units are uniquely used in transactions without a function selector, indicating transfers to Externally Owned Accounts (EOAs).
- **Non-Smart Contract Activity:** Such activity typically does not include a contract address in the transaction data.

## Gas Calculations

Understanding gas calculations is crucial for analyzing transaction costs and behaviors.

### Equation for Maximum Fee:

**MAX FEE = Base Fee + (Priority Fee x Units of Gas Used)**

- **Base Fee:** Determined by network demand. It can increase by up to 12.5% if transactions in a block exceed the target.
- **Priority Fee:** A tip paid to validators for including the transaction in the block.


