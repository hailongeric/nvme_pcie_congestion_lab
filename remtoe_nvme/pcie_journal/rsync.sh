#!/bin/bash

rsync -avz --exclude "time_line.log" ./ vam@10.177.74.236:/home/vam/pcie_journal/
rsync -avz --exclude "time_line.log" ./ vam@10.177.74.243:/home/vam/pcie_journal/