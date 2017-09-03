# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets, linear_model,svm
import time

inicio = time.time()

# Function to get data
def get_data(file_name):
    '''
    Método que separa a metade do csv para treinamento e a outra para testar as predições.
    Utiliza três variaveis(temperatura minima, preciptação e velocidade do vento) e o boolean de chuva.
    '''
    data = pd.read_csv(file_name)

    variables_fit = []
    boolean_fit = []
    variables_test = []
    boolean_test = []
    #Dados da primeira linha até 1373
    for tempmin,precip,avgwind in zip(data['temperaturemin'][:1372],data['precipitation'][:1372], data['avgwindspeed'][:1372]):
        variables_fit.append([float(tempmin), float(precip), float(avgwind)])

    for rain in data['rain'][:1372]:
        boolean_fit.append(rain)
    #Dados a partir da linha 1373
    for tempmin,precip,avgwind in zip(data['temperaturemin'][1373:],data['precipitation'][1373:], data['avgwindspeed'][1373:]):
        variables_test.append([float(tempmin), float(precip), float(avgwind)])

    for rain in (data['rain'][1373:]):
        boolean_test.append(rain)
    return variables_fit,boolean_fit,variables_test,boolean_test


# Function for Fitting our data to Linear model
def svm_model_main(X_parameters, Y_parameters,x_test_,y_test_):
    # Criando um objeto SVM
    model = svm.SVC(kernel='linear', C = 1.0)
    model.fit(X_parameters, Y_parameters)

    result = []
    cont = 1375
    num = 0
    for i in x_test_:
        #import ipdb;ipdb.set_trace()
        predicted = model.predict(np.array([i]))
        result.append([cont,y_test_[num],predicted[0]]) # .append(nº da linha .csv, boolean real, boolean previsto)

        num+=1
        cont+=1

    return result

X,Y,x,y = get_data('dataset_rain.csv')



result = svm_model_main(X,Y,x,y)

list_final = []
for numeros in result:
    if numeros[1] == numeros[2]:
        list_final.append(numeros)


fim = time.time()
print "SVM"
print "Quantidade de itens iniciais",len(result)
print "Quantidade de itens que coincidiram",len(list_final)
print "Tempo de execução: ", fim-inicio, "segundos"