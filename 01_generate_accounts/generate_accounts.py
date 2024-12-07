from multiversx_sdk import Mnemonic, Address, AddressComputer, UserWallet, UserSecretKey, UserPublicKey
from pathlib import Path
import subprocess

CHAIN = "D"
SHARDS = 1
ACCOUNTS = 1

ROOT_PATH = Path(__file__).parent.parent
PASSFILE_PATH = ROOT_PATH/"wallets_password.txt"
ACC_JSON_PATH = ROOT_PATH/"_accounts/json"
MNEMONIC_PATH = ROOT_PATH/"_accounts/mnemonic"


def generate_account_for_shard(target_shard: int):

    address_computer = AddressComputer()
    password = open(PASSFILE_PATH, "r").read()

    while True:
        mnemonic = Mnemonic.generate()
        wallet = UserWallet.from_mnemonic(mnemonic.get_text(), password)
        secret_key = mnemonic.derive_key()
        public_key = secret_key.generate_public_key()
        address = Address(public_key.buffer)

        shard = address_computer.get_shard_of_address(address) 
        if shard == target_shard:
            return wallet, mnemonic, secret_key, address


def create_accounts():
    if not ACC_JSON_PATH.exists(): ACC_JSON_PATH.mkdir(parents=True, exist_ok=True)
    if not MNEMONIC_PATH.exists(): MNEMONIC_PATH.mkdir(parents=True, exist_ok=True)

    accounts = []
    # Generate accounts in each shard
    for shard in range(SHARDS): 
        
        print(f"\nGenerating accounts for Shard {shard}:")
        for acc in range(ACCOUNTS):
            # Generate accounts
            wallet, mnemonic, secret_key, address = generate_account_for_shard(shard)
            accounts.append(wallet)

            print(f"\nAccount {len(accounts)} (Shard {shard}):")
            print(f"Address: {address.bech32()}")

            # Save account files
            account_filename = f"s{shard}_a{acc+1}_{address.bech32()}"
            
            # Save json files
            json_file = ACC_JSON_PATH / f"{account_filename}.json"
            wallet.save(json_file)
            print(f"Json saved to: {json_file}")

            # Save mnemonic files
            mnemonic_file = MNEMONIC_PATH / f"{account_filename}.mnemonic"
            with open(mnemonic_file, "w") as m:
                m.write(mnemonic.get_text())
            print(f"Mnemonic saved to: {mnemonic_file}")

            
def fund_accounts():
    if (CHAIN != "D" and CHAIN != "T") : 
        print("Only devnet and testnet are supported for funding accounts")
        return
    
    account_number=0
    json_files = list(ACC_JSON_PATH.glob("*.json"))
    for json_file_path in json_files:
        account_number += 1
        input(f"\nPress any key to call the faucet and fund account number {account_number} ...")

        filename = json_file_path.name
        print(f"Execute faucet for account {filename}")

        exit_code = subprocess.run(["mxpy", "faucet", "request", "--keyfile", str(json_file_path), "--passfile", str(PASSFILE_PATH), "--chain", CHAIN], check=True)
        if(exit_code.returncode != 0):
            print(f"Error executing faucet for account {filename}. Check mxpy installation")
            
    print("\nDone")    


def main():
    create_accounts()
    fund_accounts()

if __name__ == "__main__":
    main()

