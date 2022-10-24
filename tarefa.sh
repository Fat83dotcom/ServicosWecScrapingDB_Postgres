#! /bin/bash
# Scrip a ser executado pelo CRON
#echo "Tarefa Realizada $(date '+%d-%m-%Y %H:%M:%S')" >> logs/log.txt
<<<<<<< HEAD
source /home/fernando/Documentos/ServicosWecScrapingDB_Postgres/venv/bin/activate
=======

source ./venv/bin/activate
>>>>>>> b63fc7042bbb41aaccf78472ad1bfaa8bdbd2497
python -u "/home/fernando/Documentos/ServicosWecScrapingDB_Postgres/main.py"