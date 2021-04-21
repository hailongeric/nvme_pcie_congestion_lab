#! /usr/bin/python3
import os
import shutil
import struct
import numpy as np
import matplotlib.pyplot as plt

def read_records(filename="records.bin"):
    fin = open(filename, 'rb')
    fin.seek(0, os.SEEK_END)
    length = fin.tell()
    fin.seek(0, os.SEEK_SET)
    print("records length:", length)
    assert length % 0x18 == 0
    records_query = []
    records_rdtscp = []
    records_timestrap = []

    for i in range(length//0x18):
        r1 = fin.read(8)
        r2 = fin.read(8)
        r3 = fin.read(8)
        d1 = struct.unpack('1Q', r1)
        d2 = struct.unpack('1Q', r2)
        d3 = struct.unpack('1Q', r3)
        records_query.append(d1[0])
        records_rdtscp.append(d2[0])
        records_timestrap.append(d3[0])
    fin.close()
    return records_query, records_rdtscp, records_timestrap

        # fig = plt.figure(1)
        # ax = fig.add_subplot(111)
        # # ax.plot(x1[8000:-60000],y1[8000:-60000])
        # ax.plot(x1, y1, linewidth=0.25)
        # plt.savefig(save_path + str(k) + '.jpg')
        # plt.cla()
def summary(records_query=[], records_rdtscp=[], records_timestrap=[]):
    Average_query_time = np.mean(records_query)
    print("Average query times:", Average_query_time)

    ARR = [(records_rdtscp[i] - records_rdtscp[i-1]) /
           3600.0 for i in range(1, len(records_rdtscp))]
    Average_rdtscp_gap = np.mean(ARR)
    print("Average rdtscp gap:", Average_rdtscp_gap, "us")

    ARR = [(records_timestrap[i] - records_timestrap[i-1]) /
           3600.0 for i in range(1, len(records_timestrap))]
    Average_timestrap_gap = np.mean(ARR)
    print("Average timestramp gap:", Average_timestrap_gap, "us")

def show_picture_feature(feature=[]):
    fig = plt.figure(figsize=(15, 8))
    ax = fig.add_subplot(1, 1, 1)

    ax.plot(range(len(feature)), feature, linewidth=0.15)

    #ax.scatter(noise1, [0]*len(noise1), s=10, color="red")

    #ax.set_ylim(0, 2.5)
    plt.xlabel('order')
    plt.ylabel('time gap by timestrap(us)')

    plt.show()

def draw_picture_feature(feature=[], fig_name=""):
    fig = plt.figure(figsize=(15, 8))
    ax = fig.add_subplot(1, 1, 1)

    ax.plot(range(len(feature)), feature, linewidth=0.15)

    #ax.scatter(noise1, [0]*len(noise1), s=10, color="red")

    ax.set_ylim(0, 2.5)
    plt.xlabel('order')
    plt.ylabel('time gap by timestrap(us)')

    # plt.savefig(save_dir + 'draw_picture_feature'  + '.jpg')

    # plt.show()
    if fig_name:
        fig.savefig(fig_name)
        dir_name = fig_name[:-5] + "feature"
        os.mkdir(dir_name)
        shutil.copy2(fig_name, dir_name)
        shutil.copy2("records.bin", dir_name)


def draw_picture(records_query=[], records_rdtscp=[], records_timestrap=[], save_dir ='', log_name='' , fig_name=""):
    fig = plt.figure(figsize=(15, 3))

    # ax = fig.add_subplot(3, 1, 1)
    # ax.plot(range(len(records_query)), records_query, linewidth=0.15)
    # ax.set_ylim(0, 500)
    # plt.xlabel('wc id')
    # plt.ylabel('query time')
    #
    # ax = fig.add_subplot(3, 1, 2)
    # ARR = [(records_rdtscp[i] - records_rdtscp[i-1]) /
    #        3600.0 for i in range(1, len(records_rdtscp))]
    # ax.plot(range(len(ARR)), ARR, linewidth=0.15)
    # ax.set_ylim(0, 25)
    # plt.xlabel('wc id')
    # plt.ylabel('time gap by rdtscp(us)')

    ax = fig.add_subplot(3, 1, 3)
    ARR2 = [(records_timestrap[i] - records_timestrap[i-1]) /
            1000 for i in range(1, len(records_timestrap))]
    ax.plot(range(len(ARR2)), ARR2, linewidth=0.15)
    ax.set_ylim(0, 2.5)
    plt.xlabel('wc id')
    plt.ylabel('time gap by timestrap(us)')

    # ax.scatter(x2, y2 , s=10, color="red")
    # plt.show()
    plt.savefig(save_dir + log_name + '.jpg')

    if fig_name:
        fig.savefig(fig_name)
        os.mkdir(fig_name[:-5])
        shutil.copy2(fig_name, fig_name[:-5])
        shutil.copy2("records.bin", fig_name[:-5])


if __name__ == "__main__":
    # for debug, here you can show a old record
    # file_dir = '../new_lab4_data_add_1/www.Amazon.com/log0'
    # file_dir ='/mnt/usb/new_lab4_data_add_1/'
    file_dir ='/mnt/usb/new_lab4_data_add_1/'
    save_pic = '/mnt/usb/lab4_show_pattern/pic/'
    have_d   = 0
    for web_site in os.listdir(file_dir):
        web_logs = file_dir + web_site + '/'
        web_pics = save_pic + web_site + '/'

        if len(os.listdir( web_logs)) > 20 :
            have_d+=1
        else: continue

        if not os.path.exists(web_pics) :
            os.mkdir(web_pics)
        draw_n = 0



        for w_log in os.listdir( web_logs):
            web_log = web_logs + w_log
            print('have_d : ' , have_d)
            records_query, records_rdtscp, records_timestrap = read_records(
                web_log)
            print(records_query[0:10])
            print(records_rdtscp[0:10])
            print(records_timestrap[0:10])
            summary(records_query, records_rdtscp, records_timestrap)
            draw_picture(records_query, records_rdtscp, records_timestrap, save_dir= web_pics ,log_name= w_log)
            draw_n +=1
            if draw_n >5 :
                break