# MultiversX Winter Coding Challenge 2024

## Python implementation

A collection of python scripts for automating MultiversX blockchain operations.

## Environment Installation

1. Create a virtual environment (optional but recommended):

    ```bash
    cd mx-wcc24-py
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt --upgrade
    ```

Required packages:

- multiversx-sdk>=0.19.0

## Scripts

### 01. [Generate Accounts](01_generate_accounts/README.md)

Generates MultiversX accounts on devnet (3 accounts per shard) and requests xEGLD from the faucet.

### 02. [Issue Tokens](02_issue_tokens/README.md)

Issues WINTER ESDT fungible tokens to each account generated in Step 01 and saves the token IDs.

### 03. [Transfer Tokens](03_transfer_tokens/README.md)

Performs WINTER token transfers from the tokens issued in Step 02 to multiple configurable receiver addresses.

### 04. [Account Transactions](04_account_transactions/README.md)

Retrieves and displays transaction history for MultiversX accounts generated in previous steps, using the MultiversX DevNet API.

### *[Token Smart Contract](https://github.com/413x5/mx-wcc24-rs/tree/main)*

The token manager smart contract rust implementation and instructions for issuing the SNOW ESDT tokens.

### 05. [Claim Tokens](05_claim_tokens/README.md)

Claims SNOW ESDT tokens from the token smart contract for each account in Step 01.
