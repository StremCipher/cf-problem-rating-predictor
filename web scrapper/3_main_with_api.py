
from os import rename, times
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import re
import numpy as np
import json
import math


contests = requests.get(
    "https://codeforces.com/api/contest.list")

data = pd.DataFrame(columns=['contest_type', 'question_no',
                    'q_rating', 'accuracy', 'avg_solving_time'])
json_file_1 = contests.json()
contests = json_file_1['result']
taken = 1
cnt = 1
saved = 1
for ids in contests:
  if(ids['phase'] != 'FINISHED'):
    continue
  id = str((ids['id']))
  # print(cnt,id)
  # id="1514"
  standing = requests.get(
      "https://codeforces.com/api/contest.standings?contestId="+id)

  # print(standing.json()
  json_file = standing.json()
  if (json_file['status']) != "OK":
    time.sleep(2)
    continue
  re = json_file['result']['rows']
  contest_name = json_file['result']['contest']['name']
  print(cnt, contest_name)
  cnt += 1
  # useful data
  total_participant = len(re)
  total_correct_sub_for_each_question = {}
  problem_rating = {}
  tried_but_not_solved = {}
  total_time_to_solve_q = {}
  total_sub_for_each_question = {}
  avg_solve_time_for_each_question = {}
  total_no_of_question = 0
  accuracy = {}

  q_list = json_file['result']['problems']
  for i in q_list:
    # print(i['index'],i['rating'])
    if 'rating' in i:
      problem_rating[total_no_of_question+1] = i['rating']
    else:
      problem_rating[total_no_of_question+1] = -1
    total_no_of_question += 1
    total_time_to_solve_q[total_no_of_question] = 0
    total_correct_sub_for_each_question[total_no_of_question] = 0
    tried_but_not_solved[total_no_of_question] = 0
    total_sub_for_each_question[total_no_of_question] = 0
    accuracy[total_no_of_question] = 0
  # print(problem_rating)
  # print(total_no_of_question)
  # print(re)
  for i in re:
    user_sub_for_each_q = i['problemResults']
    question_id = 1
    temp = []
    for i in user_sub_for_each_q:
      if('bestSubmissionTimeSeconds' in i):
        temp.append([i['bestSubmissionTimeSeconds'], question_id])
        total_correct_sub_for_each_question[question_id] += 1
      else:
        temp.append([0, question_id])
        if i['rejectedAttemptCount'] > 0:
          tried_but_not_solved[question_id] += 1
      question_id += 1
    temp.sort()
    prev_time = 0
    for [x, y] in temp:
      total_time_to_solve_q[y] += x-prev_time
      prev_time = x
    # print(total_time_to_solve_q)
  for i in range(total_no_of_question):
    total_sub_for_each_question[i +
                                1] = total_correct_sub_for_each_question[i+1]+tried_but_not_solved[i+1]
    if total_sub_for_each_question[i+1] > 0:
      accuracy[i+1] = total_correct_sub_for_each_question[i+1] / \
          total_sub_for_each_question[i+1]

  #output
  # print(total_participant)
  # print(total_correct_sub_for_each_question)
  # print(total_sub_for_each_question)
  # print(tried_but_not_solved)
  # print(total_time_to_solve_q)
  # print("avg solving time in second")
  for i in range(total_no_of_question):
    if(total_correct_sub_for_each_question[i+1] > 0):
      avg_solve_time_for_each_question[i+1] = total_time_to_solve_q[i+1] / \
          total_correct_sub_for_each_question[i+1]
    else:
      avg_solve_time_for_each_question[i+1] = 0
  # print(avg_solve_time_for_each_question)
  contest_type = 4  # for all other contest
  if "Div. 3" in contest_name:
    contest_type = 3
  if "Div. 2" in contest_name:
    contest_type = 2
  if "Div. 1" in contest_name:
    contest_type = 1
  if "Global Round" in contest_name:
    contest_type = 0
  for i in range(total_no_of_question):
    data = data.append({'contest_type': contest_type, 'question_no': i+1,
                       'q_rating': problem_rating[i+1], 'accuracy': accuracy[i+1], 'avg_solving_time': avg_solve_time_for_each_question[i+1]}, ignore_index=True)
  # print(data)
  # print(taken)
  if(taken % 50 == 0):
    m = str(saved)
    data.to_csv('output'+m+'.csv', index=False)
    data = pd.DataFrame(
        columns=['contest_type', 'question_no', 'q_rating', 'accuracy', 'avg_solving_time'])
    saved += 1
    # break
  taken += 1
# print(data)
