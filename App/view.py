"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
    """
        Se crea una instancia del controlador
    """
    control = controller.new_controller()
    return control


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control,memflag):
    """
    Carga los datos
    """
    nombre_archivo= tamanio_muestra()
    tipo_mapa,factor_carga=conf_mapa()
    return controller.load_data(control, nombre_archivo,tipo_mapa,factor_carga,memflag)


def print_load_data(control):
    mapa=controller.get_map_anios(control)
    headers=["Año","Código actividad económica","Nombre actividad económica","Código sector económico","Nombre sector económico","Código subsector económico","Nombre subsector económico","Total ingresos netos","Total costos y gastos","Total saldo a pagar","Total saldo a favor"]
    lista_anios=mp.keySet(mapa)
    controller.sort(lista_anios,"anio")
    
    for anio in lt.iterator(lista_anios):
        mapa_anio=me.getValue(mp.get(mapa,anio))
        arraylist=me.getValue(mp.get(mapa_anio,"elements"))
        controller.sort(arraylist,"cod_act_eco")
            
        if lt.size(arraylist)<6:
            print("Solo hay "+str(lt.size(arraylist))+" actividades económicas en el año "+str(anio)+".")
            imprimir_tabla(arraylist,headers)
        else:
            print("Las actividades tres primeras y tres últimas actividades económicas cargadas en "+str(anio)+ " son:")       
            
            sub_arraylist=lt.newList("ARRAY_LIST")
            for i in range(1,4):
                lt.addLast(sub_arraylist,lt.getElement(arraylist,i))
            for i in range(2,-1,-1):
                lt.addLast(sub_arraylist,lt.getElement(arraylist,lt.size(arraylist)-i))
        
            imprimir_tabla(sub_arraylist,headers)
   

def print_req_1(control,anio,sector):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    lista=lt.newList("ARRAY_LIST")
    act = controller.req_1(control,anio,sector)
    lt.addLast(lista,act)
    imprimir_tabla(lista,act.keys())


def print_req_2(control,anio,cod_sector):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    lista=lt.newList("ARRAY_LIST")
    respuesta,delta_time = controller.req_2(control,anio,cod_sector)
    lt.addLast(lista,respuesta)
    imprimir_tabla(lista,["Código actividad económica","Nombre actividad económica","Código subsector económico","Nombre subsector económico","Total ingresos netos","Total costos y gastos","Total saldo a pagar","Total saldo a favor"])
    
    #Tiempo
    print("El tiempo que tomó ejecutar este requerimiento fue "+ f"{delta_time:.3f}" +" ms.")

def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control,anio):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    dic,time = controller.req_4(control,anio)
    diccio,lista_act = dic
    lista=lt.newList("ARRAY_LIST")
    lt.addLast(lista, diccio)
    print("El tiempo es ",time)
    print("--------------------------------------------------")
    imprimir_tabla(lista,diccio.keys())
    
    #TODO MODIFICAR HEADERS E IMPRIMIR LOS TÍTULOS DE LA TABLA
    print("Las actividades  económicas que más y menos contribuyeron en el subsector "+str(lt.getElement(diccio,1)["Código subsector económico"])+" son:")
    imprimir_tabla(lista_act,["Código actividad económica","Nombre actividad económica","ZWASEXDCFTVGBHNJKM","Total ingresos netos","Total costos y gastos","Total saldo a pagar","Total saldo a favor"])

def print_req_5(control,anio):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    mayor_subsector,arraylist,delta_time=controller.req_5(control,anio)
    
    print("Subsector económico con los mayores Descuentos tributarios en "+str(anio))
    imprimir_tabla(mayor_subsector,lt.getElement(mayor_subsector,1).keys())
    
    print("Las actividades  económicas que más y menos contribuyeron en el subsector "+str(lt.getElement(mayor_subsector,1)["Código subsector económico"])+" son:")
    imprimir_tabla(arraylist,["Código actividad económica","Nombre actividad económica","Descuentos tributarios","Total ingresos netos","Total costos y gastos","Total saldo a pagar","Total saldo a favor"])

    #Tiempo
    print("El tiempo que tomó ejecutar este requerimiento fue "+ f"{delta_time:.3f}" +" ms.")
    
def print_req_6(control,anio):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    lista_sector,mayor_subsector,menor_subsector,delta_time = controller.req_6(control,anio)
    print("El sector económico con mayores ingresos netos en el año "+ str(anio) +" es:")
    imprimir_tabla(lista_sector,lt.getElement(lista_sector,1).keys())
    
    print("El subsector que más contribuyó es:")
    imprimir_tabla(mayor_subsector,lt.getElement(mayor_subsector,1).keys(),25,30)
    
    print("El subsector que menos contribuyó es:")
    imprimir_tabla(menor_subsector,lt.getElement(menor_subsector,1).keys(),25,30)
    
    #Tiempo
    print("El tiempo que tomó ejecutar este requerimiento fue "+ f"{delta_time:.3f}" +" ms.")


def print_req_7(control,subsector,top,anio):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    
    lst_top = controller.req_7(control,anio,subsector,top)

    #TODO COMPLETAR LOS HEADERS
    headers= lt.firstElement(lst_top).keys()
    
    imprimir_tabla(lst_top,headers)


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea el controlador asociado a la vista
control = new_controller()

#Funciones para el view
def tamanio_muestra():
    """
        Permite seleccionar el tamaño de la muestra que el usuario desea

    Args:
        opcion: la opcion seleccionada por el usuario
    """
    print("Seleccione el porcentaje de la lista que desea usar\n")
    print("1 0.5%")
    print("2 5%")
    print("3 10%")
    print("4 20%")
    print("5 30%")
    print("6 50%")
    print("7 80%")
    print("8 100%")
                
    opcion=int(input("-> "))
    
    text = "/Data/DIAN/"
    if opcion == 1:
       return text + "Salida_agregados_renta_juridicos_AG-small.csv"
    elif opcion == 2:
        return text + "Salida_agregados_renta_juridicos_AG-5pct.csv"
    elif opcion == 3:
        return text + "Salida_agregados_renta_juridicos_AG-10pct.csv"
    elif opcion == 4:
        return text + "Salida_agregados_renta_juridicos_AG-20pct.csv"
    elif opcion == 5:
        return text + "Salida_agregados_renta_juridicos_AG-30pct.csv"
    elif opcion == 6:
        return text + "Salida_agregados_renta_juridicos_AG-50pct.csv"
    elif opcion == 7:
        return text + "Salida_agregados_renta_juridicos_AG-80pct.csv"
    elif opcion == 8:
        return text + "Salida_agregados_renta_juridicos_AG-large.csv"

def conf_mapa():
    print("Seleccione el tipo de mapa que desea escoger: \n 1:PROBING \n 2:CHAINING")
    opcion_mapa=int(input("-> "))
    
    if opcion_mapa == 1:
        tipo_mapa="PROBING"
    elif opcion_mapa ==2:
        tipo_mapa="CHAINING"
    
    print("Seleccione el factor de carga que desea utilizar. Recuerde utilizar puntos y escribir su número con al menos una cifra decimal.")
    factor_carga=float(input("-> "))
    #if tipo_mapa=="PROBING" and factor_carga>=1.0:
    #    print("Recuerde que no se debe usar un factor de carga mayor o igual que uno con PROBING. \nEs recomendable que detenga la ejecución de INMEDIATO.")
    return tipo_mapa,factor_carga

def castBoolean(value):
    """
    Convierte un valor a booleano
    """
    if value in ('True', 'true', 'TRUE', 'T', 't', '1', 1, True):
        return True
    else:
        return False

def printLoadDataAnswer(answer):
    """
    Imprime los datos de tiempo y memoria de la carga de datos
    """
    if isinstance(answer, (list, tuple)) is True:
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "||",
              "Memoria [kB]: ", f"{answer[1]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{answer:.3f}")
#imprimir tablas
def imprimir_tabla(lista,headers,maxcolwidths=12,maxheadercolwidths=12):
    
    datos=[]
    for dato in lt.iterator(lista):
        fila = []
        for header in headers:
            try:
                sub_datos=[]
                for lista in lt.iterator(dato[header]):
                    for sub_header in lista.keys():
                        sub_datos.append([sub_header,lista[sub_header]])
                    
                fila.append(tabulate(sub_datos, tablefmt='grid',maxheadercolwidths=3,maxcolwidths=9))
            except:
                fila.append(dato[header])
        datos.append(fila)

    print(tabulate(datos, headers, tablefmt='grid', maxcolwidths=maxcolwidths, maxheadercolwidths=maxheadercolwidths,stralign='center'))
    

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        try:
            if int(inputs) == 1:

                print("Cargando información de los archivos ....\n")
                
                print("Desea observar el uso de memoria? (True/False)")
                mem = input("Respuesta: ")
                mem = castBoolean(mem)
                answer = load_data(control, memflag=mem)
                printLoadDataAnswer(answer)
                
                print("El total de filas guardas es ",controller.tamanio_filas_cargadas(control))
                print_load_data(control)
                
            elif int(inputs) == 2:
                anio = input("Año a consultar: ")
                sector = input("Ingrese el sector del cual desea revisar: ")
                print_req_1(control,anio,sector)

            elif int(inputs) == 3:
                anio_req2 = input("Ingrese el año: ")
                cod_sector=input("Ingrese el código del sector: ")
                print_req_2(control,anio_req2,cod_sector)

            elif int(inputs) == 4:
                print_req_3(control)

            elif int(inputs) == 5:
                anio = input("Ingrese el año del cual año desea conocer el subsector con mas gastos y costos nomina: ")
                print_req_4(control,anio)

            elif int(inputs) == 6:
                anio_req5 = input("Ingrese el año para el cual desea encontrar el subsector que tuvo los mayores descuentos tributarios: \n ->")
                print_req_5(control,anio_req5)

            elif int(inputs) == 7:
                anio_req6 = input("Ingrese el año del que desea conocer el sector con los mayores ingresos netos: \n ->")
                print_req_6(control,anio_req6)

            elif int(inputs) == 8:
                anio = input("Ingrese el año del cual desea ver el top de actividades economicas: ")
                subsector = input("Ingrese el subsector del cual desea ver el top de actividades economicas: ")
                top = int(input("Ingrese el top que desea ver: "))
                print_req_7(control,subsector,top,anio)

            elif int(inputs) == 9:
                print_req_8(control)

            elif int(inputs) == 0:
                working = False
                print("\nGracias por utilizar el programa")
                
            else:
                print("Opción errónea, vuelva a elegir.\n")
        except Exception as exp:
            print("ERR:", exp)
            traceback.print_exc()
    sys.exit(0)
