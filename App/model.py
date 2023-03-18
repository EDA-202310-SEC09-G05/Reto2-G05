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
            "size": 0,
            "anios": None
            }
    data_structs["anios"] = mp.newMap(numelements=11,maptype = "PROBING",
                                              loadfactor= 0.5,
                                              cmpfunction=None)    
    return data_structs
    
    


# Funciones para agregar informacion al modelo
def create_base(data_structs,data):
        new_map = me.newMapEntry(data["Año"],mp.newMap(3,
                                              maptype = "PROBING",
                                              loadfactor= 0.5,
                                              cmpfunction=None))
        mp.put(data_structs["anios"],me.getKey(new_map),me.getValue(new_map))
        
        map = me.getValue(mp.get(data_structs["anios"],data["Año"]))
                
        element_entry = me.newMapEntry("elements",lt.newList(datastructure="ARRAY_LIST",cmpfunction=
                                                                  compare))
        
        mp.put(map,me.getKey(element_entry),me.getValue(element_entry))
        
        subsector_entry = me.newMapEntry("sub_sector",mp.newMap(21,maptype = "PROBING",
                                              loadfactor= 0.5,
                                              cmpfunction=None))
        mp.put(map,me.getKey(subsector_entry),me.getValue(subsector_entry))
        
        sector_entry = me.newMapEntry("sector",mp.newMap(12,maptype = "PROBING",
                                              loadfactor= 0.5,
                                              cmpfunction=None))
        mp.put(map,me.getKey(sector_entry),me.getValue(sector_entry))
        

        
        entry_sector = me.newMapEntry(data["Código sector económico"],mp.newMap(numelements=2,maptype = "PROBING",
                                              loadfactor= 0.5,
                                              cmpfunction=None))
        
        map_sectores = me.getValue(mp.get(map,"sector")) # obtenemos el map por sectores
        
        # [obtenemos el map de sector el cual tendra parejas (cod sector,map) , obtenemos la llave que deseamos meter, obtenemos el value que deseamos obtener]
        mp.put(map_sectores,me.getKey(entry_sector),me.getValue(entry_sector)) 
         
        map_sector_cod = me.getValue(mp.get(map_sectores,me.getKey(entry_sector))) #encuentra el map de un sector economico especifico
        
        lst_sector = me.newMapEntry("elements",lt.newList(datastructure="ARRAY_LIST",cmpfunction=
                                                                  None)) # esta pareja llave valor contiene como llave un  str y como valor el array_klist de los elementos pertencienctes al a un sector economico especifico
             
        mp.put(map_sector_cod,me.getKey(lst_sector),me.getValue(lst_sector)) # ponemos el array_list que contendra todos los elementos de este sector en el map pertenciente a ese sector
        
        #---------- suma ----------
        suma_ingresos_netos_sector = me.newMapEntry("ingresos netos",0)
        mp.put(map_sector_cod,me.getKey(suma_ingresos_netos_sector),me.getValue(suma_ingresos_netos_sector)) # añadimos la sumatoria ingresos netos inicial 0
        #---------- suma ---------
        
        entry_sub = me.newMapEntry(data["Código subsector económico"],mp.newMap(numelements=8,maptype = "PROBING",
                                              loadfactor= 0.5,
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
        
        #------------- parte de la suma --------------#
def add(data_structs,data):
        map =  me.getValue(mp.get(data_structs["anios"],data["Año"]))
        lst = me.getValue(mp.get(map,"elements"))
        lt.addLast(lst,data) #añade la nueva actividad economica a la lista con todas las actividades economicas del año
        
        map_sectores = me.getValue(mp.get(map,"sector"))
        
        if not(mp.contains(map_sectores,data["Código sector económico"])):
            entry = me.newMapEntry(data["Código sector económico"],mp.newMap(numelements=2,maptype = "PROBING",
                                              loadfactor= 0.5,
                                              cmpfunction=None)) # Creamos la pareja llave valor de (cod_sector,map_sector)
            mp.put(map_sectores,me.getKey(entry),me.getValue(entry))
            
            map_sector_cod = me.getValue(mp.get(map_sectores,data["Código sector económico"]))
            lst = me.newMapEntry("elements",lt.newList(datastructure="ARRAY_LIST",cmpfunction=
                                                                  compare))
            mp.put(map_sector_cod,me.getKey(lst),me.getValue(lst)) #ponemos la lista en el el el mapa de su respectivo sector
            #---------- Creamos la suma -----------
            suma_ingresos_netos_sector = me.newMapEntry("ingresos netos",0)
            mp.put(map_sector_cod,me.getKey(suma_ingresos_netos_sector),me.getValue(suma_ingresos_netos_sector)) # añadimos la sumatoria ingresos netos inicial 0
            #---------- Creamos la suma ----------
            
            
        map_sector_cod = me.getValue(mp.get(map_sectores,data["Código sector económico"]))
        lst = me.getValue(mp.get(map_sector_cod,"elements")) # obtenemos la lista de elementos que pertenecen al codigo de sector economico actual
        lt.addLast(lst,data) # añadimos el nuevo elemento a esta lista
        
        #------------- suma ingresos netos -------
        ingresos_netos = me.getValue(mp.get(map_sector_cod,"ingresos netos"))
        ingresos_netos += int(data["Total ingresos netos"])
        entry_ingresos_netos = me.newMapEntry("ingresos netos",ingresos_netos)
        mp.put(map_sector_cod,me.getKey(entry_ingresos_netos),me.getValue(entry_ingresos_netos))
        #------------- suma ingresos netos------
            
    
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
            
            #TODO
            
            #/pareja (llave,valor) Total descuentos tributarios
        
            #------------- parte de la suma --------------#

        else:
            entry = me.newMapEntry(data["Código subsector económico"],mp.newMap(numelements=8,maptype = "PROBING",
                                              loadfactor= 0.5,
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
            
            #TODO realizar suma de descuentos tributarios
            
            #/pareja (llave,valor) descuentos tributarios
        
            #------------- parte de la suma --------------#
    
def add_data(data_structs,data):
    
    if not(mp.contains(data_structs["anios"],data["Año"])): # se revisa si el año existe
        create_base(data_structs,data)
    add(data_structs,data)
    
    return data_structs
        
    
    
    

# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass


# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass


def req_1(data_structs):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    pass


def req_2(data_structs):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    pass


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
    merg.sort(lst,sort_req_4)
    dic_act = {"mas": [],"menos":[]}

    for i in range(1,4):
        dic_act["mas"].append(lt.getElement(lst,i))
        #lt.addLast(dic_act["mas"], )
    for x in range(lt.size(lst)-2,lt.size(lst)+1):
        dic_act["menos"].append(lt.getElement(lst,i))
        #lt.addLast(dic_act["menos"],lt.getElement(lst,x))
        
    return diccio,dic_act #falta de dovelver la tupla con ambos dict


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(data_structs):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    pass


def req_7(data_structs):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    pass


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

def sort_req_4(data_1,data_2):
    if data_1["Costos y gastos nómina"] > data_2["Costos y gastos nómina"]:
        return True
    else:
        return False
    
def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    pass


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass

