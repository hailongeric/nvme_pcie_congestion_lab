#!/usr/bin/python


out = open("grap_data_1k.csv",'a+')
out.write("data_size,gap_num,high index,low index, high wave duration mean, high wave duration median, low wave duration mean,low wave duration median,bandwith\n")

file_name = "data_4_7"

list_data = ["sss"*10]

f = open(file_name,encoding='utf-16')
list_data = ["sss"]*11

for lines in f:
    if lines == '\n':
        continue
    if ':' not in lines:
        continue
    tmp = lines.split(":")
    tmp[1] = tmp[1].strip()
    if tmp[0] == "data_size ":
        list_data[0]= tmp[1]
    if tmp[0] == "gap_num ":
        list_data[1]= tmp[1]
    if tmp[0] == "per_size ":
        list_data[9]= tmp[1]
    if tmp[0] == "high index":
        list_data[2]= tmp[1]
    if tmp[0] == "low index":
        list_data[3]= tmp[1]
    if tmp[0] == "high wave duration mean":
        list_data[4]= tmp[1]
    if tmp[0] == "high wave duration median":
        list_data[5]= tmp[1]
    if tmp[0] == "low wave duration mean":
        list_data[6]= tmp[1]
    if tmp[0] == "low wave duration median":
        list_data[7]= tmp[1]
    if tmp[0] == "bandwith ":
        list_data[8]= tmp[1]
        out.write("{},{},{},{},{},{},{},{},{},{}\n".format(list_data[0],list_data[1],list_data[2],list_data[3],list_data[4],list_data[5],list_data[6],list_data[7],list_data[8],list_data[9]))
        list_data = ["sss"]*10

f.close()
out.close()