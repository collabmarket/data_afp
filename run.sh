#!/bin/bash

export DISPLAY=:0
export PATH=$HOME/miniconda/bin:$PATH
cd $(dirname "$0")
LOG_FILE="spension.log"
DATE=$(date +%Y-%m-%d)
shopt -s expand_aliases
alias NBC="jupyter nbconvert --to notebook --execute"

{
git pull
ruby vc_historical.rb
ruby vc_year.rb
ruby vc_month.rb
python cleancsv.py
python curator.py
NBC ValoresCuotaCapital.ipynb --output ValoresCuotaCapital.ipynb
NBC ValoresCuotaCuprum.ipynb --output ValoresCuotaCuprum.ipynb
NBC ValoresCuotaHabitat.ipynb --output ValoresCuotaHabitat.ipynb
NBC ValoresCuotaModelo.ipynb --output ValoresCuotaModelo.ipynb
NBC ValoresCuotaPlanvital.ipynb --output ValoresCuotaPlanvital.ipynb
NBC ValoresCuotaProvida.ipynb --output ValoresCuotaProvida.ipynb
git add rawdata/*.csv data/*.csv *.ipynb
git commit -m "Update data and nb $DATE"
git push
} 2>&1 | tee -a ${LOG_FILE}
