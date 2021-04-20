#!/bin/bash

gap_num_arr=(3 4 5 6 7 8 9 10 11 12 13 14 15 16 20 30 40 60)
#gap_num_arr=(1 2 4 8)
#payload_size_arr=(600 700 800 900 1000 1100 1200 1300 1400 1500 1600 1700 1800 1900 2000 2100 2200 2300 2400 2500 2600 2700 2800 2900 3000 3100 3200 3300 3400 3500 3600 3700 3800 3900 4000 4100 4200 4300 4400 4500 4600 4700 4800 4900 5000 5100 5200 5300 5400 5500 5600 5700 5800 5900 6000 6100 6200 6300 6400 6500 6600 6700 6800 6900 7000 7100 7200 7300 7400 7500 7600 7700 7800 7900 8000 8100 8200 8300 8400 8500 8600 8700 8800 8900 9000 9100 9200 9300 9400 9500 9600 9700 9800 9900 10000 20000)

payload_size_arr=(100 200 300 400 500 600 700 800 900 1000 1100 1200 1300) #600 700 800 900 1000 1100 1200 1300 1400 1500 1600 1700 1800 1900 2000 2100 2200)
#payload_size_arr=(11000 15000 20000 30000 40000 50000 60000 65000)

for gap_num in ${gap_num_arr[@]};
do

for payload_size in ${payload_size_arr[@]};
do

ssh vam@10.177.74.236  << eeooff
echo "-----start recv_data_client -----"
if pgrep recv_data_clien; then pkill recv_data_clien; fi
cd /home/vam/pcie_journal
nohup nice -20 taskset 4 ./recv_data_client > log &
echo "----- finish start recv_data_client -----"
exit
eeooff



ssh vam@10.177.74.243 << eeooff
echo "-----start send_data_server -----"
if pgrep send_data_serve; then pkill send_data_serve; fi
cd /home/vam/eric
nohup nice -20 taskset 4 ./send_data_server ${payload_size} ${gap_num} > log &
echo "----- finish start send_data_server -----"
exit
eeooff


ssh vam@10.177.74.236 << eeooff
echo "-----start time_line -----"
if pgrep time_line; then exit; fi
cd /home/vam/main_line
./time_line
echo "----- finish start time_line -----"
exit 
eeooff

scp vam@10.177.74.236:/home/vam/main_line/time_line.log  time_line_${payload_size}_${gap_num}_2.log

echo "payload_size: ${payload_size} , gap_num: ${gap_num} "
sleep 1

done
done
#python3 show_line.py

