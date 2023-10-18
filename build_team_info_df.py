import requests
import constant
import json
import time
import pandas as pd
import utils
import sys


api_key = constant.API_KEY
second_limit = constant.REQUESTS_PER_SECOND_LIMIT
two_minute_limit = constant.REQUESTS_PER_2_MINUTES_LIMIT

match_ids_all_tier = json.load(open('match_ids.json'))
unique_match_ids = set()

# # rebuild the dataframe from a specific row if necessary
# row_start = len(df)
# if len(df) < row_start and len(df) > 0:
#     row_start = len(df)
#     print('Will continue from row #:', row_start)
#     df = df.head(row_start)
# row_tracker = 0
tiers = ['platinum', 'gold', 'silver']

for tier in tiers:
    print('\nGetting information in %s matches...' % tier.upper())

    match_ids = list(match_ids_all_tier[tier]) 
    print('Unique match ids:', len(set(match_ids)))

    # define the CSV file path
    csv_file_path = 'team_info_%s.csv' % tier
    try:
        df = pd.read_csv(csv_file_path)
    except:
        columns=['team_side', 'top_champ', 'top_puuid', 'jg_champ', 'jg_puuid', 'mid_champ', 
                'mid_puuid', 'bot_champ', 'bot_puuid', 'sup_champ', 'sup_puuid', 'enemy_top_champ', 
                'enemy_top_puuid', 'enemy_mid_champ', 'enemy_jg_champ', 'enemy_jg_puuid', 
                'enemy_mid_puuid', 'enemy_bot_champ', 'enemy_bot_puuid', 'enemy_sup_champ', 
                'enemy_sup_puuid', 'tier', 'win']
        df = pd.DataFrame(columns=columns)

    for match_id in match_ids:
        if match_id in unique_match_ids:
            pass
        else:
            unique_match_ids.add(match_id)
            try:
                while True:
                    url = 'https://americas.api.riotgames.com/lol/match/v5/matches/%s?api_key=%s' % (match_id, api_key)
                    resp = requests.get(url)

                    if resp.status_code == 429: # handle the rate limit
                        time.sleep(1)
                        continue
                    if resp.status_code == 403: # handle expired API key
                        print('API key expired, please update the API key:')
                        api_key = input()      
                        continue
                    if resp.status_code == 200:
                        match_log =  resp.json()
                        break
                    else:
                        print('Failed to collect the information of match:', match_id)
                        print('Status Code:', resp.status_code)
                        break

                # match_log = utils.get_match_log(match_id, api_key)
                team_info = utils.seperate_team_info(match_log)
                row = utils.generate_one_row(team_info)
                row['tier'] = tier  # assign the value of tier

                df.loc[len(df)] = row
                df.to_csv(csv_file_path, index=False)   # update the CSV file after each iteration
            except KeyboardInterrupt:
                df.to_csv(csv_file_path, index=False)
                sys.exit()
            except:
                print('Having trouble getting information from match id:', match_id)

    # save a DataFrame for each tier to the a CSV file
    df.to_csv(csv_file_path, index=False)


