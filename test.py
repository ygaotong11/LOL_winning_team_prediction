import requests
import constant
import json
import time
import pandas as pd
import utils
import sys

match_ids_all_tier = json.load(open('match_ids.json'))


row_tracker = 0
row_start = 0

tier = 'challenger'

print('Getting information in %s matches...' % tier.upper())
match_ids = list(set(match_ids_all_tier[tier]))     # get the unique match ids
print('Unique match ids:', len(match_ids))

for match_id in match_ids[:100]:
    if row_tracker <= row_start:
        row_tracker += 1
    else:
        print(match_id)