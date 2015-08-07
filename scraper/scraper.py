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
  card = {} # start a new card dictionary

  # For the first part let's grab the things every card will have that's NOT in the
  # <ul> section

  tag.find('div', {'class': 'cardImage'}).find('img')['src']
  tag.find('div', {'class': 'cardText'}).find('h1').text
  
  # Now let's add things from the list
  for attribute in tag.findAll('li'):
    
    # a few items have class, that makes it easy!
    if attribute.has_attr('class') and len(attribute.text) > 0:
       attribute.text
       if 'traits' in attribute['class']:
           card['traits'] = attribute.text
       elif 'flavorText' in attribute['class']:
           card['flavorText'] = attribute.text
    # There is a <SPAN> object for the card text, most of the rest are just X: Y text.         
    break # TEMP: Just to speed things up instead of processing ALL the cards.



