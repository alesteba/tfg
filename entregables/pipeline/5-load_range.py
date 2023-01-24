from pathlib import Path
from core.models import *
import random
from datetime import date

from django.core.management.base import BaseCommand
from django.core.management import call_command

from .managment_command import LoggingBaseCommand

import pandas as pd

class Command(BaseCommand):

    help = 'Llama a los scrips de descarga con solo un índice poder obtener sus valores en diferentes fechas. Luego se persite.'

    def add_arguments(self, parser):

        parser.add_argument('-d', '--data', type=pd.DataFrame)
        parser.add_argument('-i', '--indices', type=str)

    def handle(self,  *args, **kwargs):

        df = kwargs['data']
        indices = kwargs['indices']

        self.run(df, indices)

    def run (self, DATA, INDICES):

        # el data frame de descarga proveniente del script anterior es una mezcla de todos los índices.
        # necesitamos limpiarlo para quedarnos solo con las columnas respectivas a ese índice
        # para posteriormente extraer los valores en las diferentes fechas.

        for indice in INDICES:

            # CLEAN DF: quedarnos solo con las columnas de un índice:

            df = DATA.copy()

            drop_cols = []

            for col_name in list(df):

                if indice.upper() not in col_name:

                    if (col_name == 'ID'):

                        continue

                    drop_cols.append(col_name)

            df1 = df.drop(drop_cols, axis=1)

            # pass new df to load_indice

            call_command('4-load_indice', data=df1, indice=indice)