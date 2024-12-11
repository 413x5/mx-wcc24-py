"""
This script transfers tokens from owner accounts to receivers.
Loads user wallets and initiates token transfers.
"""
from pathlib import Path
import time

from multiversx_sdk import (
    Address, UserWallet, UserSecretKey, ProxyNetworkProvider,
    TransactionComputer, UserSigner, AccountNonceHolder,
    TransactionsFactoryConfig, TransferTransactionsFactory,
    TokenTransfer, Token
)

CHAIN = "D"
GATEWAY = "https://devnet-gateway.multiversx.com"
PROXY = ProxyNetworkProvider(GATEWAY)

TOKEN_DECIMALS = 8
TRANSFER_AMOUNT = 10000
RECEIVERS_COUNT = 1000
TRANSACTIONS_BATCH_SIZE = 100  # Number of transactions to send in each batch

ROOT_PATH = Path(__file__).parent.parent
PASSFILE_PATH = ROOT_PATH/"wallets_password.txt"
ACC_JSON_PATH = ROOT_PATH/"_accounts/json"
TOKEN_FILE_PATH = ROOT_PATH/"_tokens"
RECEIVERS_FILE = ROOT_PATH/"receivers.txt"


def read_accounts_password():
    """
    Reads and returns the password for wallet accounts from the password file.
    Returns:
        str: The password string with whitespace trimmed
    """
    with open(PASSFILE_PATH, "r", encoding="utf-8") as f:
        return f.read().strip()


def get_owner_accounts():
    """
    Retrieves a list of account JSON files that represent the owner's accounts.
    Returns:
        list: A list of paths to account JSON files
    """
    accounts = []
    for json_file in ACC_JSON_PATH.glob("*.json"):
        accounts.append(json_file)
    return accounts


def get_or_create_receiver_addresses(count: int):
    """
    Retrieves or generates a specified number of receiver addresses.
    If existing addresses are found in the receivers file,
    they are returned first.
    New addresses are generated if there are not enough existing ones.
    Args:
        count (int): The number of receiver addresses to retrieve or create
    Returns:
        list: A list of receiver addresses
    """
    receivers = []

    # Read existing receivers if file exists
    if RECEIVERS_FILE.exists():
        with open(RECEIVERS_FILE, "r", encoding="utf-8") as f:
            existing_receivers = [Address.from_bech32(
                line.strip()) for line in f if line.strip()]
            if len(existing_receivers) >= count:
                return existing_receivers[:count]
            else:
                receivers.extend(existing_receivers)

    # Generate new addresses if needed
    new_receivers = []
    for _ in range(count - len(receivers)):
        secret_key = UserSecretKey.generate()
        address = secret_key.generate_public_key().to_address()
        new_receivers.append(address)

    # Append new addresses to file if any were generated
    if new_receivers:
        with open(RECEIVERS_FILE, "a", encoding="utf-8") as f:
            for new_address in new_receivers:
                f.write(f"{new_address.to_bech32()}\n")
        receivers.extend(new_receivers)

    return receivers


def get_account_tokens(account: Address):
    """
    Retrieves a list of token IDs owned by the specified account.
    It reads all token files from the _tokens folder and checks
    if the owner matches the account.
    Args:
        account (Address): The address of the account to check for tokens
    Returns:
        list: A list of token IDs owned by the account
    """
    tokens = []
    address = account.to_bech32()

    # Read all token files from _tokens folder
    for token_file in TOKEN_FILE_PATH.glob("*.token"):
        try:
            # Each file contains the owner's address
            with open(token_file, "r", encoding="utf-8") as f:
                owner_address = f.read().strip()
                if owner_address == address:
                    # The token ID is the filename without the extension
                    token_id = token_file.stem
                    tokens.append(f"{token_id}")
        except Exception as e:
            print(f"Error reading token file {token_file}: {str(e)}")

    return tokens


def transfer_tokens(
        sender_address: Address,
        sender_signer: UserSigner,
        token_id: str,
        receiver_addresses: list[Address]):
    """
    Transfers a specified token from the sender's address
    to multiple receiver addresses.
    Args:
        sender_address (Address): The address of the sender
        sender_signer (UserSigner): The signer for the transaction
        token_id (str): The ID of the token to transfer
        receiver_addresses (list[Address]):
        A list of addresses to receive the token
    """
    print(f"Transferring {token_id} from {sender_address.to_bech32()} to {
          len(receiver_addresses)} receivers...")

    config = TransactionsFactoryConfig(CHAIN)
    token_transfer_factory = TransferTransactionsFactory(config)

    account_on_network = PROXY.get_account(sender_address)
    nonce_holder = AccountNonceHolder(account_on_network.nonce)
    transaction_computer = TransactionComputer()
    receiver_counter = 0
    # Split receiver addresses into batches
    for i in range(0, len(receiver_addresses), TRANSACTIONS_BATCH_SIZE):
        batch = receiver_addresses[i:i + TRANSACTIONS_BATCH_SIZE]
        transactions = []

        for receiver in batch:
            tx = token_transfer_factory.create_transaction_for_esdt_token_transfer(
                sender=sender_address,
                receiver=receiver,
                token_transfers=[
                    TokenTransfer(
                        token=Token(token_id),
                        amount=TRANSFER_AMOUNT*10**TOKEN_DECIMALS
                    )
                ]
            )

            tx.nonce = nonce_holder.get_nonce_then_increment()
            bytes_to_sign = transaction_computer.compute_bytes_for_signing(tx)
            tx.signature = sender_signer.sign(bytes_to_sign)
            transactions.append(tx)

        # Retry in case of sending error
        max_retries = 10
        retries = 0
        while True:
            try:
                if retries > max_retries:
                    print("Retry limit exceeded, exiting...")
                    return

                # Send the batch of transactions
                PROXY.send_transactions(transactions)
                # Optional: Add a delay between batches for rate limiting
                # time.sleep(1)
                receiver_counter += TRANSACTIONS_BATCH_SIZE
                print(f"Sent {TRANSFER_AMOUNT} {token_id} to {
                      receiver_counter} receivers")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
                print("Retrying...")
                time.sleep(1)
            finally:
                retries += 1


def main():
    """
    Main entry point of the script. Processes the transfer of tokens
    from owner accounts to receivers.
    Loads the password, retrieves owner accounts,
    and initiates token transfers.
    """
    password = read_accounts_password()
    owner_accounts = get_owner_accounts()
    if not owner_accounts:
        print("No token owner accounts found."
              "Run the generate_accounts script first.")
        return

    for account_json in owner_accounts:
        user_secret_key = UserWallet.load_secret_key(
            Path(account_json), password)
        sender_address = user_secret_key.generate_public_key().to_address()
        sender_signer = UserSigner.from_wallet(Path(account_json), password)

        print(f"\nProcessing account: {sender_address.to_bech32()}")

        # Get all tokens owned by this account
        tokens = get_account_tokens(sender_address)
        if not tokens:
            print("No tokens found for this account."
                  "Run the issue_tokens script first.")
            continue

        # Get receivers
        receivers = get_or_create_receiver_addresses(RECEIVERS_COUNT)

        # Transfer each token to receivers
        for token_id in tokens:
            transfer_tokens(sender_address, sender_signer, token_id, receivers)


if __name__ == "__main__":
    main()
