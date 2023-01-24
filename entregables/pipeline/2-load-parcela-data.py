from django.core.management.base import BaseCommand, CommandError
from core.models import *
import pandas as pd
from pathlib import Path
from random import randrange

class Command(BaseCommand):

    help = 'Leer datos de parcelas y estaciones de excels. Completa los datos no georeferenciados de las parcelas.'

    def add_arguments(self, parser):
    
        parser.add_argument('-xls', '--excel', type=Path)

    def handle(self,  *args, **kwargs):

        FICHERO_PATH = kwargs['excel']

        self.run(FICHERO_PATH)

    def run(self, FICHERO_PATH):

        data = pd.read_excel(FICHERO_PATH)

        for i in data.index:

            # ESTACION:

            if (not Estacion.objects.filter(id=data["estacion"][i]).exists()):

                estacion = Estacion(data["estacion"][i])

                estacion.save()

            # PARCELA

            if (Parcela.objects.filter(idx=data["referencia"][i]).exists()):

                parcela = Parcela.objects.filter(idx=data["referencia"][i])[0]

                parcela.estacion = Estacion.objects.filter(id=data["estacion"][i])[0]

                parcela.provincia =  data["provincia"][i]
                parcela.municipio = data["municipio"][i]
                parcela.poligono = data["poligono"][i]

                parcela.altitud = data["elevacionm"][i]
                parcela.pendiente = data["pendientem"][i]
                parcela.orientacion = data["aspectmean"][i]

                parcela.save()

                print(parcela)