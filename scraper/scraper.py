# Primary python script

# Workflow: access card library on cardgamedb.com and gather the card
# information, translating it into information that can be imported
# into a database.

import requests
from bs4 import BeautifulSoup

core_url = 'http://www.cardgamedb.com/index.php/agameofthrones2ndedition/a-game-of-thrones-2nd-edition-cards/_/core/?sort_col=field_554&sort_order=asc&per_page=300'