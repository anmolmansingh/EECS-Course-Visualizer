# this is the readme for the SI 507: improving EECS course access with graphs and trees

This is a fun little course project aimed at improving your understanding of the EECS course structure visually, rather than navigate through a labyrinth of poorly-designed pages.


The three categories required to be checked are briefly given below:
1. Data collection
2. Data processing
3. Data presentation


# Setup
Clone this git repository (web hosting available soon!): <Enter git repo here>

## Installation

- 
Create virtual env
- `conda create -n eecscs python=3.9`
Activate env
- 'conda activate eecscs'
Install requirements
- `pip install -r requirements.txt`
Run the flask app in local
- 'flask --app app run'
IF 

# Add client key and secret:
- Visit UMich API page
- create any app account
- request key
- create env_variables.env file in your local and add the key, secret values
Run docker
- 'sdfaf'

## Running the Application
- `python manage.py runserver --insecure`
- temporarily using user: 'admin', pass: 'userpass'
- NOTE: if you're running the system locally, you'll need to set:
    - environment variables: 
        - On Windows: `set DEVELOPMENT_MODE=True` & `set DEBUG=True` 
        - On MacOS: `export DEVELOPMENT_MODE=True` & `export DEBUG=True`