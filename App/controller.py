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
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros


def init():
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos


def loadData(analyzer, airportsfile, routesfile, citiesfile):
    airportsfile = cf.data_dir + airportsfile
    routesfile = cf.data_dir + routesfile
    citiesfile = cf.data_dir + citiesfile
    inputFileAirport = csv.DictReader(
        open(airportsfile, encoding="utf-8"), delimiter=",")
    inputFileRoutes = csv.DictReader(
        open(routesfile, encoding="utf-8"), delimiter=",")
    inputFileCities = csv.DictReader(
        open(citiesfile, encoding="utf-8"), delimiter=",")

    for city in inputFileCities:
        model.addCity(analyzer, city)
        model.addCiudad(analyzer, city)

    for airport in inputFileAirport:
        model.addAirport(analyzer,airport)
        model.addVertex(analyzer, airport)

    for ruta in inputFileRoutes:
        model.addRutaConexion(analyzer, ruta)


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def req1(analyzer):
    return model.req1(analyzer)

def req2(analyzer, codigoIATA1, codigoIATA2):
    return model.req2(analyzer,codigoIATA1,codigoIATA2)


def req3(analyzer, ciudadOrigen, ciudadDestino):
    model.req3(analyzer, ciudadOrigen, ciudadDestino)
