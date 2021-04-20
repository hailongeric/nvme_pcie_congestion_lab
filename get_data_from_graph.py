#!/usr/bin/python3

import numpy
import sys

def minDistance(word1, word2):
    if not word1:
        return len(word2 or '') or 0

    if not word2:
        return len(word1 or '') or 0

    size1 = len(word1)
    size2 = len(word2)

    last = 0
    tmp = list(range(size2 + 1))
    value = None

    for i in range(size1):
        tmp[0] = i + 1
        last = i
        # print word1[i], last, tmp
        for j in range(size2):
            if word1[i] == word2[j]:
                value = last
            else:
                value = 1 + min(last, tmp[j], tmp[j + 1])
                # print(last, tmp[j], tmp[j + 1], value)
            last = tmp[j+1]
            tmp[j+1] = value
        # print tmp
    return value


def longestCommonSubsequence(A, B):
        m, n = len(A), len(B)
        ans = 0
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if A[i - 1] == B[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                    ans = max(ans, dp[i][j])
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return ans

def find_lcsubstr(s1, s2):
    #生成0矩阵，为方便后续计算，比字符串长度多了一行一列
    m=[[0 for i in range(len(s2)+1)]  for j in range(len(s1)+1)]
    #最长匹配的长度
    mmax=0
    #最长匹配对应在s1中的最后一位
    p=0  
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i]==s2[j]:
                m[i+1][j+1]=m[i][j]+1
                if m[i+1][j+1]>mmax:
                    mmax=m[i+1][j+1]
                    p=i+1
    #返回最长子串及其长度                
    return mmax

#
#  8 3 1500
#  low mean 1.14e-4
#  high mean 8e-5
#

class SolveData:
    def __init__(self,filename="time_line.log",m_filter=True):
        self.m_filter = m_filter
        self.fence_divation = 1.6e-5 # TODO
        self.split_value = 1.195e-6  # TODO
        self.high_wave_range = [5.94e-4, 1.939e-3] # TODO
        self.low_wave_range = [5.94e-4, 1.939e-3] # TODO

        self.high_wave_mean_value = 9e-5 # TODO 90 %   value mean 
        self.low_wave_mean_value =  9e-5  # TODO 90 %   value mean 
        self.raw_data = numpy.loadtxt(filename)

        self.INTERVAL_SIZE =50
        self.get_data = []
        
        return

    def init_interval_list(self):
        k, t  = 0, 0
        last_number = 0 # TODO
        interval_list = []
        flag_litter_or_big = 0 # TODO [0 1 2]  1 --> high wave
                                            #  2 --> low wave
                
        for i in range(10000, len(self.raw_data)):
            t += self.raw_data[i]  # time axis    
            # choice according what
            if self.m_filter:
                if self.raw_data[i] > 1.27341e-6 or self.raw_data[i] < 1.15199e-6:   # noise filtration   data may be modify
                    continue
            if k != self.INTERVAL_SIZE-1:    # mean  data smooth  duration gap 50 
                k += 1
                tmp = self.raw_data[i]
                interval_list.append(self.raw_data[i])
                if sum(interval_list)/k > self.split_value:
                    flag_litter_or_big = 2
                else:
                    flag_litter_or_big = 1
            else:
                interval_list.append(self.raw_data[i])
                tmp = sum(interval_list)/self.INTERVAL_SIZE
                interval_list.remove(interval_list[0])

            if tmp >= self.split_value and flag_litter_or_big == 2:  # 一直在高波形
                continue
            if tmp <= self.split_value and flag_litter_or_big == 1:  # 一直在低波形
                continue

            if tmp > self.split_value and flag_litter_or_big == 1:  # 低波形出现高波形
                self.get_data.append(t)
                flag_litter_or_big = 2
                continue
            if tmp < self.split_value and flag_litter_or_big ==  2:
                self.get_data.append(t)
                flag_litter_or_big = 1
                continue
        return
    

    def filter_getData(self):

        for i in range(1,len(self.get_data)):
            self.get_data[i-1] = self.get_data[i] -self.get_data[i-1]
        print(self.get_data)

        self.get_data.pop()
        if self.get_data[0] <= self.fence_divation:
            self.get_data[1] += self.get_data[0]
            self.get_data.pop(0)
        print(self.get_data)
        input()
        si = len(self.get_data)
        i=1
        while i < si:
            if self.get_data[i] < self.fence_divation:
                self.get_data[i-1] += self.get_data[i]
                self.get_data[i-1] += self.get_data[i+1]
                self.get_data.pop(i)
                self.get_data.pop(i+1)
                i -= 2
                si -= 2
            i += 1
        return

    def error_rate(self,data):
        schr ="10101010101010101010100000000000000010100000010010011000011001001001011100000000010101010001111101110011010001110110011001001101110000010010100011011111000001100101001111110000010110001001010000010010100011101101010011111001000011111011100010001101111111000110111011001011110101110000010001000110101000000111101101100101011110100111011101111110111101"
        size = len(schr)
        m = 0
        t = 999999999
        for i in range(size):
            lg_edit_size = minDistance(data[i:i+size],schr)
            if t > lg_edit_size:
                t = lg_edit_size
                m = i
        print(data)
        print("offset->{}\nmin_edit_distance->{}".format(t,m))

    def solve_main(self):
        self.init_interval_list()
        self.filter_getData()

        print(self.get_data)

        data = ""
        for i in range(0,len(self.get_data)):
            if i%2==0:
                data += round(self.get_data[i]/self.high_wave_mean_value)*'1'
            else:
                data += round(self.get_data[i]/self.low_wave_mean_value)*'0'
        self.error_rate(data)

        data =""
        for i in range(0,len(self.get_data)):
            if i%2==1:
                data += round(self.get_data[i]/self.high_wave_mean_value)*'1'
            else:
                data += round(self.get_data[i]/self.low_wave_mean_value)*'0'
        
        self.error_rate(data)
        return








        


if __name__=="__main__":
    if len(sys.argv) == 3:
        m_filter = False
        filename = sys.argv[1]
    else:
        m_filter =  True
        filename = sys.argv[1]
    SD = SolveData(filename,m_filter)
    SD.solve_main()
