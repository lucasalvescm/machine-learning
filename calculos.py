#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
    Implementação de cálculos de ajuste de curva.

    Esse módulo implementa cálculos necessários para ajuste curva. São eles:
    Método dos Mínimos Quadrados, Desvio, Coeficiente de Determinação e Variância Residual 
     
     
"""
 
__author__ = "Lucas Alves de Souza"
__copyright__ = "Copyright 2017, by Alves"
__credits__ = "Todos desenvolvedores de software livre"
__license__ = "GNU General Public License"
__version__ = "1.0.0"
__maintainer__ = "Lucas Alves"
__email__ = "lucasalves.s@outlook.com"

 
import math, os, sys

class AjusteCurva:

    def modelo_mmq(list_x,list_y):
        '''
        Criar um modelo a partir do Método dos Mínimos Quadrados.
        entrada:
         - lista de elementos x.
         - lista de elementos y.
        saída: 
         - b0 e b1 que são os elementos do modelo Y = b0 + b1x

        '''
        list_x_square = []
        list_y_square = []
        list_x_y = []
           
        cont = 0


        for x in list_x:
            x = x ** 2
            list_x_square.append(x)

        for y in list_y:
            y = y ** 2
            list_y_square.append(y)

        for x in list_x:
            list_x_y.append(list_x[cont] * list_y[cont])
            cont+=1

          
        sum_list_x_square = sum(list_x_square)
        sum_list_y_square = sum(list_y_square)
        sum_list_x_y = sum(list_x_y)
        sum_list_x = sum(list_x)
        sum_list_y = sum(list_y)
        try:

            B1 = ((sum_list_x*sum_list_y) - (len(list_x)*sum_list_x_y)) / ((sum_list_x ** 2) - (len(list_x)*sum_list_x_square))
        except ZeroDivisionError:
            B1 = 0    
        try:
            B0 = (sum_list_y - (B1 * sum_list_x)) / len(list_x)
        except ZeroDivisionError:
            B0 = 0        

        print('y=',str(B0),'+',str(B1),'x')

        return B0,B1, sum_list_y_square, sum_list_y

    def desvio(b0,b1,list_x,list_y):
        '''
        Calcular desvio a partir do modelo gerado pelo MMQ.
        entrada:
         - b0 e b1 que são os elementos do modelo Y = b0 + b1x
         - lista de elementos x.
         - lista de elementos y.
        saída: 
         - valor de desvio.

        '''
        cont = 0
        list_resultados = []
        for x in list_x:
            resultado = 0
            resultado = (list_y[cont] - (b0 + (b1*list_x[cont]))) ** 2
            list_resultados.append(resultado)
            cont+=1

        desvio = sum(list_resultados)    

        return desvio
        
    def coeficiente_determinacao(desvio, sum_y_square, sum_y, len_elements):
        '''
        Calcular coeficiente de determinação.
        entrada:
         - desvio
         - lista de elementos y ²
         - lista de elementos y
         - quantidade de pontos
        saída: 
         - coeficiente de determinação

        '''
        try:
            coef = 1 - (desvio / (sum_y_square - ((sum_y ** 2)/len_elements)))
        except ZeroDivisionError:
            coef = 0
        return coef

    def variancia_residual(desvio,len_elements):
        '''
        Calcular variância residual.
        entrada:
         - desvio
         - quantidade de pontos.
        saída: 
         - variância residual

        '''
        try:
            variancia = desvio / (len_elements - 2)
        except ZeroDivisionError:
            variancia = 0

        return variancia
    

     
    