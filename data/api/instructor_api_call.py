#%%
# calling the UMich Instructors API (OAuth call included)
# imports
import requests
import os
import sys
import json
import time

from dotenv import load_dotenv

from constants import GRANT_TYPE, SCOPE
# load env variables
load_dotenv("/Users/anmolmansingh/Documents/Winter 2023/SI 507/EECS Course Selector/env_variables.env")  

# constant variables
BASE_URL = "https://gw.api.it.umich.edu"
MAX_RETRIES = 5

#%%
# Call OAuth API for token (call only once)
def oauth_call():
    client_key = os.environ.get('CLIENT_KEY')
    client_secret = os.environ.get('CLIENT_SECRET')

    payload = { "grant_type": GRANT_TYPE, "scope": SCOPE }
    oauth_api_url = f"{BASE_URL}/um/oauth2/token?grant_type={GRANT_TYPE}&scope={SCOPE}"
    response = requests.post(oauth_api_url, data=payload, auth=(client_key, client_secret))

    if response.status_code != 200:
        print("Failed to obtain token from the OAuth 2.0 server", file=sys.stderr)
        print(response.reason)
        sys.exit(1)
    else:
        print("Successfuly obtained a new token")
        tokens = json.loads(response.text)
        access_token = tokens['access_token']

    return access_token

# %%
# call the instructor api
# TODO: make it loop through all the instructor lists gotten by scraping
def instructor_courses(access_token, uniqname, term_code):
    instructor_url = f"{BASE_URL}/um/aa/Instructors/{uniqname}/Terms/{term_code}/Classes"
    headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
    }
    # implementing exponential backoff
    retry_count = 0
    while retry_count < MAX_RETRIES:
        try:
            response = requests.get(instructor_url, headers=headers)
            if response.status_code == 200:
                break
            # if the response status code is 429, implement exponential backoff
            elif response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', '1'))
                time.sleep(retry_after)
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            # if there's a connection error or timeout, retry the request
            if retry_count < MAX_RETRIES - 1:
                retry_count += 1
                continue
            else:
                raise e

    # try:
    #     response = requests.get(instructor_url, headers=headers)
    #     response.raise_for_status()
    # except requests.exceptions.HTTPError as e:
    #     print("Error: ", e)
    # except requests.exceptions.RequestException as e:
    #     print("Error: Could not connect to instructors API")
    #     print(e)
    #     exit()

    # load json data
    try:
        instructor_courses_dict = json.loads(response.text)
    except json.decoder.JSONDecodeError as e:
        print(e)
        exit()

    return instructor_courses_dict["getInstrClassListResponse"]
