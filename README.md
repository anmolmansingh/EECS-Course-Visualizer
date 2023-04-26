# SI 507: Improving EECS course literacy with graphs

This is a course project aimed at improving your understanding of the EECS course structure visually, rather than navigate through a labyrinth of poorly-designed pages.


The three categories required to be checked are briefly given below:
1. Data collection
2. Data processing
3. Data presentation


# Setup
Clone this git repository (web hosting available soon!): <Enter git repo here>

## Installation


Install requirements: `pip install -r requirements.txt` 
Run the flask app in local: `flask --app app run`

## To call Instructors API:
### Add client key and secret:
- Visit UMich API page (https://dir.api.it.umich.edu/):
    - Refer to relevant resources to fetch the API key and secret
- create env_variables.env file in your local and add the key, secret values as CLIENT_KEY, CLIENT_SECRET
- Run instructor_api.py in "data/api" directory
