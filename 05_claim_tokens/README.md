# 05. Claim Tokens

This script claims SNOW tokens from the token smart contract for each account generated in [Step 01](../01_generate_accounts/README.md).

## Prerequisites

Before running the script, ensure you have:

1. Generated wallet accounts using Step 01
2. [Token smart contract](https://github.com/413x5/mx-wcc24-rs/tree/main) deployed and having issued at least one SNOW token
3. Configured the token smart contract address in the `SC_ADDRESS` variable
3. Configure the SNOW token ID in the `TOKEN_ID` variable
4. Configure the claim amount in the `CLAIM_AMOUNT` variable
5. Sufficient EGLD in your accounts for transaction fees

## Features

- Automatically loads wallet accounts from account files
- Claims the configured amount of SNOW tokens for each account

## Usage

Run the script:

```bash
python3 claim_tokens.py
```

## Important Notes

- Script outputs the claim transaction hashes
- Transaction status can be verified on the [MultiversX DevNet Explorer](https://devnet-explorer.multiversx.com)

## *Challenge proof*

Claim transaction hashes: [transactions.txt](transactions.txt)
