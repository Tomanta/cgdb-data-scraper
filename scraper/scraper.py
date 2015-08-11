# Primary python script

# Workflow: access card library on cardgamedb.com and gather the card
# information, translating it into information that can be imported
# into a database.

import requests
from bs4 import BeautifulSoup
import csv
import re

core_url = 'http://www.cardgamedb.com/index.php/agameofthrones2ndedition/a-game-of-thrones-2nd-edition-cards/_/core/?sort_col=field_554&sort_order=asc&per_page=300'

# These are all the attributes of a given card.
key_list = ['Title', 'Set', 'Pack', 'Number', 'Illustrator', 'Type',
            'Unique', 'Gold', 'Initiative', 'Claim', 'Reserve', 'Cost',
            'Faction', 'Loyal', 'Military', 'Intrigue', 'Power', 'Strength',
            'Traits', 'Text', 'Flavor', 'Deck Limit', 'Image', 'Unique']

card_list = []

def init_card():
    c = {}
    for k in key_list:
        c[k] = ""
    
  # These should be the only two that don't default and aren't gathered.
    c['Set'] = 'Core'
    c['Pack'] = 'Core'
    return c

r = requests.get(core_url)
soup = BeautifulSoup(re.sub('<BR>', '\n', r.content), 'html.parser')

for tag in soup.findAll('div', {'class': "cardRecord"}):
    card = init_card() # start a new card dictionary

    # For the first part let's grab the things every card will have that's NOT in the
    # <ul> section

    card['Image'] = tag.find('div', {'class': 'cardImage'}).find('img')['src'].strip().encode("utf-8", "replace")

    title = tag.find('div', {'class': 'cardText'}).find('h1').text.strip()
    if title[0] == u'\u2022':
        card['Unique'] = 'True'
        card['Title'] = title.split(' ',1)[1].strip().encode("utf-8", "replace")
    else:
        card['Title'] = title.strip().encode("utf-8", "replace")

  # Now let's add things from the list
    for attribute in tag.findAll('li'):
        # a few items have class, that makes it easy!
        if attribute.has_attr('class') and len(attribute.text) > 0:
            if 'traits' in attribute['class']:
                card['Traits'] = attribute.text.strip().encode("utf-8", "replace")
            elif 'flavorText' in attribute['class']:
                card['Flavor'] = attribute.text.strip().encode("utf-8", "replace")
        # Benjen Stark *has* to be different for some reason and not use SPAN.
        elif attribute.find('span') or (attribute.find('em') and 'bbc' in attribute.find('em')['class']):
            card['Text'] = attribute.text.strip().strip().encode("utf-8", "replace")
           if card['Text'].find('Plot deck limit') != -1:
             card['Deck Limit'] = 1
        elif attribute.text.find(':') != -1:
            sarr = attribute.text.split(':', 1)
            if len(sarr[1].strip()) > 0:  # Some blank fields show up, ignore those
                if sarr[0] == 'Icons':
                    if sarr[1].find('Military') != -1:
                        card['Military'] = 'True'
                    if sarr[1].find('Intrigue') != -1:
                        card['Intrigue'] = 'True'
                    if sarr[1].find('Power') != -1:
                        card['Power'] = 'True'
                elif sarr[0] == 'Quantity':
                    continue # skip
                elif sarr[0] == 'Faction' and sarr[1].find('(Loyal)') != -1:
                    card['Loyal'] = 'True'
                    card['Faction'] = sarr[1].rsplit(' ', 1)[0].strip().encode("utf-8", "replace")
                else:
                    card[sarr[0]] = sarr[1].strip().encode("utf-8", "replace")
    card_list.append(card)

with open('cards.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, key_list)
    dict_writer.writeheader()
    dict_writer.writerows(card_list)
