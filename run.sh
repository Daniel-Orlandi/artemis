#!/bin/sh
source /opt/conda/bin/activate
conda activate carga
python /home/mdata/planilhas_carga/carga/main.py
conda deactivate
