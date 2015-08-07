# Primary python script

# Workflow: access card library on cardgamedb.com and gather the card
# information, translating it into information that can be imported
# into a database.

import requests
from bs4 import BeautifulSoup

core_url = 'http://www.cardgamedb.com/index.php/agameofthrones2ndedition/a-game-of-thrones-2nd-edition-cards/_/core/?sort_col=field_554&sort_order=asc&per_page=300'

r = requests.get(core_url)

soup = BeautifulSoup(r.content, 'html.parser')

# As a starting point, this extracts the card image and the card name.
# TODO: Maybe change this to a MAP call?
for tag in soup.findAll('div', {'class': "cardRecord"}):
  tag.find('div', {'class': 'cardImage'}).find('img')['src']
  tag.find('div', {'class': 'cardText'}).find('h1').text
  break  # TEMP: Let's get this down for the first record before worrying about the rest
    
