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
 """

import config as cf
import model
import time
import csv
import tracemalloc

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    control = {
        "model": None
    }
    control["model"] = model.new_data_structs()
    return control


# Funciones para la carga de datos

def load_data(control, filename, tipo_mapa,factor_carga,memflag=True):
    """
    Carga los datos del reto
    """
    # toma el tiempo al inicio del proceso
    start_time = getTime()

    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    
    #Carga de datos
    Data_struct = control["model"]
    filename = cf.data_dir + filename
    Input_file = csv.DictReader(open(filename,encoding="utf-8"))
    
    for i in Input_file:
        try:
            int(i["Código actividad económica"])
        except:
            c = ""
            for x in i["Código actividad económica"]:
                try:
                    int(x)
                    c += x
                except:
                    break
            i["Código actividad económica"] = c
            int(i["Código actividad económica"])
        model.add_data(Data_struct,i,tipo_mapa,factor_carga)
        Data_struct["size"]+=1
        #print(Data_struct["size"])
    
        # toma el tiempo al final del proceso
    stop_time = getTime()
    # calculando la diferencia en tiempo
    delta_time = deltaTime(stop_time, start_time)

    # finaliza el proceso para medir memoria
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory = deltaMemory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return delta_time, delta_memory

    else:
        # respuesta sin medir memoria
        return delta_time

def tamanio_filas_cargadas(control):
    size=model.data_size(control["model"])
    return size

# Funciones de ordenamiento

def sort(lista,tipo):
    """
    Ordena los datos del modelo
    """
    model.sort(lista,tipo)


# Funciones de consulta sobre el catálogo

def get_map_anios(control):
    """
    Retorna el mapa con las parejas llave-valor años-mapa.
    """
    return control["model"]["anios"]


def req_1(control,anio,sector):
    """
    Retorna el resultado del requerimiento 1
    """
    return model.req_1(control["model"],anio,sector)


def req_2(control,anio,cod_sector):
    """
    Retorna el resultado del requerimiento 2
    """
    return model.req_2(control["model"],anio,cod_sector)


def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(control,anio):
    """
    Retorna el resultado del requerimiento 4
    """
    tupla = model.req_4(control["model"],anio)
    return tupla


def req_5(control,anio):
    """
    Retorna el resultado del requerimiento 5
    """
    return model.req_5(control["model"],anio)

def req_6(control,anio):
    """
    Retorna el resultado del requerimiento 6
    """
    return model.req_6(control["model"],anio)


def req_7(control,anio,subsector,top):
    """
    Retorna el resultado del requerimiento 7
    """
    return model.req_7(control["model"],anio,subsector,top)


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def deltaTime(end,start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
