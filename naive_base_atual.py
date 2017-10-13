# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets, linear_model,svm
from sklearn.naive_bayes import GaussianNB
import time
import json

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
    for flood_data,flood in zip(data['json_data'][:25000],data['flood'][:25000]):
        x = flood_data.replace("'",'"')
        json_after = json.loads(x)
        if json_after.get('history'):
            json_dailly = json_after['history']['dailysummary']
            if json_dailly:
                variables_fit.append(flood_data)
                boolean_fit.append(flood)

    for flood_data_test,flood_test in zip(data['json_data'][25001:],data['flood'][25001:]):
        x_ = flood_data_test.replace("'",'"')
        json_after_ = json.loads(x_)
        if json_after_.get('history'):
            json_dailly_ = json_after_['history']['dailysummary']
            if json_dailly_:
                variables_test.append(flood_data_test)
                boolean_test.append(flood_test)

   

   
    return variables_fit,boolean_fit,variables_test,boolean_test


# Function for Fitting our data to Linear model
def svm_model_main(X_parameters, Y_parameters, x_test_,y_test_):
    #import ipdb;ipdb.set_trace()
    list_all = []
    list_flood = []
    for x in X_parameters:
        #import ipdb;ipdb.set_trace
        x = x.replace("'",'"')
        json_after = json.loads(x)
        json_dailly = json_after['history']['dailysummary']
        # if json_dailly:
        #     try:
        try:
            temperatura = json_dailly[0]['maxtempm'] if json_dailly[0]['maxtempm'] != '' and json_dailly[0]['maxtempm'] != 'T' else '0'
            temperatura = json_dailly[0]['mintempm'] if json_dailly[0]['mintempm'] != '' and json_dailly[0]['mintempm'] != 'T' else '0'
            humidade = json_dailly[0]['minhumidity'] if json_dailly[0]['minhumidity'] != '' and json_dailly[0]['minhumidity'] != 'T' else '0'
            preciptacao = json_dailly[0]['precipm'] if json_dailly[0]['precipm'] != '' and json_dailly[0]['precipm'] != 'T' else '0'
            list_temp = [float(temperatura),float(humidade)]
        except Exception as e:
            
            import ipdb;ipdb.set_trace()
            print(e)
        
        list_all.append(list_temp)
    # except Exception as e:
            #     pass
                #import ipdb;ipdb.set_trace()    

    model = GaussianNB()
    #import ipdb;ipdb.set_trace()
    # Train the model using the training sets
    model.fit(list_all, Y_parameters)

    result = []
    cont = 25001
    num = 0

    for i in x_test_:
        i = i.replace("'",'"')
        json_after_ = json.loads(i)
        json_dailly_ = json_after_['history']['dailysummary']
        if json_dailly_:
            try:
                temperatura = json_dailly[0]['maxtempm'] if json_dailly[0]['maxtempm'] != '' and json_dailly[0]['maxtempm'] != 'T' else '0'
                temperatura = json_dailly[0]['mintempm'] if json_dailly[0]['mintempm'] != '' and json_dailly[0]['mintempm'] != 'T' else '0'
                humidade_ = json_dailly_[0]['minhumidity'] if json_dailly_[0]['minhumidity'] != '' else '0'
                preciptacao_ = json_dailly_[0]['precipm'] if json_dailly_[0]['precipm'] != '' else '0'
                list_temp_ = [float(temperatura),float(humidade)]
                
            except Exception as e:
                pass
                #import ipdb;ipdb.set_trace()    

        #import ipdb;ipdb.set_trace()
        predicted = model.predict(np.array([list_temp_]))
        #import ipdb;ipdb.set_trace()
        result.append([cont,y_test_[num],predicted[0]]) # .append(nº da linha .csv, boolean real, boolean previsto)

        num+=1
        cont+=1

    return result

inicio = time.time()
X,Y,x_test,y_test = get_data('data_bases/amostra_base_2.csv')
#import ipdb;ipdb.set_trace()

print(Y)
result = svm_model_main(X,Y,x_test,y_test)

list_final = []
for numeros in result:
    print(numeros)
    if numeros[1] == numeros[2]:
        list_final.append(numeros)


fim = time.time()
print ("Naive Bayes")
print ("Quantidade de itens iniciais",len(result))
print ("Quantidade de itens que coincidiram",len(list_final))
print ("Tempo de execução: ", fim-inicio, "segundos")