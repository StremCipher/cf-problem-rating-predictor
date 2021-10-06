from os import rename, times
from bs4 import BeautifulSoup
import requests
import time
import json
import pandas as pd
data = pd.DataFrame(columns=['contest_id'])


def find_contest_list():
    contests = requests.get(
        "https://codeforces.com/api/contest.list")
    json_file = contests.json()
    contests = json_file['result']
    for ids in contests:
        if(ids['phase'] != 'FINISHED'):
            continue
        id = str((ids['id']))
        data.append({'contest_id': id}, ignore_index=True)

    data.to_csv('contest_list.csv', index=False)


if __name__ == '__main__':
    find_contest_list()
