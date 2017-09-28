# viz_graphs
Visualiza Grafos / Visualize Graphs
# Autor: Jairo Alves.

Entrada:
- Lista pré-definida de labirintos para escolha
- Novos labirintos: Imagem BMP monocromática de livre escolha
                    Imagem BMP RGB de livre escolha
- Capacidade de processar com múltiplas tonalidades (inclusive RGB) no labirinto
- Capacidade de processar com tamanho de livre escolha
- Capacidade de processar identificando as componentes conexas
- Capacidade de processar identificando as componentes de mesma tonalidade
- Opção para gerar todos os passos de um nível de uma vez, em um único quadro
- Opção para ignorar as regiões conexas pretas - útil em labirintos tradicionais
- Flags para selecionar quais algoritmos rodar (BFS, DFS ou ambos)
- Possibilidade de usar mais de uma fonte de dados para o BFS

Classe Grafo:
- Criação de uma classe Grafo
  - Definição das operações necessárias:
    - Criar ou Listar Vértices
    - Criar ou Listar Arestas
    - Listar ou Consultar Vértices visitados
    - Impressão textual do Grafo
    - Métodos BFS e DFS para gerar todas as componentes conexas do grafo
    - Métodos BFS_v e DFS_v para gerar a componente conexa a que um dado vértice pertence

- Geração do Grafo do Labirinto / Conversão do Labirinto em Grafo:
    - Criação dos Vértices do Grafo:
      - Criação de um vértice para cada célula do labirinto
    - Criação das Arestas do Grafo:
      - Critério de Criação de arestas:
        - Criar aresta se duas células são colaterais e possuem a mesma cor
      - Loop de criação das arestas:
        - Comeca do topo e da esquerda
        - Testa a celula de baixo e da direita
        - Se atender ao critério, adiciona a aresta
        - Verifica se atingiu os limites do labirinto

Processamento:
- Conversão das imagens dos labirintos em Arrays numéricos
- Conversão dos Arrays em Grafos por similaridade de cor nas células colaterais
- Processamento dos Grafos com os Algoritmos BFS e DFS
  - Loop de processamento BFS ou DFS:
    - Escolha de um vértice inicial
    - Geração do componente conexo a partir deste vértice
    - Escolha do próximo vértice ainda não visitado
  - Para cada passo dado percorrendo o grafo, geração da imagem do passo
    - identificando a posição visitada com alteração adequada da cor da célula

Saída em texto (console):
- Impressão do Labirinto em modo texto para conferência
- Impressão das componentes conexas em lista, separadas por linhas

Processamento das imagens:
- Criação de pastas raiz com o nome do labirinto escolhido
- Geração das imagens de saída em pastas separadas para BFS e DFS
- Preservação dos arquivos pre-existentes de outros labirintos
- Limpeza dos arquivos pre-existentes do labirinto atual antes da execução
- Geração dos arquivos com nome composto do algoritmo e do número do passo

Geração de Imagens para visualização:
- Geração de uma imagem para cada passo, cada passo será um quadro da animação
- Redimensionamento das imagens para uma resolução de fácil visualização
  - Labirintos são geralmente imagens BMP pequenas de difícil visualização
  - Imagens de saída são imagens equivalentes, porém ampliadas para a largura padrão de 300px
- Alteração do formato da imagem de saída para PNG gerando ganho de 20 vezes no tamanho total

Geração da Animação para visualização:
- Programa gerador de GIF: GIMP
- Estratégia: Importar arquivos PNG e exportar como GIF
- Leitura dos arquivos na pasta
- Geração de GIFs manualmente (obs.: processo relativamente longo)
