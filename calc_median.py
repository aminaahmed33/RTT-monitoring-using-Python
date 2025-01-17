import json
import sys
from time import mktime
import numpy as np
from math import sqrt
import time
from datetime import datetime, timedelta
from statistics import median
from slidding_window import *
from wilson import *

###### Calculate the median and confidence interval for the current hour ###########

def calc_median (hour, date, interconn_dict):
     if hour == 00:
         interconn_dict = {}
     print(date.day)
     try:
        if date.day > 9:
          path = "inter_conn/inter_conn_" + str(date.year) + "-" + str(date.month) + "-" + str(date.day) + "T" + hour + "00.json"
        else:
          path = "inter_conn/inter_conn_" + str(date.year) + "-" + str(date.month) + "-0" + str(date.day) + "T" + hour + "00.json"
        file = open(path)
        interconn_file = json.load(file)
        for facA in interconn_file:
         for facB in interconn_file[facA]:
             media = round(median(sorted(interconn_file[facA][facB])), 2)
             distrib = interconn_file[facA][facB]
             n =len(distrib)/2
             lb , ub = wilson(distrib , n, alpha = 0.05)
             lb = round(lb, 2)
             ub = round(ub, 2)
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
     except:
            pass
     
     return(interconn_dict)
