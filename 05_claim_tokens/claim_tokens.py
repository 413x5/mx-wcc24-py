"""
This script claims tokens from the token manager smart contract
for all the account wallets found in the specified path.
"""
from pathlib import Path

from multiversx_sdk import (
    Address, UserWallet, ProxyNetworkProvider,
    TransactionComputer, UserSigner, AccountNonceHolder,
    TransactionsFactoryConfig, SmartContractTransactionsFactory
)

CHAIN = "D"
GATEWAY = "https://devnet-gateway.multiversx.com"
PROXY = ProxyNetworkProvider(GATEWAY)

ROOT_PATH = Path(__file__).parent.parent
PASSFILE_PATH = ROOT_PATH/"wallets_password.txt"
ACC_JSON_PATH = ROOT_PATH/"_accounts/json"

SC_ADDRESS = "erd1qqqqqqqqqqqqqpgqc50cgesrvkpurrxkclz4qql7ukg36uxjjpzqayczg3"
FUNCTION_NAME = "claim_tokens"
CLAIM_AMOUNT = 100
TOKEN_ID = "SNOW-1a790f"
TOKEN_DECIMALS = 8


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


def claim_tokens_for_account(account_address: Address, signer: UserSigner):
    """
    Claims tokens from the token manager smart contract.
    Args:
        account_address (Address): The address of the account to claim tokens
        signer (UserSigner): The signer for the account
    """
    tx_factory = SmartContractTransactionsFactory(
        TransactionsFactoryConfig(CHAIN)
    )
    # Create a transaction to call the claim_tokens function
    tx = tx_factory.create_transaction_for_execute(
        sender=account_address,
        contract=Address.from_bech32(SC_ADDRESS),
        function=FUNCTION_NAME,
        gas_limit=10000000,
        arguments=[
            TOKEN_ID,
            CLAIM_AMOUNT*10**TOKEN_DECIMALS
        ]
    )
    # get the nonce
    account_on_network = PROXY.get_account(account_address)
    nonce_holder = AccountNonceHolder(account_on_network.nonce)
    tx.nonce = nonce_holder.get_nonce_then_increment()
    # sign the transaction
    computer = TransactionComputer()
    bytes_to_sign = computer.compute_bytes_for_signing(tx)
    tx.signature = signer.sign(bytes_to_sign)
    # send the transaction
    print("Sending claim transaction...")
    tx_hash = PROXY.send_transaction(tx)
    print(f"Transaction hash: {tx_hash}")


def main():
    """
    Main entry point of the script.
    Claims tokens from the token manager smart contract.
    """
    password = read_accounts_password()
    accounts = get_accounts()

    if not accounts:
        print("No accounts found. Run the generate_accounts script first.")
        return

    # Get all account wallets
    for account_json in accounts:
        user_secret_key = UserWallet.load_secret_key(
            Path(account_json), password)
        account_address = user_secret_key.generate_public_key().to_address()
        signer = UserSigner.from_wallet(Path(account_json), password)
        # Claim tokens for each account
        print(f"\nProcessing account: {account_address.to_bech32()}")
        claim_tokens_for_account(account_address, signer)


if __name__ == "__main__":
    main()
