# Azul Bot
This is a Blue (Azul in Portuguese) Bot that posts random photos

## Setup
- Install the requirements `pip install -r requirements.txt`
- Create a folder named `photos` and place the photos you wish to post in there.
- Set the environment variables *BSKY_USERNAME* and *BSKY_PASSWORD*
- Execute: `python3 main.py --sync` for initial DB population.

## Usage

```
usage: main.py [-h] [--sync] [--dump] [--replies]

AzulBot - Blue Sky Image Bot

optional arguments:
  -h, --help  show this help message and exit
  --sync      syncronize imagedir with database
  --dump      dump database
  --replies   syncronize replies
```
