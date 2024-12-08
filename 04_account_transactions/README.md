# 04. Account Transactions

This script retrieves and displays transaction history for the accounts generated in the script `01_generate_accounts`.

## Features

- Fetches transaction count for each account
- Retrieves detailed transaction information using pagination
- Displays transaction details in a formatted way
- Supports batch processing of transactions to handle large transaction counts
- Saves all transaction data to a JSON file for future reference

## Configuration Parameters

The script uses the following default parameters:
- Batch Size: 100 transactions per API request
- Display Format: Transaction hash, receiver, function name, and status

## Prerequisites

- Generated accounts from the account generation script
- Active MultiversX DevNet API access

## Usage

Run the script using Python:
```bash
python3 account_transactions.py
```

The script will automatically:
1. Load account information from the previous scripts
2. For each account:
   - Display the account address
   - Show the total transaction count
   - Fetch all transactions in batches
   - Display transaction details in a formatted way

## Output Format

For each transaction, the script displays:
- Transaction Hash
- Receiver Address
- Function Name (if applicable)
- Transaction Status

## Output Files

### Transaction Data (`transactions.json`)
- Contains all transactions for each account
- Organized by account address
- Includes detailed transaction information:
  - Transaction Hash
  - Receiver Address
  - Function Name
  - Transaction Status

## API Endpoints Used

The script interacts with the following MultiversX DevNet API endpoints:
- Transaction Count: `/accounts/{address}/transactions/count`
- Transaction Details: `/accounts/{address}/transactions?from={index}&size={batch_size}`
