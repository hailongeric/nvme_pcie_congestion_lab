#!/usr/bin/python3
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Process


class InfoExtracter:
    def __init__(self, log_name):
        _, _, self.data = self.read_records(log_name)

        '''7K
        self.start = 0
        self.ave_two_gap = 13.5  # 查看log取平均得到
        self.ave_gap = self.ave_two_gap/2
        #Error Rate:  0.22338731841109535
        '''
        #8K
        self.start = 0
        self.ave_two_gap = 13  # 查看log取平均得到
        self.ave_gap = self.ave_two_gap/2
        #Error Rate:  0.2055874087613104
        '''14K
        self.start = 0
        self.ave_two_gap = 15  # 查看log取平均得到
        self.ave_gap = self.ave_two_gap/2
        Error Rate:  0.004652431450171213
        '''

        '''28K
        self.start = 0         # 从0开始, 尖峰不会跨区域; begins with 0;
        self.ave_two_gap = 15  # 查看log取平均得到
        self.ave_gap = self.ave_two_gap/2
        #Error Rate:  0.004379143298974435
        '''

        '''56K
        self.start = 0 
        self.ave_two_gap = 18  # 查看log取平均得到
        self.ave_gap = self.ave_two_gap/2
        Error Rate:  0.00360177949125539
        '''

        '''84K
        self.start = 0
        self.ave_two_gap = 22  # 查看log取平均得到
        self.ave_gap = self.ave_two_gap/2
        #Error Rate:  0.0032246437444485923
        '''
        
        '''112K
        self.start = 0
        self.ave_two_gap = 26  # 查看log取平均得到
        self.ave_gap = self.ave_two_gap/2
        #Error Rate:  0.002912675740771859
        '''


    def _record3_gap(self):
        _, line2, line3 = self.read_records("records.bin")
        rdtscp_gap  = line2[-1] - line2[0]
        unknown_gap = line3[-1] - line3[0]
        print("How much cycles per one strap: ", rdtscp_gap/unknown_gap)
        print("Time(ns):", (rdtscp_gap/unknown_gap)*(1/2300000000)*1000000000)
        '''
        How much cycles per one strap:  46.07895155417581
        Time(ns): 20.034326762685133
        Time(us): 0.020034326762685132
        '''
        return 


    def extract(self):
        self.data_preprocess()

        self.draw_picture()
        self.error_rate_method2()

    def classify(self, peroid):
        p1 = peroid[0: int(self.ave_two_gap/2)+1]
        p2 = peroid[int(self.ave_two_gap/2)+1:]
        M1 = np.max(p1)
        M2 = np.max(p2)
        result1 = M1 > 0.75
        result2 = M2 > 0.75
        #p = np.sort(peroid)

        return result1, result2


    def error_rate_method2(self):
        peaks = np.where(self.data>0.75)[0]
        correct_num = 0
        error_num = 0
        p = 0

        normal = self.ave_gap
        keys = []

        for index in peaks:
            #index = peaks[i]
            gap = index - p

            if gap < self.ave_gap - 3:
                pass
            elif gap < self.ave_gap +2:
                keys.append(1)
            elif gap < self.ave_two_gap +2:
                keys.append(0)
                keys.append(1)
            else:
                k = int(gap/self.ave_gap)
                for i in range(k-1):
                    keys.append(0)
                keys.append(1)
                
            # # print(index)
            # # print(gap)
            # if gap >= self.ave_two_gap - 2 and gap <= self.ave_two_gap + 2:
            #     correct_num += 2
            # elif gap < self.ave_two_gap-2:
            #     error_num +=1
            # else:
            #     error_num += 1 * int(gap/self.ave_two_gap)
                

            p = index

        keys_len = len(keys)
        print(keys_len)
    
        print(keys)
        #ground_truth = [(x+1)%2 == 1  for x in range(keys_len)] # True and False
        #print("error rate: ",  error_num/(correct_num+error_num))
        for i in range(1,keys_len):
            if keys[i]==keys[i-1]:
                error_num+=1
            # if ground_truth[i] != keys[i]:
            #     error_num += 1

        error_rate = error_num/keys_len
        print("Error Rate: ",error_rate)


    def error_rate_method1(self):
        length = int(self.data.shape[0]/self.ave_two_gap)*self.ave_two_gap
        peroids = self.data[:int(length)].reshape(-1, self.ave_two_gap)
        print(peroids.shape)
        #peroids = peroids[:1000]
        keys_len = peroids.shape[0] * 2


        ground_truth = [(x+1)%2 == 0  for x in range(keys_len)] # True and False

        # 每次判断2个peroid的key;
        predict = []
        for peroid in peroids:
            result1, result2 = self.classify(peroid)
            predict.append(result1)
            predict.append(result2)
            print(result1, result2)
        
        error_num = 0
        for i in range(keys_len):
            if ground_truth[i] != predict[i]:
                error_num += 1

        error_rate = error_num/keys_len
        print("Error Rate: ",error_rate)

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
    IE = InfoExtracter("records.bin")
    #IE._record3_gap()
    IE.extract()
