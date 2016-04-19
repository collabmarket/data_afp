#!/bin/bash

export DISPLAY=:0
cd $(dirname "$0")
LOG_FILE="spension.log"

ruby vc_historical.rb 2>&1 | tee -a ${LOG_FILE}
ruby vc_this_year.rb  2>&1 | tee -a ${LOG_FILE}
ruby vc_this_month.rb  2>&1 | tee -a ${LOG_FILE}
python cleancsv.py  2>&1 | tee -a ${LOG_FILE}
python curator.py 2>&1 | tee -a ${LOG_FILE}
