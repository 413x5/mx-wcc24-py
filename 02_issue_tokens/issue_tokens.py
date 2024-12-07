from multiversx_sdk import (
    Address, UserWallet, UserSecretKey, ProxyNetworkProvider, 
    Transaction, TransactionComputer, UserSigner, AccountNonceHolder, 
    TokenManagementTransactionsFactory, TransactionsFactoryConfig,
)
from multiversx_sdk.network_providers.transactions import TransactionOnNetwork
from multiversx_sdk.converters.transactions_converter import TransactionsConverter
from pathlib import Path
import time

CHAIN = "D"
GATEWAY = "https://devnet-gateway.multiversx.com"
PROXY = ProxyNetworkProvider(GATEWAY)

TOKENS_PER_ACCOUNT=1
TOKEN_NAME="WICT" #"WinterIsComing"
TOKEN_TICKER_NAME="WINTER"
TOKEN_INITIAL_SUPPLY=100000000
TOKEN_DECIMALS=8

ROOT_PATH = Path(__file__).parent.parent
PASSFILE_PATH = ROOT_PATH/"wallets_password.txt"
ACC_JSON_PATH = ROOT_PATH/"_accounts/json"
TOKEN_FILE_PATH = ROOT_PATH/"_tokens"


def save_token_file(ticker: str):
    token_file = TOKEN_FILE_PATH / f"{ticker}"
    with open(token_file, "w") as f:
        f.write(ticker)
    print(f"Token file saved to {token_file}")


def process_transaction_result(tx_hash: str):

    print("Process transaction hash:", tx_hash)

    #sometimes there is a delay before the transaction is immediately available
    retries=0
    while(True):
        try:
            time.sleep(3)
            if(retries>10): 
                print("Retry limit exceeded. Transaction not found")
                return
            tx_on_network = PROXY.get_transaction(tx_hash, True)
            if(tx_on_network is not None): break #transaction found
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Retrying...")
        finally:    
            retries+=1

    pending = None
    while(tx_on_network.status.is_pending()):    
        if(pending is None):
            pending = True
            print("Transaction is pending...")         

        tx_on_network = PROXY.get_transaction(tx_hash, True)
        time.sleep(5)

    print(f"Transaction status: {tx_on_network.status}")

    if(tx_on_network.status.is_successful()):
        converter = TransactionsConverter()
        transaction_outcome = converter.transaction_on_network_to_outcome(tx_on_network)

        for event in transaction_outcome.logs.events:
            if(event.identifier == "issue"):
                ticker = event.topics[0].decode()
                print(f"Successfully issued token {ticker}")
                save_token_file(ticker)
                return
        print(f"Cannot find issue event in transaction {tx_hash}")
    else:
        print(f"Transaction {tx_hash} failed")


def issue_tokens_for_account(address: Address, userSigner: UserSigner):
    try:
        account_on_network = PROXY.get_account(address)
        nonce_holder = AccountNonceHolder(account_on_network.nonce)
        
        for i in range(TOKENS_PER_ACCOUNT):
            
            factory = TokenManagementTransactionsFactory(TransactionsFactoryConfig(CHAIN))
            tx = factory.create_transaction_for_issuing_fungible(
                sender=address,
                token_name=TOKEN_NAME,
                token_ticker=TOKEN_TICKER_NAME,
                initial_supply=TOKEN_INITIAL_SUPPLY*10**TOKEN_DECIMALS,
                num_decimals=TOKEN_DECIMALS,
                can_freeze=True,
                can_wipe=True,
                can_pause=True,
                can_change_owner=True,
                can_upgrade=True,
                can_add_special_roles=True
            )
            
            tx.nonce = nonce_holder.get_nonce_then_increment()
            transaction_computer = TransactionComputer()
            bytes_to_sign = transaction_computer.compute_bytes_for_signing(tx)
            tx.signature = userSigner.sign(bytes_to_sign)
            
            print("Sending issue transaction...")
            tx_hash = PROXY.send_transaction(tx)
            process_transaction_result(tx_hash)
            
    except Exception as e:
        print(f"Error for address {address.to_bech32()}: {str(e)}")


def issue_tokens():
    try:
        with open(PASSFILE_PATH, "r") as passfile:
            password = passfile.read()

        json_files = list(ACC_JSON_PATH.glob("*.json"))
        if len(json_files) == 0:
            print(f"No accounts files found in {ACC_JSON_PATH}. \nUse the generate_accounts script first.")
            return
        
        for json_file_path in json_files:
            userSecretKey = UserWallet.load_secret_key(Path(json_file_path), password)
            address = userSecretKey.generate_public_key().to_address()
            signer = UserSigner.from_wallet(Path(json_file_path), password)
            print(f"\nCreating tokens for account: {address.to_bech32()}")
            issue_tokens_for_account(address, signer) 

    except Exception as e:
        print(f"Error: {str(e)}")
        

def main():
    print("\nStarting...\n")
    if not TOKEN_FILE_PATH.exists(): TOKEN_FILE_PATH.mkdir(parents=True, exist_ok=True)

    issue_tokens()
    
    print("\nEnd.\n")

if __name__ == "__main__":
    main()