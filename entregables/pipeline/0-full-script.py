

from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.contrib.gis.gdal import DataSource

from .managment_command import LoggingBaseCommand

import os
from pathlib import Path

import pandas as pd
import csv
import datetime
from datetime import datetime

class Command(LoggingBaseCommand):

    help = 'Carga la geometría a las parcelas y a los pixeles'

    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

    PARCELA_SHAPE = BASE_DIR / 'data' / 'parcelas' / '25' / 'parcelas.shp'
    PIXEL_SHAPE = BASE_DIR / 'data' / 'parcelas' / '25' / 'pixeles.shp'
    FICHERO_PATH  = BASE_DIR / 'data' / 'excels' /  'datos-test-2.xls'
    TRILINEA_PATH = BASE_DIR / 'data' / 'trilineas' / 'PRilineas.json'

    def handle(self,  *args, **kwargs):
    
        self.run()

    def run(self):
    
        # rango de fechas para las imágenes satelitales:

        fecha_start = datetime.strptime('2022/06/01', '%Y/%m/%d')
        fecha_end = datetime.strptime('2022/07/01', '%Y/%m/%d')

        # execute in order:

        print(Path(self.PARCELA_SHAPE))

        call_command('1-load-qgis', parcelas=self.PARCELA_SHAPE, pixels=self.PIXEL_SHAPE)

        call_command('2-load-parcela-data', excel=str(self.FICHERO_PATH))

        call_command('3-load-cultivos', excel=str(self.FICHERO_PATH))

        # call_command(
            
        #     '4-download_img', 
        #     date1=fecha_start, 
        #     date2=fecha_end, 
        #     pixels=self.PIXEL_SHAPE, 
        #     indices=['ndvi', 'ndre']
        # )

        # load downloaded indices:

        df = pd.read_csv('down_img.csv')

        call_command('4-load_range', data=df, indices=['ndvi', 'ndre'])

    