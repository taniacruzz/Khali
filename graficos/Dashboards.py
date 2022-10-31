import matplotlib.pyplot as  plt 
from .Integrador import *

# Gera um grafico multi barra
def multi_bar (title, names, y_label, matrix, x_label, x_ticks, colors):

    # Esconde a barra de comandos do matplotlib
    plt.rcParams['toolbar'] = 'None'

    # Define a ampliação do grafico
    # plt.figure(figsize = (10, 5))
    
    # Define a largura de cada barra individual sendo 1 dividido pela quantidade de listas da matriz
    # somado por um valor constante de espaçamento entre cada x_tick
    bar_width = 1. / (len(matrix) + 1.75)

    # Para cada lista na matriz
    for i, lst in enumerate(matrix):

        # Define a posição da barra. Indice da barra * espaçamento definido pela quantidade de barras por x_tick
        offset = (i * bar_width) 

        # move todas as barras para esquerda em (tamanho total da soma das barras / 2)
        offset -= bar_width * int(len(matrix) / 2)

        # caso o numero de barras seja par, move o metade do tamanho de UMA barra para a direita
        if len(matrix) % 2 == 0: offset += bar_width / 2

        # define a posição de cada barra da lista de indice 'i'
        positions = [j + offset for j in range(len(x_ticks))]
        
        # Cria um grafico de barras para cada item da lista 'lst'  
        plt.bar(positions, lst, color=colors[i % len(colors)], width=bar_width, label=names[i])

    plt.ylim([0, 5])

    # Adiciona o título
    plt.title(title)

    # Adiciona a label e os marcadores x
    plt.xlabel(x_label)
    plt.xticks([r for r in range(len(x_ticks))], x_ticks)

    # Adiciona a label y
    plt.ylabel(y_label)

    # Adiciona a legenda representando cada lista da matriz
    plt.legend()

    # Renderiza o grafico
    plt.show()


# Gera um grafico de linha
def line (title, names, y_label, values, x_label, x_ticks, colors):
    plt.rcParams['toolbar'] = 'None'

    # Define a ampliação do grafico
    # plt.figure(figsize = (10, 5))
    barWidth = .2 

    for i, value in enumerate(values):

        # Aqui eu construo a barra
        positions = [j + barWidth for j in range(len(x_ticks))]
        plt.plot(positions, value, color=colors[i % len(colors)], label=names[i])

    plt.ylim([0, 5])

    plt.title(title)

    plt.xlabel(x_label)
    plt.xticks([r + barWidth for r in range(len(x_ticks))], x_ticks)

    plt.ylabel(y_label)

    plt.legend()

    plt.show()

# ------------------------------------------------------------------------------------------------------------------|
#                          |    calculo    |    barras    |      label      |    acesso     |        função         |
# ------------------------------------------------------------------------------------------------------------------|
# media membro             | media sprint  | por sprint   | criterio        | PO LT DEV     | user_media_sprints    |
# media membro / time      | media sprints | membro, time | criterio        | PO LT DEV     |                       |
# media de cada time       | media sprints | time         | criterio        | LG FK         |                       |
# media membros da função  |               | membro       |                 | LG FK         |                       |
# ------------------------------------------------------------------------------------------------------------------|
# media do time            | media sprint  | sprint       | criterio        | PO LT         | time_media_sprints    |
# ------------------------------------------------------------------------------------------------------------------|
# media membros time       | media sprint  | membro       | criterio        | PO LT         |                       |
# media do grupo           | media sprint  | sprint       | criterio        | PO LT         |                       |
# ------------------------------------------------------------------------------------------------------------------|


def user_media_sprints (user_id):

    # importa as funções de acesso ao banco de dados de cada modelo
    from Models.User import get_user
    from Models.Rating import get_ratings_to_user
    from Models.Sprint import get_group_sprints

    # importa a lista de criterios utilizados nas avaliações
    from Models.id_criteria import criteria

    # Objetivo:
    #   - calcular a média do usuário para cada criterio em cada sprint
    # Passos executados:
    # 1 - Requisitar do banco de dados as sprints do grupo do usuário
    # 2 - Requisitar do banco de dados todas as avaliações do usuário
    # 3 - Calcular a média do usuário em cada criterio de cada sprint utilizando as avaliações do passo 2
    # 4 - Gerar o gráfico com as informações adquiridas no passo 3

    # carrega as informações do usuário
    user = get_user(user_id)

    # Lista as sprints (em objeto da classe Sprint)
    sprints = get_group_sprints(user.group_id)

    # Lista todas as avaliações em que o usuário está sendo avaliado 
    ratings = get_ratings_to_user(user.id)

    # Retorna o grafico representando as médias calculadas 
    multi_bar(
        f'Média de {user.name} ao longo das sprints',
        [f'Sprint {i}' for i in range(len(sprints))],
        'Médias',
        medias_por_sprint(criteria, sprints, ratings),
        'Críterio avaliativo',
        criteria,
        ['orange', 'yellow', 'red', 'green', 'darkgoldenrod', 'brown', 'lightgreen', 'magenta', 'royalblue', 'pink', ]
    )


# Retorna um Dashboard com a media de um determinado time em cada criterio de cada sprint
def time_media_sprints (team_id):

    # importa as funções de acesso ao banco de dados de cada modelo
    from Models.Team import get_team
    from Models.Rating import get_ratings_to_team
    from Models.Sprint import get_group_sprints

    # importa a lista de criterios utilizados nas avaliações
    from Models.id_criteria import criteria

    # Objetivo:
    #   - calcular a média do time para cada criterio em cada sprint
    # Passos executados:
    # 1 - Requisitar do banco de dados as sprints do grupo do time
    # 2 - Requisitar do banco de dados todas as avaliações em que o usuario avaliado pertence ao time
    # 3 - Calcular a média do time em cada criterio de cada sprint utilizando as avaliações do passo 2
    # 4 - Gerar o gráfico com as informações adquiridas no passo 3

    # carrega o time com o id especificado
    team = get_team(team_id)
    
    # Lista as sprints (em objeto da classe Sprint)
    sprints = get_group_sprints(team.group_id)

    # Lista todas as avaliações em que o id do usuário avaliado corresponda a qualquer id da lista 'user_ids' 
    ratings = get_ratings_to_team(team_id)

    # Retorna o grafico representando as médias calculadas 
    multi_bar(
        f'Média do time {team.name} ao longo das sprints',
        [f'Sprint {i}' for i in range(len(sprints))],
        'Médias',
        medias_por_sprint(criteria, sprints, ratings),
        'Críterio avaliativo',
        criteria,
        ['orange', 'yellow', 'red', 'green', 'darkgoldenrod', 'brown', 'lightgreen', 'magenta', 'royalblue', 'pink', ]
    )






def PO():
    multi_bar(
        'desempenho individual',
        ['Rodrigo', 'rogerio', 'marta', 'Cleitinho'],
        'Notas',
        [
            [4, 3, 5, 4, 2],
            [5, 4, 3, 4, 6],
            [4, 2, 4, 5, 4],
            [4, 2, 4, 5, 4],
            [2, 3, 4, 5, 3]
        ],
        'Críterio avaliativo',
        ['TG', 'PO', 'KE', 'PT', 'QU'],
        ['orange', 'green', 'blue', 'pink']
    )




def estudantes ():
    multi_bar(
        'Seu desempenho em comparativo ao seu time',
        ['Sua média', 'Média dos seu time'],
        'Criterios',
        [
            [2, 3, 2, 4, 5],
            [3, 4, 2, 5, 4]
        ],
        None,
        ['TG', 'PO', 'KE', 'PT', 'QU'],
        ['orange', 'green']
    )





def Estudante_2 ():
    multi_bar(
        'Desempenho ao decorrer das Sprints',
        ['Sprint 1', 'Sprint 2', 'Sprint 3', 'Sprint 4'],
        'Criterios',
        [
            [2, 3, 2, 4, 5],
            [3, 4, 2, 5, 4],
            [4, 4, 3, 4, 3],
            [4, 5, 4, 5, 4]
        ],
        None,
        ['TG', 'PO', 'KE', 'PT', 'QU'],
        ['orange', 'green', 'blue', 'red']
    )


