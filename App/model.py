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


from math import e
from haversine import haversine
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT.graph import gr, vertices
from DISClib.Algorithms.Graphs import dfs as dfs
from DISClib.Algorithms.Graphs import scc as scc
from DISClib.Algorithms.Graphs import bellmanford as bf
from DISClib.Algorithms.Graphs import prim as prim
from DISClib.Algorithms.Graphs import dijsktra as dijsktra
from DISClib.Algorithms.Graphs import cycles as cycles
from DISClib.Algorithms.Sorting import mergesort as sm
from DISClib.ADT import queue as q
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos


def newAnalyzer():
    analyzer = {'listaCiudades': None,
                'listaAeropuertos': None,
                'mapaAeroPuertosPorPais': None,
                'mapaAeropuertos': None,
                'mapaCiudades': None,
                'mapCiudades': None,
                'digrafo': None,
                'grafoDirigido': None,
                'arrayCiudades': None}

    analyzer['listaCiudades'] = lt.newList(datastructure='ARRAY_LIST')

    analyzer['listaAeropuertos'] = lt.newList(datastructure='ARRAY_LIST')

    analyzer['arrayCiudades'] = lt.newList(datastructure='ARRAY_LIST')

    analyzer['mapaAeropuertosPorPais'] = mp.newMap(
        maptype='PROBING', comparefunction=compareMapCountry)

    analyzer['mapaAeropuertosPorCiudadyPais'] = mp.newMap(
        maptype='PROBING', comparefunction=compareMapCity)

    analyzer['mapaAeropuertosPorIATA'] = mp.newMap(
        maptype='PROBING', comparefunction=compareMapIATA)

    analyzer['mapaCiudades'] = mp.newMap(numelements=41001, maptype='PROBING')

    analyzer['mapCiudades'] = mp.newMap(
        numelements=41001, maptype='PROBING', comparefunction=compareMapCity)

    analyzer['digrafo'] = gr.newGraph(datastructure='ADJ_LIST',
                                      directed=True, size=9076,
                                      comparefunction=compareIATA)

    analyzer['grafoNoDirigido'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False, size=9076,
                                              comparefunction=compareIATA)
    return analyzer

# Funciones para agregar informacion al catalogo


def addVertex(analyzer, airport):
    iata = airport['IATA']
    if not gr.containsVertex(analyzer['digrafo'], iata):
        gr.insertVertex(analyzer['digrafo'], iata)
    if not gr.containsVertex(analyzer['grafoNoDirigido'], iata):
        gr.insertVertex(analyzer['grafoNoDirigido'], iata)
    return analyzer


def addRutaConexion(analyzer, ruta):
    origen = ruta['Departure']
    llegada = ruta['Destination']
    distancia = float(ruta['distance_km'])
    gr.addEdge(analyzer['digrafo'], origen, llegada, distancia)


def addCiudad(analyzer, city):
    lt.addLast(analyzer['listaCiudades'], city)
    mapaCiudades = analyzer['mapCiudades']
    nombreCiudad = city['city_ascii']

    existCity = mp.contains(mapaCiudades, nombreCiudad)
    if existCity:
        entry = mp.get(mapaCiudades, nombreCiudad)
        ciudad_final = me.getValue(entry)
        lt.addLast(ciudad_final[nombreCiudad], city)

    else:
        ciudad_final = newCity(nombreCiudad)
        lt.addLast(ciudad_final[nombreCiudad], city)
        mp.put(mapaCiudades, nombreCiudad, ciudad_final)


def newCity(nombreCiudad):
    entry = {nombreCiudad: None}
    entry[nombreCiudad] = lt.newList('ARRAY_LIST')
    return entry


def addAirport(analyzer, airport):
    lt.addLast(analyzer['listaAeropuertos'], airport)
    iatas = analyzer['mapaAeropuertosPorIATA']
    ciudades = analyzer['mapaAeropuertosPorCiudadyPais']
    paises = analyzer['mapaAeropuertosPorPais']
    iata = airport['IATA']
    ciudad = airport['City']
    pais = airport['Country']

    mp.put(iatas, iata, airport)

    existCiudad = mp.contains(ciudades, ciudad)
    if existCiudad:
        entry = mp.get(ciudades, ciudad)
        ciudadAeroFinal = me.getValue(entry)
        lt.addLast(ciudadAeroFinal[ciudad], airport)

    else:
        ciudadAeroFinal = newCity2(ciudad)
        lt.addLast(ciudadAeroFinal[ciudad], airport)
        mp.put(ciudades, ciudad, ciudadAeroFinal)

    existCountry = mp.contains(paises, pais)
    if existCountry:
        entry = mp.get(paises, pais)
        paisAeroFinal = me.getValue(entry)
        lt.addLast(paisAeroFinal, airport)

    else:
        paisAeroFinal = newCountry(airport)
        mp.put(paises, pais, paisAeroFinal)


def newCity2(ciudad):
    entry = {ciudad: None}
    entry[ciudad] = lt.newList(datastructure='ARRAY_LIST')
    return entry


def newCountry(airport):
    entry = lt.newList(datastructure='ARRAY_LIST')
    lt.addLast(entry, airport)
    return entry


def addInfoGrafoNoDirigido(analyzer):
    lista = gr.edges(analyzer['digrafo'])
    for arco in lt.iterator(lista):
        verticeA = arco['vertexA']
        verticeB = arco['vertexB']
        comparacion = gr.getEdge(analyzer['digrafo'], verticeB, verticeA)
        if comparacion:
            comparacion2 = gr.getEdge(
                analyzer['grafoNoDirigido'], verticeB, verticeA)
            comparacion3 = gr.getEdge(
                analyzer['grafoNoDirigido'], verticeA, verticeB)
            if comparacion2 == None and comparacion3 == None:
                gr.addEdge(analyzer['grafoNoDirigido'],
                           verticeA, verticeB, arco['weight'])


def addCity(analyzer, ciudades):
    city = ciudades['city_ascii']
    pais = ciudades['country']
    latitud = ciudades['lat']
    longitud = ciudades['lng']
    lt.addLast(analyzer['arrayCiudades'], city)


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


def compareMapIATA(keyIATA, IATAS):
    IATAEntry = me.getKey(IATAS)
    if keyIATA == IATAEntry:
        return 0
    elif keyIATA > IATAEntry:
        return 1
    else:
        return -1


def compareMapCountry(keyCountry, countries):
    countryEntry = me.getKey(countries)
    if keyCountry == countryEntry:
        return 0
    elif keyCountry > countryEntry:
        return 1
    else:
        return -1


def compareMapCity(keyCity, cities):
    cityEntry = me.getKey(cities)
    if keyCity == cityEntry:
        return 0
    elif keyCity > cityEntry:
        return 1
    else:
        return -1


def sortbyConexiones(airport1, airport2):
    conexiones1 = airport1['conexiones']
    conexiones2 = airport2['conexiones']

    if conexiones1 > conexiones2:
        return 1
    else:
        return 0


def sortbyDistance(airport1, airport2):
    distancia1 = airport1['distancia']
    distancia2 = airport2['distancia']
    if distancia1 < distancia2:
        return 1
    else:
        return 0


# Funciones de ordenamiento

def req1(analyzer):
    listaVertex = gr.vertices(analyzer['digrafo'])
    nuevaList = lt.newList(datastructure='ARRAY_LIST')
    for codigo in lt.iterator(listaVertex):
        outbound = gr.outdegree(analyzer['digrafo'], codigo)
        inbound = gr.indegree(analyzer['digrafo'], codigo)
        conexiones = inbound + outbound
        if conexiones != 0:
            airport = mp.get(analyzer['mapaAeropuertosPorIATA'], codigo)
            valores = me.getValue(airport)
            addList = {'IATA': codigo, 'ciudad': valores['City'],
                       'pais': valores['Country'], 'name': valores['Name'], 'conexiones': conexiones}
            lt.addLast(nuevaList, addList)

    listaVertex2 = gr.vertices(analyzer['grafoNoDirigido'])
    nuevaList2 = lt.newList(datastructure='ARRAY_LIST')
    for codigo in lt.iterator(listaVertex2):
        outbound = gr.outdegree(analyzer['grafoNoDirigido'], codigo)
        inbound = gr.indegree(analyzer['grafoNoDirigido'], codigo)
        conexiones = inbound + outbound
        if conexiones != 0:
            airport = mp.get(analyzer['mapaAeropuertosPorIATA'], codigo)
            valores = me.getValue(airport)
            addList = {'IATA': codigo, 'ciudad': valores['City'],
                       'pais': valores['Country'], 'name': valores['Name'], 'conexiones': conexiones}
            lt.addLast(nuevaList2, addList)

    sortedList = sm.sort(nuevaList, sortbyConexiones)
    sortdeList2 = sm.sort(nuevaList2, sortbyConexiones)
    return sortedList, sortdeList2


def req2(analyzer, codigoIATA1, codigoIATA2):
    componentesFuertementeMapa = scc.KosarajuSCC(analyzer['digrafo'])
    conectados = scc.stronglyConnected(
        componentesFuertementeMapa, codigoIATA1, codigoIATA2)
    aeropuerto1 = mp.get(analyzer['mapaAeropuertosPorIATA'], codigoIATA1)
    valorAeropuerto1 = me.getValue(aeropuerto1)
    nombreAeropuerto1 = valorAeropuerto1['Name']
    aeropuerto2 = mp.get(analyzer['mapaAeropuertosPorIATA'], codigoIATA2)
    valorAeropuerto2 = me.getValue(aeropuerto2)
    nombreAeropuerto2 = valorAeropuerto2['Name']
    return componentesFuertementeMapa, conectados, nombreAeropuerto1, nombreAeropuerto2


def req3(analyzer, ciudadOrigen, ciudadDestino):
    ciudadesOrigen = mp.get(analyzer['mapCiudades'], ciudadOrigen)
    valuesOrigen = me.getValue(ciudadesOrigen)
    listaOrigen = valuesOrigen[ciudadOrigen]
    print('\nPara la Ciudad de Origen: '+ciudadOrigen)
    i = 1
    for ciudad in lt.iterator(listaOrigen):
        print(str(i) + '. Pais: ' + ciudad['country'] + ', Nombre Admin: ' + ciudad['admin_name'] + ', Latitud: ' +
              ciudad['lat'] + ', Longitud: ' + ciudad['lng'])
        i += 1
    numeroCiudadOrigen = int(input('\nSeleccione el número de la ciudad: '))

    print('\nPara la Ciudad de Destino: '+ciudadDestino)
    ciudadesDestino = mp.get(analyzer['mapCiudades'], ciudadDestino)
    valuesDestino = me.getValue(ciudadesDestino)
    listaDestino = valuesDestino[ciudadDestino]
    i = 1
    for ciudad in lt.iterator(listaDestino):
        print(str(i) + '. Pais: ' + ciudad['country'] + ', Nombre Admin: ' + ciudad['admin_name'] + ', Latitud: ' +
              ciudad['lat'] + ', Longitud: ' + ciudad['lng'])
        i += 1

    numeroCiudadDestino = int(input('\nSeleccione el número de la ciudad: '))

    infoOrigen = lt.getElement(listaOrigen, numeroCiudadOrigen)
    infoDestino = lt.getElement(listaDestino, numeroCiudadDestino)

    paisOrigen = infoOrigen['country']
    paisDestino = infoDestino['country']

    origenLatLng = (float(infoOrigen['lat']), float(infoOrigen['lng']))
    destinoLatLng = (float(infoDestino['lat']), float(infoDestino['lng']))

    aeropuertosEnPaisOrigen = mp.get(
        analyzer['mapaAeropuertosPorPais'], paisOrigen)
    aeropuertosEnPaisDestino = mp.get(
        analyzer['mapaAeropuertosPorPais'], paisDestino)

    listaAeropuertosOrigen = me.getValue(aeropuertosEnPaisOrigen)
    listaAeropuertosDestino = me.getValue(aeropuertosEnPaisDestino)

    listaOrigen = lt.newList(datastructure='ARRAY_LIST')
    listaDestino = lt.newList(datastructure='ARRAY_LIST')

    for aeropuerto in lt.iterator(listaAeropuertosOrigen):
        coordenandas = (float(aeropuerto['Latitude']), float(
            aeropuerto['Longitude']))
        iata = aeropuerto['IATA']
        harvensiano = haversine(coordenandas, origenLatLng)
        listaAdd = {'IATA': iata, 'distancia': harvensiano}
        lt.addLast(listaOrigen, listaAdd)

    for aeropuerto in lt.iterator(listaAeropuertosDestino):
        coordenandas = (float(aeropuerto['Latitude']), float(
            aeropuerto['Longitude']))
        iata = aeropuerto['IATA']
        harvensiano = haversine(coordenandas, destinoLatLng)
        listaAdd = {'IATA': iata, 'distancia': harvensiano}
        lt.addLast(listaDestino, listaAdd)

    sortOrigen = sm.sort(listaOrigen, sortbyDistance)
    sortDestino = sm.sort(listaDestino, sortbyDistance)

    finalOrigen = lt.getElement(sortOrigen, 1)
    finalDestino = lt.getElement(sortDestino, 1)

    infoOrigenFinal = mp.get(
        analyzer['mapaAeropuertosPorIATA'], finalOrigen['IATA'])
    infoDestinoFinal = mp.get(
        analyzer['mapaAeropuertosPorIATA'], finalDestino['IATA'])
    valuesOrigenFinal = me.getValue(infoOrigenFinal)
    valuesDestinoFinal = me.getValue(infoDestinoFinal)

    x = dijsktra.Dijkstra(analyzer['digrafo'], finalOrigen['IATA'])
    distanciaRuta = dijsktra.distTo(x, finalDestino['IATA'])
    camino = dijsktra.pathTo(x, finalDestino['IATA'])

    distanciaTotal = distanciaRuta + \
        float(finalOrigen['distancia']) + float(finalDestino['distancia'])

    return valuesOrigenFinal, valuesDestinoFinal, distanciaRuta, camino, distanciaTotal


def req4(analyzer, codigoOrigen, millasViajero):
    mst = prim.PrimMST(analyzer['grafoNoDirigido'])
    edgesto = prim.edgesMST(analyzer['grafoNoDirigido'], mst)
    nodos = lt.size(edgesto['edgeTo'])
    millasDisponibles = 1.6 * float(millasViajero)
    pathslist = lt.newList(datastructure='ARRAY_LIST')
    pesoTotal = 0

    for each in edgesto['edgeTo']['table']['elements']:
        if each['key'] != None:
            air1 = each['value']['vertexA']
            air2 = each['value']['vertexB']
            peso = each['value']['weight']
            lt.addLast(pathslist, [air1, air2, peso])
            pesoTotal += peso

    millasExcedentes = millasDisponibles - pesoTotal

    return nodos, millasDisponibles, pesoTotal, millasExcedentes, pathslist


def req5(analyzer, codigoCerrado):
    digrafo = analyzer['digrafo']
    nuevoDigrafo = gr.newGraph(datastructure='ADJ_LIST',
                               directed=True, size=9076,
                               comparefunction=compareIATA)
    listaVerticesDigrafo = gr.vertices(digrafo)
    listaArcosDigrafo = gr.edges(digrafo)

    listaAeropuertoAfectado = lt.newList(datastructure='ARRAY_LIST')
    mapaComparacion = mp.newMap(
        maptype='PROBING', comparefunction=compareMapIATA)

    for vertice in lt.iterator(listaVerticesDigrafo):
        if vertice != codigoCerrado:
            gr.insertVertex(nuevoDigrafo, vertice)

    for arco in lt.iterator(listaArcosDigrafo):
        if arco['vertexA'] != codigoCerrado and arco['vertexB'] != codigoCerrado:
            gr.addEdge(nuevoDigrafo, arco['vertexA'],
                       arco['vertexB'], float(arco['weight']))
        else:
            if arco['vertexA'] == codigoCerrado:
                aeropuertoAfectado = arco['vertexB']
                existIATA = mp.contains(mapaComparacion, aeropuertoAfectado)
                if existIATA == False:
                    mp.put(mapaComparacion, aeropuertoAfectado, 0)
                    infoAeropuertoAfectado = mp.get(
                        analyzer['mapaAeropuertosPorIATA'], aeropuertoAfectado)
                    valores = me.getValue(infoAeropuertoAfectado)
                    addList = {'IATA': aeropuertoAfectado, 'Name': valores['Name'], 'City': valores['City'],
                               'Country': valores['Country']}
                    lt.addLast(listaAeropuertoAfectado, addList)
            else:
                aeropuertoAfectado = arco['vertexA']
                existIATA = mp.contains(mapaComparacion, aeropuertoAfectado)
                if existIATA == False:
                    mp.put(mapaComparacion, aeropuertoAfectado, 0)
                    infoAeropuertoAfectado = mp.get(
                        analyzer['mapaAeropuertosPorIATA'], aeropuertoAfectado)
                    valores = me.getValue(infoAeropuertoAfectado)
                    addList = {'IATA': aeropuertoAfectado, 'Name': valores['Name'], 'City': valores['City'],
                               'Country': valores['Country']}
                    lt.addLast(listaAeropuertoAfectado, addList)

    grafoNoDirigido = analyzer['grafoNoDirigido']
    nuevoGrafoNoDirigido = gr.newGraph(datastructure='ADJ_LIST',
                                       directed=False, size=9076,
                                       comparefunction=compareIATA)
    listaVerticesGrafoNoDirigido = gr.vertices(grafoNoDirigido)
    listaArcosGrafoNoDirigido = gr.edges(grafoNoDirigido)

    for vertice in lt.iterator(listaVerticesGrafoNoDirigido):
        if vertice != codigoCerrado:
            gr.insertVertex(nuevoGrafoNoDirigido, vertice)

    for arco in lt.iterator(listaArcosGrafoNoDirigido):
        if arco['vertexA'] != codigoCerrado and arco['vertexB'] != codigoCerrado:
            gr.addEdge(nuevoGrafoNoDirigido,
                       arco['vertexA'], arco['vertexB'], float(arco['weight']))

    return nuevoDigrafo, listaAeropuertoAfectado, nuevoGrafoNoDirigido
