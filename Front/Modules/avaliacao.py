from tkinter import * 
from tkinter import ttk

# Configurações da janela
window = Tk() 
window.configure(bg='#fae8e8')  # Cor do plano de fundo da tela
window.geometry("1200x600")
window.title('Autoavaliação')  # Título da janela

# Criar um frame para comportar o canvas
frm_main=Frame(window, bg='#fae8e8')
frm_main.pack(fill=BOTH, expand=1) 

# O canvas aceita o scrollbar, mas ela só faz o papel da responsividade
canvas=Canvas(frm_main, bg='#fae8e8')
canvas.pack(side=LEFT, fill=BOTH, expand=1)

# Configurações do scrollbar
scrollbar_ver = ttk.Scrollbar(frm_main, orient=VERTICAL, command=canvas.yview) # Comando xview para orientação HORIZONTAL
scrollbar_ver.pack(side=RIGHT, fill=Y)

# Configurações do canvas
canvas.configure(yscrollcommand=scrollbar_ver.set) # xscrollcomand para barra horizontal
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all'))) # Seleciona qual parte do canvas o scrollbar deve identificar

frm_geral=Frame(canvas, bg='#fae8e8', relief=FLAT, bd=3) # Não colocamos o frame com o .pack nesse caso

# Integração do frame geral a uma janela do canvas
canvas.create_window((0,0), window=frm_geral, anchor='nw')

# Criação de um frame para as questões da avaliação
frm_avaliacao=Frame(frm_geral, bg='#fae8e8', relief=FLAT, bd=3)
frm_avaliacao.grid(row=4, column=0, columnspan=3, sticky='w')

frm_feedback=Frame(frm_avaliacao, bg='#fae8e8', relief=FLAT, bd=3)
frm_feedback.grid(row= 6, rowspan=20, column=1, sticky='nsew')
frm_feedback.columnconfigure(0, weight=1)
frm_feedback.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 19, 20], weight=1)

# Função para criação de texto
def criar_label(master, text, tamanho, column, row, padx, pady, sticky):
    label=Label(master=master, text=text
    , bg='#fae8e8', font=('Calibre', tamanho))
    label.grid(column=column, row=row, padx=padx, pady=pady, sticky=sticky)

# Função para criação de caixas de entrada
def criar_entrada(master, row, column, padx, pady, sticky):
    feedback=Entry(master=master, width=75, fg='#1a1d1a', font=('Calibre 10'))
    feedback.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

# Função para criação de escalas
def criar_escala(master, row, padx, pady):
    escala = Scale(master=master, from_=1, to=5, length=500, tickinterval=1, orient=HORIZONTAL, 
    bg='#fae8e8', font='Calibre, 10', highlightcolor='#c5a8b0', troughcolor='#c5a8b0', state='normal', variable=IntVar())
    escala.grid(column=0, row=row, padx=padx, pady=pady, sticky='w')
    escala.set(1)
    print(escala.get())
    return escala

# Criação de uma escala para cada pergunta
p1 = criar_escala(frm_avaliacao, 6, 30, 2)
p2 = criar_escala(frm_avaliacao, 9, 30, 2)
p3 = criar_escala(frm_avaliacao, 12, 30, 2)
p4 = criar_escala(frm_avaliacao, 15, 30, 2)
p5 = criar_escala(frm_avaliacao, 18, 30, 2)

respostas = [p1, p2, p3, p4, p5]

def resposta(nome, row):
    for i in respostas:
     if nome.get() <= 3:
        #frm_feedback=Frame(frm_avaliacao, bg='#fae8e8', relief=GROOVE, bd=3)  # Frame individual para cada feedback obrigatório
        #frm_feedback.grid(row=row, column=1, sticky='w')
        criar_label(frm_feedback, 'Feedback obrigatório: ', 11, 0, row, 0, 24, 'e')
        criar_entrada(frm_feedback, row, 1, 0, 0, 'w')

def enviar_retorno():
    criar_label(frm_geral, 'Avaliação enviada com sucesso!', 13, 0, 5, 0, 0, 'e')

# Botão para registrar notas e conferir a necessidade de feedback
button=Button(master=frm_geral, text='Registrar Notas', fg='#1a1d1a', bg='#d9d9d9', 
font=('Calibre', 10), width=13, height=1, activebackground='#c5a8b0', command=[resposta(p1, 0), resposta(p2, 5), resposta(p3, 10), resposta(p4, 15), resposta(p5, 20)])
button.grid(row=5, column=1, padx=5, pady=5, sticky='e')

# Botão para enviar notas para o banco de dados
button=Button(master=frm_geral, text='Enviar Avaliação', fg='#1a1d1a', bg='#d9d9d9', 
font=('Calibre', 10), width=13, height=1, activebackground='#c5a8b0', command=enviar_retorno)
button.grid(row=5, column=2, padx=5, pady=5, sticky='w')

# Textos gerais da tela
criar_label(frm_geral, 'Autoavaliação', 30, 0, 0, 30, 30, 'w')
criar_label(frm_geral, 'Nome do usuário', 20, 0, 1, 30, 0, 'w')  # PUXAR DADO VINCULADO COM TELA DE RETORNO - NOME E FUNÇÃO ???
criar_label(frm_geral, 'Prazo para realizar a autoavaliação da {nº da Sprint}', 15, 0, 2, 30, 20, 'w')  # PUXAR DADO VINCULADO COM TELA DE RETORNO ???
criar_label(frm_geral, 'Breve explicação sobre a avaliação: Falar sobre a escala Likert e dos feedbacks obrigatórios para notas abaixo ou iguais a 3',
10, 0, 3, 30, 30, 'w')  

# Textos das questões da avaliação
criar_label(frm_avaliacao, 'Como você se avalia em trabalho em equipe, cooperação e descentralização de conhecimento?', 11, 0, 4, 30, 5, 'w')
criar_label(frm_avaliacao, 'Como você se avalia em iniciativa e proatividade?', 11, 0, 7, 30, 5, 'w')
criar_label(frm_avaliacao, 'Como você se avalia em autodidaxia e agregação de conhecimento ao grupo?', 11, 0, 10, 30, 5, 'w')
criar_label(frm_avaliacao, 'Como você se avalia em entrega de resultados e participação efetiva no projeto?', 11, 0, 13, 30, 5, 'w') 
criar_label(frm_avaliacao, 'Como você se avalia em competência técnica?', 11, 0, 16, 30, 5, 'w')

# Descrição da tabela
criar_label(frm_avaliacao, 'Péssimo (1)           Ruim (2)              Regular (3)                Bom (4)               Ótimo (5)', 10, 0, 5, 30, 0, 'w')
criar_label(frm_avaliacao, 'Péssimo (1)           Ruim (2)              Regular (3)                Bom (4)               Ótimo (5)', 10, 0, 8, 30, 0, 'w')
criar_label(frm_avaliacao, 'Péssimo (1)           Ruim (2)              Regular (3)                Bom (4)               Ótimo (5)', 10, 0, 11, 30, 0, 'w')
criar_label(frm_avaliacao, 'Péssimo (1)           Ruim (2)              Regular (3)                Bom (4)               Ótimo (5)', 10, 0, 14, 30, 0, 'w') 
criar_label(frm_avaliacao, 'Péssimo (1)           Ruim (2)              Regular (3)                Bom (4)               Ótimo (5)', 10, 0, 17, 30, 0, 'w')

window.mainloop()