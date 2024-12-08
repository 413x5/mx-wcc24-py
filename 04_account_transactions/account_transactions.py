from multiversx_sdk import (
    Address, UserWallet, UserSecretKey, 
)
import requests
from pathlib import Path
import json

ROOT_PATH = Path(__file__).parent.parent
TRANSACTIONS_FILE = Path(__file__).parent / "transactions.json"
PASSFILE_PATH = ROOT_PATH/"wallets_password.txt"
ACC_JSON_PATH = ROOT_PATH/"_accounts/json"


BATCH_SIZE = 100 # Number of transactions to fetch in each batch
API_URL = "https://devnet-api.multiversx.com"  # MultiversX API endpoint


def read_accounts_password():
    with open(PASSFILE_PATH, "r") as f:
        return f.read().strip()

def get_accounts():
    accounts = []
    for json_file in ACC_JSON_PATH.glob("*.json"):
        accounts.append(json_file)
    return accounts

def get_account_transactions_from_api(address, from_idx=0, size=100):
    api_url = f"{API_URL}/accounts/{address}/transactions"
    params = {
        'from': from_idx,
        'size': size
    }
    headers = {
        'accept': 'application/json'
    }
    
    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching transactions: {e}")
        return None

def get_transaction_count(address):
    api_url = f"{API_URL}/accounts/{address}/transactions/count"
    headers = {
        'accept': 'application/json'
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching transaction count: {e}")
        return None

def get_transactions(address, tx_count = None):
    if tx_count is None:
        tx_count = get_transaction_count(address)
        if tx_count is None:
            return None
        
    transactions = []
    batch_size = BATCH_SIZE
    
    for from_idx in range(0, tx_count, batch_size):
        print(f"Fetching transactions {from_idx + 1} to {min(from_idx + batch_size, tx_count)}...")
        batch = get_account_transactions_from_api(address, from_idx, batch_size)
        if batch:
            transactions.extend(batch)
        else:
            break
            
    return transactions

def display_transactions(transactions):
    if not transactions:
        print("No transactions found or error occurred")
        return
    
    print("\nTransaction History:")
    print("-" * 80)
    
    for tx in transactions:
        print(f"Transaction Hash: {tx.get('txHash')}")
        print(f"Receiver: {tx.get('receiver')}")
        print(f"Function: {tx.get('function')}")
        print(f"Status: {tx.get('status')}")
        print("-" * 80)

def save_transactions_to_json(transactions_data, append=False):
    if append and TRANSACTIONS_FILE.exists():
        # Read existing data
        with open(TRANSACTIONS_FILE, "r") as f:
            existing_data = json.load(f)
        # Update with new data
        existing_data.update(transactions_data)
        transactions_data = existing_data
    
    with open(TRANSACTIONS_FILE, "w") as f:
        json.dump(transactions_data, f, indent=4)
    print(f"\nTransactions saved to: {TRANSACTIONS_FILE}")

def main():

    password = read_accounts_password()
    accounts = list(ACC_JSON_PATH.glob("*.json"))

    if not accounts:
        print("No token owner accounts found. Run the generate_accounts script first.")
        return

    for account_json in accounts:
        userSecretKey = UserWallet.load_secret_key(Path(account_json), password)
        account_address = userSecretKey.generate_public_key().to_address()
        address = account_address.to_bech32()

        tx_count = get_transaction_count(address)
        print(f"\nAccount: {address}")
        print(f"Transaction count: {tx_count}")
        
        input("Press any key to fetch transactions...")     
        transactions = get_transactions(address, tx_count)
        display_transactions(transactions)

        # Save transactions for this account immediately
        if transactions:
            save_transactions_to_json({address: transactions}, append=True)

if __name__ == "__main__":
    main()