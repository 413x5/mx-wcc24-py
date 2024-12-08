# 02. Issue Tokens

This script issues configurable MultiversX ESDT fungible tokens.

## Features

- Issues tokens for each account generated in the [Previous Script](../01_generate_accounts/README.md)
- Creates tokens with configurable parameters (name, ticker, supply, decimals)
- Automatically processes and verifies transactions
- Handles transaction monitoring and confirmation
- Saves token information

## Configuration Parameters

The script uses the following default parameters:
- Token Name: "WinterIsComing"
- Token Ticker: "WINTER"
- Initial Supply: 100,000,000
- Token Decimals: 8
- Tokens per Account: 1

## Output Files

The script generates token information files in the `_tokens` directory:

### Token Files (`_tokens/`)
Files named in the format: `{token_ticker}.token`, containing the owner's address,

## Prerequisites

- Generated accounts from the account generator script
- Sufficient EGLD balance in the issuer account for token creation fees

## Usage

Run the script using Python:
```bash
python3 issue_tokens.py
```

The script will automatically:
1. Load the previously generated accounts
2. Issue tokens for each account
3. Save token information
4. Monitor transaction status

## *Challenge proof*

Issue transaction hashes: [txs_hash.txt](txs_hash.txt)

### [HOME](../README.md)
