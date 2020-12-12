import random
from colorama import init, Fore, Back, Style
from time import sleep

ENTRADA = 0
SALIDA = 5
CAMINO = 6
PASILLOS = 0
CALLEJON = 7
COLOR_ENTRADA = Fore.WHITE+Style.BRIGHT
COLOR_PARED = Fore.CYAN+Style.BRIGHT
COLOR_SALIDA = Fore.RED+Style.BRIGHT
COLOR_CAMINO = Fore.GREEN+Style.BRIGHT
COLOR_CALLEJON = Fore.BLUE+Style.BRIGHT

def CreateSpaceMatrice(tam_ren, tam_col):
    matriz = []
    for i in range(tam_ren):
        matriz.append([0] * tam_col)
    return matriz

def generaAleatorio(num):
    valor = random.randint(0, num)
    if valor == 0:      
        return 0
    else:
        return 1
    
def crear_matriz_alea(f,c):
    matriz = CreateSpaceMatrice(f, c)
    for i in range(f):
        for j in range(c):
            matriz[i][j] = generaAleatorio(1)
            matriz[i][j] = generaAleatorio(1)
    matriz = marco(matriz,1)
    return matriz

def marco(matriz,num):
    for i in range(0,len(matriz)):
        matriz[i][0] = num
        matriz[0][i] = num
        matriz[i][len(matriz)-1] = num
        matriz[len(matriz)-1][i] = num
    return matriz 

def obtener_ceros_lado_izq(matriz):
    posBarraIzquierda = []
    columna = 1
    for fila in range(len(matriz)):
        #print(matriz[fila][columna])    
        if(matriz[fila][columna] == 0):
            pos = [fila,columna]
            #print("cero en pos ",pos)    
            posBarraIzquierda.append(pos)   
    return posBarraIzquierda

def obtener_ceros_lado_der(matriz):
    posBarraDerecha = []
    columna = len(matriz[0])-2
    for fila in range(len(matriz)):
        if(matriz[fila][columna] == 0):
            pos = [fila,columna]
            posBarraDerecha.append(pos)   
    return posBarraDerecha

def validaSolucionSalida(fila_salida,columna_salida,camino,callejon):    
    if matriz[fila_salida][columna_salida] == camino:
        print(COLOR_CAMINO+"si hay solucion de este laberinto"+Fore.WHITE)
        return 0
    else:
        matriz[fila_salida][columna_salida] = callejon
        print(COLOR_CALLEJON+"no hay solucion de este laberinto (7)"+Fore.WHITE)
        return 1

def buscarSolucion(fila,columna,encontrado,tamFila,tamColum,salida,camino,pasillo):
    #---COMPARACIONES PARA DETERMINAR QUE NO SE SALGA DE LAS FILAS Y COLUMNAS---
    if fila<tamFila and columna<tamColum and encontrado == False:
        if matriz[fila][columna] == salida:
            #print(f"Hay salida en pos [{fila},{columna}]")    
            matriz[fila][columna]=camino
            encontrado=True
            buscarSolucion(fila,columna,encontrado,tamFila,tamColum,salida,camino,pasillo)
        #---SI ENCUENTRA 0 SE MUEVE---            
        if matriz[fila][columna] == pasillo:
            #print(f"Hay cero en pos [{fila},{columna}]")
            matriz[fila][columna]=camino
            buscarSolucion(fila+1,columna,encontrado,tamFila,tamColum,salida,camino,pasillo) 
            buscarSolucion(fila-1,columna,encontrado,tamFila,tamColum,salida,camino,pasillo)
            buscarSolucion(fila,columna+1,encontrado,tamFila,tamColum,salida,camino,pasillo)
            buscarSolucion(fila,columna-1,encontrado,tamFila,tamColum,salida,camino,pasillo)
    
def borra_Camino(matriz,camino,pasillo,callejon): 
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if matriz[i][j] == camino or matriz[i][j] == callejon:
                matriz[i][j] = pasillo

def empieza_busqueda(PosDer,PosIzq,entrada,salida,matriz,camino,pasillo,callejon):
    #---inicializo variables---
    lista_Solucion = []
    fila_inicial = 0
    columna_inicial = 0
    fila_salida = 0
    columna_salida = 0
    ENCONTRADO = False  
    tam_fila = len(matriz)
    tam_columna = len(matriz[0])

    izq = 0
    while True:
        ENCONTRADO = False
        for pd in range(0,len(PosDer)): 
            fila_inicial = PosIzq[izq][0]
            columna_inicial = PosIzq[izq][1]
            fila_salida = PosDer[pd][0]
            columna_salida = PosDer[pd][1]
            print(f'ENTRADA={COLOR_CAMINO}[{fila_inicial}][{columna_inicial}]{Fore.WHITE} y SALIDA={COLOR_SALIDA}[{fila_salida}][{columna_salida}]{Fore.WHITE}')
            #--- ASIGNA VALORES ----
            matriz[fila_inicial][columna_inicial] = entrada
            matriz[fila_salida][columna_salida] = salida
            #--- BUSCA SOLUCION ---
            buscarSolucion(fila_inicial,columna_inicial,ENCONTRADO,tam_fila,tam_columna,salida,camino,pasillo)        
            print("REPRESENTACION :")
            solucion = validaSolucionSalida(fila_salida,columna_salida,camino,callejon)
            #--- GUARDA SOLUCIONES ---
            if solucion == 0:
                lista_Solucion.append(solucion)
            #--- MUESTRA SOLUCION ---
            mostrar(matriz , "solucion")
            #--- BORRA EL CAMINO DE CADA RECORRIDO ---
            borra_Camino(matriz,camino,pasillo,callejon)
            print("")
            #sleep(1)
        izq = izq + 1  
        if(izq >= len(PosIzq) ):  
            break
           
    return lista_Solucion

def mostrar(matriz,mensaje):
    tam_fila = len(matriz)
    tam_columna = len(matriz[0])
    nueva_matriz = CreateSpaceMatrice(tam_fila, tam_columna)
    for i in range(0,tam_fila):
        for j in range(0,tam_columna):
            #--- entrada ---
            if matriz[i][j] == 0:
                nueva_matriz[i][j] = COLOR_ENTRADA+str(matriz[i][j])
            #--- pared ---
            if matriz[i][j] == 1:
                nueva_matriz[i][j] = COLOR_PARED+str(matriz[i][j])
            #--- camino ---
            if matriz[i][j] == 6:
                nueva_matriz[i][j] = COLOR_CAMINO+str(matriz[i][j])
            #--- salida ---
            if matriz[i][j] == 5:
                nueva_matriz[i][j] = COLOR_SALIDA+str(matriz[i][j])
            #--- callejon ---
            if matriz[i][j] == 7:
                nueva_matriz[i][j] = COLOR_CALLEJON+str(matriz[i][j])
    print("\n",Fore.MAGENTA,Style.BRIGHT,"-> MATRIZ",tam_fila,"X",tam_columna,"-->",mensaje,Fore.WHITE)
    for i in range(0,len(nueva_matriz)):
        for j in range(0,len(nueva_matriz[0])):
            print('['+nueva_matriz[i][j]+"]",end="")
        print("")
    print(Fore.WHITE)
    
matriz = crear_matriz_alea(10,10)
"""matriz = [
    [1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,1,0,1,1,0,1], 
    [0,0,1,1,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1], 
    [0,1,1,1,0,1,1,1,1,1,1],
    [1,1,1,0,0,1,0,0,0,0,0],
    [1,0,1,1,1,0,1,1,1,1,1],
    [1,0,0,0,1,1,1,1,0,0,0], 
    [1,1,1,1,1,1,1,1,1,1,1] 
]"""
mostrar(matriz, "GENERADA")
PosIzq = obtener_ceros_lado_izq(matriz)
PosDer = obtener_ceros_lado_der(matriz)
print("Entrada Izquierda = ",PosIzq)
print("Entrada Derecha = ",PosDer)
print("sus combinaciones son :",(len(PosDer)*len(PosIzq)),"\n")
contador_Solucion = empieza_busqueda(PosDer,PosIzq,ENTRADA,SALIDA,matriz,CAMINO,PASILLOS,CALLEJON)
print("las soluciones correctas son : ",len(contador_Solucion))