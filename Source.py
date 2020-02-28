import time
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

# All possible types
all_types = ['Normal', 'Fighting', 'Flying', 'Poison', 'Ground',
             'Rock', 'Bug', 'Ghost', 'Steel', 'Fire', 'Water',
             'Grass', 'Electric', 'Psychic', 'Ice', 'Dragon',
             'Dark', 'Fairy']

# Effectiveness rates, 2: super, .5: not very, 0: not at all
effectiveness = {'Normal': [1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 'Fighting': [1, 1, 2, 1, 1, .5, .5, 1, 1, 1, 1, 1, 1, 2, 1, 1, .5, 2],
                 'Flying': [1, .5, 1, 1, 0, 2, .5, 1, 1, 1, 1, .5, 2, 1, 2, 1, 1, 1],
                 'Poison': [1, .5, 1, .5, 2, 1, .5, 1, 1, 1, 1, .5, 1, 2, 1, 1, 1, .5],
                 'Ground': [1, 1, 1, .5, 1, .5, 1, 1, 1, 1, 2, 2, 0, 1, 2, 1, 1, 1],
                 'Rock': [.5, 2, .5, .5, 2, 1, 1, 1, 2, .5, 2, 2, 1, 1, 1, 1, 1, 1],
                 'Bug': [1, .5, 2, 1, .5, 2, 1, 1, 1, 2, 1, .5, 1, 1, 1, 1, 1, 1],
                 'Ghost': [0, 0, 1, .5, 1, 1, .5, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
                 'Steel': [.5, 2, .5, 0, 2, .5, .5, 1, .5, 2, 1, .5, 1, .5, .5, .5, 1, .5],
                 'Fire': [1, 1, 1, 1, 2, 2, .5, 1, .5, .5, 1, .5, 1, 1, .5, 1, 1, .5],
                 'Water': [1, 1, 1, 1, 1, 1, 1, 1, .5, .5, .5, 2, 2, 1, .5, 1, 1, 1],
                 'Grass': [1, 1, 2, 2, .5, 1, 2, 1, 1, 2, .5, .5, .5, 1, 2, 1, 1, 1],
                 'Electric': [1, 1, .5, 1, 2, 1, 1, 1, .5, 1, 1, 1, .5, 1, 1, 1, 1, 1],
                 'Psychic': [1, .5, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, .5, 1, 1, 2, 1],
                 'Ice': [1, 2, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, .5, 1, 1, 1],
                 'Dragon': [1, 1, 1, 1, 1, 1, 1, 1, 1, .5, .5, .5, .5, 1, 2, 2, 1, 2],
                 'Dark': [1, 2, 1, 1, 1, 1, 2, .5, 1, 1, 1, 1, 1, 0, 1, 1, .5, 2],
                 'Fairy': [1, .5, 1, 2, 1, 1, .5, 1, 2, 1, 1, 1, 1, 1, 1, 0, .5, 1]
                 }

df = pd.DataFrame(columns=all_types, data=effectiveness, index=all_types)

types = []

print('Enter the name of the Pokemon')
pokemon = input()

#pokemon = 'CHARIZARD'

url = "https://www.serebii.net/pokedex-swsh/" + pokemon.lower() + '/'

resp = requests.get(url)

if resp.ok == False:
    print('Fail')

soup = BeautifulSoup(resp.text, features='lxml')
td = soup.find('td', {"class": "cen"}).find_all('img')
for type in td:
    types.append(type['alt'].replace('-type', ''))

# Possible damage multipliers
most, very, little, least, no = 4, 2, .5, .25, 0
multipliers = [most, very, little, least, no]

def weakness(list):
    rates = []
    for type in list:
        rates.append(df[type])
    return rates

data = weakness(types)

# Dual types
effective = 1
for type in data:
    effective *= type

x = effective[effective != 1].sort_values(ascending=False)

print('Multiplier: Type')
print('-------------')
for multiplier in multipliers:
    fin = str(multiplier) + 'x: ' + ' '.join(list(x[x == multiplier].index))
    print(fin)



