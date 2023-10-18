import requests
import time
import sys
import constant


def get_match_log(match_id: str) -> dict:
    url = 'https://americas.api.riotgames.com/lol/match/v5/matches/%s?api_key=%s' % (match_id, api_key)

    while True:
        resp = requests.get(url)

        if resp.status_code == 429: # handle the rate limit
            time.sleep(1)
            continue
        if resp.status_code == 403: # handle expired API key
            print('API key expired, please update the API key:')
            api_key = input()
            url = 'https://americas.api.riotgames.com/lol/match/v5/matches/%s?api_key=%s' % (match_id, api_key)
            continue
        if resp.status_code == 200:
            return resp.json()
        else:
            print('Failed to collect the information of match:', match_id)
            return None

def seperate_team_info(match_log: dict) -> list:
    '''
    This function collect information about the participants of two different teams in a match from a match log.
    Return: a list of 2 teams, each containing their participants' info.
    '''
    teams = match_log['info']['teams']
    participants = match_log['info']['participants']

    team1_id = teams[0]['teamId']
    team2_id = teams[1]['teamId']

    team1 = [p for p in participants if p['teamId'] == team1_id]
    team2 = [p for p in participants if p['teamId'] == team2_id]
    return [team1, team2]

def generate_one_row(team_info: list) -> dict:
    '''
    This function generates one row for the dataframe from the output from 'seperate_team_info'.
    Return: a dictionary that contains the value for each feature in the dataframe.
    '''
    row = {}

    team_sides = {100: 'blue', 200: 'red'}
    team_side = team_sides[team_info[0][0]['teamId']]
    row['team_side'] = team_side

    for participant in team_info[0]:
        if participant['teamPosition'] == 'TOP':
            row['top_champ'] = participant['championId']
            row['top_puuid'] = participant['puuid']
        if participant['teamPosition'] == 'JUNGLE':
            row['jg_champ'] = participant['championId']
            row['jg_puuid'] = participant['puuid']
        if participant['teamPosition'] == 'MIDDLE':
            row['mid_champ'] = participant['championId']
            row['mid_puuid'] = participant['puuid']
        if participant['teamPosition'] == 'BOTTOM':
            row['bot_champ'] = participant['championId']
            row['bot_puuid'] = participant['puuid']
        if participant['teamPosition'] == 'UTILITY':
            row['sup_champ'] = participant['championId']
            row['sup_puuid'] = participant['puuid']
    for participant in team_info[1]:
        if participant['teamPosition'] == 'TOP':
            row['enemy_top_champ'] = participant['championId']
            row['enemy_top_puuid'] = participant['puuid']
        if participant['teamPosition'] == 'JUNGLE':
            row['enemy_jg_champ'] = participant['championId']
            row['enemy_jg_puuid'] = participant['puuid']
        if participant['teamPosition'] == 'MIDDLE':
            row['enemy_mid_champ'] = participant['championId']
            row['enemy_mid_puuid'] = participant['puuid']
        if participant['teamPosition'] == 'BOTTOM':
            row['enemy_bot_champ'] = participant['championId']
            row['enemy_bot_puuid'] = participant['puuid']
        if participant['teamPosition'] == 'UTILITY':
            row['enemy_sup_champ'] = participant['championId']
            row['enemy_sup_puuid'] = participant['puuid']

    row['win'] = team_info[0][0]['win']
    return row