import json
import sys
from time import mktime
#from tqdm import tqdm
import numpy as np
from math import sqrt
import time
from datetime import datetime, timedelta
from statistics import median
from slidding_window import *
from wilson import *

########### Calculate the median and confidence interval for the initial values, which is the fist day values ###########

interconn_dict = {}
filtered_interconn_dict ={}
start_date = datetime.strptime("2022-11-25", "%Y-%m-%d")
yesterday_date = start_date - timedelta(hours=24)
before_yesterday_date = start_date - timedelta(hours=48)
before_prev_date, prev_date, curr_date, hours_array = check_date(interval_length = 24, hour = 0)

path = "inter_conn/inter_conn_" + str(yesterday_date.year) + "-" + str(yesterday_date.month) + "-" + str(yesterday_date.day) + "T0000.json"
file = open(path)
interconn = json.load(file)
for hour in hours_array:
     path = "inter_conn/inter_conn_" + str(yesterday_date.year) + "-" + str(yesterday_date.month) + "-" + str(yesterday_date.day) + "T" + hour + "00.json"
     print(path)
     file = open(path)
     interconn_file = json.load(file)
     for facA in interconn_file:
         for facB in interconn_file[facA]:
             media = round(median(sorted(interconn_file[facA][facB])), 2)
             distrib = interconn_file[facA][facB]
             n =len(distrib)/2
             lb , ub = wilson(distrib , n, alpha = 0.05)
             if facA not in interconn_dict:
               interconn_dict[facA]= {}
               interconn_dict[facA][facB]= {}
               interconn_dict[facA][facB]["Median"]= {}
               interconn_dict[facA][facB]["Median"]= [media]
               interconn_dict[facA][facB]["lower_bd"]= {}
               interconn_dict[facA][facB]["lower_bd"]= [lb]
               interconn_dict[facA][facB]["upper_bd"]= {}
               interconn_dict[facA][facB]["upper_bd"]= [ub]
             elif facB not in interconn_dict[facA]:
                  interconn_dict[facA][facB] = {}
                  interconn_dict[facA][facB]["Median"]= {}
                  interconn_dict[facA][facB]["Median"]= [media]
                  interconn_dict[facA][facB]["lower_bd"]= {}
                  interconn_dict[facA][facB]["lower_bd"]= [lb]
                  interconn_dict[facA][facB]["upper_bd"]= {}
                  interconn_dict[facA][facB]["upper_bd"]= [ub]
             else:
                interconn_dict[facA][facB]["Median"].append(media)
                interconn_dict[facA][facB]["lower_bd"].append(lb)
                interconn_dict[facA][facB]["upper_bd"].append(ub)
######### check the 24 values are exist#########
for facA in interconn_dict:
        for facB in interconn_dict[facA]:
              median_length_checek = interconn_dict[facA][facB]["Median"]
              if len(median_length_checek) == 24    :
            
                  if facA not in filtered_interconn_dict:
                     filtered_interconn_dict[facA]= {}
                     filtered_interconn_dict[facA][facB]= {}
                     filtered_interconn_dict[facA][facB]["Median"]= {}
                     filtered_interconn_dict[facA][facB]["Median"]= (interconn_dict[facA][facB]["Median"])
                     filtered_interconn_dict[facA][facB]["lower_bd"]= {}
                     filtered_interconn_dict[facA][facB]["lower_bd"]= (interconn_dict[facA][facB]["lower_bd"])
                     filtered_interconn_dict[facA][facB]["upper_bd"]= {}
                     filtered_interconn_dict[facA][facB]["upper_bd"]= (interconn_dict[facA][facB]["upper_bd"])
                  else:
                       filtered_interconn_dict[facA][facB] = {}
                       filtered_interconn_dict[facA][facB]["Median"]= {}
                       filtered_interconn_dict[facA][facB]["Median"]= (interconn_dict[facA][facB]["Median"])
                       filtered_interconn_dict[facA][facB]["lower_bd"]= {}
                       filtered_interconn_dict[facA][facB]["lower_bd"]= (interconn_dict[facA][facB]["lower_bd"])
                       filtered_interconn_dict[facA][facB]["upper_bd"]= {}
                       filtered_interconn_dict[facA][facB]["upper_bd"]= (interconn_dict[facA][facB]["upper_bd"])
with open(("medians/median_" + str(yesterday_date.year) + "-" + str(yesterday_date.month) + "-" + str(yesterday_date.day) + ".json"), "w") as outfile:
                       json.dump(filtered_interconn_dict, outfile)