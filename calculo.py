import cv2
import numpy as np
import math

# função para calcular a distancia e  o angulo 
def  calculo_angulo  (x1, y1, x2, y2):
# chamada na funçao x = lista[0],[0]; y = lista [0],[1].
    distancia = math.dist ((x1, y1), (x2, y2))
    # math.atan2 é uma função da biblioteca math para calcular o angulo em radianos  
    angulo_rad = math.atan2 (( y2 - y1), (x2 - x1))
    #  math. degrees é uma função da biblioteca math para transformar os graus de radianos para graus
    angulo_graus = math.degrees (angulo_rad)

    #  isso é para retornar a distancia e o angulo para o código principal
    return distancia, angulo_graus