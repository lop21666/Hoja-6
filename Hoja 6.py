#Universidad del Valle de Guatemala
#Algoritmos y estructuras de datos

#Hoja seis.py
#Fecha de creación: 11/03/2022
#Última modificación: 11/03/2022

#Programa para la simulación  de  corrida  de  programas  en  un  sistema  operativo  de  tiempo  compartido
#(el  procesador  se  comparte  por  una porción de tiempo entre cada programa que se desea correr), se llama
#“proceso” a un programa que se ejecuta. 


#Se importan los módulos necesarios para el correcto funcionamiento de la aplicación
#Simpy es un despachador de eventos que se basa en los generadores de Python y también puede utilizarse para redes asincrónicas o para implementar sistemas multiagente.
import simpy
#Nos permite generar cualquier cantidad de numeros aleatorios entre un rango especificado
import random
#Nos permitirá el calculo de la desciacion estandar
import statistics

#Definicion de la funcion proceso, que es la que maneja casi en totalidad la simulacion requerida
def proceso(nombre, env, memoria, cpu, llegada, cantidad_instrucciones, cantidad_ram):
    
    #Tiempos para la desciacion estandar
    global tiempos
    tiempos = []

    # Llega un nuevo proceso a la ram
    yield env.timeout(llegada)

    #Variable que guarda el tiempo de llegada
    tiempo_llegada = env.now

    #Imprime un mensaje en el que se indica que un nuevo proceso se a añadido a la cola
    print('%s Nuevo proceso: %d Ram reuqerida = %d, Ram disponible = %d' % (nombre, env.now, cantidad_ram, memoria.level))
    
    #Solicita la cantidad de memoria necesaria para poder llevar el proceso a cabo, sino hay suficiente se queda en la cola
    yield memoria.get(cantidad_ram)

    #Ciclo que se repite las veces necesarios para terminar todos los procesos
    while cantidad_instrucciones > 0:
        
        #Cuando detecta que ya hay suficiente memoria para continuar los procesos se ejecuta
        print('%s Proceso en cola, tiempo = %d instrucciones por ejecutar = %d' % (nombre, env.now, cantidad_instrucciones))

        #Solicitud del CPU
        with cpu.request() as req:
            yield req

            #Simulacion del control de procesos del reloj del procesador
            cantidad_instrucciones = cantidad_instrucciones - 3
            yield env.timeout(1)

            # Ya tiene procesador
            print('%s Proceso ejecutandose en = %d Ram usandose = %d, Instrucciones por ejecutar = %d Ram sin uso = %d' % (nombre, env.now, cantidad_ram, cantidad_instrucciones, memoria.level))

    # Cuando ya finaliza devuelve la memoria utilizada
    yield memoria.put(cantidad_ram)

    #Se ejecuta cuando un proceso es terminado y una cantidad de ram es devuelta
    print('%s PROCESO EJECUTADO %d , Ram que deja sin uso = %d, Cantidad de memoria total sin uso = %d' % (nombre, env.now, cantidad_ram, memoria.level))
    global tiempo_total
    tiempos.append(env.now - tiempo_llegada)
    tiempo_total += env.now - tiempo_llegada
    print('Tiempo total = %d' % (env.now - tiempo_llegada))


random.seed(10)

# Se crea la simulación
env = simpy.Environment()

# Se crea la ram
initial_ram = simpy.Container(env, 30, init=30)

# se crea el procesador con capacidad establecida
initial_cpu = simpy.Resource(env, capacity=10)

#Numero de procesos a ejecutar
initial_procesos = 25

#Tiempo total igual a 0
tiempo_total = 0

for i in range(initial_procesos):
    #Todos los procesos llegan al mismo tiempo
    llegada = 0
    # cantidad de operaciones por proceso
    cantidad_instrucciones = random.randint(1, 10)
     # cantidad de ram que requiere cada proceso
    UsoRam = random.randint(1, 10)
    env.process(proceso('Proceso numero = %d |' % i, env, initial_ram, initial_cpu, llegada, cantidad_instrucciones, UsoRam))

# correr la simulacion
env.run()
print('tiempo promedio = %d ' % (tiempo_total / initial_procesos))

#Desviacion estandar
st_dev = statistics.pstdev(tiempos)
print("Desviacion estandar = " + str(st_dev))




