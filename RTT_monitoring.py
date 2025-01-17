import json
import numpy as np
from math import sqrt
import time
from shutil import copyfile
from datetime import datetime, timedelta
from slidding_window import *
from wilson import *
from calc_median import *
from smoothed_medians import *
from Inter_conn_hourly import *
from WriteToDict import *
import re

filename = "links_file_2022-10-13T0300.json"
#filename="links_file_2022-10-18T1600.json"
def rtt_model(filename):
    medians = {}
    median_yesterday = {}
#alarms_detection = {"alarms" :[]}
    alarms_detection = {}
    active_alarms = {}
    cleared_alarms = {}
    inter_conn(filename)
#filename = '/home/csd/part12_output_7_weeks/part12_output/links/links_file_2022-10-07T0300.json.bz'
    i = re.split('_|T|00.',filename)[-2]
    date_str = re.split('_|T|00.',filename)[-3]
#date_from_user = sys.argv[1]
#date = datetime.strptime(date_from_user, "%Y-%m-%d")
    date = datetime.strptime(date_str, "%Y-%m-%d")
    yesterday_date = date - timedelta(hours=24)
    before_yesterday = yesterday_date - timedelta(hours=24)
    calc_ref_dict = {}

####### Calculate median and confidence intervals for this hour ##############
## Monitor the current hour by opening the detected facilities in this hour from interconn file, and calculate the median and confidence interval
## some facilities may not appear each hour, so the totol values could be less that 24 value
    medians = calc_median(i, date, medians)
    curr_medians = {}
    curr_medians = calc_median(i, date, curr_medians)
    #print(curr_medians)
    #with open(("medians/test test" + str(i)+ ".json"), "w") as outfile:
     #    json.dump(medians, outfile)
    #print(medians)
    with open(("Final demo result/median_" + str(date.year) + "-" + str(date.month) + "-" + str(date.day) + "T" + str(i) +  ".json"), "w") as outfile:
         json.dump(curr_medians, outfile)
         print("Median and Confidence intervals for the current hour created")
    if i == 23:
       if curr_medians != {}:
           with open(("medians/median_" + str(date.year) + "-" + str(date.month) + "-" + str(date.day) + ".json"), "w") as outfile:
             json.dump(curr_medians, outfile)

####### List median values of the previous 24 hours######
    #calc_ref_dict = {}
    if curr_medians != {}:
       before_prev_date, prev_date, curr_date, hours_array = check_date(interval_length = 24, hour= i)
       for facA in curr_medians:
            for facB in curr_medians[facA]:
                #print(facA)
                #print(facB)
                try:
                   file_1= open("alarms1/active_alarms.json")
                   active_alarms = json.load(file_1)
                except:
                        pass
                value_diff = 0

                if len(curr_date) != 0 and median_yesterday.get(facA) != None and median_yesterday[facA].get(facB) != None: ### write its else when all values in the previous date
                       value_diff = len(curr_date) - (len(medians[facA][facB]["Median"]) -1)
                       #print("value", value_diff)
                       if value_diff == 0:
                          indexC = int(curr_date[0])
                          
                #print ("indexC",indexC)
                          end = len(medians[facA][facB]["Median"]) - 1
                          median_p_ref = medians[facA][facB]["Median"][indexC:end] 
                          lower_bd_p_ref = medians[facA][facB]["lower_bd"][indexC:end]
                          ubber_bd_p_ref= medians[facA][facB]["upper_bd"][indexC:end]
                          calc_ref_dict = WriteToDict (facA,facB,calc_ref_dict,median_p_ref,lower_bd_p_ref,ubber_bd_p_ref)
                #print("median_c_ref", median_c_ref)
                       else:
                          median_p_ref = medians[facA][facB]["Median"][0:-1]
                          lower_bd_p_ref = medians[facA][facB]["lower_bd"][0:-1]
                          ubber_bd_p_ref= medians[facA][facB]["upper_bd"][0:-1]
                          calc_ref_dict = WriteToDict (facA,facB,calc_ref_dict,median_p_ref,lower_bd_p_ref,ubber_bd_p_ref)
    #----------#####--------#####-------
                file = open("median2/median_" + str(yesterday_date.year) + "-" + str(yesterday_date.month) + "-" + str(yesterday_date.day) + ".json")
                median_yesterday = json.load(file)
                
                if len(prev_date) != 0 and median_yesterday.get(facA) != None and median_yesterday[facA].get(facB) != None:#facB in median_yesterday[facA]:#curr_medians[facA][facB] in median_yesterday[facA][facB]:
                       list_length = len(median_yesterday[facA][facB]["Median"])
                       #print("yesterday leng",list_length)
                       if list_length == 24 and value_diff == 0:
                         #print("=24")
                         indexP = int(prev_date[0])
                         median_p_ref = median_yesterday[facA][facB]["Median"][indexP:]
                         lower_bd_p_ref = median_yesterday[facA][facB]["lower_bd"][indexP:]
                         ubber_bd_p_ref = median_yesterday[facA][facB]["upper_bd"][indexP:]
                         calc_ref_dict = WriteToDict (facA,facB,calc_ref_dict,median_p_ref,lower_bd_p_ref,ubber_bd_p_ref)
                       elif list_length == 24 and value_diff != 0:
                           #print("this value diff", value_diff)
                           #print("==24 and value diff exist")
                           if (len(prev_date)) + value_diff <= list_length:
                            indexP = list_length - (len(prev_date) + value_diff)
                            median_p_ref = median_yesterday[facA][facB]["Median"][indexP:]
                            lower_bd_p_ref = median_yesterday[facA][facB]["lower_bd"][indexP:]
                            ubber_bd_p_ref = median_yesterday[facA][facB]["upper_bd"][indexP:]
                            calc_ref_dict = WriteToDict (facA,facB,calc_ref_dict,median_p_ref,lower_bd_p_ref,ubber_bd_p_ref)
                           else:
                                median_p_ref = median_yesterday[facA][facB]["Median"]
                                lower_bd_p_ref = median_yesterday[facA][facB]["lower_bd"]
                                ubber_bd_p_ref = median_yesterday[facA][facB]["upper_bd"]
                                calc_ref_dict = WriteToDict (facA,facB,calc_ref_dict,median_p_ref,lower_bd_p_ref,ubber_bd_p_ref)
                                file = open("medians/median_" + str(before_yesterday.year) + "-" + str(before_yesterday.month) + "-" + str(before_yesterday.day) + ".json")
                                median_beofre_yesterday = json.load(file)
                                #if curr_medians[facA][facB] in median_beofre_yesterday[facA][facB]:
                                if median_beofre_yesterday.get(facA) != None and median_beofre_yesterday[facA].get(facB) != None:
                                   vd3 = (len(median_beofre_yesterday[facA][facB]["Median"]) - value_diff) + 1
                                   median_p_ref = median_beofre_yesterday[facA][facB]["Median"][vd3:]
                                   lower_bd_p_ref = median_beofre_yesterday[facA][facB]["lower_bd"][vd3:]
                                   ubber_bd_p_ref = median_yesterday[facA][facB]["upper_bd"][vd3:]
                                   calc_ref_dict = WriteToDict (facA,facB,calc_ref_dict,median_p_ref,lower_bd_p_ref,ubber_bd_p_ref)
                       elif list_length < 12:
                            #print("less that 12 will pass")
                        ### delete the written facility data from the current data part and then exit
                            pass
                       
                       elif list_length > (len(prev_date)) + value_diff:
                           #print("greater than prev +value diff")
                           vd = list_length - (len(prev_date)+ value_diff)
                           median_p_ref = median_yesterday[facA][facB]["Median"][vd:]
                           lower_bd_p_ref = median_yesterday[facA][facB]["lower_bd"][vd:]
                           ubber_bd_p_ref = median_yesterday[facA][facB]["upper_bd"][vd:]
                           calc_ref_dict = WriteToDict (facA,facB,calc_ref_dict,median_p_ref,lower_bd_p_ref,ubber_bd_p_ref)
                           #print("amina")
                       
                       elif list_length < (len(prev_date)) + value_diff:
                           #print("less than prev +value diff")
                           file = open("median2/median_" + str(before_yesterday.year) + "-" + str(before_yesterday.month) + "-" + str(before_yesterday.day) + ".json")
                           #print("amina")
                           median_beofre_yesterday = json.load(file)
                           if median_beofre_yesterday.get(facA) != None and median_beofre_yesterday[facA].get(facB) != None:
                               if (len(prev_date)) + value_diff > (len(median_beofre_yesterday[facA][facB]["Median"])):
                                   continue
                                   #print("last if but pass")
                                   
                                #print(median_beofre_yesterday)
                               else:
                                  
                                  median_p_ref = median_yesterday[facA][facB]["Median"]
                                  #print(median_p_ref)
                                  lower_bd_p_ref = median_yesterday[facA][facB]["lower_bd"]
                                  #print(lower_bd_p_ref)
                                  ubber_bd_p_ref = median_yesterday[facA][facB]["upper_bd"]
                                  #print(ubber_bd_p_ref)
                                  calc_ref_dict = WriteToDict (facA,facB,calc_ref_dict,median_p_ref,lower_bd_p_ref,ubber_bd_p_ref)
                                  before_list_length = (len(prev_date) + value_diff) - list_length
                                  #print("previous day length",len(median_beofre_yesterday[facA][facB]["Median"]))
                                  vd1= len(median_beofre_yesterday[facA][facB]["Median"]) - before_list_length
                                  median_p_ref = median_beofre_yesterday[facA][facB]["Median"][vd1:]
                                  lower_bd_p_ref = median_beofre_yesterday[facA][facB]["lower_bd"][vd1:]
                                  ubber_bd_p_ref = median_beofre_yesterday[facA][facB]["upper_bd"][vd1:]
                                  #print("special case",median_p_ref)
                                  calc_ref_dict = WriteToDict (facA,facB,calc_ref_dict,median_p_ref,lower_bd_p_ref,ubber_bd_p_ref)
                    
                else:
                    continue
    reference_files = smoothed_medians(calc_ref_dict, date, i)
    #print(reference_files)
####### calulate the deviation from the reference values of the previous 24 hours/values######

### take the previous 48 hours in case of alarm detection
### take 24 values even for links that are rarely appear
### consider links with rtt diff from 6x 
        #calc_ref_dict = {}
    for facA in curr_medians:
                 for facB in curr_medians[facA]:
                   if (reference_files.get(facA)) != None and (reference_files[facA].get(facB)) != None:
                     if (curr_medians[facA][facB]["lower_bd"][-1] > reference_files[facA][facB]["upper_bd"][0]) or (curr_medians[facA][facB]["upper_bd"][-1] < reference_files[facA][facB]["lower_bd"][0]):
                      #print("alarm detected")
                      timeN = (str(date.year) + "-" + str(date.month) + "-0" + str(date.day) + "T" + str(i) + "00")   
                      deviation = round(curr_medians[facA][facB]["Median"][-1] - reference_files[facA][facB]["Median"][0],2)
                      medianD = [curr_medians[facA][facB]["Median"][-1]]
                      alarms_detection = alarm_detection_dict (facA, facB,timeN,deviation,medianD,alarms_detection)
                      medianR = reference_files[facA][facB]["Median"][0]
                      lowerR = reference_files[facA][facB]["lower_bd"][0]
                      upperR = reference_files[facA][facB]["upper_bd"][0]
                      active_alarms = active_alarms_dict (facA,facB,timeN,medianR,lowerR,upperR,active_alarms)
                     elif (active_alarms.get(facA)) != None and (active_alarms[facA].get(facB)) != None:
                       start_time = active_alarms[facA][facB]["Start_Time"]
                       del active_alarms[facA][facB]                    
                       end_time = (str(date.year) + "-" + str(date.month) + "-0" + str(date.day) + "T" + str(i) + "00")
                       file = open("alarms1/cleared_alarms.json")
                       cleared_alarms = json.load(file)
  
                       cleared_alarms = cleared_alarms_dict (facA,facB,start_time,end_time,cleared_alarms)
    calc_ref_dict ={}
    reference_files = {}
    #with open(("Final demo result/active_alarms.json"), "w") as outfile:
    #        json.dump(active_alarms, outfile)
     #       print("Active alarm dic created")
    with open(("Final demo result/active_alarms_"+ str(date.year) + "-" + str(date.month) + "-" + str(date.day) + ".json"), "w") as outfile:
            json.dump(active_alarms, outfile)
            print("Active alarm created")
    #with open(("Final demo result/cleared_alarms.json"), "w") as outfile:
    #         json.dump(cleared_alarms, outfile)
    with open(("Final demo result/cleared_alarms_"+ str(date.year) + "-" + str(date.month) + "-" + str(date.day) + ".json"), "w") as outfile:
             print("Cleared alarm created")
             json.dump(cleared_alarms, outfile)
#print(alarms_detection)
    with open(("Final demo result/alarms_"+  str(date.year) + "-" + str(date.month) + "-" + str(date.day) + ".json"), "w") as outfile:
     json.dump(alarms_detection, outfile)
     print("Alarm file created")
    alarms_detection = {} 
    return()
rtt_model(filename)