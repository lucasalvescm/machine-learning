# -*- coding: utf-8 -*-
import MySQLdb
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets, linear_model,svm
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.linear_model import LogisticRegression
import time
import json
from calculos import AjusteCurva


# nome_algoritmo = ''
# inicio = time.time()
# # Function to get data
# def get_data(file_name):
#     '''
#     Método que separa a metade do csv para treinamento e a outra para testar as predições.
#     Utiliza três variaveis(temperatura minima, preciptação e velocidade do vento) e o boolean de chuva.
#     '''
#     data = pd.read_csv(file_name)

#     listx = []
#     listy=[]
#     #Dados da primeira linha até 1373
#     for sepal_length,sepal_width in zip(data['sepal_length'],data['sepal_width']):
#         listx.append(sepal_length)
#         listy.append(sepal_width)
        

#     return listx,listy


# x, y = get_data('iris_setosa.csv')

# b0,b1,sum_y_square, sum_y = AjusteCurva.modelo_mmq(x,y)

# desvio = AjusteCurva.desvio(b0,b1,x,y)

# coeficiente = AjusteCurva.coeficiente_determinacao(desvio,sum_y_square,sum_y,len(x))

# variancia = AjusteCurva.variancia_residual(desvio,len(x))

# print(desvio, coeficiente, variancia)


listx = [3.8,3.4,3.2,4,3.2]
listy=[5.1,5,4.4,5.8,4.7]
listp=[3.49,3.41,2.9,4.07,3.16]

plt.plot(listx,listy,'ro')
plt.plot(listp,listy,'bo')


plt.show()

