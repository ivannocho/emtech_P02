#imprtación de la librería CSV
import csv

#Lista donde se guardarán los datos leídos del archivo CSV
lista_base_datos = [] 

#Abrimos el archivo CSV
with open("synergy_logistics_database.csv", "r") as archivo_csv:
    #Lee cada registro del archivo CSV
    registro_csv = csv.DictReader(archivo_csv)
    #Captura cada registro en lista_base_datos
    for registro_lista in registro_csv:
        lista_base_datos.append(registro_lista)


#Caso 1 Rutas más demandadas

#Función que suma las rutas de acuerdo a su
#tipo (Importación/Exportación)

def rutas_export_import(tipo):
    num_ruta = 0 #cuenta el número de veces que aparece la ruta en la base
    rutas_contadas = []
    rutas_conteo = []
    
    for ruta in lista_base_datos: #ciclo para contar las rutas
        if ruta["direction"] == tipo: #si es importación/exportación
            ruta_actual = [ruta["origin"], ruta["destination"]] 
            
            if ruta_actual not in rutas_contadas:
                for ruta_bd in lista_base_datos:
                    if ruta_actual == [ruta_bd["origin"], ruta_bd["destination"]] and ruta_bd["direction"] == tipo:
                        num_ruta+=1
                
                rutas_contadas.append(ruta_actual)
                rutas_conteo.append([ruta["origin"], ruta["destination"], num_ruta])
                num_ruta = 0
        
    rutas_conteo.sort(reverse = True, key = lambda x:x[2])
    return rutas_conteo

#Caso 2 Medio de transporte utilizado

def medio_transporte(tipo):
    suma_valor_tipo_transporte = 0
    transporte_contado = []
    transporte_conte = []
    
    for transporte in lista_base_datos: #realizar el recorrido de todos los registros de la base
        if transporte["direction"] == tipo: #si el tipo Imports/Exports coincide
            transporte_actual = [transporte["transport_mode"]] #guarda el medio de transporte que se va a sumar actualmente
            
            if transporte_actual not in transporte_contado: #si el tipo de transporte no ha sido calculado
                for modo_transporte in lista_base_datos: #realizar el recorrido de toda la base
                    #Si el sentido de la transacción y el modo de transporte coinciden
                    if transporte_actual == [modo_transporte["transport_mode"]] and modo_transporte["direction"] == tipo:
                        #acumula la suma por sentido de transacciín y modo de transporte
                        suma_valor_tipo_transporte += int(modo_transporte["total_value"])
                
                transporte_contado.append(transporte_actual)
                transporte_conte.append([transporte["transport_mode"], suma_valor_tipo_transporte])
                suma_valor_tipo_transporte = 0
    
    transporte_conte.sort(reverse = True, key = lambda x:x[1])
    return transporte_conte

#Caso 3 Valor total de importaciones y exportaciones

def valor_total(tipo):
    pais_contado = [] #lista que lleva el registro de paises calculados
    valor_paises = [] #lista resultante que regresa la función
    
    for pais_origen in lista_base_datos: #ciclo principal que recorre la base
        pais_actual = [tipo, pais_origen["origin"]] #país actual en el conteo
        valor_total = 0 #valor total de operación
        operaciones = 0 #número de operaciones de ese país
        
        if pais_actual in pais_contado: #si el país calculado está en la lista de contados
            continue
        
        for tipo_movimiento in lista_base_datos: #ciclo para sumar de acuerdo al tipo de movimiento
            if pais_actual == [tipo_movimiento["direction"], tipo_movimiento["origin"]]:
                valor_total += int(tipo_movimiento["total_value"])
                operaciones +=1
                
        pais_contado.append(pais_actual) #actualizar la lista de paises contabilizados
        #agrega el país calculado a la lista de paises
        valor_paises.append([tipo, pais_origen["origin"], valor_total, operaciones]) 
    #ordena los paises calculados de mayor a menor    
    valor_paises.sort(reverse = True, key = lambda x:x[2])
    return valor_paises

def porcentaje_x_pais(lista_paises, porcentaje = 0.8):
    valor_total = 0 #variable para calcular el total
    
    for pais in lista_paises: #itera la lista para calcular el valir total de operaciones de la base
        valor_total += pais[2]
        
    paises = [] #lista de paises
    porcentajes_calculados = [] #lista para guardar porcentajes calculados
    valor_actual = 0 
    
    for pais in lista_paises: #ciclo para calcular el porcentaje de cada país
        valor_actual += pais[2]
        porcentaje_actual = round(valor_actual / valor_total, 3)
        
        paises.append(pais)
        porcentajes_calculados.append(porcentaje_actual)
        
        #condiciones para delimitar la lista de paises que acumulan el 80% del total de operaciones
        if porcentaje_actual <= porcentaje:
            continue
        else:
            if porcentaje_actual - porcentaje <= porcentajes_calculados[-2] - porcentaje:
                break
            else:
                paises.pop(-1)
                porcentajes_calculados.pop(-1)
                break
    return paises

def imprimir_lista(lista, mensaje): #función para imprimir listas
    print("\n")
    print(mensaje)
    for i in range(len(lista)):
        print(lista[i])

#Imprimir Caso 1
imprimir_lista(rutas_export_import("Exports"),"Rutas de Exportación")

imprimir_lista(rutas_export_import("Imports"),"Rutas de Importación")

#Imprimir Caso 2
imprimir_lista(medio_transporte("Exports"),"Medio de transporte utilizado en Exportaciones")

imprimir_lista(medio_transporte("Imports"),"Medio de transporte utilizado en Importaciones")

#Imprimir Caso 3
imprimir_lista(porcentaje_x_pais(valor_total("Exports")),"Paises que conforman el 80% de las operaciones")

imprimir_lista(porcentaje_x_pais(valor_total("Imports")),"Paises que conforman el 80% de las operaciones")
