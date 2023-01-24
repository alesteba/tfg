from django import forms
from django.db.models import Avg

from core.models.models import Parcela, Mirar_Indice, Indice

import numpy as np

class ParcelaIndices_Service():

    """consultas frequentes sobre los indices"""

    def get_all_indices(parcela, indice_p):

        """ devuelve todos los valores de un índice para una parcela, es decir en todos sus avistamientos (fechas) """
    
        pixels = parcela.get_pixeles()

        indice_p = Indice.objects.get(nombre=indice_p) if type(indice_p) == str else indice_p

        return Mirar_Indice.objects.filter(pixel__in = pixels, indice = indice_p)

    def get_current_status(parcela, indice_p):

        """ estado actual de una parcela para un índice concreto """

        pixels = parcela.get_pixeles()

        indice_p = Indice.objects.get(nombre=indice_p) if type(indice_p) == str else indice_p

        mi = Mirar_Indice.objects.filter(pixel__in = pixels, indice = indice_p)

        return mi.values('fecha').annotate(Avg('valor')).order_by('fecha')

    def get_indice_func(parcela, indice_p, fecha_p, func, filtro):

        """Método que encapsula el uso de una función agregada junto con un filtro """

        indice_p = Indice.objects.get(nombre=indice_p) #if type(indice_p) == str else indice_p
    
        if ParcelaIndices_Service.is_parcela_filter(parcela, filtro):

            pixels = parcela.get_pixeles()

            indices_pixels = Mirar_Indice.objects.filter(pixel__in = pixels, indice = indice_p, fecha = fecha_p)

            if ParcelaIndices_Service.get_indice_filter(indices_pixels, filtro):

                array_valores = list(indices_pixels.values_list('valor', flat=True))

                return func(array_valores)
            
            else:

                return None

        else:

            return None
        
