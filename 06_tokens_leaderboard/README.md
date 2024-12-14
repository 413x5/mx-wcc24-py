# 06. Token Leaderboard

This script generates a leaderboard of token holders for tokens with a specific identifier prefix using the MultiversX API.

## Features

- Retrieves all tokens with a specific identifier prefix (e.g., "WINTER")
- Fetches holder information for each token
- Sorts tokens by number of holders in descending order
- Displays top holders for each token with their balances
- Supports pagination for console output
- Caches holder data for faster subsequent runs
- Saves the complete leaderboard to a text file

## Configuration Parameters

The script uses the following default parameters:

- Token ID Prefix: "WINTER"
- Token Decimals: 8
- Batch Size: 1000 items per API request
- Display Top Holders: 5 holders per token
- Display Tokens Batch: 20 tokens per console page

## Prerequisites

- Active MultiversX DevNet API access
- Python 3.x with the MultiversX SDK installed

## Usage

Run the script using Python:

```bash
python3 leaderboard.py
```

The script will:

1. Check for cached holder data
   - Use existing data if available and selected
   - Or fetch fresh data from the API
2. For each token:
   - Display token information (ID, name)
   - Show total holder count
   - List top holders with their balances
3. Save the complete leaderboard to a text file

## Output Files

### Holders Data Cache (`holders_data_cache.json`)
- Contains cached holder information for all tokens
- Used to avoid unnecessary API calls in subsequent runs

### Leaderboard Output (`leaderboard_output.txt`)
- Complete leaderboard with all tokens and their top holders
- Formatted for easy reading

## API Endpoints Used

The script interacts with the following MultiversX DevNet API endpoints:

- `/tokens` - Get all fungible tokens
- `/tokens/{tokenId}/accounts` - Get token holders

## *Challenge proof*

Output: [leaderboard_output.txt](leaderboard_output.txt)
