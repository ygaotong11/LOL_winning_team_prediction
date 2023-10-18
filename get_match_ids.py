import requests
import json
import constant
import time

api_key = constant.API_KEY
second_limit = constant.REQUESTS_PER_SECOND_LIMIT
two_minute_limit = constant.REQUESTS_PER_2_MINUTES_LIMIT

puuids_all_tier = json.load(open('puuids.json'))

num_requests = 0    # tracker the number of requests to avoid limit
start_time = time.time()

res = {}
for tier in puuids_all_tier:
    print('Collecting match ids in %s...' % tier.upper())
    puuids = puuids_all_tier[tier]
    print('Total puuids:', len(puuids))

    temp_res = []
    for puuid in puuids:
        url = 'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/%s/ids?type=ranked&start=0&count=50&api_key=%s' % (puuid, api_key)

        resp = requests.get(url)
        num_requests += 1

        # check if reaching the rate limit of API key, if yes, wait for the corresponding time.
        if num_requests % 20 == 0:
            print('Exceeding the Second Limit, waiting for 1s...')
            end_time = time.time()
            if end_time - start_time < second_limit:
                time.sleep(1)
                start_time = time.time()
        if num_requests % 100 == 0:
            print('Exceeding the 2-Minute Limit, waiting for 120s...')
            end_time = time.time()
            if end_time - start_time < two_minute_limit:
                time.sleep(120)
                start_time = time.time()
        
        try:
            match_ids = resp.json()
            # print(len(match_ids))
            temp_res.extend(match_ids)
        except Exception as e:
            print('An exception occured:', e)
    
    print('Total match ids collected:', len(temp_res))
    print('\n')
    res[tier] = temp_res

with open('match_ids.json', 'w') as f:
    json.dump(res, f)

print('Done.')
