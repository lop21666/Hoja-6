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

#Definicion de la funcion proceso, que es la que maneja casi en totalidad la 
def proceso(nombre, env, memoria, cpu, llegada, cantidad_instrucciones, cantidad_ram):

    # Simula la espera de llegada del proceso
    yield env.timeout(llegada)

    #grabo el tiempo de llegada
    tiempo_llegada = env.now

    print('%s proceso en cola [NEW llegada] -> %d cantidad ram requerida %d, disponible %d' % (nombre, env.now, cantidad_ram, memoria.level))
    yield memoria.get(cantidad_ram)  #Pide la memoria que necesita o espera automaticamente hasta que haya suficiente

    while cantidad_instrucciones > 0:  #repite hasta que se acabe la cantidad de instrucciones pendientes
        # Ya tiene memoria para iniciar
        print('%s proceso en cola READY tiempo -> %d cantidad instrucciones pendientes %d' % (nombre, env.now, cantidad_instrucciones))

        with cpu.request() as req:  #pide el procesador
            yield req

            cantidad_instrucciones = cantidad_instrucciones - 3
            yield env.timeout(1) #Simula un ciclo de reloj del procesador

            # Ya tiene procesador
            print('%s proceso en estado RUNNING fue atendido en tiempo -> %d cantidad ram %d, Instrucciones pendientes %d ram disponible %d' % (nombre, env.now, cantidad_ram, cantidad_instrucciones, memoria.level))

    # Cuando ya finaliza devuelve la memoria utilizada
    yield memoria.put(cantidad_ram)

    print('%s proceso TERMINATED salida -> %d cantidad ram devuelta %d, nueva cantidad de memoria disponible %d' % (nombre, env.now, cantidad_ram, memoria.level))
    global tiempo_total
    tiempo_total += env.now - tiempo_llegada
    print('Tiempo total %d' % (env.now - tiempo_llegada))


random.seed(10)
env = simpy.Environment()  # crear ambiente de simulacion
initial_ram = simpy.Container(env, 30, init=30)  # crea el container de la ram
initial_cpu = simpy.Resource(env, capacity=10)  # se crea el procesador con capacidad establecida
initial_procesos = 25  # cantidad de procesos a generar
tiempo_total = 0

for i in range(initial_procesos):
    llegada = 0 #Todos los procesos llegan al mismo tiempo
    cantidad_instrucciones = random.randint(1, 10)  # cantidad de operaciones por proceso
    UsoRam = random.randint(1, 10)  # cantidad de ram que requiere cada proceso
    env.process(proceso('proceso %d' % i, env, initial_ram, initial_cpu, llegada, cantidad_instrucciones, UsoRam))

# correr la simulacion
env.run()
print('tiempo promedio %d ' % (tiempo_total / initial_procesos))