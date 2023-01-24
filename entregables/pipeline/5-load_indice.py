from pathlib import Path
from core.models import *
from django.core.management.base import BaseCommand
import random
from datetime import date

from sentinelS2 import SentinelS2
import geopandas as gpd
import pandas as pd

class Command(BaseCommand):

    help = 'Persiste los datos de NDVIs para el parecelario establecido'

    def add_arguments(self, parser):

        # con esta estructura no casca:

        parser.add_argument('-d', '--data', type=pd.DataFrame)
        parser.add_argument('-i', '--indice', type=str)

    def handle(self,  *args, **kwargs):

        df = kwargs['data']
        indice = kwargs['indice']

        self.run(df, indice)

    def run (self, df1, INDICE):

        # INDICE:

        indice, created = Indice.objects.get_or_create(nombre=INDICE)

        # ANADIR DATOS AL MODELO

        for p in Pixel.objects.all():

            for col_name in list(df1):

                if col_name == 'ID':

                    continue

                date_transform = datetime.strptime(col_name[-8:], '%Y%m%d')

                id_to_str = float(str(p.idx) + '.0')

                pixel_in_df = df1[df1['ID'] == id_to_str][col_name] 

                valor = float(pixel_in_df)

                # comprobar que la fecha no existe y no hay otro indice para el mismo pixel

                if (Mirar_Indice.objects.filter(

                    pixel=p, indice=indice, fecha=date_transform

                ).count() == 0):

                    m = Mirar_Indice(

                        pixel=p, 
                        indice=indice, 
                        valor=valor, 
                        fecha=date_transform,
                    )
                        
                m.save()