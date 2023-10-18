'''
This file will scrape a certain number of summoner names in each of different tiers of rank on op.gg using selenium.
'''

import constant
import numpy as np
import json
from selenium import webdriver
from selenium.webdriver.common.by import By


tiers = constant.TIERS
num_per_page = constant.NUM_PER_PAGE

# build the chrome driver
options = webdriver.ChromeOptions()
options.add_argument('--headless')   
options.add_argument('--incognito')     # in private mode
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})    # do not load images
options.add_experimental_option('excludeSwitches', ['enable-automation'])   # avoid being detected
driver = webdriver.Chrome(options=options)

summoner_ids = {}
for tier in tiers:
    num_needed = tiers[tier]
    page_needed = int(np.ceil(num_needed/num_per_page))
    print('Number needed in %s:' % tier.upper(), num_needed)
    print('Page needed:', page_needed)

    ids = []
    for page in range(1, page_needed+1):
        url = 'https://www.op.gg/leaderboards/tier?page=%s&tier=%s' % (page, tier)
        driver.get(url)

        driver.implicitly_wait(5)

        elements = driver.find_elements(By.XPATH, '//*[@class="css-1glhec8 e1r55j542"]/a')
        
        if num_needed < len(elements):
            elements = elements[:num_needed]

        for e in elements:
            href = e.get_attribute('href')

            id = href.split('/')[-1]
            ids.append(id)

        num_needed -= len(elements)

    print('number of summoners collected in %s:' % tier, len(ids))
    print('\n')
    summoner_ids[tier]=ids

with open('summoners.json', 'w') as f:
    json.dump(summoner_ids, f)

print('Done.')

driver.quit()
