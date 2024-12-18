"""
This script generates MultiversX accounts on the devnet and requests xEGLD
from the faucet for funding each account.
"""
from pathlib import Path
import subprocess

from multiversx_sdk import (
    Mnemonic, Address, AddressComputer, UserWallet
)


CHAIN = "D"
SHARDS = 3
ACCOUNTS = 3

ROOT_PATH = Path(__file__).parent.parent
PASSFILE_PATH = ROOT_PATH / "wallets_password.txt"
ACC_JSON_PATH = ROOT_PATH / "_accounts/json"
MNEMONIC_PATH = ROOT_PATH / "_accounts/mnemonic"


def read_accounts_password():
    """
    Reads and returns the password for wallet accounts from the password file.
    Returns:
        str: The password string with whitespace trimmed
    """
    with open(PASSFILE_PATH, "r", encoding="utf-8") as f:
        return f.read().strip()


def generate_account_for_shard(target_shard: int):
    """
    Generates a MultiversX wallet account for a specific shard.
    Keeps generating accounts until one matching the target shard is found.
    Args:
        target_shard (int): The target shard number for the account
    Returns:
        tuple: (UserWallet, Mnemonic, Address) containing:
            - wallet: The generated wallet object
            - mnemonic: The mnemonic phrase object
            - address: The wallet's address
    """
    address_computer = AddressComputer()
    password = read_accounts_password()

    while True:
        mnemonic = Mnemonic.generate()
        wallet = UserWallet.from_mnemonic(mnemonic.get_text(), password)
        secret_key = mnemonic.derive_key()
        public_key = secret_key.generate_public_key()
        address = Address(public_key.buffer)

        shard = address_computer.get_shard_of_address(address)
        if shard == target_shard:
            return wallet, mnemonic, address


def create_accounts():
    """
    Creates multiple MultiversX wallet accounts distributed across shards.
    For each shard and account:
    - Generates a new wallet with matching shard
    - Saves the wallet JSON file
    - Saves the mnemonic phrase to a separate file
    Creates necessary directories if they don't exist.
    """
    if not ACC_JSON_PATH.exists():
        ACC_JSON_PATH.mkdir(parents=True, exist_ok=True)
    if not MNEMONIC_PATH.exists():
        MNEMONIC_PATH.mkdir(parents=True, exist_ok=True)

    accounts = []
    # Generate accounts in each shard
    for shard in range(SHARDS):

        print(f"\nGenerating accounts for Shard {shard}:")
        for acc in range(ACCOUNTS):
            # Generate accounts
            wallet, mnemonic, address = generate_account_for_shard(shard)
            accounts.append(wallet)

            print(f"\nAccount {len(accounts)} (Shard {shard}):")
            print(f"Address: {address.bech32()}")

            # Save account files
            account_filename = f"s{shard}_a{acc + 1}_{address.bech32()}"

            # Save json files
            json_file = ACC_JSON_PATH / f"{account_filename}.json"
            wallet.save(json_file)
            print(f"Account saved to: {json_file}")

            # Save mnemonic files
            mnemonic_file = MNEMONIC_PATH / f"{account_filename}.mnemonic"
            with open(mnemonic_file, "w", encoding="utf-8") as m:
                m.write(mnemonic.get_text())
            print(f"Mnemonic saved to: {mnemonic_file}")


def fund_accounts():
    """
    Funds all generated accounts using the MultiversX faucet.
    Only works for devnet and testnet chains.
    Processes each account JSON file and calls the faucet.
    Requires mxpy CLI tool to be installed.
    """
    if (CHAIN not in ["D", "T"]):
        print("Only devnet and testnet are supported for funding accounts")
        return

    account_number = 0
    json_files = list(ACC_JSON_PATH.glob("*.json"))
    for json_file_path in json_files:
        account_number += 1
        input(f"\nPress any key to call the faucet and fund account number {
              account_number} ...")

        filename = json_file_path.name
        print(f"Execute faucet for account {filename}")

        exit_code = subprocess.run(["mxpy", "faucet", "request",
                                    "--keyfile", str(json_file_path),
                                    "--passfile", str(PASSFILE_PATH),
                                    "--chain", CHAIN], check=True)
        if exit_code.returncode != 0:
            print(f"Error executing faucet for account {
                  filename}. Check mxpy installation")

    print("\nDone.\n")


def main():
    """
    Main entry point of the script.
    Executes the account generation and funding process in sequence.
    """
    create_accounts()
    fund_accounts()


if __name__ == "__main__":
    main()
