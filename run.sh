#!/bin/bash

export DISPLAY=:0
export PATH=$HOME/miniconda/bin:$PATH
cd $(dirname "$0")
LOG_FILE="spension.log"

ruby vc_historical.rb 2>&1 | tee -a ${LOG_FILE}
ruby vc_this_year.rb  2>&1 | tee -a ${LOG_FILE}
ruby vc_this_month.rb  2>&1 | tee -a ${LOG_FILE}
python cleancsv.py  2>&1 | tee -a ${LOG_FILE}
python curator.py 2>&1 | tee -a ${LOG_FILE}
jupyter nbconvert --to notebook --execute ValoresCuotaCapital.ipynb --output ValoresCuotaCapital.ipynb 2>&1 | tee -a ${LOG_FILE}
jupyter nbconvert --to notebook --execute ValoresCuotaCuprum.ipynb --output ValoresCuotaCuprum.ipynb 2>&1 | tee -a ${LOG_FILE}
jupyter nbconvert --to notebook --execute ValoresCuotaHabitat.ipynb --output ValoresCuotaHabitat.ipynb 2>&1 | tee -a ${LOG_FILE}
jupyter nbconvert --to notebook --execute ValoresCuotaModelo.ipynb --output ValoresCuotaModelo.ipynb 2>&1 | tee -a ${LOG_FILE}
jupyter nbconvert --to notebook --execute ValoresCuotaPlanvital.ipynb --output ValoresCuotaPlanvital.ipynb 2>&1 | tee -a ${LOG_FILE}
jupyter nbconvert --to notebook --execute ValoresCuotaProvida.ipynb --output ValoresCuotaProvida.ipynb 2>&1 | tee -a ${LOG_FILE}
