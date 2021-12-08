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
from DISClib.ADT import stack
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
import threading
assert cf

def printTotalCiudades(lista):
    tamanho = lt.size(lista)
    numero1 = lt.getElement(lista,1)
    print('Primera Ciudad: '+ str(numero1['city_ascii']) + ' Pais: ' + str(numero1['country']) + ' Latitud: ' +str(numero1['lat']) + 
            ' Longitud: ' + str(numero1['lng']) + ' Población: '+ str(numero1['population']))
    numerof = lt.getElement(lista,tamanho)
    print('Última Ciudad: '+ str(numerof['city_ascii']) + ' Pais: ' + str(numerof['country']) + ' Latitud: ' +str(numerof['lat']) + 
            ' Longitud: ' + str(numerof['lng']) + ' Población: '+ str(numerof['population']))

def print5aeropuertos(lista):
    i = 1
    while i <= 5:
        airport = lt.getElement(lista,i)
        print(str(i)+'. Nombre: ' + airport['name']+', Ciudad: '+airport['ciudad']+', Pais: '+airport['pais']+
                ', IATA: '+airport['IATA']+', Conexiones: '+str(airport['conexiones']))
        i+=1

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

airportsfile = 'airports-utf8-small.csv'
routesfile = 'routes-utf8-small.csv'
citiesfile = 'worldcities-utf8.csv'


def printMenu():
    print("\nBienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de aeropuertos y vuelos")
    print("3- Encontrar puntos de interconexion áerea")
    print("4- Encontrar clústeres de tráfico aéreo")
    print("5- Encontrar la ruta más corta entre ciudades")
    print("6- Utilizar las millas de viajero")
    print("7- Cuantificar el efecto de un aeropuerto cerrado")


def optionTwo(cont):
    print("\nCargando información de aeropuertos")
    controller. loadData(cont, airportsfile, routesfile, citiesfile)
    aeropuertos = (gr.numVertices(cont['digrafo']))
    rutas = (gr.numEdges(cont['digrafo']))
    print('Total aeropuertos en el Digrafo: '+str(aeropuertos))
    print('Total rutas aéreas en Digrafo: '+str(rutas))

    print('\nTotal de Ciudades: ' + str(lt.size(cont['listaCiudades'])))
    printTotalCiudades(cont['listaCiudades'])

def optionThree(cont):
    total = controller.req1(cont)
    print('\nÁeropuertos conectados en la red: ' + str(lt.size(total)))
    print('Los 5 áeropuertos mas conectados son: ')
    print5aeropuertos(total)
    

def optionFour(cont):
    codigoIATA1 = input('Ingrese el código IATA del primer áeropuerto: ')
    codigoIATA2 = input('Ingrese el código IATA del segundo áeropuerto: ')
    total = controller.req2(cont, codigoIATA1, codigoIATA2)
    print('\nNúmero total de clústeres presentes en la red de transporte aéreo: ' + str(total[0]['components']))
    print('¿Estan '+total[2]+' ('+codigoIATA1+') y '+ total[3]+' ('+codigoIATA2+') conectados?: '+str(total[1]))


def optionFive(cont):
    ciudadOrigen = input('Ingrese el nombre de la ciudad de origen: ')
    ciudadDestino = input('Ingrese el nombre de la ciudad de destino: ')
    controller.req3(cont, ciudadOrigen, ciudadDestino)


def optionSix(cont):
    codigoOrigen = input('Ingrese el código IATA del áeropuerto de origen: ')
    millasViajero = input('Ingrese las millas disponibles: ')
    total = controller.req4(cont,codigoOrigen,millasViajero)


def optionSeven(cont):
    ''''''


"""
Menu principal
"""


def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs[0]) == 1:
            print("\nInicializando....")
            cont = controller.init()

        elif int(inputs[0]) == 2:
            optionTwo(cont)

        elif int(inputs[0]) == 3:
            optionThree(cont)

        elif int(inputs[0]) == 4:
            optionFour(cont)

        elif int(inputs[0]) == 5:
            optionFive(cont)

        elif int(inputs[0]) == 6:
            optionSix(cont)

        elif int(inputs[0]) == 7:
            optionSeven(cont)

            pass

        else:
            sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
sys.exit(0)
