# nexar-multi-match-search

## Prerequisites

To use this example you will need the following:

- A Nexar account - [Login or signup here](https://identity.nexar.com/Account/Login).

- An Altium 365 workspace.

- A Nexar application with the supply and design scopes enabled.

- You will need to set your client ID and secret for the application mentioned above in your environment variables. Set them as NEXAR_CLIENT_ID and NEXAR_CLIENT_SECRET. Alternatively, you can set them as their variables in `python/apiQueries.py` but do not share these credentials publicly.

- This example uses `PySimpleGui` and other Python packages. To install them, run the command `pip install -r requirements.txt`

## The Code

An overview of each part of this example.

### nexarClient

This folder contains the `NexarClient` class that handles authorization and has a generic `get_query` function to query the Nexar API.

### apiQueries.py

Contains all of the API queries and also functions that specifically return the data that will be used.

### program.py

Contains the code to create the GUI.
