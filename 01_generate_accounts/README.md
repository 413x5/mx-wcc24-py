# 01. Generate Accounts

This script generates MultiversX accounts on the devnet and requests xEGLD from the faucet for funding each account.

## Prerequisites

Before running the script, ensure you have:
1. Set up the Python environment (see main [README](../README.md))
2. Created a `wallets_password.txt` file in the root directory containing the password for encrypting the wallets
3. `mxpy` installed for automated faucet funding requests

## Features

- Generates 9 accounts (3 accounts for each shard). Variables SHARDS and ACCOUNTS can be configured
- Saves accounts as encrypted wallet files
- Saves mnemonic phrases separately
- Automatically requests xEGLD from the devnet faucet for each account by calling `mxpy faucet request`

## Output Files

The script generates two types of files in the `_accounts` directory:

### Wallet Files (`_accounts/json/`)
Files are named in the format: `s{shard_number}_a{account_number}_{address}.json`

### Mnemonic Files (`_accounts/mnemonic/`)
Corresponding mnemonic phrases are saved in: `s{shard_number}_a{account_number}_{address}.mnemonic`


## Usage

Run the script:
```bash
python3 generate_accounts.py
```

## Important Notes

- Keep your wallet password and mnemonic phrases secure
- The script is configured for devnet by default (CHAIN = "D")
- Current configuration: 3 shards, 3 accounts per shard (total 9 accounts)
- All wallet files are encrypted using the password from `wallets_password.txt`

### [HOME](../README.md)
