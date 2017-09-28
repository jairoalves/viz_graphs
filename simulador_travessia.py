# -*- coding: utf-8 -*-

from collections import deque
from PIL import Image
import numpy
import os, shutil
import sys
import random
from threading import Thread

sys.setrecursionlimit(400000)
#------------------------------------------------------------------------------
# Definicoes Iniciais
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Escolha do algoritmo de geracao da imagem
#------------------------------------------------------------------------------
# - 'todas_as_imgs' gera um frame por cada nova operacao, sequencialmente
# - 'img_unica_por_nivel_de_prof' gera img somente apos completar um nivel de profund. 
tipo_geracao_img = {1: 'todas_as_imgs' , 2: 'img_unica_por_nivel_de_prof'}

# Seleciona o tipo de geracao de imagem
sel_tipo_geracao_img = tipo_geracao_img[2]

#------------------------------------------------------------------------------
# Escolha dos Mapas / labirintos disponiveis para execucao
#------------------------------------------------------------------------------
imagens = { 1: 'labirinto_1'     ,  2: 'labirinto_2'           , \
            3: 'labirinto_mini'  ,  4: 'labirinto_micro'       , \
            5: 'peixinha'        ,  6: 'cor'                   , \
            7: 'cor_mini'        ,  8: 'pb_mini'               , \
            9: 'vazio'           , 10: 'duas_fontes'           , \
           11: 'labirinto_3'     , 12: 'labirinto_tradicional' , \
           13: 'labirinto_trad_2', 14: 'rbritto'                  }

# Selecione qual o labirinto desejado
img_sel = 11

#------------------------------------------------------------------------------
# Escolhas do modo de preenchimento
#------------------------------------------------------------------------------

# Selecione ignorar ou nao partes pretas para componentes conexas
ignorar_componentes_pretas = 1

# Selecione quais algoritmos rodar
fazer_dfs = 0
fazer_bfs = 1

#------------------------------------------------------------------------------
# Escolhas do numero de fontes / vertices iniciais
#------------------------------------------------------------------------------

# Usando mais de uma fonte, reocmenda-se setar as cores no modo original abaixo

# Seleciona o numero de fontes desejado
num_fontes_sel = 1

#------------------------------------------------------------------------------
# Escolha da configuracao de preenchimento de cor
#------------------------------------------------------------------------------
# - Condição 'originais': o algoritmo preenche alterando as cores originais
# - Condicao 'componentes_conexas': preenchimento com cores únicas em cada cc.
op_cores = {1: 'originais'     , 2: 'destacar_componentes_conexas'}

# Seleciona a opcao de alteracao de cores
cores_sel = op_cores[2]

#------------------------------------------------------------------------------
# Diretorio corrente e composicao do arquivo do labirinto / mapa
dir_atual = os.path.dirname(os.path.abspath(__file__))
arq_imagem = os.path.join(dir_atual, "Mapas", imagens[img_sel] + ".bmp")

# cor atual é a cor default a ser usada em cada componente conexa
cor_atual = [0, 0, 0] # placeholder, sera alterada antes da execucao

def nova_cor():
# Retorna uma nova cor aleatoria RGB
    global cor_atual
    v1 = random.choice(range(0, 255))
    v2 = random.choice(range(0, 255))
    v3 = random.choice(range(0, 255))
    cor_atual = [v1, v2, v3]
    return cor_atual


# Lista com os diretorios para depositar as imagens de cada algoritmo
dir_img_passos = [os.path.join(dir_atual, "Passos", imagens[img_sel], "DFS"), \
                  os.path.join(dir_atual, "Passos", imagens[img_sel], "BFS")]

# Nome dos arquivos com os passos 
imagens_passos = { 'DFS': dir_img_passos[0] + "\\" + "lab_dfs_passo.png", \
                   'BFS': dir_img_passos[1] + "\\" + "lab_bfs_passo.png" }

def recarrega_imagem():
#   limpa os valores de cores dos pixels da imagem para um novo processamento
    global im_array, image, posicao
    image = Image.open(arq_imagem).convert("RGB")
    im_array = numpy.array(image)
    

    # complemento do nome dos arquivos de passos, 
    # posicao sera incrementada a cada passo
    posicao = 0

    
def apaga_imgs_passos_antigos():
#   Apaga todas as imagens dos passos percorridos salvas nos diretorios
#   Serve para garantir que todas as imagens sejam da execucao atual
    for diretorio in dir_img_passos:
        try:
            shutil.rmtree(diretorio) # apaga os arquivos anteriores 
        except:
            pass
        os.makedirs(diretorio)

apaga_imgs_passos_antigos()
recarrega_imagem()  

largura, altura  = image.size    



#------------------------------------------------------------------------------
# Funcoes e Classes
#------------------------------------------------------------------------------

def print_q(queue_to_print):
    elementos = ""
    for elem in queue_to_print:
        if(elementos == ""):
            elementos = elem
        else:
            elementos = elementos + " -> " + elem
    print("Fila: ", elementos)
        
            
class Grafo:
    def __init__(self):
        self.vertices = set()
        self.arestas = {}
        self.visitados = set()
        self.fila_de_visita = deque()
        self.percorridos = ""
    
    def add_v(self, lista_de_vertices):
        for vertice in lista_de_vertices:
            self.vertices.add(vertice)
            self.arestas[vertice] = []
        
    def add_e(self, vertice_origem, vertice_destino):
        if( vertice_destino == vertice_origem):
            return
        
        if(not (vertice_origem in self.vertices) or \
           not (vertice_destino in self.vertices)):
               return
        
        self.arestas[vertice_origem].append(vertice_destino)
        self.arestas[vertice_destino].append(vertice_origem)
        
    def lista_vertices(self):
        lista_de_vertices = []
        for vertice in self.vertices:
            lista_de_vertices.append(vertice)
        return self.vertices
    
    def lista_arestas(self):
        lista_de_arestas = []
        for aresta in self.arestas:
            lista_de_arestas.append(aresta)
        return lista_de_arestas

    def imprime_grafo(self):
        print('Lista de vertices = ', self.lista_vertices())
        print('Lista de arestas  = ', self.lista_arestas())    

#   DFS partindo de um vertice e cobrindo apenas seus vizinhos
    def dfs_v(self, vertice_origem, cor = 'default'):
        self.visitados.add(vertice_origem)
        self.percorridos = self.percorridos + " -> " + str(vertice_origem)
        
        # gera a imagem atualizada com o passo atual
        linha  = int(vertice_origem) // largura
        coluna = int(vertice_origem) % largura  
        
        # Se usuario deseja ignorar partes pretas
        if(ignorar_componentes_pretas):
            if(pixel_total(im_array[linha][coluna]) == 0):
                # seta todas as celulas pretas como visitadas
                self.visitados.add(vertice_origem)
                return
            
        im_array[linha][coluna] = altera_pixel(im_array[linha][coluna], cor)
        gera_imagem(im_array, imagens_passos['DFS'])
        
        for vertice_destino in self.lista_arestas_v(vertice_origem):
            if(vertice_destino in self.visitados):
                continue
            self.visitados.add(vertice_destino)
            self.dfs_v(vertice_destino)
        return self.percorridos

#   BFS partindo de um vertice e cobrindo apenas seus vizinhos        
    def bfs_v(self, vertice_origem, cor = 'default'):
        global im_array
        profund_origem = 0
        profundidade = 0
        
        # prepara o passo inicial
        linha  = int(vertice_origem) // largura
        coluna = int(vertice_origem) % largura  
        
        # Se usuario deseja ignorar partes pretas
        if(ignorar_componentes_pretas):
            if(pixel_total(im_array[linha][coluna]) == 0):
                # seta todas as celulas pretas como visitadas
                self.visitados.add(vertice_origem)
                return
        
        im_array[linha][coluna] = altera_pixel(im_array[linha][coluna], cor)            
                
        self.fila_de_visita.append([vertice_origem, profund_origem])
        
        
        self.visitados.add(vertice_origem)
        self.percorridos = self.percorridos + " -> " + str(vertice_origem) 

        while(True):
            try:
                # verifica se ainda existem vertices a percorrer
                [vertice_origem, profund_origem] = self.fila_de_visita.popleft()
                
            except:
                # gera a imagem do estado final
                gera_imagem(im_array, imagens_passos['BFS'])
                break

            self.visitados.add(vertice_origem)
                
            for vertice_destino in self.lista_arestas_v(vertice_origem):
                vertices_ja_na_fila = [vert for [vert, prof] in self.fila_de_visita]
                if(vertice_destino not in self.visitados and \
                   vertice_destino not in vertices_ja_na_fila):
                    profundidade_anterior = profundidade
                    profundidade = profund_origem + 1
                    self.percorridos = self.percorridos + " -> " + \
                                       str(vertice_destino) + \
                                       ' (' + str(profundidade) + ')'
                    self.fila_de_visita.append([vertice_destino, profundidade])
                    
                    
                    
                    # gera a imagem atualizada com o passo atual
                    linha  = int(vertice_destino) // largura
                    coluna = int(vertice_destino) % largura

                    if(sel_tipo_geracao_img == 'todas_as_imgs'):
                        gera_imagem(im_array, imagens_passos['BFS'])
                    
                    if(sel_tipo_geracao_img == 'img_unica_por_nivel_de_prof'):
                        if(profundidade_anterior != profundidade):
                            gera_imagem(im_array, imagens_passos['BFS'])

                    im_array[linha][coluna] = altera_pixel(im_array[linha][coluna], cor)                    
                        
                                                
        
        return self.percorridos
 
#   BFS cobrindo todos os vertices do grafo
    def bfs(self):
#     Para cada vertice do grafo, 
#     se ele ainda nao foi visitado, imprime os seus vizinhos
        global im_array
        gera_imagem(im_array, imagens_passos['BFS'])
        for vertice in self.lista_vertices():
            if(not self.vertice_visitado(vertice)):
                nova_cor()
                print(" - BFS", self.bfs_v(str(vertice)))
                self.percorridos = ""

#   DFS cobrindo todos os vertices do grafo
    def dfs(self):
#     Para cada vertice do grafo, 
#     se ele ainda nao foi visitado, imprime os seus vizinhos
        global im_array
        gera_imagem(im_array, imagens_passos['DFS'])
        for vertice in self.lista_vertices():
            if(not self.vertice_visitado(vertice)):
                nova_cor()
                print(" - DFS", self.dfs_v(str(vertice)))
                self.percorridos = ""    
    def vertice_visitado(self, vertice):
        return (vertice in self.visitados)
    
    def lista_arestas_v(self, vertice = 0):
        
        return self.arestas[vertice]
          



#--------------------------------------------------
# Ler a Imagem
#--------------------------------------------------
# Entrada: Recebe um arquivo imagem do labirinto em bmp
# Saida:   Cria um vetor onde cada quadrado e um numero
# O vetor final esta organizado no formato [linha][coluna], ini em 0.

def pr_img(image):
#   Imprime em texto o aspecto do labirinto
    print("".join(["-" for j in range(largura + 2)]))
    for i in range(altura):
        linha = "|"
        for j in range(largura):
            if(pixel_total(im_array[i][j]) >= 200):
                linha = linha + " "
            else:
                linha = linha + "X"
        print(linha + "|")
    print("".join(["-" for j in range(largura + 2)]))
    return

def array_para_img(im_array):
    return Image.fromarray(im_array.astype('uint8'))    

def img_para_img(image):
    return numpy.array(image)    

def pixels_iguais(pixel1, pixel2):
    return  pixel1[0] == pixel2[0] and \
            pixel1[1] == pixel2[1] and \
            pixel1[2] == pixel2[2]

def pixel_total(pixel):
    return int(pixel[0]) + int(pixel[1]) + int(pixel[2])
    
def gera_imagem(im_array, nome):
#   Gera uma imagem redimensionada para exibir os passos intermediarios do caminho
#   recebe o nome e a posicao do passo que sera concatenada no titulo da imagem
    global posicao
    posicao = posicao + 1
 
    nome, ext = nome[:-4], nome[-3:]
    nome = nome + "_" + str(posicao) + "." + ext
    
    largura_desejada = 400
    altura_desejada  = int((altura / largura) * largura_desejada) 
    
    image = array_para_img(im_array)
    image = image.resize((largura_desejada, altura_desejada))
    image.save(nome)
    
def altera_pixel(valor, cor = 'default'):
# Altera o pixel do labirinto para sinalizar que ele foi percorrido

# Comportamento do algoritmo de coloracao do mapa
    if(cores_sel == 'originais'):
#    Se o pixel total for menor que 128, aumenta o seu valor
#    Se o pixel total for maior que 128, reduz seu valor
        if(pixel_total(valor) < 3 * 128):
            v1 = min(255, valor[0] + 48)
            v2 = min(255, valor[1] + 48)
            v3 = min(255, valor[2] + 48)
            return [v1, v2, v3]
        else:
            v1 = max(0, int(valor[0]) * 0.8)
            v2 = max(0, int(valor[1]) * 0.8)
            v3 = max(0, int(valor[2]) * 0.8)
            return [v1, v2, v3]

    elif (cores_sel == 'destacar_componentes_conexas'):
        if(cor == 'default'):
            return cor_atual
        else:
            return cor


#--------------------------------------------------
# Gerar o Grafo do Labirinto
#--------------------------------------------------

# Entrada: Recebe o vetor numerico da imagem do labirinto
# Saida:   Cria um Grafo onde cada quadrado é um vertice
# Funcionamento:
# - Um vertice sera vizinho dos quadrados colaterais 
#   desde que possuam a mesma cor que ele
# Produz ao final um grafo da Classe Grafo com essas caracteristicas        
    
def gera_grafo_do_labirinto(vetor_da_imagem):
    lab = Grafo()
    altura_do_grafo = altura
    largura_do_grafo = largura
    num_vertices = altura_do_grafo * largura_do_grafo 
    print("Numero de Vertices do Grafo = ", num_vertices)

    lista_de_vertices = []
    for vertice in range(num_vertices):
        lista_de_vertices.append(str(vertice))
        
    lab.add_v(lista_de_vertices)
    
    for pos_vertice in range(num_vertices):
        # Calcula conversao posicao[linear] <=> posicao[linha][coluna]
        linha  = pos_vertice // largura_do_grafo
        coluna = pos_vertice % largura_do_grafo
        
        # Se for possivel, adiciona as arestas direita e inferior.
        # Assim, partindo do canto sup esq, eu cubro todas as arestas
        
        # Adiciona a aresta direita, se existir vertice a direita
        # e as cores de ambas os vértices forem iguais
        if(coluna + 1 < largura_do_grafo):
            lin_direita = linha
            col_direita = coluna + 1
            pos_direita = lin_direita * largura_do_grafo + col_direita
            # Se a posicao direita nao for uma parede, adiciona uma aresta
            if(pixels_iguais(im_array[lin_direita][col_direita], \
               im_array[linha][coluna])):
                lab.add_e(str(pos_vertice), str(pos_direita))            
            
        # Adiciona a aresta de baixo, se existir vertice abaixo
        # e as cores de ambos os vertices forem iguais
        if(linha + 1 < altura_do_grafo):
            lin_inferior = linha + 1
            col_inferior = coluna
            pos_inferior = lin_inferior * largura_do_grafo + col_inferior
            # Se a posicao inferior nao for uma parede, adiciona uma aresta
            if(pixels_iguais(im_array[lin_inferior][col_inferior], \
                             im_array[linha][coluna]              )):
                lab.add_e(str(pos_vertice), str(pos_inferior)) 
        
    return lab

pr_img(image)

if(fazer_dfs):
    lab = gera_grafo_do_labirinto(image)
    lab.dfs()

recarrega_imagem()
if(fazer_bfs):
    lab = gera_grafo_do_labirinto(image)
    for execucoes_paralelas in range(num_fontes_sel):
        Thread(target = lab.bfs).start()