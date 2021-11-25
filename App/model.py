﻿"""
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
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    analyzer = {'mapaAeropuertos': None,
                'mapaCiudades': None,
                'digrafo': None,
                'grafoDirigido': None}

    analyzer['mapaAeropuertos'] = mp.newMap(numelements=9075, maptype='PROBING')

    analyzer['mapaCiudades'] = mp.newMap(numelements=41001, maptype='PROBING')

    analyzer['digrafo'] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=True,size=9076,
                                        comparefunction=compareIATA)

    '''analyzer['grafoDirigido'] = gr.newGraph(datastructure='ADJ_LIST',
                                            directed=False,
                                            size=)'''
    return analyzer

# Funciones para agregar informacion al catalogo

def addVertex(analyzer, airport):
    iata = airport['IATA']
    if not gr.containsVertex(analyzer['digrafo'], iata):
        gr.insertVertex(analyzer['digrafo'], iata)
    return analyzer
    

def addRutaConexion(analyzer, ruta):
    origen = ruta['Departure']
    llegada = ruta['Destination']
    distancia = ruta['distance_km']
    gr.addEdge(analyzer['digrafo'],origen,llegada,distancia)


# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

def compareIATA(iata, keyvalueIata):
    """
    Compara dos estaciones
    """
    iatacode = keyvalueIata['key']
    if (iata == iatacode):
        return 0
    elif (iata > iatacode):
        return 1
    else:
        return -1

# Funciones de ordenamiento
