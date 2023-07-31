# -*- coding: utf-8 -*-

# ######################### INFO ################################# #
# gspread originally imported 3.4.2 run command to update to 5.4.0 #
# ################################################################ #
# !pip install gspread==5.4.0

import gspread
import pandas as pd

# Provide json file downloaded from google cloud console with credentials
path_to_file = 'path/to/creds.json'
gc = gspread.service_account(filename=path_to_file)

# provide name of worksheet to work with
# workseet where tasks are added
tasks_sheet = "tasks_input"
tsh = gc.open(tasks_sheet)
# worksheet where results are saved
results_sheet = "tasks_results"
rsh = gc.open(results_sheet)
# worksheet with daily data for magtag to use
btn1_sheet = "daily_data_btn1"
btn1_sh = gc.open(btn1_sheet)
btn2_sheet = "daily_data_btn2"
btn2_sh = gc.open(btn2_sheet)
btn3_sheet = "daily_data_btn3"
btn3_sh = gc.open(btn3_sheet)

# Results worksheet has all the results
results_sh = rsh.worksheet('results')
# get data and put in dataframe
results_df = pd.DataFrame(results_sh.get_all_records())

# only want ids that have a complete
d = {'complete': True, 'skip': False, 'pass': False}
results_df['result'] = results_df['result'].map(d).copy()

# Create list of completed id's
list_of_ids = list(results_df.loc[results_df['result']]['task_id'])

# Tasks worksheet has all the tasks
tasks_sh = tsh.worksheet('tasks')
# get data and put in dataframe
tasks_df = pd.DataFrame(tasks_sh.get_all_records())
# drop rows with empty title
tasks_df = tasks_df.loc[tasks_df['title'] != ''].copy()
# reset index
tasks_df.reset_index(drop=True, inplace=True)

# only include these columns
sub_cols = ['id', 'title', 'category', 'time_estimate', 'repeat',
       'repeat_interval', 'points', 'sub_tasks', 'sub_task_ids',
       'sub_tasks_complete']
tasks_df = tasks_df[sub_cols].copy()

# Set datatypes for DF
# Set boolean columns
d = {'T': True, 'F': False, '': False}
tasks_df['repeat'] = tasks_df['repeat'].map(d).copy()
tasks_df['sub_tasks'] = tasks_df['sub_tasks'].map(d).copy()
tasks_df['sub_tasks_complete'] = tasks_df['sub_tasks_complete'].map(d).copy()

# Create keep column & set all to true initially
tasks_df['keep'] = True
# remove tasks that do not repeat and have been completed
tasks_df.loc[
    (tasks_df['repeat'] == False) &
     (tasks_df['id'].isin(list_of_ids)), 'keep'] = False

# Remove spaces and turn sub_task_ids string to a list
tasks_df.loc[
    (tasks_df['sub_tasks']) &
     (tasks_df['sub_task_ids'].notna()),
    'sub_task_ids'] = tasks_df.apply(lambda row:
                                     list(str(row['sub_task_ids']).strip().split(',')), axis=1)

def is_subset_of_list(row):
  subset_list = row['sub_task_ids']
  if isinstance(subset_list, list):
    return set([int(ele) for ele in subset_list]).issubset(list_of_ids)
  else:
    return False

# check all values in sub_task_ids in list_of_ids
tasks_df['sub_tasks_complete'] = tasks_df.apply(is_subset_of_list, axis=1)

# update keep to false if id is in results.task_id and tasks_df.sub_tasks_complete is true
tasks_df.loc[(tasks_df['id']).isin(list_of_ids) & (tasks_df['sub_tasks_complete']), 'keep'] = False

# tasks_df.time_estimate.unique()
estimate_bins = {'< 15': 0,
                 '15 - 30': 1,
                 '60 +': 2,
                 '31 - 60': 2}

tasks_df['time_estimate'] = tasks_df['time_estimate'].map(estimate_bins).copy()

# Buttons by repeat interval
incl_cols = ['id', 'title', 'category', 'points']

# Create 3 dataframes one for each button
btn1 = tasks_df.loc[(tasks_df['keep'] == True) & (tasks_df['time_estimate'] == 0)].copy()
# Only include the columns needed for the magtag project
btn1 = btn1[incl_cols].copy()
# reset the index after pulling out btn1 records
btn1.reset_index(inplace=True, drop=True)
# mix up the order of the rows
btn1 = btn1.sample(frac = 1)
# reset the index after mixing up the rows
btn1.reset_index(inplace=True, drop=True)

btn2 = tasks_df.loc[(tasks_df['keep'] == True) & (tasks_df['time_estimate'] == 1)].copy()
btn2 = btn2[incl_cols].copy()
btn2.reset_index(inplace=True, drop=True)
btn2 = btn2.sample(frac = 1)
btn2.reset_index(inplace=True, drop=True)

btn3 = tasks_df.loc[(tasks_df['keep'] == True) & (tasks_df['time_estimate'] == 2)].copy()
btn3 = btn3[incl_cols].copy()
btn3.reset_index(inplace=True, drop=True)
btn3 = btn3.sample(frac = 1)
btn3.reset_index(inplace=True, drop=True)

# update daily data
# clear data from worksheet
btn1_ws = btn1_sh.worksheet('btn1')
btn1_ws.clear()
btn1_ws.update([btn1.columns.values.tolist()] + btn1.values.tolist())

# sht2.worksheet('btn2').clear()
btn2_ws = btn2_sh.worksheet('btn2')
btn2_ws.clear()
btn2_ws.update([btn2.columns.values.tolist()] + btn2.values.tolist())

# sht2.worksheet('btn3').clear()
btn3_ws = btn3_sh.worksheet('btn3')
btn3_ws.clear()
btn3_ws.update([btn3.columns.values.tolist()] + btn3.values.tolist())

# tasks_df.loc[tasks_df['keep']]
