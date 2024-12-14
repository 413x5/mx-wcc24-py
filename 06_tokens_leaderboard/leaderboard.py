'''
This script generates a leaderboard of token holders for a given token ID.
It uses the MultiversX API to retrieve token information and token holders.
The leaderboard is saved to a file for later use.
'''
from pathlib import Path
from typing import Any, Dict, List
import json
from classes import TokenHolder

from multiversx_sdk import ApiNetworkProvider

from multiversx_sdk.network_providers.interface import IPagination
from multiversx_sdk.network_providers.api_network_provider import (
    DefaultPagination
)

TOKEN_ID_NAME = "WINTER"
TOKEN_DECIMALS = 8
API_URL = "https://devnet-api.multiversx.com"
BATCH_SIZE = 1000  # Number of items to fetch in each api request batch
# Cache data for large datasets to use in output formatting
HOLDERS_DATA_CACHE = Path(__file__).parent / "holders_data_cache.json"
# Leaderboard output file
LEADERBOARD_OUTPUT = Path(__file__).parent / "leaderboard_output.txt"
# Number of top holders to display
DISPLAY_TOP_HOLDERS = 5
# Number of tokens to display in each batch for console output
DISPLAY_TOKENS_BATCH = 20


class ApiProviderExtension(ApiNetworkProvider):
    # Extend the ApiNetworkProvider SDK class with additional methods for tokens

    # Get all fungible tokens
    def get_fungible_tokens_all(self, pagination: IPagination = DefaultPagination()) -> List[Dict[str, Any]]:
        url = f'/tokens?type=FungibleESDT&fields=identifier,name,ticker&{self._build_pagination_params(pagination)}'
        return self.do_get_generic_collection(url)

    # Get token accounts
    def get_fungible_token_accounts(self, token_id, pagination: IPagination = DefaultPagination()) -> List[Dict[str, Any]]:
        url = f'/tokens/{token_id}/accounts?{self._build_pagination_params(pagination)}'
        return self.do_get_generic_collection(url)


def get_tokens_with_id_from_api(token_id) -> List[Dict[str, Any]]:
    '''
    Retrieves a list of tokens with the specified identifier from the API.
    '''
    api_provider = ApiProviderExtension(API_URL)
    pagination = DefaultPagination()
    pagination.size = BATCH_SIZE
    pagination.start = 0
    all_tokens = []
    while token_batch := api_provider.get_fungible_tokens_all(pagination):
        if token_batch is None:
            break
        all_tokens.extend(token_batch)
        pagination.start += pagination.size

    tokens_with_id = [token for token in all_tokens if token.get('identifier').startswith(token_id)]

    return tokens_with_id


def get_token_holders_from_api(token_id) -> List[Dict[str, Any]]:
    '''
    Retrieves a list of token holders for the specified token ID from the API.
    '''
    api_provider = ApiProviderExtension(API_URL)
    pagination = DefaultPagination()
    pagination.size = BATCH_SIZE
    pagination.start = 0
    token_holders = []
    while token_batch := api_provider.get_fungible_token_accounts(token_id, pagination):
        if token_batch is None:
            break
        token_holders.extend(token_batch)
        pagination.start += pagination.size
    return token_holders


def get_holders_data_from_api() -> List[TokenHolder]:
    '''
    Retrieves the list of token holders from the API.
    '''
    tokens = get_tokens_with_id_from_api(TOKEN_ID_NAME)
    print(f"\nFound {len(tokens)} tokens with identifier '{TOKEN_ID_NAME}'")
    token_holders = []
    for token in tokens:
        token_id = token.get('identifier')
        token_name = token.get('name')
        token_ticker = token.get('ticker')

        holders = get_token_holders_from_api(token_id)
        print(f"{tokens.index(token) + 1}/{len(tokens)} Token ID: {token_id}, Name: {token_name}, Ticker: {token_ticker} Token holders: {len(holders)}")

        for holder in holders:
            holder_address = holder.get('address')
            balance = holder.get('balance')
            token_holders.append(TokenHolder(token_id, token_name, holder_address, balance))

    return token_holders


def format_balance(balance: int) -> str:
    '''
    Formats the balance with decimal places.
    '''
    # Convert balance to float considering decimals
    decimal_balance = float(balance) / (10 ** TOKEN_DECIMALS)
    # Format with appropriate decimal places and thousand separators
    return f"{decimal_balance:,.{TOKEN_DECIMALS}f}"


def generate_leaderboard(token_holders):
    '''
    Generates the leaderboard from the list of token holders.
    '''
    # Group holders by token_id
    token_groups = {}
    for holder in token_holders:
        if holder.token_id not in token_groups:
            token_groups[holder.token_id] = []
        token_groups[holder.token_id].append(holder)

    # Sort tokens by number of holders in descending order, then by token name
    sorted_tokens = sorted(
        token_groups.items(),
        key=lambda x: (-len(x[1]), x[1][0].token_name)  # Sort by -holder_count (desc), then token_name (asc)
    )
    total_tokens = len(sorted_tokens)

    display_batch = 0
    output = []

    # For each token, sort holders and displays the top number of holders configured in DISPLAY_TOP_HOLDERS
    for token_index, (token_id, holders) in enumerate(sorted_tokens, 1):
        if display_batch == 0:
            display_batch = DISPLAY_TOKENS_BATCH
            input(f"\nPress any key to display next {display_batch} tokens...")

        # Sort holders by amount in descending order
        sorted_holders = sorted(holders, key=lambda x: int(x.balance), reverse=True)
        top_holders = sorted_holders[:DISPLAY_TOP_HOLDERS]
        total_holders = len(sorted_holders)
        actual_holders_count = len(top_holders)

        header = f"\nToken {token_index}/{total_tokens}: Top {actual_holders_count} out of {total_holders:,} holders"
        subheader = f"Token ID: {token_id} Name: {holders[0].token_name}"
        separator = "-" * 112
        table_header = f"{'Rank':<4} | {'Address':<62} | {'Balance':<30}"

        # Calculate the number of lines in this token's display
        display_lines = [header, subheader, separator, table_header, separator]
        # Add the top holders
        for rank, holder in enumerate(top_holders, 1):
            formatted_balance = format_balance(holder.balance)
            line = f"{rank:<4} | {holder.address:<62} | {formatted_balance:>40}"
            display_lines.append(line)
        display_lines.append(separator)
        # Add to the output
        output.extend(display_lines)

        # Print to console in batches
        for line in display_lines:
            print(line)

        display_batch -= 1

    return output


def save_holders_to_cache(token_holders: List[TokenHolder]):
    '''
    Saves the list of token holders to the cache file.
    '''
    with open(HOLDERS_DATA_CACHE, "w", encoding="utf-8") as f:
        json.dump([holder.to_dict() for holder in token_holders], f, indent=4)


def load_holders_from_cache() -> List[TokenHolder]:
    '''
    Loads the list of token holders from the cache file.
    '''
    with open(HOLDERS_DATA_CACHE, "r", encoding="utf-8") as f:
        return [TokenHolder.from_dict(data) for data in json.load(f)]


def main():
    if (Path(HOLDERS_DATA_CACHE).exists() and
            input("\nFound token holders data cache file. Press 'y' to use it, or any other key to get new data from API...") == "y"):
        print("\nReading token holders data from cache...")
        token_holders = load_holders_from_cache()
    else:
        print("\nReading token holders data from API...")
        token_holders = get_holders_data_from_api()
        save_holders_to_cache(token_holders)
        print(f"\nToken holders saved to: {HOLDERS_DATA_CACHE}")

    output = generate_leaderboard(token_holders)

    # Save to file
    with open(LEADERBOARD_OUTPUT, "w", encoding="utf-8") as f:
        f.write('\n'.join(output))
    print(f"\nLeaderboard saved to: {LEADERBOARD_OUTPUT}\n")


if __name__ == "__main__":
    main()
