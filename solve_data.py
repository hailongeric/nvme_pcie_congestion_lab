#!/usr/bin/python3

import numpy
import matplotlib.pyplot as plt

data_size_arr = [i for i in range(600,10000,100)]
data_size_arr =data_size_arr[::-1]
gap_num_arr = [1,2,4,6,8]


fence_divation = 1.6e-5 # TODO
split_value = 1.1998e-6  # TODO
high_wave_range = [0.94e-4, 1.939e-3] # TODO
low_wave_range = [0.94e-4, 1.939e-3] # TODO



#
# flag = 1 low wave
# flag = 2 high wave 
#

INTERVAL_SIZE =50


for data_size in data_size_arr:
    for gap_num in gap_num_arr:

        flag_litter_or_big = 0 # TODO [0 1 2]       
        last_number = 0 # TODO
        interval_list = []

        filename = "time_line_{}_{}_2.log".format(data_size,gap_num)
        try:
            raw_data = numpy.loadtxt(filename)
        except IOError:
            continue
        high_duration_arry = numpy.arange(100000, dtype = float)
        low_duration_arry = numpy.arange(100000, dtype = float)
        high_index=0
        low_index=0

        get_data = []
        x1, y1 =[], []
        k, t  = 0, 0
        for i in range(10000, len(raw_data)):
            t += raw_data[i]
            if raw_data[i] > 1.27341e-6 or raw_data[i] < 1.15199e-6:
                continue
            x1.append(t)
            if k != INTERVAL_SIZE-1:
                k += 1
                tmp = raw_data[i]
                interval_list.append(raw_data[i])
                last_number = t
                if sum(interval_list)/k > split_value:
                    flag_litter_or_big = 2
                else:
                    flag_litter_or_big = 1
            else:
                interval_list.append(raw_data[i])
                tmp = sum(interval_list)/INTERVAL_SIZE
                interval_list.remove(interval_list[0])

            y1.append(tmp)
            if tmp > split_value and flag_litter_or_big == 2:  # 一直在高波形
                continue
            if tmp < split_value and flag_litter_or_big == 1:  # 一直在低波形
                continue
            if tmp > split_value and flag_litter_or_big == 1:  # 低波形出现高波形
                if t-last_number > low_wave_range[0]:         # 存在正常的间隔
                    low_duration_arry[low_index] = t-last_number
                    low_index += 1
                    last_number = t
                    flag_litter_or_big = 2 
                    # if t -  last_number < low_wave_range[1]:   # 窄一点的波形
                    #     last_number = t
                    #     flag_litter_or_big = 2 
                    #     get_data.append(0)
                    # else:
                    #     if t - last_number < high_wave_range[1]:  # 宽一点的波形
                    #         last_number = t
                    #         flag_litter_or_big = 2
                    #         get_data.append(2)
                else:
                    if t-last_number < fence_divation:    #出现噪音
                        continue
                    #else:
                        #print("found error wave x: {}  y: {}  duration: {}  flag_value: {} ".format(t,raw_data[i],t-last_number,flag_litter_or_big))
                continue
            if tmp < split_value and flag_litter_or_big ==  2:
                if t - last_number > high_wave_range[0]:
                    high_duration_arry[high_index] =  t-last_number
                    high_index += 1
                    last_number = t
                    flag_litter_or_big = 1
                    # if t -last_number < high_wave_range[1]:
                    #     last_number = t
                    #     flag_litter_or_big = 1
                    #     get_data.append(1)
                    # else:
                    #     print("found error wave too wide high wave x: {} \ny: {} \nduration: {} \nflag_value: {} \n".format(t,raw_data[i],t-last_number,flag_litter_or_big))
                    #     last_number = t
                    #     flag_litter_or_big = 1
                    #     get_data.append(3)    # 3 is too much wide high wave
                else:
                    if t-last_number < fence_divation:
                        continue
                    #else:
                        #print("found error wave x: {} y: {} duration: {} flag_value: {} ".format(t,raw_data[i],t-last_number,flag_litter_or_big))
                continue
        high_duration_arry.resize(high_index)
        low_duration_arry.resize(low_index)

        med1 = numpy.median(high_duration_arry)
        med2 = numpy.median(low_duration_arry)

        print("\n\n\n")
        print("data_size : {}\ngap_num : {}\n".format(data_size,gap_num))
        print("high index: {}\nlow index: {}".format(high_index,low_index))
        print("high wave duration mean: {}\nhigh wave duration median: {}\n".format(numpy.mean(high_duration_arry),med1))
        print("low wave duration mean: {}\nlow wave duration median: {}\n".format(numpy.mean(low_duration_arry),med2))
        print("bandwith : {}\n\n\n".format(1/(med1+med2)))
        #print(get_data)
        print("finished solve data")

            
     
