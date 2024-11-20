
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np




ruta_base="Nombre_estudiante Tensión PLA  XX-XX-2024_"

Esfuerzo_key= "Esfuerzo de tracción"
Deformacion_key= "Deformación por tracción (Deformación 1)"

error_zona_lineal=1



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


def cargar_conjunto():
    dataset=[]
    for i in range(1,6):
        data=importar_archivo(ruta_base+str(i)+"_1.csv")
        dataset.append(data)
    return dataset

def graficar_conjunto(dataset,lineal=False):
    global Esfuerzo_key
    global Deformacion_key 
    
    plt.figure()
    for i in range(0,5):
        plt.plot(dataset[i][Deformacion_key],dataset[i][Esfuerzo_key],label=str(i+1))
        
    if lineal:
        plt.title("Curva $\sigma$ vs $\epsilon$ (Zona lineal)")
    else:   
        plt.title("Curva $\sigma$ vs $\epsilon$ ")
        
    plt.legend()
    plt.xlabel("Deformación [%]")
    plt.ylabel("Esfuerzo [MPa]")
    plt.grid()
    plt.show()
    
def esfuerzo_maximo(dataset):
    F=[]
    for i in range(0,5):
        F.append(max(dataset[i][Esfuerzo_key]))
    return np.array(F)


def Zona_lineal(dataset, error):
    global Esfuerzo_key
    global Deformacion_key  
    E=[]
    errores=[]
    for i in range(0,5):
        err=100
        p=1
        while err>error and p>0.2:
            dataset[i]=dataset[i][0:int(p*len(dataset[i]))]
            Esfuerzo=dataset[i][Esfuerzo_key]
            Deformacion=dataset[i][Deformacion_key]/100
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
    return np.array(E),np.array(errores)
        
    


dataset=cargar_conjunto()
graficar_conjunto(dataset)
max_stress=esfuerzo_maximo(dataset)
E,error=Zona_lineal(dataset,error_zona_lineal)
graficar_conjunto(dataset, lineal=True)    

print("El esfuerzo máximo promedio de las probetas es: "+ str(round(np.mean(max_stress),2))+" MPa")
print("El Módulo de elasticidad promedio de las probetas es: "+ str(round(np.mean(E),2))+" MPa")



        

    


 