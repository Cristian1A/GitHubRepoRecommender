import requests
import json
import argparse


"""
Makes a petition to Gihub's Api to extract usefull data to train the model
"""

fetching_url = 'https://api.github.com/search/repositories'

def get_args():
    parser = argparse.ArgumentParser(description='Fetch GitHub repository data.')
    parser.add_argument('token', type=str, help='GitHub personal access token')
    parser.add_argument('--max_pages', type=int, default=11, help='Number of pages to fetch')
    parser.add_argument('--output_file', type=str, default='../repo_data.json', help='Output JSON file')
    return parser.parse_args()

def repo_fetcher(token: str, max_pages: int, output_file: str) -> None:

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    for page in range(1, max_pages):
        all_repo_data = []

        params = {
            'q': 'stars:>1',
            'sort': 'stars',
            'order': 'desc',
            'per_page': 100,
            'page': page
        }

        api_response = requests.get(fetching_url, headers=headers, params=params)

        if api_response.status_code == 200:
            json_data = api_response.json()
            repo_data = json_data.get('items', [])
            all_repo_data.extend(repo_data)
        elif api_response.status_code == 422:
            print("Error 422: Validation failed, or the endpoint has been reached.")
            break;
        elif api_response.status_code == 503:
            print("Error 503: Service unavailable.")
            break;

        with open(output_file, 'a') as json_file:
            json.dump(all_repo_data, json_file, indent=4)

if __name__ == '__main__':
    args = get_args()
    repo_fetcher(args.token, args.max_pages, args.output_file)
