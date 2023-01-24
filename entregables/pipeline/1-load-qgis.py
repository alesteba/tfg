from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.utils import LayerMapping
from core.models import *

from pathlib import Path

class Command(BaseCommand):

    help = 'Carga la geometría a las entidades de parcela y pixel. Los datos son leidos desde QGIS.'

    def add_arguments(self, parser):

        parser.add_argument('-par', '--parcelas', type=Path)
        parser.add_argument('-pxl', '--pixels', type=Path)

    def handle(self,  *args, **kwargs):

        parcelas = kwargs['parcelas']
        piexels = kwargs['pixels']

        self.run(parcelas, piexels)

    def run(self, PARCELA_SHAPE=None, PIXEL_SHAPE=None, verbose=True):

        PARCELA_MAPPING = {
            'idx': 'idx',
            'geom': 'MULTIPOLYGON',
        }

        PIXEL_MAPPING = {
            'idx': 'id',
            'geom': 'MULTIPOLYGON',
            'parcela': {'idx' : 'idx'}
        }

        print(PARCELA_SHAPE)

        # Carga las parcelas
        lm = LayerMapping(Parcela, PARCELA_SHAPE, PARCELA_MAPPING)

        lm.save(strict=True, verbose=verbose)

        # Carga los pixels
        lmp = LayerMapping(Pixel, PIXEL_SHAPE, PIXEL_MAPPING)
        
        lmp.save(strict=True, verbose=verbose)

        # link pixel-parcela
        for p in Pixel.objects.all():

            p.geojson = {'type': 'Feature',
                        'properties': {'idx': str(p.idx)},
                        'geometry': {
                            'type': 'MultiPolygon',
                            'coordinates': p.geom.coords,
                            }
                        }
            p.save()

        # add geojson to parcela
        for p in Parcela.objects.all():

            p.geojson = {
                'type': 'Feature',
                'properties': {'idx': str(p.idx)},
                'geometry': {
                    'type': 'MultiPolygon',
                    'coordinates': p.geom.coords,
                }
            }

            p.save()