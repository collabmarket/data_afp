#!/bin/bash

export DISPLAY=:0
export PATH=$HOME/miniconda/bin:$PATH
cd $(dirname "$0")
LOG_FILE="spension.log"
DATE=$(date +%Y-%m-%d)

{
git pull
ruby vc_historical.rb
ruby vc_year.rb
ruby vc_month.rb
python cleancsv.py
python curator.py
jupyter nbconvert --to notebook --execute ValoresCuotaCapital.ipynb --output ValoresCuotaCapital.ipynb
jupyter nbconvert --to notebook --execute ValoresCuotaCuprum.ipynb --output ValoresCuotaCuprum.ipynb
jupyter nbconvert --to notebook --execute ValoresCuotaHabitat.ipynb --output ValoresCuotaHabitat.ipynb
jupyter nbconvert --to notebook --execute ValoresCuotaModelo.ipynb --output ValoresCuotaModelo.ipynb
jupyter nbconvert --to notebook --execute ValoresCuotaPlanvital.ipynb --output ValoresCuotaPlanvital.ipynb
jupyter nbconvert --to notebook --execute ValoresCuotaProvida.ipynb --output ValoresCuotaProvida.ipynb
git add rawdata/*.csv data/*.csv *.ipynb
git commit -m "Update data and nb $DATE"
git push
} 2>&1 | tee -a ${LOG_FILE}
