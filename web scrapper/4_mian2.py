from os import rename, times
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import re
import numpy as np


def string_to_int(input_string):
    # print(input_string)
    output_int = int(input_string)
    return output_int


q_list = []
q_index = {}


def find_all_q_and_rating(url):
    html_text = requests.get(url).text
    table = pd.read_html(url, match="Name")
    df = table[0]
    r = len(df)
    # print(r)
    # print(df.loc[[1],['#']].values)
    for i in range(0, r):
        val = (df.loc[[i], ['#']].values)
        val = str(val)
        val = val.replace('[', '')
        val = val.replace(']', '')
        val = val.replace('\'', '')
        # print(val)
        q_list.append(val)
    cur = 0
    for i in ((q_list)):
        q_index[i] = cur
        cur += 1


def user_submission(profile_url, row_num):
    final_ans_row = pd.DataFrame(columns=q_list)
    print(profile_url)

    print(df.loc[:, ['When', 'Problem', 'Verdict']])
    row = []
    for i in range(r):
        cur = []
        row.append(cur)
    for i in range(0, r):
        q_id = (df.loc[[i], ['Problem']].values)
        q_id = str(q_id)
        q_id = q_id.replace('[', '')
        q_id = q_id.replace(']', '')
        q_id = q_id.replace('\'', '')
        q_id = q_id[:2]
        q_id = q_id.replace(' ', '')
        # print(q_id)
        sub_time = (df.loc[[i], ['When']].values)
        sub_time = str(sub_time)
        sub_time = sub_time.replace('[', '')
        sub_time = sub_time.replace(']', '')
        sub_time = sub_time.replace('\'', '')
        verdict = (df.loc[[i], ['Verdict']].values)
        verdict = str(verdict)
        verdict = verdict.replace('[', '')
        verdict = verdict.replace(']', '')
        verdict = verdict.replace('\'', '')
        print(sub_time)
        row[q_index[q_id]].append([sub_time, verdict])
        print(q_index[q_id])
        arr = np.array([1, 2, 3])
        print(i)
        final_ans_row = final_ans_row.append(q_id: arr)
        final_ans_row = final_ans_row.loc[[row_num]:[q_id]].values = arr


def solve():
    main_contest_url = "https://codeforces.com/contest/"+"1527"
    find_all_q_and_rating(main_contest_url)
    url = "https://codeforces.com/contest/1527/standings"
    html_text = requests.get(url).text
    # print(url)
    soup = BeautifulSoup(html_text, 'lxml')
    rows = soup.find_all("tr")
    head = rows[0]
    rows = rows[1:]
    headings = q_list
    all_rows = []
    sub_list = pd.DataFrame()
    for row_num in range(0, len(rows)):
        for row_item in rows[row_num].find_all("td"):
            aa = re.sub("(\xa0)|(\n)|,", "", row_item.text)
            if aa.isalpha():
                profile_url = "https://codeforces.com/submissions/"+"alya_wow"+"/contest/1527"
                html_text = requests.get(profile_url).text
                table = pd.read_html(profile_url, match="Problem")
                df = table[0]
                r = len(df)
                # print(df)
                sub_list = sub_list.append(df, ignore_index=False)
                break
        # break
    # df = pd.DataFrame(data=all_rows,columns=headings)
    # print(df.loc[[0],[0]])
    # print(final_ans)
    sub_list.to_csv('output.csv', index=False)


if __name__ == '__main__':
    solve()
