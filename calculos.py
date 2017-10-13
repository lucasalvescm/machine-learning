#!/usr/bin/env python
#-*- encoding: utf-8 -*-
 
# Autor: Thiago Monteiro
# Data: 10/10/2012
# Local: Goiânia/Goiás/Brasil
 
import math, os, sys

class Calculos:

    def criando_modelo(list_x,list_y):
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

        B1 = ((sum_list_x*sum_list_y) - (len(list_x)*sum_list_x_y)) / ((sum_list_x ** 2) - (len(list_x)*sum_list_x_square))

        B0 = (sum_list_y - (B1 * sum_list_x)) / len(list_x)

        print('y=',str(B0),'+',str(B1),'x')
    
     
    