#!/usr/bin/python3
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Process
'''
1. 应用graph1的信息, 将每个bit的时钟周期数考虑在内; 然后以此划分区域;
2. 只考虑2000个点就可以; 或者多取几段来求;

'''
import json
def read_json(file_name):
    with open(file_name,'r') as file_object:
        c = json.load(file_object)
    return c

class InfoExtracter:
    def __init__(self, log_name="records.bin", DataSize=8):
        self.log_name = log_name
        #self.DataSize = DataSize #K
        _, _, self.data = self.read_records(log_name)

    def extract(self):
        self.data_preprocess()
        #self.draw_picture()
        self.error_rate_dynamic()

    def error_rate_dynamic(self):
        '''
        1. 通过median粗略求gap
        2. 在窗口平移的时候, 在[-2,+2]范围内动态调整下一个添加的范围;
        '''
        peaks = np.where(self.data > 1)[0]
        peaks_p = []
        tem_p = []
        for x in peaks:
            if len(tem_p)==0:
                tem_p.append(x)
            elif x-tem_p[-1]==1:
                tem_p.append(x)
            else:
                peaks_p.append(tem_p)
                tem_p=[x]
        peaks = []
    
        for p in peaks_p:
            peaks.append(np.mean(p))
        peaks = np.array(peaks)

        peaks_gap = peaks[1:] - peaks[:-1]
        ave_gap = int(np.median(peaks_gap))
        print("ave_gap", ave_gap)

        # 先找到第一个尖峰，作为1
        print(peaks[1])
        start = peaks[1]
        print("first peak", start)

        P = int(start - ave_gap/4)
        predicts = []
        # 往后遍历20000个点;
        for i in range(100000):
            peroid = self.data[P: P+ave_gap]
            r1, r2 = self.classify_double(peroid)
            predicts.extend([r1, r2])
            
            inner_peaks = np.where(np.array(peroid)>1)[0]

            '''
            inner peaks 中间噪音比较多, 则不考虑它;
            '''
            if inner_peaks.shape[0]==0:
                P = P+ave_gap
                continue
            
            flag = False
            for i in range(0, inner_peaks.shape[0] - 1):
                if inner_peaks[i+1] - inner_peaks[i] !=1:
                    flag = True
            if flag:
                P = P+ave_gap
                continue
            
            '''
            使用尖峰的平均值来动态调整位置;
            '''
            mean_peak = np.mean(inner_peaks)

            if mean_peak < ave_gap/4 - 2:
                P = P+ave_gap - 2
            elif mean_peak > ave_gap/4 + 2: # and mean_peak < ave_gap/2:
                P = P+ave_gap + 2
            else:
                P = P+ave_gap
        
        #print(predicts)
        keys_len = len(predicts)

        error_num=0
        ground_truth = [(x+1)%2 == 0  for x in range(keys_len)] # True and False
        #print("error rate: ",  error_num/(correct_num+error_num))
        for i in range(0, keys_len):
            if predicts[i]==ground_truth[i]:
                error_num+=1
            # if ground_truth[i] != keys[i]:
            #     error_num += 1

        error_rate = error_num/keys_len
        print("Error Rate: ",error_rate*100, "%")


    def classify_double(self, peroid):
        length = len(peroid)
        p1 = peroid[0: int(length/2)+1]
        p2 = peroid[int(length/2)+1:]
        M1 = np.max(p1)
        M2 = np.max(p2)
        result1 = M1 > 1
        result2 = M2 > 1
        #p = np.sort(peroid)
        return result1, result2

    def read_records(self, filename="records.bin"):
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
        return np.array(records_query), np.array(records_rdtscp), np.array(records_timestrap)


    def draw_picture(self):
        fig = plt.figure(figsize=(15, 8))
        ax = fig.add_subplot(1, 1, 1)
        plt.xlabel('Timestamp ID')
        plt.ylabel('latency(us)')
        ax.plot(range(self.data.shape[0]), self.data, linewidth=0.15)
        plt.show()

    def data_preprocess(self):
        self.data = self.data[1:] - self.data[:-1]
        self.data = self.data * 0.020034326762685132

        self.median = np.median(self.data)
        self.data[self.data > 7] = self.median
        self.data[self.data > 5] = 5
        #self.mean = np.mean(self.data)
        self.data = self.data - self.median
        return

if __name__=="__main__":
    # IE = InfoExtracter("logs_back/256K")
    # IE.extract()
    X = [4,    8,    16,    20,   24 ,  28,   32,   64,   128,  256]
    for x in X:
        IE = InfoExtracter("logs_back/%dK"%x)
        IE.extract()
        print("==============")


'''
自动化:
A: 在104机器上运行脚本;
    1. for data size
    2. 104 ./zz
    3. ./cuda
    4. ssh 103: ./zz 192.168.2.1
    5. scp 数据拷贝到104上的大盘;
B: 
    for data size
        提取时钟周期; 转化成大概的gaps数目;(方法2: 提取所有尖峰, 取中位数/2);
        根据gaps数目, 在log上运行error_rate_dynamic()
'''