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

def add_data(data_structs,data):
    

    if mp.contains(data_structs["anios"],data["Año"]): # se revisa si el año existe
        map =  me.getValue(mp.get(data_structs["anios"],data["Año"]))
        
        map_sectores = me.getValue(mp.get(map,"sector"))
        if mp.contains(map_sectores,data["Código sector económico"]):
            map_sector_cod = me.getValue(mp.get(map_sectores,data["Código sector económico"]))
            lst = me.getValue(mp.get(map_sector_cod,"elements")) # obtenemos la lista de elementos que pertenecen al codigo de sector economico actual
            lt.addLast(lst,data) # añadimos el nuevo elemento a esta lista
            
            #falta hacer la suma
            
        else:
            entry = me.newMapEntry(data["Código sector económico"],mp.newMap(numelements=8,maptype = "PROBING",
                                              loadfactor= 0.5,
                                              cmpfunction=None)) # Creamos la pareja llave valor de (cod_sector,map_sector)
            map_sectores = me.getValue(mp.get(map,"sector"))
            mp.put(map_sectores,me.getKey(entry),me.getValue(entry))
            
            map_sector_cod = me.getValue(mp.get(map_sectores,data["Código sector económico"]))
            lst = me.newMapEntry("elements",lt.newList(datastructure="ARRAY_LIST",cmpfunction=
                                                                  compare))
            mp.put(map_sector_cod,me.getKey(lst),me.getValue(lst)) #ponemos la lista en el el el mapa de su respectivo sector
            
            lt.addLast(me.getValue(mp.get(map_sector_cod,me.getKey(lst))),data) #añadimos a la lista este nuevo elemento
            
            #falta hacer la parte de la suma
            
                 
        map_sub_sectores = me.getValue(mp.get(map,"sub_sector"))
        
        if mp.contains(map_sub_sectores,data["Código subsector económico"]):
            map_sub_sector_cod = me.getValue(mp.get(map_sub_sectores,data["Código subsector económico"]))
            lst = me.getValue(mp.get(map_sub_sector_cod,"elements")) # obtenemos la lista de elementos que pertenecen al codigo de sector economico actual
            lt.addLast(lst,data) # añadimos el nuevo elemento a esta lista
            
            #falta hacer la suma
            
        else:
            entry = me.newMapEntry(data["Código subsector económico"],mp.newMap(numelements=8,maptype = "PROBING",
                                              loadfactor= 0.5,
                                              cmpfunction=None)) # Creamos la pareja llave valor de (cod_sub_sector,map_sector)
            map_sub_sectores = me.getValue(mp.get(map,"sub_sector"))

            mp.put(map_sub_sectores,me.getKey(entry),me.getValue(entry))

            
            map_sub_sector_cod = me.getValue(mp.get(map_sub_sectores,data["Código subsector económico"]))

            lst = me.newMapEntry("elements",lt.newList(datastructure="ARRAY_LIST",cmpfunction=
                                                                  compare))
            mp.put(map_sub_sector_cod,me.getKey(lst),me.getValue(lst)) #ponemos la lista en el el el mapa de su respectivo sector
            
            lt.addLast(me.getValue(mp.get(map_sub_sector_cod,me.getKey(lst))),data) #añadimos a la lista este nuevo elemento
            
            #falta hacer la parte de la suma
    else:
        
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
        
        lst = me.getValue(mp.get(map,"elements"))
        lt.addLast(lst,data)
        
        entry_sector = me.newMapEntry(data["Código sector económico"],mp.newMap(numelements=8,maptype = "PROBING",
                                              loadfactor= 0.5,
                                              cmpfunction=None))
        
        map_sectores = me.getValue(mp.get(map,"sector")) # obtenemos el map por sectores
        
        # [obtenemos el map de sector el cual tendra parejas (cod sector,map) , obtenemos la llave que deseamos meter, obtenemos el value que deseamos obtener]
        mp.put(map_sectores,me.getKey(entry_sector),me.getValue(entry_sector)) 
         
        map_sector_cod = me.getValue(mp.get(map_sectores,me.getKey(entry_sector))) #encuentra el map de un sector economico especifico
        
        lst_sector = me.newMapEntry("elements",lt.newList(datastructure="ARRAY_LIST",cmpfunction=
                                                                  None)) # esta pareja llave valor contiene como llave un  str y como valor el array_klist de los elementos pertencienctes al a un sector economico especifico
             
        mp.put(map_sector_cod,me.getKey(lst_sector),me.getValue(lst_sector)) # ponemos el array_list que contendra todos los elementos de este sector en el map pertenciente a ese sector
        lt.addLast(me.getValue(mp.get(map_sector_cod,me.getKey(lst_sector))),data) # añade el elemento a la lista del subsector al que pertenece
        
        #falta hacer la parte de la suma
        
        entry_sub = me.newMapEntry(data["Código subsector económico"],mp.newMap(numelements=8,maptype = "PROBING",
                                              loadfactor= 0.5,
                                              cmpfunction=None)) # crea pareja llave valor entry_sub (codigo_sub_sector,map del sub_sector)
        
        map_sub_sector = me.getValue(mp.get(map,"sub_sector"))
        mp.put(map_sub_sector,me.getKey(entry_sub),me.getValue(entry_sub))
        
        lst_sector = me.newMapEntry("elements",lt.newList(datastructure="ARRAY_LIST",cmpfunction=
                                                                  None))
        map_sub_sector_cod =me.getValue(mp.get(map_sub_sector,me.getKey(entry_sub))) # obtenemos el map de un cod de un subsector
        
        mp.put(map_sub_sector_cod,me.getKey(lst_sector),me.getValue(lst_sector))
        lt.addLast(me.getValue(mp.get(map_sector_cod,"elements")),data) # añadimos el elemento a la lista de su respectivo sub:sector
                
        #falta hacer la parte de la suma
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


def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    pass


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

