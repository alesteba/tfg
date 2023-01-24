from django import forms

from core.models.models import Parcela, Mirar_Indice, Mirar_Fenologico

class ParcelaCultivos_Service():

    def get_cultivo(parcela_p):
    
        """ último cultivo que se está cultivando en una parcela """

        mirar_feno = Mirar_Fenologico.objects.filter(parcela = parcela_p.idx)

        if (mirar_feno.count() > 0):

            return mirar_feno.order_by('fecha')[0].cultivo

        else:

            return None

    def get_historico_fenologicos(parcela_p):

        """ todos los estados fenológicos por los que ha pasado una parcela """

        return Mirar_Fenologico.objects.filter(parcela = parcela_p.referencia)

    def get_historico_range(fecha_inicio, fecha_end):

        """ histórico de todas las parcelas en un rango de fechas """
    
        return Mirar_Fenologico.objects.filter(fecha__range=[fecha_inicio, fecha_end])

    def get_historico_parcela(parcela1):

        """ todo el histórico de una parcela """
    
        return Mirar_Fenologico.objects.filter(parcela = parcela1)

    def get_historico_parcela_range(parcela1, fecha_inicio, fecha_end):

        """ hostórico de una parcela en un rango de fechas """

        historico = ParcelaCultivos_Service.get_historico_range(fecha_inicio, fecha_end)

        return historico.filter(parcela = parcela1)

    def get_historico_mismo_fenologico(valor_fenologico):
    
        """ todo los cultivos que están en un mismo estado fenológico """

        return Mirar_Fenologico.objects.filter(estado = valor_fenologico)