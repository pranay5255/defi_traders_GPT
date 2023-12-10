import requests
import datetime
import sys
import json


def get_current_block_number(api_key):
    """Fetch the current block number."""
    url = 'https://api.etherscan.io/api'
    params = {
        'module': 'proxy',
        'action': 'eth_blockNumber',
        'apikey': api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data['status'] == '1':
        return int(data['result'], 16)  # Convert hex to int
    else:
        raise Exception('Error fetching current block number')

def estimate_block_number_for_timestamp(target_timestamp, api_key):
    """Estimate the block number for a given timestamp."""
    current_block_number = get_current_block_number(api_key)
    current_timestamp = int(datetime.datetime.now().timestamp())

    average_block_time = 14  # Average block time in seconds (estimated)
    seconds_difference = current_timestamp - target_timestamp
    block_difference = seconds_difference // average_block_time
    estimated_block_number = current_block_number - block_difference
    return estimated_block_number

def get_transactions(wallet_address, start_block, end_block, api_key):
    """Fetch transactions for the given wallet address between two block numbers."""
    url = 'https://api.etherscan.io/api'
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': wallet_address,
        'startblock': start_block,
        'endblock': end_block,
        'sort': 'asc',
        'apikey': api_key
    }
    sleep(5)
    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == '1':
        return data['result']
    else:
        raise Exception('Error fetching transactions:', data['message'])

# Main script
if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    wallet_address = sys.argv[1]
    api_key = ""

    # Get current and past block numbers
    current_block = get_current_block_number(api_key)
    six_months_ago = int((datetime.datetime.now() - datetime.timedelta(days=180)).timestamp())
    past_block = estimate_block_number_for_timestamp(six_months_ago, api_key)

    # Fetch transactions
    try:
        transactions = get_transactions(wallet_address, past_block, current_block, api_key)
        filename = f'transactions_{wallet_address}.json'
        print("Writing transactions for wallet address: {}".format(wallet_address))
        with open(filename, 'w') as file:
            json.dump(data['result'], file, indent=4)
    except Exception as e:
        print(str(e))
