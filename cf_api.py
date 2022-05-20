import requests

CF_API_URL = 'https://codeforces.com/api'

def get_contests():
    """
    Get all available contests from Codeforces
    """
    response = requests.get(CF_API_URL + '/contest.list', json=True)

    if response.status_code != 200:
        raise Exception('Error: {}'.format(response.status_code))

    return response.json()

def get_problems():
    """
    Get all problems. We recommend to not call this endpoint frequently, as the response is big (1MB). It's desirable to store the JSON
    as a file for further processing
    """
    response = requests.get(CF_API_URL + '/problemset.problems', json=True)

    if response.status_code != 200:
        raise Exception('Error: {}'.format(response.status_code))

    return response.json()

