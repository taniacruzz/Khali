from tkinter import *
from Settings import co0

def add_scrollbar (target_frame, bg=co0, bd=3):

    # cria um frame dentro do target_frame, que é a frame "root"
    frm_main = Frame(target_frame, bg=bg)
    frm_main.columnconfigure(0, minsize=1, weight=1)
    frm_main.rowconfigure(0, minsize=0, weight=1)
    frm_main.grid(row=0, column=0, sticky='news')

    # cria um canvas dentro do frame
    canvas = Canvas(frm_main, bg=bg)
    canvas.columnconfigure(0, minsize=0, weight=1)
    canvas.rowconfigure(0, minsize=0, weight=1)
    canvas.grid(row=0, column=0, sticky='news')
    # canvas.config(bg='red')

    # canvas.grid_columnconfigure(0, minsize=0, weight=1)
    # canvas.grid_rowconfigure(0, minsize=0, weight=1)

    # inicializa a scrollbar
    scrollbar_ver=Scrollbar(frm_main, orient=VERTICAL, command=canvas.yview)
    scrollbar_ver.grid(row=0, column=1, sticky='nse')

    # configura o canvas com o comando da scrollbar
    canvas.configure(yscrollcommand=scrollbar_ver.set)

    # expande os widgets dentro do canvas para preencher todo o espaço disponivel 
    def canvas_configure(event):
        canvas = event.widget
        canvas.itemconfigure(1, width=canvas.winfo_width())
        canvas.itemconfigure(2, height=canvas.winfo_height()-4)
    canvas.bind("<Configure>", canvas_configure)

    # cria outro Frame dentro do Canvas
    module_frame=Frame(canvas, bg=bg, relief = FLAT, bd = bd)
    module_frame.columnconfigure(0, minsize = 0, weight = 1)
    module_frame.rowconfigure(0, minsize = 0, weight = 1)
    module_frame.grid(row=0, column=0, sticky="nsew")

    # frame secundário que define uma altura minima para a tela
    # impede o canvas de scrollar caso module_frame não seja grande o suficiente para ocupar o espaço de uma tela
    frame_min_size_height=Frame(canvas, bg=None)
    frame_min_size_height.columnconfigure(0, minsize = 0, weight = 1)
    frame_min_size_height.rowconfigure(0, minsize = 0, weight = 1)
    frame_min_size_height.grid(row=0, column=0, sticky="nsew")

    module_frame.bind('<Configure>', lambda _: canvas.configure(scrollregion=canvas.bbox('all')))

    # adicionar a nova frame a uma janela no canvas
    canvas.create_window((0,0), window=module_frame, anchor='nw')
    canvas.create_window((0,0), window=frame_min_size_height, anchor='nw')

    # adiciona um evento ao module_frame para permitir rolagem com scroll wheel enquanto o mouse estiver sobre ele
    module_frame.bind('<Enter>', lambda _: canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units")))
    module_frame.bind('<Leave>', lambda _: canvas.unbind_all("<MouseWheel>"))

    # registra uma reação para descadastrar o comando de mousewheel do canvas caso um sub modulo seja aberto
    from Events import register
    register('sub_module_open', lambda c=canvas: c.unbind_all('<MouseWheel>'))

    # retorna o novo frame onde estará o conteudo da tela
    return module_frame
