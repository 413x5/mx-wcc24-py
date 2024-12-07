# MultiversX Winter Coding Challenge 2024 
### Python implementation

A collection of scripts for automating MultiversX blockchain operations.

## Environment Installation

1. Create a virtual environment (optional but recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Required packages:
- multiversx-sdk>=0.19.0

## Scripts

### 01. [Generate Accounts](01_generate_accounts/README.md) ([01_generate_accounts/](01_generate_accounts/))
Generates MultiversX accounts on devnet (3 accounts per shard) and requests xEGLD from the faucet.
Generated files are stored in:
- `_accounts/json/` - Encrypted wallet files
- `_accounts/mnemonic/` - Mnemonic phrases for each wallet

### 02. [Issue Tokens](02_issue_tokens/README.md) ([02_issue_tokens/](02_issue_tokens/))
Issues WINTER fungible tokens to each account generated in step 01 and saves the token IDs.

Generated files are stored in:
- `_tokens/` - Token IDs for each account
