﻿"""
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
    numero1 = lt.getElement(lista, 1)
    print('Primera Ciudad: ' + str(numero1['city_ascii']) + ' Pais: ' + str(numero1['country']) + ' Latitud: ' + str(numero1['lat']) +
          ' Longitud: ' + str(numero1['lng']) + ' Población: ' + str(numero1['population']))
    numerof = lt.getElement(lista, tamanho)
    print('Última Ciudad: ' + str(numerof['city_ascii']) + ' Pais: ' + str(numerof['country']) + ' Latitud: ' + str(numerof['lat']) +
          ' Longitud: ' + str(numerof['lng']) + ' Población: ' + str(numerof['population']))


def print5aeropuertos(lista):
    i = 1
    while i <= 5:
        airport = lt.getElement(lista, i)
        print(str(i)+'. Nombre: ' + airport['name']+', Ciudad: '+airport['ciudad']+', Pais: '+airport['pais'] +
              ', IATA: '+airport['IATA']+', Conexiones: '+str(airport['conexiones']))
        i += 1


def printCamino(lista):
    for camino in lt.iterator(lista):
        texto = camino['vertexA']+' - '+camino['vertexB']
        print(texto + ', Distancia: ' + str(camino['weight'])+' (km)')


def printPrimeros3(lista):
    tamanho = lt.size(lista)

    if tamanho >= 3:
        i = 1
        while i <= 3:
            airport = lt.getElement(lista, i)
            print(str(i)+'. IATA: '+airport['IATA']+', Nombre: '+airport['Name']+', Ciudad: '+airport['City'] +
                  ', Pais: '+airport['Country'])
            i += 1
    elif tamanho == 2:
        i = 2
        while i <= 3:
            airport = lt.getElement(lista, i)
            print(str(i)+'. IATA: '+airport['IATA']+', Nombre: '+airport['Name']+', Ciudad: '+airport['City'] +
                  ', Pais: '+airport['Country'])
            i += 1
    else:
        airport = lt.getElement(lista, 1)
        print('1. IATA: '+airport['IATA']+', Nombre: '+airport['Name']+', Ciudad: '+airport['City'] +
              ', Pais: '+airport['Country'])


def printUltimos3(lista):
    tamanho = lt.size(lista)
    if tamanho >= 3:
        i = tamanho-2
        while i <= tamanho:
            airport = lt.getElement(lista, i)
            print(str(i)+'. IATA: '+airport['IATA']+', Nombre: '+airport['Name']+', Ciudad: '+airport['City'] +
                  ', Pais: '+airport['Country'])
            i += 1
    elif tamanho == 2:
        i = tamanho-1
        while i <= tamanho:
            airport = lt.getElement(lista, i)
            print(str(i)+'. IATA: '+airport['IATA']+', Nombre: '+airport['Name']+', Ciudad: '+airport['City'] +
                  ', Pais: '+airport['Country'])
            i += 1
    else:
        airport = lt.getElement(lista, 1)
        print('1. IATA: '+airport['IATA']+', Nombre: '+airport['Name']+', Ciudad: '+airport['City'] +
              ', Pais: '+airport['Country'])


def printorden(lista):
    for each in lt.iterator(lista):
        print(each)


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

    aeropuertos2 = (gr.numVertices(cont['grafoNoDirigido']))
    rutas2 = (gr.numEdges(cont['grafoNoDirigido']))
    print('\nTotal aeropuertos en el Grafo No Dirigido: '+str(aeropuertos2))
    print('Total rutas aéreas en Grafo No Dirigido: '+str(rutas2))

    print('\nTotal de Ciudades: ' + str(lt.size(cont['listaCiudades'])))
    printTotalCiudades(cont['listaCiudades'])


def optionThree(cont):
    total = controller.req1(cont)
    print('\nPara el Digrafo: ')
    print('Aeropuertos conectados en la red: ' + str(lt.size(total[0])))
    print('Los 5 aeropuertos mas conectados son: ')
    print5aeropuertos(total[0])


def optionFour(cont):
    codigoIATA1 = input('Ingrese el código IATA del primer aeropuerto: ')
    codigoIATA2 = input('Ingrese el código IATA del segundo aeropuerto: ')
    total = controller.req2(cont, codigoIATA1, codigoIATA2)
    print('\nNúmero total de clústeres presentes en la red de transporte aéreo: ' +
          str(total[0]['components']))
    print('¿Estan '+total[2]+' ('+codigoIATA1+') y ' +
          total[3]+' ('+codigoIATA2+') conectados?: '+str(total[1]))


def optionFive(cont):
    ciudadOrigen = input('Ingrese el nombre de la ciudad de origen: ')
    ciudadDestino = input('Ingrese el nombre de la ciudad de destino: ')
    total = controller.req3(cont, ciudadOrigen, ciudadDestino)
    print('\nEl aeropuerto de salida en la ciudad de '+ciudadOrigen+' es:')
    print('IATA: ' + total[0]['IATA'] + ', Nombre: ' + total[0]['Name'] +
          ', Ciudad: ' + total[0]['City']+', Pais: '+total[0]['Country'])
    print('\nEl aeropuerto de llegada en la ciudad de '+ciudadDestino+' es:')
    print('IATA: ' + total[1]['IATA'] + ', Nombre: ' + total[1]['Name'] +
          ', Ciudad: ' + total[1]['City']+', Pais: '+total[1]['Country'])
    print('\nDetalles de Vuelo:')
    print('Distancia Total: ' + str(total[2])+' (km)')
    print('Ruta:')
    printCamino(total[3])
    print('Distancia con Distancia Terrestre: ' +
          str(round(total[4], 3))+' (km)')


def optionSix(cont):
    codigoOrigen = input('Ingrese el código IATA del aeropuerto de origen: ')
    millasViajero = input('Ingrese las millas disponibles: ')
    total = controller.req4(cont, codigoOrigen, millasViajero)
    print('Numero de nodos conectados al arbol de expansion minima: ' +
          str(total[0]))
    print('Distancia en millas disponibles del viajero: '+str(total[1]))
    print('Costo total del arbol (km): '+str(total[2]))
    print('Millas Excedentes/Sobrantes: '+str(total[3]))
    print('Rama mas larga posible: ')
    printorden(total[4])


def optionSeven(cont):
    codigoCerrado = input('Ingrese el código IATA del aeropuerto cerrado: ')
    total = controller.req5(cont, codigoCerrado)
    print('\nCerrando el aeropuerto con código IATA: '+codigoCerrado)
    print('\nEn el Digrafo original:')
    aeropuertos = (gr.numVertices(cont['digrafo']))
    rutas = (gr.numEdges(cont['digrafo']))
    print('Total aeropuertos en el Digrafo: '+str(aeropuertos))
    print('Total rutas aéreas en Digrafo: '+str(rutas))
    print('\nEn el Grafo No Dirigido: ')
    aeropuertos2 = (gr.numVertices(cont['grafoNoDirigido']))
    rutas2 = (gr.numEdges(cont['grafoNoDirigido']))
    print('Total aeropuertos en el Grafo No Dirigido: '+str(aeropuertos2))
    print('Total rutas aéreas en Grafo No Dirigido: '+str(rutas2))
    print('\nRemoviendo el aeropuerto con código IATA: '+codigoCerrado)
    print('\nEn el Digrafo:')
    print('Número resultante de aeropuertos: ' +
          str(gr.numVertices(total[0]))+' y Rutas aéreas: '+str(gr.numEdges(total[0])))
    print('\nEn el Grafo No Dirigido: ')
    print('Número resultante de aeropuertos: ' +
          str(gr.numVertices(total[2]))+' y Rutas aéreas: '+str(gr.numEdges(total[2])))

    print('\nHay '+str(lt.size(total[1])) +
          ' aeropuertos afectados por el cierre de: '+codigoCerrado)
    print('Los primeros son:')
    printPrimeros3(total[1])
    print('Los últimos son: ')
    printUltimos3(total[1])


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
