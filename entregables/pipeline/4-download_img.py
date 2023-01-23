from pathlib import Path
from core.models import *
from django.core.management.base import BaseCommand
import random
from datetime import date

from sentinelS2 import SentinelS2
import geopandas as gpd
import pandas as pd

# algunos comentarios:
# si no hay datos, no hay columnas, por lo que no se persiste nada.

class Command(BaseCommand):

    help = 'Descarga datos de NDVIs para el parecelario establecido'

    def add_arguments(self, parser):

        parser.add_argument('-a', '--date1', type=date)
        parser.add_argument('-b', '--date2', type=date)

        parser.add_argument('-p', '--pixels', type=Path)
        parser.add_argument('-i', '--indices', type=str)

    def handle(self,  *args, **kwargs):

        fecha_start = kwargs['date1']
        fecha_end = kwargs['date2']

        pixels = kwargs['pixels']
        indice = kwargs['indices']

        self.run(fecha_start, fecha_end, pixels, indice)

    def run (self, FECHA_START, FECHA_END, PIXEL_SHAPE=None, INDICES = ['ndvi', 'ndre']):

        # today = date.today()
        # fecha_end = today - timedelta(days = 0)
        # fecha_start = today - timedelta(days = RANGE)

        # EJECUCIÓN SCRIPT

        #ruta_parcelas = r'/mnt/c/Users/reuni/Desktop/Agrai-World/agrai/data/parcelas/25/pixeles.shp'

        # descargar todos los indices 

        s2 = SentinelS2(str(PIXEL_SHAPE), 'id')

        fecha_start = FECHA_START.strftime('%Y-%m-%d')
        fecha_end = FECHA_END.strftime('%Y-%m-%d')

        # en este caso el mean hace referencia al valor del pixel, no necesitamos nada más.
        estadisticos = ['mean']
        indices_vegetativos = INDICES # ejecutar solo con un índice para quedarte con cols por fecha
        start_date = fecha_start
        end_date = fecha_end

        df = s2.download_data(start_date, end_date, indices_vegetativos, estadisticos)

        # no podemos devolver, persistimos valores:

        df.to_csv('down_img.csv', index=False)
