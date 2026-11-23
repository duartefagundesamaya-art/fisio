# importa a biblioteca do openCV do python 
import cv2
#  importa uma biblioteca para usar vetores e matrizes
import numpy as np
# importa a função que está contida em "detectarCOR.py"
import math
# essa linha importa a biblioteca 'math' que será utilizada para fazer os calculos

from detectaCOR import segmentar_amarelo
# from calculo import calculo_angulo
# essas duas linhas importam (pegam) os resultados obtidos a partir das duas funções (detecta e calculo)

from calculo import calculo_angulo

# carrega a imagem na variável "imagem"
imagem = cv2.imread("./img/imagem.jpeg")


# apenas uma verificação para ver se a imagem foi carregada, para não dar erro na compilação do código 
if imagem is None:
    print("Erro: não foi possível carregar a imagem.")
   

else:
    # salva o resultado que vem do detctarCOR.py na variável mascara
    mascara = segmentar_amarelo(imagem)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    #(cv2.getStructuringElement)esse comando cria a matriz auxiliar
    #esse é o que da o formato que será usado de modelo para corrigir máscara (9,9)esse é o tamanho da matriz
    # Essa linha cria uma matriz de referência em formato elíptico
    # (um formato parecido com um oval).
    # Essa matriz será utilizada pelas operações morfológicas
    # para ajudar a corrigir pequenas falhas na máscara,
    # como buracos pretos dentro das regiões brancas.


    mascara = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel, iterations=3)
    #essa linha vai ampliar o pontos pretos falhados e depois utilizar okernel para corrigi-los

    mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel, iterations=1)
    #essa linha tenta remover pequenos ruidos brancos da máscara, ele tenta fechar todos os ruidos
    # iterations=1 isso é quantas vezes ele vai fazer esse processo

    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #essa linha é utilizada para extrair os pixels que formam a borda da circunferencia

    resultado = imagem.copy()
    #essa linha só serve para fazer uma cópia da imagem original na variável resultado

    lista = []
    for c in contornos:
    #essa linha é utilizada para analisar circulo por circulo
        print('opa')
        area = cv2.contourArea(c)
        #esse calcula a area de cada esfera.
        if area < 20:  # ignora ruídos pequenos
            print('area menor')
            continue
        # essas duas linhas trabalham juntas,funciona basicamente assim:
        # se a area for menor que 20 pixel² ele ignora e o 'continue' é basicamente para ele ignorar esse contorno e continuar a analise;o break 

        # Verifica se o formato é aproximadamente circular
        perimetro = cv2.arcLength(c, True)
        # essalinha serve para ver se os contornos identificados são circulos fechados, o 'c' é o contorno que está sendo analisado nomomento e o 'true' serve com verificação para dizer que é um circulo mesmo.
        circularidade = 4 * np.pi * area / (perimetro ** 2)
        # essa linha usa o perimetro que achamos na linha de cima para calcular o quão o contorno se parece com um circulo, quanto mais próximo de 1 mais circulo ele, quanto mais próximo de 0 ele for, menos circulo ele é.
        if circularidade < 0.7:
            print('circularidade menor 0.7')
        #esse if serve como um filtro para os contornos que forem menores que 0.7 serão descartados, apenas os que forem bem próximos de um círculo 'perfeito' serão computados e salvos.
            continue
            # essa linha apenas faz com que o programa ignore os contornos que não passaram no teste e continue fazendo olaço de repetição.
          
        # Círculo mínimo que envolve TODO o contorno
        (x, y), raio = cv2.minEnclosingCircle(c)
        # essa linha serve para encontar o menor contorno que envolve todo a esfera.
        # essa linha retorna as coordenadas de todos os pontos que envolvem o circulo;
        x, y, raio = int(x), int(y), int(raio)
        # essa linha transfroma as coordenadas (caso sejam), de decimais para inteiros 
        
        #FELIPE
        lista.append( (x,y,raio) )
        print(lista)

        cv2.circle(resultado, (x, y), raio, (0, 255, 0), 2)
        # essa linha pega as coordenadas de x e y de todos os pontos que envolvem a esfera e desenha um circulo verde em volta da esfera.
        cv2.circle(resultado, (x, y), 3, (0, 0, 255), -1)
        # essa linha faz um ponto vermelho exatamente no centro da esfera.
        cv2.putText(resultado, str(len(lista)), (x + 10, y),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

    lista.sort(key=lambda ponto: ponto[0])
    
    #FELIPE
    print(lista)
    # print(lista[0], lista[0][0], lista[0][1])
    print(lista[1])

    x1 = lista[0][0]  # essa linha e as próximas 3 são o jeito que o código vai entender as cordenadas x,y dospontos que é para ele calculare e fazer a linha.
    y1 = lista[0][1]
    x2 = lista[1][0]
    y2 = lista[1][1]
    cv2.circle(resultado, (x1, y1), raio, (230, 230, 250), 2)    #essa linha e a próxima é para  trocar a cor das bolinhas que estão sendo verificadas no momento.
    cv2.circle(resultado, (x2, y2), raio, (230, 230, 250), 2)

    resultado1, angulo_graus  = calculo_angulo (x1,y1, x2, y2)
    # essa linha apenas chama a função calculo_angulo e passa as cordenadas como parâmetro para serem calculadas
    cv2.line(resultado, (x1, y1),(x2, y2), (0, 0, 0) , 2)
    # essa linha serve para desenhar a linha 


    print (resultado1, angulo_graus)
    # essa linha apenas mostra nomeu terminal o valor da distancia e do angulo que está sendo calculado.
    
# essas três linhas servem para mostrar a imagem original
    # cv2.namedWindow("Imagem original", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("Imagem original", 640, 480)
    # cv2.imshow("Imagem original", imagem)

# essas três linhas servem para mostar o resultado da segmentação 
    cv2.namedWindow("Mascara amarela", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Mascara amarela", 640, 480)
    cv2.imshow("Mascara amarela", mascara)

# essas três linhas servem para mostar o resultado 
    cv2.namedWindow("Resultado", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Resultado", 640, 480)
    cv2.imshow("Resultado", resultado)


    # essas  duas servem para fechar a janela
    cv2.waitKey(0)
    cv2.destroyAllWindows()