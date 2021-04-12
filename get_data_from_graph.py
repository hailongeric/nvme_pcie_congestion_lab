#!/usr/bin/python3

import numpy
import matplotlib.pyplot as plt
import sys

fence_divation = 1.6e-5 # TODO
split_value = 1.1998e-6  # TODO
high_wave_range = [5.94e-4, 1.939e-3] # TODO
low_wave_range = [5.94e-4, 1.939e-3] # TODO

high_wave_mean_value = 0.00092  # TODO 90 %   value mean 
low_wave_mean_value =  0.000260  # TODO 90 %   value mean 

flag_litter_or_big = 0 # TODO [0 1 2]  1 --> high wave
                                    #  2 --> low wave

last_number = 0 # TODO

INTERVAL_SIZE =50
interval_list = []


if len(sys.argv) == 3:
    log = True
    filename = sys.argv[1]
else:
    log =  False
    filename = sys.argv[1]


raw_data = numpy.loadtxt(filename)

get_data = []

x1, y1 =[], []
k, t  = 0, 0
for i in range(4000, len(raw_data)):
    t += raw_data[i]  # time axis
    if raw_data[i] > 1.27341e-6 or raw_data[i] < 1.15199e-6:   # noise filtration   data may be modify
        continue
    x1.append(t)
    if k != INTERVAL_SIZE-1:    # mean  data smooth  duration gap 50 
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
            # if t -  last_number < low_wave_range[1]:   # 窄一点的波形
            #     last_number = t
            #     flag_litter_or_big = 2 
            #     get_data.append(0)
            # else:
            #     if t - last_number < high_wave_range[1]:  # 宽一点的波形
            #         last_number = t
            #         flag_litter_or_big = 2
            #         get_data.append(2)
            get_data.append(round((t-last_number)/low_wave_mean_value)*'0')
            #print((t-last_number)/low_wave_mean_value)
            last_number = t
            flag_litter_or_big = 2
        else:
            if t-last_number < fence_divation:  # fence can set bigger ???
                continue
            else:
                if log:
                    print("found error wave x: {} \ny: {} \nduration: {} \nflag_value: {} \n".format(t,raw_data[i],t-last_number,flag_litter_or_big))
        continue
    if tmp < split_value and flag_litter_or_big ==  2:
        if t - last_number > high_wave_range[0]:
            # if t -last_number < high_wave_range[1]:
            #     last_number = t
            #     flag_litter_or_big = 1
            #     get_data.append(1)
            # else:
            #     if log:
            #         print("found error wave too wide high wave x: {} \ny: {} \nduration: {} \nflag_value: {} \n".format(t,raw_data[i],t-last_number,flag_litter_or_big))
            #     last_number = t
            #     flag_litter_or_big = 1
            #     get_data.append(3)    # 3 is too much wide high wave
            get_data.append(round((t-last_number)/high_wave_mean_value)*'1')
            #print((t-last_number)/high_wave_mean_value)
            last_number = t
            flag_litter_or_big = 1
        else:
            if t-last_number < fence_divation:
                continue
            elif log:
                print("found error wave x: {} \ny: {} \nduration: {} \nflag_value: {} \n".format(t,raw_data[i],t-last_number,flag_litter_or_big))
        continue

print(get_data)
print("0 ->{}. 00-> {}, 000 ->{}, 0000- > {}, 00000 -> {}, 000000 -> {}, 0000000 -> {}".format(get_data.count('0'),get_data.count('00'),get_data.count('000'),get_data.count('0000'),get_data.count('00000'),get_data.count('000000'),get_data.count('0000000')))
print("1 ->{}. 11-> {}, 111 ->{}, 1111- > {}, 11111 -> {}, 111111 -> {}, 1111111 -> {}".format(get_data.count('1'),get_data.count('11'),get_data.count('111'),get_data.count('1111'),get_data.count('11111'),get_data.count('111111'),get_data.count('1111111')))
print(len(get_data))
