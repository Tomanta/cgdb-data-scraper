# Primary python script

# Workflow: access card library on cardgamedb.com and gather the card
# information, translating it into information that can be imported
# into a database.

import requests
from bs4 import BeautifulSoup


core_url = 'http://www.cardgamedb.com/index.php/agameofthrones2ndedition/a-game-of-thrones-2nd-edition-cards/_/core/?sort_col=field_554&sort_order=asc&per_page=300'

# These are all the attributes of a given card.
key_list = ['Title', 'Set', 'Pack', 'Number', 'Illustrator', 'Type',
            'Unique', 'Gold', 'Initiative', 'Claim', 'Reserve', 'Cost',
            'Faction', 'Loyal', 'Military', 'Intrigue', 'Power', 'Strength',
            'Traits', 'Text', 'Flavor', 'Deck Limit', 'Image'] 

card_list = []

def init_card():
  c = {}
  for k in key_list:
    c[k] = ""
    
  # These should be the only two that don't default and aren't gathered.
  # I think.
  c['Set'] = 'Core'
  c['Pack'] = 'Core'
  return c

r = requests.get(core_url)
soup = BeautifulSoup(r.content, 'html.parser')

# As a starting point, this extracts the card image and the card name.
# TODO: Maybe change this to a MAP call?
for tag in soup.findAll('div', {'class': "cardRecord"}):
  card = init_card() # start a new card dictionary

  # For the first part let's grab the things every card will have that's NOT in the
  # <ul> section

  card['Image'] = tag.find('div', {'class': 'cardImage'}).find('img')['src']
  card['Title'] = tag.find('div', {'class': 'cardText'}).find('h1').text
  
  # Now let's add things from the list
  for attribute in tag.findAll('li'):
    
    # a few items have class, that makes it easy!
    if attribute.find('span'):
       # TODO: Format text part of card correctly
       card['Text'] = attribute.text.strip()
    elif attribute.has_attr('class') and len(attribute.text) > 0:
       if 'traits' in attribute['class']:
           card['Traits'] = attribute.text
       elif 'flavorText' in attribute['class']:
           card['Flavor'] = attribute.text
    elif attribute.text.find(':') != -1:
      # TODO: This needs to be tested but is elegent as hell if it works. I think.
      sarr = attribute.text.split(':', 1)
      if len(sarr[1].strip()) > 0:  # Some blank fields show up, ignore those
        card[sarr[0]] = sarr[1].strip()
#    else:
#      print "Can't handle: ", attribute.text # debugging
    card_list.append(card)
  break # TEMP: Just to speed things up instead of processing ALL the cards.



