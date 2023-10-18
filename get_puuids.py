import requests
import json
import constant
import time

api_key = constant.API_KEY

summoners_all_tier = json.load(open('summoners.json'))

second_limit = constant.REQUESTS_PER_SECOND_LIMIT
two_minute_limit = constant.REQUESTS_PER_2_MINUTES_LIMIT


num_requests = 0    # tracker the number of requests to avoid limits
start_time = time.time()

res = {}
for tier in summoners_all_tier:
    print('Collecting match ID in %s...' % tier.upper())
    summoners = summoners_all_tier[tier]
    print('Total summoners:', len(summoners))

    temp_res = []
    for summoner in summoners:
        # get the puuid of the summoner
        url = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/%s?api_key=%s' % (summoner, api_key)

        resp = requests.get(url)
        num_requests += 1

        if num_requests % 20 == 0:
            print('Exceeding the Second Limit...')
            end_time = time.time()
            if end_time - start_time < second_limit:
                time.sleep(1)
                start_time = time.time()
        if num_requests % 100 == 0:
            print('Exceeding the 2-Minute Limit...')
            end_time = time.time()
            if end_time - start_time < two_minute_limit:
                print('Need to wait for 120s')
                time.sleep(120)
                start_time = time.time()

        try:
            summoner_info = resp.json()
            puuid = summoner_info['puuid']
            temp_res.append(puuid)
        except Exception as e:
            print('An exception occured with summoner id:', summoner)
            print('Error:',e)

        # # get the match_id of the last 50 ranked games of the summoner
        # match_id_url = 'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/%s/ids?type=ranked&start=0&count=50&api_key=%s' % (puuid, api_key)

        # resp = requests.get(match_id_url)
        # num_requests += 1

        # match_ids = resp.json()
        # temp_res.append(match_ids)

        # handle the rate limit of the api key
     

    print('Total puuid collected:', len(temp_res))
    print('\n')
    res[tier] = temp_res

with open('puuids.json', 'w') as f:
    json.dump(res, f)

print('Done.')

