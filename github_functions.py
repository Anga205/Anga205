import requests
import os
import time
from datetime import datetime

def get_total_contributions(username: str="Anga205", token: str=os.getenv("GITHUB_TOKEN"), start_year: int=2020) -> int:
    """
    Gets the total number of contributions for a user from a given start year to the present.
    This is done by fetching contributions one year at a time.

    Args:
        username (str): The GitHub username.
        token (str): A GitHub personal access token. A token with 'read:user' scope
                     is required to access contribution data.
        start_year (int): The year to start counting contributions from.

    Returns:
        int: The total number of contributions, or -1 if an error occurs.
    """
    if not token:
        return -1

    headers = {
        "Authorization": f"bearer {token}",
        "Content-Type": "application/json"
    }

    # GraphQL query to get total contributions for a specific time range
    query = """
    query($username: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $username) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            totalContributions
          }
        }
      }
    }
    """

    graphql_url = "https://api.github.com/graphql"
    total_contributions = 0
    current_year = datetime.now().year

    try:
        for year in range(start_year, current_year + 1):
            from_date = f"{year}-01-01T00:00:00Z"
            # The 'to' date should be the end of the year, or now if it's the current year.
            if year < current_year:
                to_date = f"{year}-12-31T23:59:59Z"
            else:
                to_date = datetime.utcnow().isoformat(timespec='seconds') + 'Z'

            variables = {
                "username": username,
                "from": from_date,
                "to": to_date
            }

            response = requests.post(
                graphql_url,
                headers=headers,
                json={"query": query, "variables": variables}
            )
            response.raise_for_status()
            data = response.json()

            if "errors" in data:
                return -1

            user_data = data.get('data', {}).get('user')
            if not user_data:
                continue

            year_contributions = user_data['contributionsCollection']['contributionCalendar']['totalContributions']
            total_contributions += year_contributions
            
            # A small delay to be respectful to the API.
            time.sleep(1)

        return total_contributions

    except requests.exceptions.RequestException:
        return -1
    except (KeyError, TypeError):
        return -1


if __name__ == "__main__":
    total_contributions = get_total_contributions()
    
    if total_contributions != -1:
        print(f"{total_contributions}")
    else:
        print("\nFailed to retrieve contribution count.")
