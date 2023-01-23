# from asyncio.windows_events import NULL
from django.core.management.base import BaseCommand, CommandError
from core.models import *
import pandas as pd
from pathlib import Path
from random import randrange

class Command(BaseCommand):

    help = 'Leer cultivos desde excel e integrar con el resto de datos'

    def add_arguments(self, parser):
        
        parser.add_argument('-xls', '--excel', type=Path)

    def handle(self,  *args, **kwargs):

        FICHERO_PATH = kwargs['excel']

        self.run(FICHERO_PATH)

    def run(self, FICHERO_PATH):

        data = pd.read_excel(FICHERO_PATH)

        for i in data.index:

            if (not Cultivo.objects.filter(nombre=data["variedad"][i]).exists()):

                variedad = Cultivo(

                    nombre = data["variedad"][i], 
                    descripcion = None, 
                    es_variedad = None,
                )

                variedad.save()

            # filtrar por los 4 a la vez:

            siembra, created = Fenologico.objects.get_or_create(nombre="siembra")
            siembra.save()

            if (Mirar_Fenologico.objects.filter(

                    parcela=data["referencia"][i], # parcela id
                    cultivo=data["variedad"][i],
                    estado=siembra.nombre, # id clave FK
                    fecha=data["siembra"][i]

                ).count() == 0):

                # creamos la entidad

                feno_id = randrange(1000)

                # from datetime import date

                mirar_feno = Mirar_Fenologico(

                    feno_id,

                    data["referencia"][i], #parcela id
                    data["variedad"][i], #como es id se lo paso;

                    siembra.nombre,
                    data["siembra"][i],
                )

                mirar_feno.save()