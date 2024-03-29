co0 = '#FAE8E8'  # rosa / fundo de telas
co1 = '#D9D9D9'  # cinzinha / botões
co2 = '#1A1D1A'  # preta
co3 = '#26413C'  # verde / botões / frame títulos
co4 = '#C5A8B0' # rosa velho / botões ativos
gr0 = '#F1D1D1' # rosa claro para gráfico
gr1 = '#896978' # lavanda
gr2 = '#260C1A' # uva
gr3 = '#4E615D' # verde claro
gr4 = '#26413C' # verde escuro
gr5 = '#03120E' # preto esverdeado


# funções genéricas de widgets do tkinter
def criar_frame(quadro, r=0, c=0, sticky='news', bg=co0, hlbg=co0, hlt=0, px=5, py=5):
    from tkinter import Frame
    frame = Frame(quadro, background=bg, highlightbackground=hlbg, highlightthickness=hlt)
    frame.grid(row=r, column=c, sticky=sticky, padx=px, pady=py)
    return frame

def criar_label(quadro, text, font='Calibri, 12', r=0, c=0, bg=co0, sticky='n', justify='left', width=0):
    from tkinter import Label
    widget = Label(quadro, text=text, font=font, background=bg , justify=justify, width=width)
    widget.grid(row=r, column=c, sticky=sticky)
    return widget

def criar_button(quadro, text, font='Calibri, 12', r=0, c=0, command=None, sticky='ne', width=12):
    from tkinter import Button
    widget = Button(quadro, text=text, font=font, background=co0, justify='right', fg=co2, command=command,
        width=width, height=0, activebackground='#c5a8b0')
    widget.grid(row=r, column=c, sticky= sticky)
    return widget

def criar_entry(quadro, font='Calibri, 12', r=0, c=0, sticky='w', px=0, py=0, justify='left'):
    from tkinter import Entry
    widget = Entry(quadro, font=font, fg=co2, justify=justify)
    widget.grid(row=r, column=c, padx=px, pady=py, sticky=sticky)
    return widget


# adiciona um texto placeholder cinza ao entry especificado
def bind_entry_placeholder (entry, text):

    # lambda chamada caso a entry não possua texto inserido pelo usuário
    no_value_lambda = lambda _, e=entry: [e.insert(0, text), e.config(fg='gray')]

    # chama a função para colocar o placeholder na entry
    no_value_lambda(entry)

    # lambda chamada quando o usuário clica on seleciona a entry
    focus_in_lambda = lambda _, e=entry: [e.delete('0', 'end'), e.unbind('<FocusIn>'), e.config(fg='black')]

    # configura o evento de FocusIn para remover o placeholder quando o usuário clicar ou selecionar a entry
    entry.bind('<FocusIn>', focus_in_lambda)

    # configura o evento para colocar novamente o placeholder caso o usuário deselecione a entry sem inserir nenhum texto
    entry.bind('<FocusOut>', lambda _, e=entry, f=focus_in_lambda: [no_value_lambda(_, e), e.bind('<FocusIn>', f)] if len(e.get()) == 0 else None)


def create_dropdown(frame_parent, r, c, options, event, command, callback=lambda _, __, ___:None):
    from tkinter import StringVar, OptionMenu
    from Events import unregister_all,register
    
    var = StringVar()
    var.set(options[0])
    var.trace_add('write', callback)

    unregister_all(event)
    register(event, lambda v=var: command(v.get()))

    dropdown = OptionMenu(frame_parent, var, *options)
    dropdown.grid(row=r, column=c, padx=5, pady=10, sticky='w', ipadx=30, ipady=6)

    return dropdown
    

# Adiciona a funcionalidade de editar uma label. Ao clicar, uma entry é criada por cima da label, 
# inicializada com o valor especificado e configurada para chamar o callback especificado ao apertar Enter, Tab ou clicar fora da entry 
def bind_edit_label (frame_group, label, initial_value, font, r, c, entry_callback):

    entry = criar_entry(frame_group, font, 0, 0, 'ew', r, c, 'center')
    entry.config(highlightthickness=0, bd=0)
    entry.insert('0', initial_value)
    entry.focus()

    from tkinter import EventType
    lambda_close = lambda event, save, lbl=label, e=entry: [entry_callback(lbl, e) if save else None, e.destroy()]

    def validate_event (event, label):
        if event.type is not EventType.ButtonPress: return True
        print(label.winfo_containing(event.x, event.y))
        return label.winfo_containing(event.x, event.y)


    [entry.bind(i, lambda _: lambda_close(_, True)) for i in ['<Return>', '<FocusOut>', '<Tab>']]
    entry.bind('<Escape>', lambda _: lambda_close(_, False))

    label.winfo_toplevel().bind('<Button-1>', lambda _, lbl=label, l=lambda_close: [l(_, True), lbl.winfo_toplevel().unbind('<Button-1>')])

    return entry