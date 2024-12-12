"""
This script processes each account found in the accounts directory:
- Loads the account's wallet
- Fetches the account's transactions from the MultiversX API
- Displays transaction details
- Writes the transactions to a JSON file for later use
"""
from datetime import datetime
from pathlib import Path
import json
import requests

from multiversx_sdk import Address, UserWallet, ApiNetworkProvider
from multiversx_sdk.network_providers.api_network_provider import (
    DefaultPagination, TransactionOnNetwork
)

ROOT_PATH = Path(__file__).parent.parent
TRANSACTIONS_FILE = Path(__file__).parent / "transactions.json"
PASSFILE_PATH = ROOT_PATH / "wallets_password.txt"
ACC_JSON_PATH = ROOT_PATH / "_accounts/json"


BATCH_SIZE = 100  # Number of transactions to fetch in each batch
API_URL = "https://devnet-api.multiversx.com"  # MultiversX API endpoint


def read_accounts_password():
    """
    Reads and returns the password for wallet accounts from the password file.
    Returns:
        str: The password string with whitespace trimmed
    """
    with open(PASSFILE_PATH, "r", encoding="utf-8") as f:
        return f.read().strip()


def get_accounts():
    """
    Retrieves a list of account JSON files from the accounts directory.
    Returns:
        list: A list of paths to account JSON files
    """
    accounts = []
    for json_file in ACC_JSON_PATH.glob("*.json"):
        accounts.append(json_file)
    return accounts


def get_transaction_count(address: Address):
    """
    Retrieves the total number of transactions for a specific address.
    Args:
        address (Address): The account address
    Returns:
        int: Total number of transactions, or None if an error occurs
    """
    api_url = f"{API_URL}/accounts/{address.to_bech32()}/transactions/count"
    headers = {'accept': 'application/json'}
    count = 0
    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        response.raise_for_status()
        count = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching transaction count: {e}")
    return count


def get_transactions(address: Address, count: int):
    """
    Retrieves all transactions for an address in batches.
    Args:
        address (str): The account address
        count (int): Total number of transactions
    Returns:
        list: List of all transactions, or None if an error occurs
    """
    api_provider = ApiNetworkProvider(API_URL)
    pagination = DefaultPagination()
    pagination.size = BATCH_SIZE
    pagination.start = 0
    transactions = []
    while transaction_batch := api_provider.get_account_transactions(
            address, pagination):
        if transaction_batch is None:
            break
        transactions.extend(transaction_batch)
        pagination.start += pagination.size
        print(f"Retrieved {len(transactions)} / {count} transactions...")
    return transactions


def display_transactions(transactions: list[TransactionOnNetwork]):
    """
    Displays transaction details in a formatted manner.
    Args:
        transactions (list): List of transaction dictionaries to display
    """
    if not transactions:
        print("No transactions found or error occurred")
        return

    print("\nTransaction History:")
    print("-" * 80)
    counter = 0
    for tx in transactions:
        formatted_timestamp = datetime.fromtimestamp(
            tx.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        counter += 1
        print(
            f"{counter:04d}. "
            f"{formatted_timestamp} "
            f"Hash: {tx.hash} "
            f"Value:{tx.value} "
            f"Data:{tx.data}"
        )

    print("-" * 80)


def save_transactions_to_json(
        transactions: list[TransactionOnNetwork]):
    """
    Saves transaction data to a JSON file.
    Args:
        transactions (list): List of transaction to save
    """
    transactions_data = [tx.to_dictionary() for tx in transactions]
    with open(TRANSACTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(transactions_data, f, indent=4)
    print(f"Transactions saved to: {TRANSACTIONS_FILE}")


def main():
    """
    Main entry point of the script.
    Processes each account found in the accounts directory:
    - Loads the account's wallet
    - Retrieves transaction count and transaction history
    - Displays transaction details
    - Saves transactions to a JSON file
    """
    password = read_accounts_password()
    accounts = list(ACC_JSON_PATH.glob("*.json"))

    if not accounts:
        print("No token owner accounts found."
              "Run the generate_accounts script first.")
        return

    all_transactions = []
    for account_json in accounts:
        user_secret_key = UserWallet.load_secret_key(
            Path(account_json), password)
        account_address = user_secret_key.generate_public_key().to_address()

        input(f"\nPress any key to process account: {
              account_address.to_bech32()}\n")
        tx_count = get_transaction_count(account_address)
        print(f"Transaction count: {tx_count}\n")
        account_transactions = get_transactions(account_address, tx_count)

        display_transactions(account_transactions)
        all_transactions.extend(account_transactions)

    # Save transactions to a JSON file
    if len(all_transactions) > 0 and (
            input("\nSave transactions to file? (y/n)\n")) == "y":
        save_transactions_to_json(all_transactions)


if __name__ == "__main__":
    main()
