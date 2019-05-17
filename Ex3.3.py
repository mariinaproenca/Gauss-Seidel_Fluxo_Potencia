from numpy import *
 
#Setar o numero de iterações Desejadas
n_iteracoes = 50
#Setar a tolerancia
tolerancia = 0.000001

# Valores Dados:
V_1 = 0.8 + 0j
V_2 = 1.1
PG_2 = 3
PL_3 = -4.5
QL_3 = -0.5j

#Numero de barras
n = 3

y = zeros((n,n),complex)
Y_barra = zeros((n,n),complex)

#Admitancias entre as linhas, onde 0 = Barra 1 // 1 = Barra 2 // 2 = Barra 3
y[0,1] = -10j
y[1,2] = -5j
y[0,2] = -10j

#criando a matriz com as admitancias entre as barras
for i in range(n):
    for j in range(n):
        y[j,i] = y[i,j]

for i in range(n):
    x = 0
    for j in range(n):
        x += y[i,j]
        Y_barra[i,j] = -y[i,j]
    Y_barra[i,i] = x

print("Matriz Admitância: \n {0} \n".format(Y_barra))

#Condição inicial:[ V1 ] [  V2  ] [ V3 ]  
V_inicial = array([ V_1, V_2 + 0j ,V_1])

x = 0
#Inicializando o calculo da potencia reativa na barra 2 (Q2)
for i in range(n):
    x += Y_barra[1,i] * V_inicial[i]
Q2_calc = -1 *  V_inicial[1] * x

print("Q2 calculado: {0:8.2f} \n".format(imag(Q2_calc)))

#Criação de uma Matriz de dimensoes (numero de iteracoes,numero de tensoes) para armazenar todos os valores calculados
V_calc = zeros((n_iteracoes,2),complex)

#Coluna 1 ficarão os valores de V2 e coluna 2 os de V3
V_calc[0,0] = V_inicial[1] #linha 1 da matriz conterá as condicão inicial de V2
V_calc[0,1] = V_inicial[2] #linha 3 conterá a condição inicial de V3

#criação de arrays para armazenar os angulos de v3 e v3 (a função'rad2degree' requer um array)
p_v2 = zeros((1,1),float) 
p_v3 = zeros((1,1),float)

angulos = zeros((n_iteracoes,2),float)#criacao de uma matriz para armazenar somente os angulos de V2 e V3. Possui a mesma dimensão de V_calc

Erro = zeros((1,2),float) #matriz com dimensao (1,2) para armazenar os erros entre V2(i+1) - V2(i) e V3(i+1) - V3(i)

teste_convergencia = 0 #inicializa a variavel que armazenará o maior erro armazenado na matriz de erros
for i in range(n_iteracoes - 1):   
        #calculo de V2(i+1)
        V_calc[i + 1, 0] = (1/Y_barra[1,1]) * (((PG_2 - Q2_calc) / conj(V_calc[i,0])) - Y_barra[1,0] * V_inicial[0] - Y_barra[1,2] * V_calc[i,1] )
        #calculo de V3(i+1)
        V_calc[i+ 1, 1] =  (1/Y_barra[2,2]) * (((PL_3 - QL_3) / conj(V_calc[i,1])) - Y_barra[2,0] * V_inicial[0] - Y_barra[2,1] * V_calc[i + 1, 0])

        rad2deg(angle( V_calc[i + 1, 0]),p_v2)
        rad2deg(angle( V_calc[i + 1, 1]),p_v3)
        #armazena os angulos na matriz 'angulos'
        angulos[i+1,0] = p_v2       
        angulos[i+1,1] = p_v3

        #encontra o erro entre os angulos de V2 e armazena na matriz Erro
        teste2 = angulos[i+1,0] - angulos[i,0]
        teste3 = angulos[i+1,1] - angulos[i,1]
        Erro[0,0] = teste2
        Erro[0,1] = teste3

        #armazena na variavel o maior valor de erro encontrado na matriz Erro
        teste_convergencia = amax(Erro)

        #o programa para se o iterador for igual ao numero de iterações OU se o maior erro for MENOR que a tolerancia
        if i == n_iteracoes or teste_convergencia < tolerancia :                
                print("V2:{0}|{1:1.2f} V3:{2:1.2f}|{3:1.2f} iteracoes: {4} Convergencia: {5}".format(V_2,angulos[i+1,0], abs(V_calc[i + 1, 1]), angulos[i+1,1], i + 1 ,teste_convergencia))
                break
        
