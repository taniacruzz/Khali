from Utils import lista_usuarios_back
from tkinter import *

# cores
co0 = "#FAE8E8"  # rosa
co1 = "#D9D9D9"  # cinza
co2 = "#1A1D1A"  # preta

# Informações do modulo
NAME = 'Lista'
REQUIRED_PERMISSIONS_REG  = [None]
REQUIRED_PERMISSIONS_RATE = [
    [3, 4, 5]  # pelo menos uma das 3
]
REQUIRED_PERMISSIONS_VIEW = [None]

# executa o modulo e retorna
def run(frame_parent):

    frm_main = Frame(frame_parent, background=co0)
    frm_main.pack(expand =1, fill=BOTH)


    canvas = Canvas(frm_main, bg=co0)
    canvas.pack(side=LEFT, expand=1, fill=BOTH)


    scrollbar_ver=Scrollbar(frm_main, orient=VERTICAL, command=canvas.yview)
    scrollbar_ver.pack(side=RIGHT, fill=Y)


    canvas.configure(yscrollcommand=scrollbar_ver.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    module_frame=Frame(canvas, bg=co0, relief=FLAT, bd=3)


    canvas.create_window((0,0), window=module_frame, anchor='nw')


    # importa o usuário logado
    from Users.Authentication import CURRENT_USER

    # cria uma lista com os usuários a serem avaliados pelo usuário logado
    grade_submitted = lista_usuarios_back.get_users(CURRENT_USER.email)[0]
    grade_to_submit = lista_usuarios_back.get_users(CURRENT_USER.email)[1]

    # função de criar frame
    # row e column referem-se a posição do frame
    def criar_frame(quadro, row, column):
        frame = Frame(quadro, background=co0)
        frame.grid(row = row, column = column, sticky = "ew", padx = 5, pady = 5)
        return frame

    # cria widget do tipo label
    def criar_label(quadro, text, font, r, c):
        Label(quadro, text=text, font=font, background = co0, justify=LEFT).grid(row=r, column=c, sticky="nw")

    def criar_button(quadro, text, font, r, c):
        Button(quadro, text = text, font = font, background = co0, justify=LEFT, fg=co2,
               width=13, height=0, activebackground='#c5a8b0').grid(row=r, column=c, sticky="ne")

    # frame com os dados do usuário que está logado
    frame_user = criar_frame(module_frame, 0, 0)

    # importa a função que transforma role_id em nome da role
    from Models.Role import get_role_name

    # ###testes
    # user_group_members = handler.find_data_list_by_field_value_csv(Settings.USERS_PATH, 'group_id', grupo_id)
    #



    criar_label(frame_user, 'Meu Perfil', 'Calibri, 30', 0, 0)

    criar_label(frame_user, get_role_name(CURRENT_USER.role_id), 'Calibri, 12',1, 0)
    criar_label(frame_user, CURRENT_USER.name, 'Calibri, 12',2, 0)

    # frame com os usuários que devem ser analisados por quem está logado
    frame_avaliados = criar_frame(module_frame, 1, 0)
    criar_label(frame_avaliados, 'Integrantes ainda não Avaliados', 'Calibri, 14', 0, 0)

    indice = 1

    for line in grade_to_submit:

        # frame_to_rate = criar_frame(frame_avaliados, indice + 1, 0)
        criar_label(frame_avaliados, get_role_name(line['role_id']), 'Calibri, 12', indice, 0)  # linha para teste
        criar_label(frame_avaliados, line['name'], 'Calibri, 12', indice + 1, 0)  # linha para teste
        criar_button(frame_avaliados, 'Avaliar', 'Calibri, 12', indice + 1, 1)  # linha para teste
        indice = indice + 2

    indice = indice + 1

    criar_label(frame_avaliados, 'Integrantes já Avaliados', 'Calibri, 14', indice, 0)

    for line in grade_submitted:

        # frame_rated = criar_frame(frame_avaliados, indice, 0)
        criar_label(frame_avaliados, get_role_name(line['role_id']), 'Calibri, 12', indice+1, 0)  # linha para teste
        criar_label(frame_avaliados, line['name'], 'Calibri, 12', indice+2, 0)  # linha para teste
        criar_button(frame_avaliados, 'Editar Avaliação', 'Calibri, 12', indice+2, 1)  # linha para teste
        indice = indice + 2
##################################################################################################
    # # cria o frame do módulo
    # module_frame = Frame(frame_parent, background=co0)
    # module_frame.grid(row=0, column=0, sticky="nwes")
    #
    # # importa o usuário logado
    # from Users.Authentication import CURRENT_USER
    #
    # # cria uma lista com os usuários a serem avaliados pelo usuário logado
    # grade_submitted = lista_usuarios_back.get_users(CURRENT_USER.email)[0]
    # grade_to_submit = lista_usuarios_back.get_users(CURRENT_USER.email)[1]
    #
    # # função de criar frame
    # # row e column referem-se a posição do frame
    # def criar_frame(quadro, row, column):
    #     frame = Frame(quadro, background=co0)
    #     frame.grid(row=row, column=column, sticky="nw", padx=5, pady=5)
    #     return frame
    #
    # # cria widget do tipo label
    # def criar_label(quadro, text, font, r, c):
    #     Label(quadro, text=text, font=font, background=co0, justify=LEFT).grid(row=r, column=c, sticky="nw")
    #
    # def criar_button(quadro, text, font, r, c):
    #     Button(quadro, text=text, font=font, background=co0, justify=RIGHT).grid(row=r, column=c, sticky="ne")
    #
    # # frame com os dados do usuário que está logado
    # frame_user = criar_frame(frame_parent, 0, 0)
    #
    # # importa a função que transforma role_id em nome da role
    # from Models.Role import get_role_name
    #
    # # ###testes
    # # user_group_members = handler.find_data_list_by_field_value_csv(Settings.USERS_PATH, 'group_id', grupo_id)
    # #
    #
    # criar_label(frame_user, 'Meu Perfil', 'Calibri, 14', 0, 0)
    #
    # criar_label(frame_user, get_role_name(CURRENT_USER.role_id), 'Calibri, 12', 1, 0)
    # criar_label(frame_user, CURRENT_USER.name, 'Calibri, 12', 2, 0)
    #
    # # frame com os usuários que devem ser analisados por quem está logado
    # frame_avaliados = criar_frame(frame_parent, 1, 0)
    # criar_label(frame_avaliados, 'Integrantes ainda não Avaliados', 'Calibri, 14', 0, 0)
    #
    # indice = 0
    #
    # for line in grade_to_submit:
    #     indice = grade_to_submit.index(line)
    #     frame_to_rate = criar_frame(frame_avaliados, indice + 1, 0)
    #     criar_label(frame_to_rate, get_role_name(line['role_id']), 'Calibri, 12', 0, 0)  # linha para teste
    #     criar_label(frame_to_rate, line['name'], 'Calibri, 12', 1, 0)  # linha para teste
    #     criar_button(frame_to_rate, 'Avaliar', 'Calibri, 12', 1, 1)  # linha para teste
    #
    # indice = indice + 2
    #
    # criar_label(frame_avaliados, 'Integrantes já Avaliados', 'Calibri, 14', indice, 0)
    #
    # for line in grade_submitted:
    #     indice = indice + 1
    #     frame_rated = criar_frame(frame_avaliados, indice, 0)
    #     criar_label(frame_rated, get_role_name(line['role_id']), 'Calibri, 12', 0, 0)  # linha para teste
    #     criar_label(frame_rated, line['name'], 'Calibri, 12', 1, 0)  # linha para teste
    #     criar_button(frame_rated, 'Editar Avaliação', 'Calibri, 12', 1, 1)  # linha para teste
####################################################################################
    # criar_label(frame_rated, text= , 'Calibri, 12', indice+1, 0)



    # for line in users:
    #     # para que os nomes dos avaliados não fiquem sobrescritos:
    #     # uso o índice dos dados daquele avaliado para posicionar as frames
    #     indice = users.index(line)
    #     # cada avaliado tem uma frame específica
    #     frame_avaliado = criar_frame(frame_avaliados, indice + 1, 0)
    #     criar_label(frame_avaliado, get_role_name(line['role_id']), 'Calibri, 12', 0, 0)  # linha para teste
    #     criar_label(frame_avaliado, line['name'], 'Calibri, 12', 1, 0)  # linha para teste
    #     criar_label(frame_avaliado, '', 'Calibri, 12', 2, 0)  # linha para teste

    # dashboard = criar_frame(frame_parent, 0, 1)
    # criar_label(dashboard, 'Dashboards', 'Calibri, 14', 0, 0)

    return module_frame


