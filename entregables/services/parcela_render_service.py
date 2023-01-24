import numpy as np
from datetime import datetime

from core.models import Indice
from core.models.models import Parcela, Mirar_Indice

from .parcela_indices_service import ParcelaIndices_Service

class ParcelaRender_Service():

    """ algunas funciones para renderizar correctamente los datos de píxels (con sus índices) y su geometría en el visor GIS de la interfaz """

    # colors

    def get_color(indice):

        if indice < 0.245710073198591:
            return 'rgba(255, 69, 96, 1)'
        elif indice < 0.445710073198591:
            return 'rgba(254, 176, 25, 1)'
        elif indice < 0.645710073198591:
            return 'rgba(0, 227, 150, 1)'
        else:
            return 'rgba(0, 143, 251, 1)'

    def get_geojson_indice_func(parcelas, indice, fecha, func, filtro):
    
        date = datetime.strptime(fecha, '%d-%m-%Y') if type(fecha) == str else fecha

        indice = Indice.objects.get(nombre=indice)

        if func is None:

            # utilizando los servicios definidos anteriormente

            indices = [ParcelaIndices_Service.get_indices(p, indice, date, filtro) for p in parcelas]

            indices = np.concatenate(indices, axis=0)

            indices = list(filter(None, indices))

            geos = []
            
            for i in indices:

                geo = i.geojson

                geo['properties'] = {indice.nombre: ParcelaRender_Service.get_color(i.valor)}

                geos.append(geo)

            return geos

        else:

            geos = []

            for p in parcelas:

                valor = ParcelaIndices_Service.get_indice_func(p, indice, date, func, filtro)
                
                if valor is not None:

                    geo = p.geojson

                    geo['properties'] = {indice.nombre: ParcelaRender_Service.get_color(valor)}

                    geos.append(geo)

            return geos


    def get_all_pixeles(parcelas):

        return [ParcelaIndices_Service.get_all_pixeles(p) for p in parcelas]
    

    def get_images_dates(parcelas, indice):

        indices = [ParcelaIndices_Service.get_all_indices(p, indice) for p in parcelas]

        indices = np.concatenate(indices, axis=0)

        fechas = [i.fecha for i in indices]

        return list(reversed(sorted(list(set(fechas)))))


    def get_best_worse_five(parcelas, indice, date):

        plist = []

        for p in parcelas:

            valor = ParcelaIndices_Service.get_indice_func(p, indice, date, np.mean, [None,None,None])
            plist.append((p, valor))

        plist = sorted(plist, key=lambda x: x[1])
        
        best = plist[-5:]
        worse = plist[:5]

        best = [b[0] for b in best]
        worse = [w[0] for w in worse]

        return best, worse