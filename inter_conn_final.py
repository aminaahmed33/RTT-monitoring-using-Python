import json
from pprint import pprint
import os
import sys
#import json
from numpy import loadtxt
import bz2
import ast
inter_conn = {}

###### Read bz2 file #######
def read_from(filename):
    bz2_file = bz2.BZ2File(filename, 'rb')      
    text = bz2_file.read()
    text = text.decode('UTF-8')
    file_dict = ast.literal_eval(text)
    link_list = file_dict["links"]
    Date = file_dict["date_time"]
    return (link_list,Date)


########### Read files ###########
for filename in os.listdir("/home/csd/part12_output_7_weeks/part12_output/link_diff"):
      destination_folder = "/home/csd/part12_output_7_weeks/part12_output/link_diff"
      new_file_path = os.path.join(destination_folder, filename)
      conn, Date = read_from(new_file_path)
      for link in conn:
            fac_near = str(link["FAC_near"][0])
            fac_far = str(link["FAC_far"][0])
            rtt_diff = link["RTT_diff"]
####### Store links that has no * #######
            if rtt_diff != "*":
               rtt_diff = round(float(rtt_diff),2)

               if fac_near not in inter_conn:
                  inter_conn[fac_near] = {}
                  inter_conn[fac_near][fac_far] = [rtt_diff]

               else:
                   if fac_far not in inter_conn[fac_near]:
                      inter_conn[fac_near][fac_far] = [rtt_diff]

                   else:
                        inter_conn[fac_near][fac_far].append(rtt_diff)

      with open(("/home/csd/delay_detection/inter_conn/inter_conn"+"_"+str(Date) +"." +"json"), "w") as outfile:
            json.dump(inter_conn, outfile)
      inter_conn = {}
