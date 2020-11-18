#!/bin/sh
cd /vmfs/volumes/1TB_USB_Direct/scripts
date >> ./vrops_cpu_temp.log
python ./vrops_cpu_temp.py >> ./vrops_cpu_temp.log
