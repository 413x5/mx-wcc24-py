# 03. Transfer Tokens

This script performs ESDT token transfers from token owners to multiple receiver addresses on the MultiversX network.

## Features

- Reads token ownership information from the [Previous Script](../02_issue_tokens/README.md)
- Generates and manages receiver addresses
- Performs token transfers with configurable amounts
- Maintains a persistent list of receiver addresses to avoid transaction spam

## Configuration Parameters

The script uses the following default parameters:

- Transfer Amount: 10,000 tokens per transfer
- Number of Receivers: 1000 addresses
- Batch Size: 100 transactions per API request

## Output Files

The script manages receiver addresses and performs transfers:

### Receiver Addresses (`receivers.txt`)

- Contains the list of receiver addresses
- New addresses are appended if needed
- Each address is stored in bech32 format

## Prerequisites

- Issued tokens from the token issuance script
- Token owner accounts with sufficient token balance

## Usage

Run the script using Python:

```bash
python3 transfer_tokens.py
```

The script will automatically:

1. Load token owner accounts
2. Read or generate receiver addresses
3. Transfer tokens from each owner to the receivers
4. Group sent transactions into batches of 100
5. Handle transaction monitoring and retries

## *Challenge proof*

1. [WINTER-3efa97](https://devnet-explorer.multiversx.com/tokens/WINTER-3efa97)
2. [WINTER-4f8d6d](https://devnet-explorer.multiversx.com/tokens/WINTER-4f8d6d)
3. [WINTER-37a258](https://devnet-explorer.multiversx.com/tokens/WINTER-37a258)
4. [WINTER-4794dc](https://devnet-explorer.multiversx.com/tokens/WINTER-4794dc)
5. [WINTER-c27ab7](https://devnet-explorer.multiversx.com/tokens/WINTER-c27ab7)
6. [WINTER-ca2868](https://devnet-explorer.multiversx.com/tokens/WINTER-ca2868)
7. [WINTER-cbfbc6](https://devnet-explorer.multiversx.com/tokens/WINTER-cbfbc6)
8. [WINTER-e7db4d](https://devnet-explorer.multiversx.com/tokens/WINTER-e7db4d)
9. [WINTER-fd400b](https://devnet-explorer.multiversx.com/tokens/WINTER-fd400b)
