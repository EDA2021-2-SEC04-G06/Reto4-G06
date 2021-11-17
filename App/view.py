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
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printMenu():
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de aeropuertos y vuelos")
    print("3- Encontrar puntos de interconexion áerea")
    print("4- Encontrar clústeres de tráfico aéreo")
    print("5- Encontrar la ruta más corta entre ciudades")
    print("6- Utilizar las millas de viajero")
    print("7- Cuantificar el efecto de un aeropuerto cerrado")

catalog = None

def optionTwo(cont):
    ''''''
def optionThree(cont):
    ''''''
def optionFour(cont):
    ''''''
def optionFive(cont):
    ''''''
def optionSix(cont):
    ''''''
def optionSeven(cont):
    ''''''
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        cont=''

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
sys.exit(0)
