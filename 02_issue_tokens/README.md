# 02. Issue Tokens

This script issues MultiversX tokens on the devnet for each previously generated account, creating test tokens for development and testing purposes.

## Features

- Issues tokens for each account generated in the [Previous Script](../01_generate_accounts/README.md)
- Creates tokens with configurable parameters (name, ticker, supply, decimals)
- Automatically processes and verifies transactions
- Saves token information for future reference
- Handles transaction monitoring and confirmation

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
Files containing token identifiers in the format: `WINTER-a1f6d2`

## Prerequisites

- Generated accounts from the account generator script
- Sufficient EGLD balance in the issuer account for token creation fees
- MultiversX SDK Python package
- Access to MultiversX devnet

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
