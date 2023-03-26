"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    
    data_structs = {
            "size": 0,#tamaño de las filas cargadas
            "anios": None
            }
    data_structs["anios"] = mp.newMap(numelements=11,maptype = "PROBING",
                                              loadfactor= 0.5,
                                              cmpfunction=None)    
    return data_structs
    

# Funciones para agregar informacion al modelo
def create_base(data_structs,data,tipo_mapa,factor_carga):
        new_map = me.newMapEntry(data["Año"],mp.newMap(3,
                                              maptype = tipo_mapa,
                                              loadfactor= factor_carga,
                                              cmpfunction=None))
        mp.put(data_structs["anios"],me.getKey(new_map),me.getValue(new_map))
        
        map = me.getValue(mp.get(data_structs["anios"],data["Año"]))
                
        element_entry = me.newMapEntry("elements",lt.newList(datastructure="ARRAY_LIST",cmpfunction=
                                                                  compare))
        
        mp.put(map,me.getKey(element_entry),me.getValue(element_entry))
        
        subsector_entry = me.newMapEntry("sub_sector",mp.newMap(21,maptype = tipo_mapa,
                                              loadfactor= factor_carga,
                                              cmpfunction=None))
        mp.put(map,me.getKey(subsector_entry),me.getValue(subsector_entry))
        
        sector_entry = me.newMapEntry("sector",mp.newMap(12,maptype = tipo_mapa,
                                              loadfactor= factor_carga,
                                              cmpfunction=None))
        mp.put(map,me.getKey(sector_entry),me.getValue(sector_entry))
        

        
        entry_sector = me.newMapEntry(data["Código sector económico"],mp.newMap(numelements=2,maptype = tipo_mapa,
                                              loadfactor= factor_carga,
                                              cmpfunction=None))
        
        map_sectores = me.getValue(mp.get(map,"sector")) # obtenemos el map por sectores
        
        # [obtenemos el map de sector el cual tendra parejas (cod sector,map) , obtenemos la llave que deseamos meter, obtenemos el value que deseamos obtener]
        mp.put(map_sectores,me.getKey(entry_sector),me.getValue(entry_sector)) 
         
        map_sector_cod = me.getValue(mp.get(map_sectores,me.getKey(entry_sector))) #encuentra el map de un sector economico especifico
        
        lst_sector = me.newMapEntry("elements",lt.newList(datastructure="ARRAY_LIST",cmpfunction=
                                                                  None)) # esta pareja llave valor contiene como llave un  str y como valor el array_klist de los elementos pertencienctes al a un sector economico especifico
             
        mp.put(map_sector_cod,me.getKey(lst_sector),me.getValue(lst_sector)) # ponemos el array_list que contendra todos los elementos de este sector en el map pertenciente a ese sector
        
        #MOD REQ 6
        subsectores_en_sector = me.newMapEntry("subsector en el sector",lt.newList("ARRAY_LIST"))
        mp.put(map_sector_cod,me.getKey(subsectores_en_sector),me.getValue(subsectores_en_sector))
        
        #---------- suma ----------
        suma_ingresos_netos_sector = me.newMapEntry("ingresos netos",0)
        mp.put(map_sector_cod,me.getKey(suma_ingresos_netos_sector),me.getValue(suma_ingresos_netos_sector)) # añadimos la sumatoria ingresos netos inicial 0
        
        suma_costos_y_gastos_sector = me.newMapEntry("costos y gastos",0)
        mp.put(map_sector_cod,me.getKey(suma_costos_y_gastos_sector),me.getValue(suma_costos_y_gastos_sector))
        
        suma_saldo_a_pagar_sector = me.newMapEntry("saldo a pagar",0)
        mp.put(map_sector_cod,me.getKey(suma_saldo_a_pagar_sector),me.getValue(suma_saldo_a_pagar_sector))
        
        suma_saldo_a_favor_sector = me.newMapEntry("saldo a favor",0)
        mp.put(map_sector_cod,me.getKey(suma_saldo_a_favor_sector),me.getValue(suma_saldo_a_favor_sector))
        #---------- suma ---------
        
        entry_sub = me.newMapEntry(data["Código subsector económico"],mp.newMap(numelements=8,maptype = tipo_mapa,
                                              loadfactor= factor_carga,
                                              cmpfunction=None)) # crea pareja llave valor entry_sub (codigo_sub_sector,map del sub_sector)
        
        map_sub_sector = me.getValue(mp.get(map,"sub_sector"))
        
        mp.put(map_sub_sector,me.getKey(entry_sub),me.getValue(entry_sub))
        
        lst_subsector = me.newMapEntry("elements",lt.newList(datastructure="ARRAY_LIST",cmpfunction=
                                                                  None))
        
        map_sub_sector_cod =me.getValue(mp.get(map_sub_sector,me.getKey(entry_sub))) # obtenemos el map de un cod de un subsector
        
        mp.put(map_sub_sector_cod,me.getKey(lst_subsector),me.getValue(lst_subsector))
        
        #aqui vamos
                
        #----------------------  parte de la suma ----------------#
        
        #pareja (llave, valor) de costos y gastos nomina #
        entry_cyg_n = me.newMapEntry("Costos y gastos nomina",0)
        mp.put(map_sub_sector_cod,me.getKey(entry_cyg_n),me.getValue(entry_cyg_n))
        
        """
        cyg_n = me.getValue(mp.get(map_sub_sector_cod,me.getKey(entry_cyg_n)))
        cyg_n += int(data["Costos y gastos nómina"])
        entry_cyg_n = me.newMapEntry("Costos y gastos nomina",cyg_n)
        mp.put(map_sub_sector_cod,me.getKey(entry_cyg_n),me.getValue(entry_cyg_n))
        """
        #/pareja llave, valor de costos y gastos nomina #
        
        #pareja llave valor retenciones  sub#
        entry_retenciones = me.newMapEntry("retenciones",0)
        mp.put(map_sub_sector_cod,me.getKey(entry_retenciones),me.getValue(entry_retenciones))
        #/pareja llave valor retenciones  sub#
        
        #pareja llave valor ingresos netos sub_sector#
        
        entry_ingresos_netos = me.newMapEntry("ingresos netos",0) #crea una pareja llave valor (ingresos netos, total ingresos netos del sub_sector)
        mp.put(map_sub_sector_cod,me.getKey(entry_ingresos_netos),me.getValue(entry_ingresos_netos)) # añade la pareja llave valor al mapa 
        """
        i_n = me.getValue(mp.get(map_sub_sector_cod,"ingresos netos")) #obtenemos el valor de la pareja llave valor (ingresos netos, total ingresos netos), el cual seran los actuales ingresos netos del subsector
        i_n += int(data["Total ingresos netos"]) # a los ingresos netos actuales le suumamos los de la nueva actividad economica
        entry_ingresos_netos = me.newMapEntry("ingresos netos",i_n) # creamos otra vez una pareja llave valor la cual tendra como lalve la misma de arriba y como valor los nuevos ingresos netod del subsector
        mp.put(map_sub_sector_cod,me.getKey(entry_ingresos_netos),me.getValue(entry_ingresos_netos)) # ponemos esta nueva pareja llave valor en el mapa
        """
        #/pareja llave valor ingresos netos sub_sector#
        
        #pareja llave valor costos y gastos sub_sector#
        entry_cyg = me.newMapEntry("costos y gastos",0)
        mp.put(map_sub_sector_cod,me.getKey(entry_cyg),me.getValue(entry_cyg))
        """
        cyg = me.getValue(mp.get(map_sub_sector_cod,"costos y gastos"))
        cyg += int(data["Total costos y gastos"])
        entry_cyg = me.newMapEntry("costos y gastos",cyg)
        mp.put(map_sub_sector_cod,me.getKey(entry_cyg),me.getValue(entry_cyg))        
        """
        #/pareja llave valor costos y gastos sub_sector#
        
        #pareja llave valor saldo a pagar sub_sector#
        entry_sp = me.newMapEntry("saldo a pagar",0)
        mp.put(map_sub_sector_cod,me.getKey(entry_sp),me.getValue(entry_sp))
        """
        sp =me.getValue(mp.get(map_sub_sector_cod,"saldo a pagar"))
        sp += int(data["Total saldo a pagar"])
        entry_sp = me.newMapEntry("saldo a pagar",sp)
        mp.put(map_sub_sector_cod,me.getKey(entry_sp),me.getValue(entry_sp))
        """
        #/pareja llave valor saldo a pagar sub_sector#
        
        #pareja llave valor saldo a favor
        entry_sf = me.newMapEntry("saldo a favor",0)
        mp.put(map_sub_sector_cod,me.getKey(entry_sf),me.getValue(entry_sf))
        """
        sf = me.getValue(mp.get(map_sub_sector_cod,"saldo a favor"))
        sf += int(data["Total saldo a favor"])
        entry_sf = me.newMapEntry("saldo a favor",sf)
        mp.put(map_sub_sector_cod,me.getKey(entry_sf),me.getValue(entry_sf))
        """
        
        #/ pareja llave valor saldo a favor
        
        #pareja llave valor descuentos tributarios
        entry_dt = me.newMapEntry("Descuentos tributarios",0)
        mp.put(map_sub_sector_cod,me.getKey(entry_dt),me.getValue(entry_sf))
        #pareja llave valor descuentos tributarios
        
        #------------- parte de la suma --------------#
def add(data_structs,data,tipo_mapa,factor_carga):
        map =  me.getValue(mp.get(data_structs["anios"],data["Año"]))
        lst = me.getValue(mp.get(map,"elements"))
        lt.addLast(lst,data) #añade la nueva actividad economica a la lista con todas las actividades economicas del año
        
        map_sectores = me.getValue(mp.get(map,"sector"))
        
        if not(mp.contains(map_sectores,data["Código sector económico"])):
            entry = me.newMapEntry(data["Código sector económico"],mp.newMap(numelements=2,maptype = tipo_mapa,
                                              loadfactor= factor_carga,
                                              cmpfunction=None)) # Creamos la pareja llave valor de (cod_sector,map_sector)
            mp.put(map_sectores,me.getKey(entry),me.getValue(entry))
            
            map_sector_cod = me.getValue(mp.get(map_sectores,data["Código sector económico"]))
            lst = me.newMapEntry("elements",lt.newList(datastructure="ARRAY_LIST",cmpfunction=
                                                                  compare))
            mp.put(map_sector_cod,me.getKey(lst),me.getValue(lst)) #ponemos la lista en el el el mapa de su respectivo sector
            
            #Subsectores en el sector---MOD req 6
            subsectores_en_sector = me.newMapEntry("subsector en el sector",lt.newList("ARRAY_LIST"))
            mp.put(map_sector_cod,me.getKey(subsectores_en_sector),me.getValue(subsectores_en_sector))
            
            #---------- Creamos la suma -----------
            suma_ingresos_netos_sector = me.newMapEntry("ingresos netos",0)
            mp.put(map_sector_cod,me.getKey(suma_ingresos_netos_sector),me.getValue(suma_ingresos_netos_sector)) # añadimos la sumatoria ingresos netos inicial 0
            
            suma_costos_y_gastos_sector = me.newMapEntry("costos y gastos",0)
            mp.put(map_sector_cod,me.getKey(suma_costos_y_gastos_sector),me.getValue(suma_costos_y_gastos_sector))
        
            suma_saldo_a_pagar_sector = me.newMapEntry("saldo a pagar",0)
            mp.put(map_sector_cod,me.getKey(suma_saldo_a_pagar_sector),me.getValue(suma_saldo_a_pagar_sector))
        
            suma_saldo_a_favor_sector = me.newMapEntry("saldo a favor",0)
            mp.put(map_sector_cod,me.getKey(suma_saldo_a_favor_sector),me.getValue(suma_saldo_a_favor_sector))
            #---------- Creamos la suma ----------
            
            
        map_sector_cod = me.getValue(mp.get(map_sectores,data["Código sector económico"]))
        lst = me.getValue(mp.get(map_sector_cod,"elements")) # obtenemos la lista de elementos que pertenecen al codigo de sector economico actual
        lt.addLast(lst,data) # añadimos el nuevo elemento a esta lista
        
        lista_subsectores_en_sector=me.getValue(mp.get(map_sector_cod,"subsector en el sector"))
        if lt.isPresent(lista_subsectores_en_sector,data["Código subsector económico"])==0:
            lt.addLast(lista_subsectores_en_sector,data["Código subsector económico"])
            
        #------------- suma ingresos netos -------
        ingresos_netos = me.getValue(mp.get(map_sector_cod,"ingresos netos"))
        ingresos_netos += int(data["Total ingresos netos"])
        entry_ingresos_netos = me.newMapEntry("ingresos netos",ingresos_netos)
        mp.put(map_sector_cod,me.getKey(entry_ingresos_netos),me.getValue(entry_ingresos_netos))
        #------------- suma ingresos netos------
        #otras sumas
        suma_costos_y_gastos_sector = me.getValue(mp.get(map_sector_cod,"costos y gastos"))
        suma_costos_y_gastos_sector += int(data["Total costos y gastos"])
        entry_costos_y_gastos_sector=me.newMapEntry("costos y gastos",suma_costos_y_gastos_sector)
        mp.put(map_sector_cod,me.getKey(entry_costos_y_gastos_sector),me.getValue(entry_costos_y_gastos_sector))
        
        suma_saldo_a_pagar_sector = me.getValue(mp.get(map_sector_cod,"saldo a pagar"))
        suma_saldo_a_pagar_sector += int(data["Total saldo a pagar"])
        entry_s_p_sec=me.newMapEntry("saldo a pagar",suma_saldo_a_pagar_sector)
        mp.put(map_sector_cod,me.getKey(entry_s_p_sec),me.getValue(entry_s_p_sec))
        
        suma_saldo_a_favor_sector = me.getValue(mp.get(map_sector_cod,"saldo a favor"))
        suma_saldo_a_favor_sector += int(data["Total saldo a favor"])
        entry_s_a_f_sec=me.newMapEntry("saldo a favor",suma_saldo_a_favor_sector)
        mp.put(map_sector_cod,me.getKey(entry_s_a_f_sec),me.getValue(entry_s_a_f_sec))
        
        #otras sumas    
    
        map_sub_sectores = me.getValue(mp.get(map,"sub_sector"))
        
        if mp.contains(map_sub_sectores,data["Código subsector económico"]):
            
            map_sub_sector_cod = me.getValue(mp.get(map_sub_sectores,data["Código subsector económico"]))
            lst = me.getValue(mp.get(map_sub_sector_cod,"elements")) # obtenemos la lista de elementos que pertenecen al codigo de sector economico actual
            lt.addLast(lst,data) # añadimos el nuevo elemento a esta lista
            
            #----------------------  parte de la suma ----------------#
        
        
        
            #pareja llave, valor de costos y gastos nomina #
            cyg_n = me.getValue(mp.get(map_sub_sector_cod,"Costos y gastos nomina"))
            cyg_n += int(data["Costos y gastos nómina"])
            entry_cyg_n = me.newMapEntry("Costos y gastos nomina",cyg_n)
            mp.put(map_sub_sector_cod,me.getKey(entry_cyg_n),me.getValue(entry_cyg_n))
            #pareja llave, valor de costos y gastos nomina #
        
            #pareja llave valor retenciones  sub#
            
            #TODO
            
            #/pareja llave valor retenciones  sub#
        
            #pareja llave valor ingresos netos sub_sector#
            i_n = me.getValue(mp.get(map_sub_sector_cod,"ingresos netos")) #obtenemos el valor de la pareja llave valor (ingresos netos, total ingresos netos), el cual seran los actuales ingresos netos del subsector
            i_n += int(data["Total ingresos netos"]) # a los ingresos netos actuales le suumamos los de la nueva actividad economica
            entry_ingresos_netos = me.newMapEntry("ingresos netos",i_n) # creamos otra vez una pareja llave valor la cual tendra como lalve la misma de arriba y como valor los nuevos ingresos netod del subsector
            mp.put(map_sub_sector_cod,me.getKey(entry_ingresos_netos),me.getValue(entry_ingresos_netos)) # ponemos esta nueva pareja llave valor en el mapa
                
            #/pareja llave valor ingresos netos sub_sector#
        
            #pareja llave valor costos y gastos sub_sector#
            cyg = me.getValue(mp.get(map_sub_sector_cod,"costos y gastos"))
            cyg += int(data["Total costos y gastos"])
            entry_cyg = me.newMapEntry("costos y gastos",cyg)
            mp.put(map_sub_sector_cod,me.getKey(entry_cyg),me.getValue(entry_cyg))        
        
            #/pareja llave valor costos y gastos sub_sector#
        
            #pareja llave valor saldo a pagar sub_sector#
            sp =me.getValue(mp.get(map_sub_sector_cod,"saldo a pagar"))
            sp += int(data["Total saldo a pagar"])
            entry_sp = me.newMapEntry("saldo a pagar",sp)
            mp.put(map_sub_sector_cod,me.getKey(entry_sp),me.getValue(entry_sp))
        
            #/pareja llave valor saldo a pagar sub_sector#
        
            #pareja llave valor saldo a favor
            sf = me.getValue(mp.get(map_sub_sector_cod,"saldo a favor"))
            sf += int(data["Total saldo a favor"])
            entry_sf = me.newMapEntry("saldo a favor",sf)
            mp.put(map_sub_sector_cod,me.getKey(entry_sf),me.getValue(entry_sf))
        
            #/ pareja llave valor saldo a favor
            #pareja (llave,valor) Total descuentos tributarios
            
            dt = me.getValue(mp.get(map_sub_sector_cod,"Descuentos tributarios"))
            dt += int(data["Descuentos tributarios"])
            entry_dt = me.newMapEntry("Descuentos tributarios",dt)
            mp.put(map_sub_sector_cod,me.getKey(entry_dt),me.getValue(entry_dt))
            #/pareja (llave,valor) Total descuentos tributarios
        
            #------------- parte de la suma --------------#

        else:
            entry = me.newMapEntry(data["Código subsector económico"],mp.newMap(numelements=8,maptype = tipo_mapa,
                                              loadfactor= factor_carga,
                                              cmpfunction=None)) # Creamos la pareja llave valor de (cod_sub_sector,map_sector)
            
            mp.put(map_sub_sectores,me.getKey(entry),me.getValue(entry))

            map_sub_sector_cod = me.getValue(mp.get(map_sub_sectores,data["Código subsector económico"]))

            lst = me.newMapEntry("elements",lt.newList(datastructure="ARRAY_LIST",cmpfunction=
                                                                  compare))
            mp.put(map_sub_sector_cod,me.getKey(lst),me.getValue(lst)) #ponemos la lista en el el el mapa de su respectivo sector
            
            lt.addLast(me.getValue(mp.get(map_sub_sector_cod,me.getKey(lst))),data) #añadimos a la lista este nuevo elemento
            
            
            #----------------------  parte de la suma ----------------#
            
            #pareja (llave, valor) de costos y gastos nomina #
            entry_cyg_n = me.newMapEntry("Costos y gastos nomina",0)
            mp.put(map_sub_sector_cod,me.getKey(entry_cyg_n),me.getValue(entry_cyg_n))
            cyg_n = me.getValue(mp.get(map_sub_sector_cod,me.getKey(entry_cyg_n)))
            cyg_n += int(data["Costos y gastos nómina"])
            entry_cyg_n = me.newMapEntry("Costos y gastos nomina",cyg_n)
            mp.put(map_sub_sector_cod,me.getKey(entry_cyg_n),me.getValue(entry_cyg_n))
            #pareja llave, valor de costos y gastos nomina #
        
            #pareja llave valor retenciones  sub#
            entry_retenciones = me.newMapEntry("retenciones",0)
            mp.put(map_sub_sector_cod,me.getKey(entry_retenciones),me.getValue(entry_retenciones))
            # TODO completar suma
            #/pareja llave valor retenciones  sub#
        
            #pareja llave valor ingresos netos sub_sector#
            entry_ingresos_netos = me.newMapEntry("ingresos netos",0) #crea una pareja llave valor (ingresos netos, total ingresos netos del sub_sector)
            mp.put(map_sub_sector_cod,me.getKey(entry_ingresos_netos),me.getValue(entry_ingresos_netos)) # añade la pareja llave valor al mapa 
            i_n = me.getValue(mp.get(map_sub_sector_cod,"ingresos netos")) #obtenemos el valor de la pareja llave valor (ingresos netos, total ingresos netos), el cual seran los actuales ingresos netos del subsector
            i_n += int(data["Total ingresos netos"]) # a los ingresos netos actuales le suumamos los de la nueva actividad economica
            entry_ingresos_netos = me.newMapEntry("ingresos netos",i_n) # creamos otra vez una pareja llave valor la cual tendra como lalve la misma de arriba y como valor los nuevos ingresos netod del subsector
            mp.put(map_sub_sector_cod,me.getKey(entry_ingresos_netos),me.getValue(entry_ingresos_netos)) # ponemos esta nueva pareja llave valor en el mapa  
            #/pareja llave valor ingresos netos sub_sector#
        
            #pareja llave valor costos y gastos sub_sector#
            entry_cyg = me.newMapEntry("costos y gastos",0)
            mp.put(map_sub_sector_cod,me.getKey(entry_cyg),me.getValue(entry_cyg))
            cyg = me.getValue(mp.get(map_sub_sector_cod,"costos y gastos"))
            cyg += int(data["Total costos y gastos"])
            entry_cyg = me.newMapEntry("costos y gastos",cyg)
            mp.put(map_sub_sector_cod,me.getKey(entry_cyg),me.getValue(entry_cyg))        
            #/pareja llave valor costos y gastos sub_sector#
        
            #pareja llave valor saldo a pagar sub_sector#
            entry_sp = me.newMapEntry("saldo a pagar",0)
            mp.put(map_sub_sector_cod,me.getKey(entry_sp),me.getValue(entry_sp))
            sp =me.getValue(mp.get(map_sub_sector_cod,"saldo a pagar"))
            sp += int(data["Total saldo a pagar"])
            entry_sp = me.newMapEntry("saldo a pagar",sp)
            mp.put(map_sub_sector_cod,me.getKey(entry_sp),me.getValue(entry_sp))
            #/pareja llave valor saldo a pagar sub_sector#
        
            #pareja llave valor saldo a favor
            entry_sf = me.newMapEntry("saldo a favor",0)
            mp.put(map_sub_sector_cod,me.getKey(entry_sf),me.getValue(entry_sf))
            sf = me.getValue(mp.get(map_sub_sector_cod,"saldo a favor"))
            sf += int(data["Total saldo a favor"])
            entry_sf = me.newMapEntry("saldo a favor",sf)
            mp.put(map_sub_sector_cod,me.getKey(entry_sf),me.getValue(entry_sf))        
            #/ pareja llave valor saldo a favor
            
            #pareja (llave,valor) descuentos tributarios
            entry_dt = me.newMapEntry("Descuentos tributarios",int(data["Descuentos tributarios"]))
            mp.put(map_sub_sector_cod,me.getKey(entry_dt),me.getValue(entry_sf))
            #/pareja (llave,valor) descuentos tributarios
        
            #------------- parte de la suma --------------#
    
def add_data(data_structs,data,tipo_mapa,factor_carga):
    
    if not(mp.contains(data_structs["anios"],data["Año"])): # se revisa si el año existe
        create_base(data_structs,data,tipo_mapa,factor_carga)
    add(data_structs,data,tipo_mapa,factor_carga)
    
    return data_structs
        

# Funciones de consulta

def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    return data_structs["size"]

#diccio req1
def diccio_req1(data)-> dict:
    diccio = {}
    diccio["Código actividad económica"] = data["Código actividad económica"]
    diccio["Nombre actividad económica"] = data["Nombre actividad económica"]
    diccio["Código subsector económico"] = data["Código subsector económico"]
    diccio["Nombre subsector económico"] = data["Nombre subsector económico"]
    diccio["Total ingresos netos"] = data["Total ingresos netos"]
    diccio["Total costos y gastos"] = data["Total costos y gastos"]
    diccio["Total saldo a pagar"] = data["Total saldo a pagar"]
    diccio["Total saldo a favor"] = data["Total saldo a favor"]
    return diccio
    

def req_1(data_structs,anio,sector):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    #data_struct tiene llaves: anio y size
    map_anios = data_structs["anios"]
    map_anio = me.getValue(mp.get(map_anios,anio))
    map_sectores = me.getValue(mp.get(map_anio,"sector"))
    map_sector = me.getValue(mp.get(map_sectores,sector))
    lst_sector = me.getValue(mp.get(map_sector,"elements"))
    mayor_cmp = 0
    mayor_dict = {}
    for i in lt.iterator(lst_sector):
        if int(i["Total saldo a pagar"]) > mayor_cmp:
            mayor_cmp = int(i["Total saldo a pagar"])
            mayor_dict = diccio_req1(i)
    
    return mayor_dict


def req_2(data_structs,anio,cod_sector):
    """
    Función que soluciona el requerimiento 2
    """
    mapa_anio=me.getValue(mp.get(data_structs["anios"],anio))
    mapa_sector=me.getValue(mp.get(me.getValue(mp.get(mapa_anio,"sector")),cod_sector))
    
    elements=me.getValue(mp.get(mapa_sector,"elements"))
    sort(elements,"cmp_2")
    
    return lt.getElement(elements,1)


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    pass


def req_4(data_structs,anio):
    """
    Función que soluciona el requerimiento 4
    """
    map_year = me.getValue(mp.get(data_structs["anios"],anio))
    
    map_sub_sector = me.getValue(mp.get(map_year,"sub_sector"))
    mayor = 0
    diccio = {}
    for sub in lt.iterator(mp.keySet(map_sub_sector)):
        map_por_sub = me.getValue(mp.get(map_sub_sector,sub))

        c_y_g = me.getValue(mp.get(map_por_sub,"Costos y gastos nomina"))
        
        if  c_y_g > mayor:
            diccio["Costos y gastos nomina"] = me.getValue(mp.get(map_por_sub,"Costos y gastos nomina"))
            diccio["ingresos netos"] = me.getValue(mp.get(map_por_sub,"ingresos netos"))
            diccio["costos y gastos"] = me.getValue(mp.get(map_por_sub,"costos y gastos"))
            diccio["saldo a pagar"] = me.getValue(mp.get(map_por_sub,"saldo a pagar"))
            diccio["saldo a favor"] = me.getValue( mp.get(map_por_sub,"saldo a favor"))
            
            actividad = lt.firstElement(me.getValue(mp.get(me.getValue(mp.get(map_sub_sector,sub)),"elements")))
            diccio["nombre sector"] =  actividad["Nombre sector económico"]
            diccio["codigo sector"] =  actividad["Código sector económico"]
            diccio["nombre subsector"] =  actividad["Nombre subsector económico"]
            diccio["codigo subsector"] =  actividad["Código subsector económico"]
            
            mayor = diccio["Costos y gastos nomina"]
            
    lst = me.getValue(mp.get(me.getValue(mp.get(map_sub_sector,diccio["codigo subsector"])),"elements"))
    merg.sort(lst,cmp_req_4)
    dic_act = lt.newList("ARRAY_LIST")

    for i in range(1,4):
        lt.addLast(dic_act,lt.getElement(lst,i))
        #lt.addLast(dic_act["mas"], )
    for x in range(lt.size(lst)-2,lt.size(lst)+1):
        lt.addLast(dic_act,lt.getElement(lst,i))
        #lt.addLast(dic_act["menos"],lt.getElement(lst,x))
        
    return diccio,dic_act #falta de dovelver la tupla con ambos dict


def diccio_requ5(registro,mapa_subsector):
    return{
        "Código sector económico":registro["Código sector económico"],
        "Nombre sector económico":registro["Nombre sector económico"],
        "Código subsector económico":registro["Código subsector económico"],
        "Nombre subsector económico":registro["Nombre subsector económico"],
        "Total de descuentro tributarios del subsector económico":me.getValue(mp.get(mapa_subsector,"Descuentos tributarios")),
        "Total de ingresos netos del subsector económico":me.getValue(mp.get(mapa_subsector,"ingresos netos")),
        "Total costos y gastos del subsector económico":me.getValue(mp.get(mapa_subsector,"costos y gastos")),
        "Total saldo a pagar del subsector económico":me.getValue(mp.get(mapa_subsector,"saldo a pagar")),
        "Total saldo a favor del subsector económico":me.getValue(mp.get(mapa_subsector,"saldo a favor"))
    }

def req_5(data_structs,anio):
    """
    Función que soluciona el requerimiento 5
    """
    #Busqueda
    
    mapa=me.getValue(mp.get(data_structs["anios"],anio))
    mapa_sub_sectores=me.getValue(mp.get(mapa,"sub_sector"))
    mayor=0
    
    for cod_subsector in lt.iterator(mp.keySet(mapa_sub_sectores)):
        subsector=me.getValue(mp.get(mapa_sub_sectores,cod_subsector))
        
        Total_descuentos_tributarios=me.getValue(mp.get(subsector,"Descuentos tributarios"))
        
        if Total_descuentos_tributarios>mayor:
            mayor=Total_descuentos_tributarios
            map_subsector_mayor=subsector
    
    #Retorno
    actividades_subsector=me.getValue(mp.get(map_subsector_mayor,"elements"))
    sort(actividades_subsector,"cmp_5")
    sub_arraylist=lt.newList("ARRAY_LIST")
    if lt.size(actividades_subsector)<=6:
        sub_arraylist=actividades_subsector
    else:
        for i in range(1,4):
            lt.addLast(sub_arraylist,lt.getElement(actividades_subsector,i))
        for i in range(2,-1,-1):
            lt.addLast(sub_arraylist,lt.getElement(actividades_subsector,lt.size(actividades_subsector)-i))
    
    mayor_subsector=lt.newList("ARRAY_LIST")    
    lt.addLast(mayor_subsector,diccio_requ5(lt.getElement(actividades_subsector,1),map_subsector_mayor))
    return mayor_subsector,sub_arraylist
   
    
def lista_mayor_sector(registro,mapa_sector,cod_mayor_subsector,cod_menor_subsector):
    lista=lt.newList("ARRAY_LIST")
    lt.addLast(lista,{"Código sector económico":registro["Código sector económico"],
                      "Nombre sector económico": registro["Nombre sector económico"],
                      "Total ingresos netos del sector económico":me.getValue(mp.get(mapa_sector,"ingresos netos")),
                      "Total costos y gastos del sector económico": me.getValue(mp.get(mapa_sector,"costos y gastos")),
                      "Total saldo a pagar del sector económico": me.getValue(mp.get(mapa_sector,"saldo a pagar")),
                      "Total saldo a favor del sector económico": me.getValue(mp.get(mapa_sector,"saldo a favor")),
                      "Subsector económico que más aportó": cod_mayor_subsector,
                      "Subsector económico que menos aportó":cod_menor_subsector
                      })
    return lista

def crear_actividad_economica(registro_act):
    return {"Código actividad económica":registro_act["Código actividad económica"],
            "Nombre actividad económica":registro_act["Nombre actividad económica"],
            "Total ingresos netos":registro_act["Total ingresos netos"],
            "Total costos y gastos":registro_act["Total costos y gastos"],
            "Total saldo a pagar":registro_act["Total saldo a pagar"],
            "Total saldo a favor":registro_act["Total saldo a favor"]
            }

def lista_subsector(mapa_subsector):
    lst=lt.newList("ARRAY_LIST")
    registros=me.getValue(mp.get(mapa_subsector,"elements"))
    sort(registros,"cmp_6")
    registro_menor=lt.getElement(registros,1)
    registro_mayor=lt.getElement(registros,lt.size(registros))
    
    lista_actividad_mayor=lt.newList("ARRAY_LIST")
    lt.addLast(lista_actividad_mayor,crear_actividad_economica(registro_mayor))
    
    lista_Actividad_menor=lt.newList("ARRAY_LIST")
    lt.addLast(lista_Actividad_menor,crear_actividad_economica(registro_menor))
    
    lt.addLast(lst,{"Código subsector económico":registro_mayor["Código subsector económico"],
                    "Nombre subsector económico":registro_mayor["Nombre subsector económico"],
                    "Total ingresos netos del subsector económico":me.getValue(mp.get(mapa_subsector,"ingresos netos")),
                    "Total costos y gastos del subsector económico":me.getValue(mp.get(mapa_subsector,"costos y gastos")),
                    "Total saldo a pagar del subsector económico":me.getValue(mp.get(mapa_subsector,"saldo a pagar")),
                    "Total saldo a favor del subsector económico":me.getValue(mp.get(mapa_subsector,"saldo a favor")),
                    "Actividad económica que más aportó":lista_actividad_mayor,
                    "Actividad económica que menos aportó":lista_Actividad_menor
    })
    return lst

def req_6(data_structs,anio):
    """
    Función que soluciona el requerimiento 6
    """
    mapa=me.getValue(mp.get(data_structs["anios"],anio))
    mapa_sectores=me.getValue(mp.get(mapa,"sector"))
    mayor=0
    
    for cod_sector in lt.iterator(mp.keySet(mapa_sectores)):
        sector=me.getValue(mp.get(mapa_sectores,cod_sector))
        ingresos_netos=me.getValue(mp.get(sector,"ingresos netos"))
        if ingresos_netos>mayor:
            mayor=ingresos_netos
            mayor_sector=sector
    
    subsectores_en_el_sector=me.getValue(mp.get(mayor_sector,"subsector en el sector"))
    mapa_sub_sectores=me.getValue(mp.get(mapa,"sub_sector"))
    mayor_sub=0
    menor_sub=None
    for cod_subsector in lt.iterator(subsectores_en_el_sector):
        subsector=me.getValue(mp.get(mapa_sub_sectores,cod_subsector))
        total_ingresos_netos=me.getValue(mp.get(subsector,"ingresos netos"))
        if total_ingresos_netos>mayor_sub:
            mayor_sub=total_ingresos_netos
            cod_mayor_subsector=cod_subsector
            subsector_mayor=subsector
        if menor_sub==None or total_ingresos_netos<menor_sub:
            menor_sub=total_ingresos_netos
            subsector_menor=subsector
            cod_menor_subsector=cod_subsector
            
    lista_sector = lista_mayor_sector(lt.getElement(me.getValue(mp.get(mayor_sector,"elements")),1),mayor_sector,cod_mayor_subsector,cod_menor_subsector)        
    
    lista_subsector_mayor = lista_subsector(subsector_mayor)
    lista_subsector_menor = lista_subsector(subsector_menor)
    return lista_sector,lista_subsector_mayor,lista_subsector_menor
    


def req_7(data_structs,anio,subsector,top):
    """
    Función que soluciona el requerimiento 7
    """
    

    año = mp.get(data_structs["anios"],anio)
    map_anio = me.getValue(año)
    sub = mp.get(map_anio,"sub_sector")
    map_sub = me.getValue(sub)
    map_subsectores = mp.get(map_sub,subsector)
    map_subsector = me.getValue(map_subsectores)
    pareja = mp.get(map_subsector,"elements")
    lst = me.getValue(pareja)
    
    lst_top = lt.newList(datastructure= "ARRAY_LIST",cmpfunction=None)
    sa.sort(lst,cmp_req7)
    for i in range(1,top+1):
        lt.addLast(lst_top,lt.getElement(lst,i))
    return lst_top        

def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    if data_1["Año"] < data_2["Año"]:
        return True
    elif data_1["Año"] == data_2["Año"]:
        if data_1["Código actividad económica"] < data_2["Código actividad económica"]:
            return True
        else:
            return False
    else:
        return False

# Funciones de ordenamiento
def cmp_cod_actividad_economica(data1,data2):
    return int(data1["Código actividad económica"]) < int(data2["Código actividad económica"])

def cmp_req2(data1,data2):
    return int(data1["Total saldo a favor"]) > int(data2["Total saldo a favor"])

def cmp_req_4(data_1,data_2):
    if int(data_1["Costos y gastos nómina"]) > int(data_2["Costos y gastos nómina"]):
        return True
    else:
        return False

def cmp_req_5(data1,data2):
    return int(data1["Descuentos tributarios"]) < int(data2["Descuentos tributarios"])
def cmp_req_6(data1,data2):
    return int(data1["Total ingresos netos"])<int(data2["Total ingresos netos"])
def cmp_req7(data1,data2):
    if int(data1["Total costos y gastos"]) < int(data2["Total costos y gastos"]):
        return True
    elif int(data1["Total costos y gastos"]) == int(data2["Total costos y gastos"]):
        if int(data1["Código actividad económica"]) > int(data2["Código actividad económica"]):
            return True
        return False
    else:
        return False
    
def cmp_anio(anio1,anio2):
    return int(anio1)>int(anio2)

def sort(lista,tipo):
    """
    Función encargada de ordenar una lista
    """
    if tipo=="cod_act_eco":
        criterio=cmp_cod_actividad_economica
    elif tipo == "anio":
        criterio=cmp_anio
    elif tipo =="cmp_2":
        criterio=cmp_req2
    elif tipo == "cmp_5":
        criterio=cmp_req_5
    elif tipo=="cmp_6":
        criterio=cmp_req_6
        
    lista = sa.sort(lista,criterio)
    

