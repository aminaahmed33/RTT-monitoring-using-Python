def check_date(interval_length =24, hour = 0):
    index_interval = []
    hours_array = []
    prev_date = []
    curr_date =[]
    threshold =[]
    before_prev_date = []
    hours = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13",
             "14","15","16","17","18","19","20","21","22","23"]
    value = hour - 1
    for x in range(interval_length):
        if value >= 0:
           index_interval.append(value)
        elif -25 < value < 0:
            index_interval.append(24 + value)
        else:
            index_interval.append(48 + value)
        value =value - 1
    index_interval.reverse()
    for h in index_interval:
        hours_array.append(hours[h])
    ###############  Window ###########
    ##### For interval length 24 and 48
    if "23" in hours_array:
        for ind, element in enumerate(hours_array):
            if element == "23":
               threshold.append(ind)

        ##### For interval length 24
        if len(threshold) == 1:

            v = int(threshold[0])
            for i in range(v + 1):
                prev_date.append(hours_array[i])
  
            for x in range(interval_length - v - 1):
                curr_date.append(hours_array[v + 1])
                v = v + 1
        else:
        ###### For interval length 48
            k = int(threshold[0])

            l = int(threshold[1])

            for i in range(k + 1):

                before_prev_date.append(hours_array[i])
            for i in range(l - k):
                prev_date.append(hours_array[k + 1])
                k =k + 1

            for x in range(interval_length - l - 1):
                curr_date.append(hours_array[l + 1])
                l = l + 1
    else:

        curr_date = hours_array

    return(before_prev_date, prev_date, curr_date, hours_array)