# -*- coding: utf-8 -*-
import MySQLdb
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets, linear_model,svm
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
import os
import csv
from itertools import product 
from sklearn.linear_model import LogisticRegression
import time
import json
from calculos import AjusteCurva
from matplotlib.pyplot import step, xlim, ylim, show

class MachineLearning:
    def get_data(self,file_name):
            '''
            Método que separa a metade do csv para treinamento e a outra para testar as predições.
            Utiliza três variaveis(temperatura minima, preciptação e velocidade do vento) e o boolean de chuva.
            '''
            data = pd.read_csv(file_name)

            

            data = data.iloc[np.random.permutation(len(data))]
            climate_data_fit = []
            flood_data_fit = []
            #Dados da primeira linha até 1373
            for climate_data,flood in zip(data['json_data'],data['flood']):
                #import ipdb;ipdb.set_trace()
                x = climate_data.replace("'",'"')
                try:
                    json_after = json.loads(x)
                    if json_after.get('history'):
                        json_dailly = json_after['history']['dailysummary']
                        if json_dailly and json_dailly[0]['mintempm'] != '-55573':
                            climate_data_fit.append(climate_data)
                            flood_data_fit.append(flood)   
                except Exception as e:
                    print(str(e))
            return climate_data_fit,flood_data_fit
    def calculando_ajuste_curva(self,list_var,content):
        dict_result = {}
        list_x = []
        list_y = []
        for json_data in content:
            try:        
                json_data = json_data.replace("'",'"')
                json_content = json.loads(json_data)

                json_dailly = json_content['history']['dailysummary']
               
                if json_dailly != []:
                    try:
                        for key in json_dailly[0].keys():
                            if key in list_var:
                                #print(key)
                                try:
                                    param = float(json_dailly[0][key]) if json_dailly[0][key] != '-999' else 0
                                except:
                                    param = 0
                                if param == '':
                                    param = 0
                                
                                if key == list_var[0]:
                                    list_x.append(param)
                                if key == list_var[1]:
                                    list_y.append(param)
                        
                    except Exception as e:
                        print(e)
                        import ipdb;ipdb.set_trace()
                    
            except:
                pass
        # plt.plot(list_x, list_y,'ro')
        # #plt.axis([0,50,0,100])
        # plt.show()  


        #import ipdb;ipdb.set_trace()   
        b0,b1,sum_y_square, sum_y = AjusteCurva.modelo_mmq(list_x,list_y)

        desvio = AjusteCurva.desvio(b0,b1,list_x,list_y)

        coeficiente = AjusteCurva.coeficiente_determinacao(desvio,sum_y_square,sum_y,len(list_x))

        variancia = AjusteCurva.variancia_residual(desvio,len(list_x))
        lista_string = [str(list_var),desvio,coeficiente,variancia]
        

        return lista_string
   
    def treinamento():
        # Open database connection
        db = MySQLdb.connect("localhost","root","root","flood_db" )
        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        list_all = []
        list_flood = []
        cursor.execute("select * from data_climate where json_data is not Null order by id_event;")
        data_ = list(cursor.fetchall())
        count = 0
        for dt in data_[:44582]:
            try:
                json_data = dt[3]
                flood = dt[4]
                
                json_data = json_data.replace("'",'"')
                json_content = json.loads(json_data)

                json_dailly = json_content['history']['dailysummary']
                #import ipdb;ipdb.set_trace()
                list_temp = []
                # if json_dailly:
                #     try:
                if json_dailly != []:
                    try:
                        for key in json_dailly[0].keys():
                            #import ipdb;ipdb.set_trace()
                            #if key in ('maxtempm','mintempm','minhumidity','maxhumidity','maxpressurei','minpressurem','maxwspdi','precipi'):
                            if key in ('mintempm','minhumidity','minpressurem','maxwspdi','precipi'):
                                #print(key)
                                try:
                                    param = float(json_dailly[0][key])
                                except:
                                    param = 0
                                if param == '':
                                    param = 0
                                list_temp.append(param)
                        list_flood.append(float(flood))        
                        #print(list_temp)
                    except Exception as e:
                        print(e)
                        import ipdb;ipdb.set_trace()
                    #import ipdb;ipdb.set_trace()
                    list_all.append(list_temp)
            except:
                pass

        #model = DecisionTreeClassifier()
        #model = KNeighborsClassifier()
        #model = svm.SVC()
        #model = GaussianNB()
        model = LogisticRegression()

        nome_algoritmo = model.__class__.__name__

        model.fit(np.array(list_all), np.array(list_flood))
        #import ipdb;ipdb.set_trace()
        result = []
        cont = 30001
        num = 0


        list_all = []
        list_flood = []
        flood = ''
        json_data = ''
        json_dailly = ''
        json_content = ''
        param = ''
        list_temp = []

        for dt in data_[44582:]:

            try:
                json_data = dt[3]
                flood = dt[4]
                
                json_data = json_data.replace("'",'"')
                json_content = json.loads(json_data)

                json_dailly = json_content['history']['dailysummary']
                #import ipdb;ipdb.set_trace()
                list_temp = []
                # if json_dailly:
                #     try:
                if json_dailly:
                    try:
                        for key_ in json_dailly[0].keys():
                            #import ipdb;ipdb.set_trace()
                            if key_ in ('mintempm','minhumidity','minpressurem','maxwspdi','precipi'):
                                try:
                                    param = float(json_dailly[0][key_])
                                except:
                                    param = 0
                                if key_ == '':
                                    param = 0
                                list_temp.append(param)
                                #print(list_temp)
                        list_flood.append(float(flood))        
                    # print(list_temp)
                    except Exception as e:
                        print(e)
                        import ipdb;ipdb.set_trace()
                if list_temp:
                    predicted = model.predict(np.array([list_temp]))
                    result.append([cont,flood,predicted[0]]) # .append(nº da linha .csv, boolean real, boolean previsto)

                num+=1
                cont+=1
            except Exception as e:
                print(str(e))
                pass

        return result,nome_algoritmo

    def treinamento_csv(self,data,flood):
        cont = 0
        list_all = []
        list_flood = []
        count = 0
        num_train = int((len(data)*0.8))
        #import ipdb;ipdb.set_trace()
        num_test = num_train+1
        #import ipdb;ipdb.set_trace()
        for dt in data[:num_train]:
            try:
                json_data = dt.replace("'",'"')
                json_content = json.loads(json_data)

                json_dailly = json_content['history']['dailysummary']
                #import ipdb;ipdb.set_trace()
                list_temp = []
                # if json_dailly:
                #     try:
                if json_dailly != []:
                    try:
                        for key in json_dailly[0].keys():
                            #import ipdb;ipdb.set_trace()
                            #if key in ('maxtempm','mintempm','minhumidity','maxhumidity','maxpressurei','minpressurem','maxwspdi','precipi'):
                            #if key in ('mintempm','minhumidity','minpressurem','maxwspdi','precipi'):
                            if key in ('minpressurem', 'precipi'):
                                #print(key)
                                try:
                                    param = float(json_dailly[0][key])
                                except:
                                    param = 0
                                if param == '':
                                    param = 0
                                list_temp.append(param)
                        list_flood.append(float(flood[cont]))  
                        
                        cont+=1
                    except Exception as e:
                        print(e)
                        import ipdb;ipdb.set_trace()
                    #import ipdb;ipdb.set_trace()
                    list_all.append(list_temp)
                    #print(list_all)
            except:
                pass

        model = DecisionTreeClassifier()
        #model = KNeighborsClassifier()
        #model = svm.SVC()
        #model = GaussianNB()
        #model = LogisticRegression()

        nome_algoritmo = model.__class__.__name__

        model.fit(np.array(list_all), np.array(list_flood))
        #import ipdb;ipdb.set_trace()
        result = []
        
        num = 0

        result = []
        list_all = []
        list_flood = []
        
        json_data = ''
        json_dailly = ''
        json_content = ''
        param = ''
        list_temp = []
        acertos = 0
        erros = 0
        cont = 0
        cont_itens = num_test
        for dt in data[num_test:]:

            try:
                
                
                json_data = dt.replace("'",'"')
                json_content = json.loads(json_data)

                json_dailly = json_content['history']['dailysummary']
                #import ipdb;ipdb.set_trace()
                list_temp = []
                # if json_dailly:
                #     try:
                if json_dailly:
                    try:
                        for key_ in json_dailly[0].keys():
                            #import ipdb;ipdb.set_trace()
                            #if key_ in ('mintempm','minhumidity','minpressurem','maxwspdi','precipi'):
                            if key_ in ('minpressurem', 'precipi'):
                                try:
                                    param = float(json_dailly[0][key_])
                                except:
                                    param = 0
                                if key_ == '':
                                    param = 0
                                list_temp.append(param)
                                #print(list_temp)
                        
                    except Exception as e:
                        print(e)
                        #import ipdb;ipdb.set_trace()
                print(list_temp)
                if list_temp:
                    #import ipdb;ipdb.set_trace()
                    predicted = model.predict(np.array([list_temp]))
                    if predicted == flood[cont]:
                        acertos +=1
                    else:
                        #import ipdb;ipdb.set_trace()
                        erros +=1

                    result.append([cont_itens,flood[cont],predicted[0]]) # .append(nº da linha .csv, boolean real, boolean previsto)
                #import ipdb;ipdb.set_trace()
                num+=1
                cont+=1
                cont_itens+=1
            except Exception as e:
                print(str(e))
                pass

        return result,nome_algoritmo,acertos,erros
  

    def calcular_ajustes_curva_csv(self):
        #for _,_,arquivo in os.walk('/home/lucas-desenv/workspace-machine/machine-learning/data_bases/America/'):
        for _,_,arquivo in os.walk('/home/lucas/workspace-ml/machine-learning/data_bases/America/'):
            list_param = ['mintempm','minhumidity','minpressurem','maxwspdi','precipi']
            list_combinado = list(product(list_param,repeat=2))
            for name_arquivo in arquivo:
                #import ipdb;ipdb.set_trace()
                content_data = ''
                try:
                    content_data,flood = self.get_data('data_bases/America/'+str(name_arquivo))
                except Exception as e:
                    print(str(e))
                    print(name_arquivo) 
                #import ipdb;ipdb.set_trace()      
                lista_final = []
                nome_arquivo_resultado = str('ajuste_curva/'+name_arquivo.replace(".csv","")+'_ajuste_curva.csv')
                with open(nome_arquivo_resultado, 'w') as csvfile:
                    fieldnames = ['variaveis', 'desvio','coeficiente','variancia']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()    
                    for dupla in list_combinado:
                        print(dupla)
                        resultado = self.calculando_ajuste_curva(dupla,content_data)
                        writer.writerow({'variaveis': resultado[0],'desvio': resultado[1],'coeficiente': resultado[2],'variancia': resultado[3]})
  
mac_lg = MachineLearning()
# mac_lg.calcular_ajustes_curva_csv()
lista_parametros,flood = mac_lg.get_data('data_bases/America/Chicago.csv')         
resultado, nome_algoritmo,acertos,erros = mac_lg.treinamento_csv(lista_parametros,flood)           
print('===============================')
#import ipdb;ipdb.set_trace()
lista_previsao = []
lista_real = []
for res in resultado:
    #import ipdb;ipdb.set_trace()
    tamanho_lista = len(lista_previsao)-1
    #print(tamanho_lista)
    if tamanho_lista>0:
        if (res[2] != lista_previsao[tamanho_lista]):
            lista_previsao.append(int(res[2]))
            lista_real.append(int(res[1])) 
        else:
            pass
    else:
        lista_previsao.append(int(res[2]))
        lista_real.append(int(res[1]))


x = np.arange(0, len(lista_real))

y = np.array(lista_real)
y2 = np.array(lista_previsao)


xlim(0, len(lista_real))
#ylim(-0.5, 1.5)
step(x, y)

show()

step(x, y2)
show()


# plt.ylabel('Pétala Width')
# plt.xlabel('Pétala Length')
# plt.legend(bbox_to_anchor=(1, 0.18), loc=1, borderaxespad=0.)



print("ACERTOS: "+str(acertos))
print("ERROS: "+str(erros))





# ACERTOS: 2671
# ERROS: 1805















# result = svm_model_main(X_treinamento,Y_treinamento,X_teste,Y_teste)
# import ipdb;ipdb.set_trace()


# result,nome_algoritmo = treinamento()

# list_default = []
# list_grafico = []

# list_final = []
# soma = 1
# for numeros in result:
#     # if numeros[2] == 1.0 and numeros[1] == 1:
#     #     print ('+++++++++++',numeros)
#     # if numeros[2] == 0.0 and numeros[1] == 0:
#     #     print ('==========',numeros)
#     list_grafico.append(numeros[2])
#     list_default.append(soma)
#     soma+=5
    
#     if numeros[1] == numeros[2]:
#         list_final.append(numeros)


#fim = time.time()

# print (nome_algoritmo)
# print ("Quantidade de itens iniciais",len(result))
# print ("Quantidade de itens que coincidiram",len(list_final))
# print ("Tempo de execução: ", fim-inicio, "segundos")




########## TESTE DA CLASSE CALCULOS ###################




# list_x = [0.3,2.7,4.5,5.9,7.8]
# list_y = [1.8,1.9,3.1,3.9,3.3]
# # list_x = [1.2,2.5,3.0,4.1,6.2,7.1,8.8,9.5]
# # list_y = [6.8,6.1,9.9,9.7,12.1,17.9,18.0,21.5]
# b0,b1,sum_y_square, sum_y = AjusteCurva.modelo_mmq(list_x,list_y)

# desvio = AjusteCurva.desvio(b0,b1,list_x,list_y)

# coeficiente = AjusteCurva.coeficiente_determinacao(desvio,sum_y_square,sum_y,len(list_x))

# variancia = AjusteCurva.variancia_residual(desvio,len(list_x))

# print(variancia)
