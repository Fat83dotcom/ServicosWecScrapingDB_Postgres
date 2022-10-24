#! /bin/bash
# Scrip a ser executado pelo CRON
#echo "Tarefa Realizada $(date '+%d-%m-%Y %H:%M:%S')" >> logs/log.txt

source /home/fernando/Documentos/ServicosWecScrapingDB_Postgres/venv/bin/activate
python -u "/home/fernando/Documentos/ServicosWecScrapingDB_Postgres/mainCNN.py"