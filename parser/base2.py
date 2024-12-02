import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


Esfuerzo_key= "Esfuerzo de tracción"
Deformacion_key= "Deformación por tracción (Deformación 1)"

error_zona_lineal=1

ruta=r"C:\Users\juanp\OneDrive\Escritorio\Trabajos\Impresion 3D\Caracterizacion"

""" Retorna un diccionario de listas de dataframes con los datos de los ensayos e bruto"""


def importar_archivo(ruta):
    global Esfuerzo_key
    global Deformacion_key
    
    convert_dict = {Esfuerzo_key: float,
                    Deformacion_key: float
                    }
    
    data=pd.read_csv(ruta,delimiter=";",encoding="cp1252",decimal=',')
    data.drop(0, inplace=True)
    data.drop(columns=data.columns[0:4], inplace=True)
    data[Esfuerzo_key] = [x.replace(',', '.') for x in data[Esfuerzo_key]]
    data[Deformacion_key] = [x.replace(',', '.') for x in data[Deformacion_key]]
    data=data.astype(convert_dict)
    return data



def eliminar_vacios(dataset):
    Dataset_limpio={}
    for probeta in dataset.keys():
        if len(dataset[probeta])>0:
            Dataset_limpio[probeta]=dataset[probeta]
    return Dataset_limpio

def cargar_conjunto():  
    Datos={}
    for probeta in os.listdir(ruta+"\Datos"):
        lista_ensayos=[]
        for ensayo in os.listdir(ruta+"\Datos/"+probeta):
            datos=importar_archivo(ruta+"\Datos/"+probeta+"/"+ensayo)
            lista_ensayos.append(datos)
        Datos[probeta]=lista_ensayos
    Datos=eliminar_vacios(Datos)
    return Datos

def graficar_conjunto(dataset,lista):
    
    global Esfuerzo_key
    global Deformacion_key 
    
    fig=plt.figure()
    for probeta in lista:
        dat=1
        
        if len(lista)==1:
            dat=len(dataset[probeta])
           
                
        for i in range(0,dat):
            plt.plot(dataset[probeta][i][Deformacion_key],dataset[probeta][i][Esfuerzo_key],label=probeta)
                
        plt.title(probeta)
    


    if len(lista)!=1:
        plt.title("Curvas $\sigma$ vs $\epsilon$ (raw)")
        plt.legend()
            
    plt.xlabel("Deformación [%]")
    plt.ylabel("Esfuerzo [MPa]")
    plt.grid()
    
    
    return fig
        
        
def esfuerzo_maximo(ensayos):
    
    global Esfuerzo_key
    
    F=[]
    for i in range(0,len(ensayos)):
        F.append(max(ensayos[i][Esfuerzo_key]))
    return np.mean(F),np.std(F)

def Zona_lineal(ensayos_or, error):
    global Esfuerzo_key
    global Deformacion_key  
    E=[]
    errores=[]
    ensayos=ensayos_or.copy()
    for i in range(0,len(ensayos)):
        err=100
        p=1
        while err>error and p>0.2:
            ensayos[i]=ensayos[i][0:int(p*len(ensayos[i]))]
            Esfuerzo=ensayos[i][Esfuerzo_key]
            Deformacion=ensayos[i][Deformacion_key]/100
            sumx=sum(Deformacion)
            sumx2=sum(Deformacion**2)
            sumy=sum(Esfuerzo)
            sumxy=sum(Esfuerzo*Deformacion)
            Matriz_reg=np.array([[len(Deformacion), sumx],[sumx, sumx2]])
            vec=np.array([[sumy],[sumxy]])
            res=np.linalg.solve(Matriz_reg,vec)
            err=(1/len(Deformacion))*sum((Esfuerzo-res[0]-res[1]*Deformacion)**2)
            p-=0.0001
        E.append(res[1])
        errores.append(err)
    return np.mean(E),np.std(E),ensayos

def propiedades(dataset):
    
    global error_lin
    
    diccioE={}
    diccioF={}
    for probeta in dataset.keys():
        E,stdE,_=Zona_lineal(dataset[probeta],error_zona_lineal)
        F,stdF=esfuerzo_maximo(dataset[probeta])
        
        diccioE[probeta]={"E (GPa)":round(E/1000,2),"std":round(stdE/1000,2)}
        diccioF[probeta]={"F (MPa)":round(F,2),"std":round(stdF,2)}
        
    return diccioE, diccioF

def sel_propiedades(dicci,options):
    dicciE={}
    dicciF={}
    for probeta in options:
        dicciE[probeta]=dicci[0][probeta]
        dicciF[probeta]=dicci[1][probeta]
    return pd.DataFrame(dicciE),pd.DataFrame(dicciF)


""" Falta analisis en t"""