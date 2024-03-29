from Front.Core import *

# Informações do modulo
NAME = 'Dashboard'
REQUIRED_PERMISSIONS_REG = [None]        
REQUIRED_PERMISSIONS_RATE = [None]
REQUIRED_PERMISSIONS_VIEW = [11]

frame_charts_parent = None
# esses parâmetros são dados de quem está logando
#  user_id, user_role, user_group
def run(frame_parent):
    
    from Front.Scrollbar import add_scrollbar
    from tkinter import Frame, Label

    frame_parent = Frame(frame_parent, background = co0)
    frame_parent.columnconfigure(0, weight = 1)
    frame_parent.rowconfigure(0, weight = 1)
    frame_parent.grid(row= 0, column=0, sticky='news')
    
    frame_parent = add_scrollbar(frame_parent)

    frame_parent.rowconfigure(0, weight=2)
    frame_parent.rowconfigure(1, weight=2)

    # criar widgets ###quadro é se seá colocado na janela ou em frame
    def criar_label(quadro, text, font, r, c, name=None, background=co0, fg=co2):
        label = Label(quadro, text=text, font=font, background=background, fg=fg)
        label.grid(row=r, column=c, padx=5, pady=3, sticky = "w")
        return label

    frame_title = criar_frame(frame_parent, 0, 0, "ew",co3, px= 0, py=0)
    frame_title.columnconfigure(0,weight=1)
    criar_label(frame_title, "Dashboards", "Calibri, 24 bold", 0, 0, None, co3, co0)

    frame_legenda = criar_frame(frame_parent, 1, 0, 'nw', hlbg=co3, hlt=1, px=0, py=0)
    from Models.id_criteria import criteria, criteria_full

    criar_label(frame_legenda, 'Critérios Avaliativos', 'Calibri, 12 bold', 0,0)
    for i in range(len(criteria)):
        criar_label(frame_legenda, f'{criteria[i]} - {criteria_full[i]}', 'Calibri 10', i%2 + 1, i//2)

    from Authentication import CURRENT_USER

    global frame_charts_parent
    frame_charts_parent = criar_frame(frame_parent, 2, 0)

    if CURRENT_USER.role_id in [1, 2]:
        
        from Models.Group import get_groups_of_instructor, get_group_of_name
        from Authentication import CURRENT_USER
        create_dropdown(
            criar_frame(frame_title, 0, 1, "ew", co3, px=12, py=0), 0, 0, 
            [i.name for i in get_groups_of_instructor(CURRENT_USER.id)], 
            'get_group_id', lambda v: get_group_of_name(v).id, lambda _, __, ___: create_charts_instructor()
        )

        create_charts_instructor()

    
    if CURRENT_USER.role_id in [3, 4, 5]:
        frame_charts = criar_frame(frame_charts_parent, 0, 0)

        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from graficos import Charts

        figure1 = Charts.user_media_sprints(CURRENT_USER.id)
        canvas = FigureCanvasTkAgg(figure1, master = frame_charts)
        canvas.get_tk_widget().grid(row=0, column=0, sticky='wens')

        figure2 = Charts.user_media_x_team(CURRENT_USER.id)
        canvas = FigureCanvasTkAgg(figure2, master = frame_charts)
        canvas.get_tk_widget().grid(row=1, column=0, sticky='wens')
        
        if CURRENT_USER.role_id in [3, 4]:
            figure3 = Charts.team_media_x_group(CURRENT_USER.team_id)
            canvas = FigureCanvasTkAgg(figure3, master = frame_charts)
            canvas.get_tk_widget().grid(row=2, column=0, sticky='wens')

            figure4 = Charts.users_media_team(CURRENT_USER.team_id)
            canvas = FigureCanvasTkAgg(figure4, master = frame_charts)
            canvas.get_tk_widget().grid(row=3, column=0, sticky='wens')

    frame_bandaid = criar_frame(frame_parent, 3, 0)
    frame_bandaid.grid(sticky='news')
    frame_bandaid.columnconfigure(0, minsize = 0, weight = 1)
    frame_bandaid.rowconfigure(0, minsize = 0, weight = 1)
    criar_label(frame_bandaid, '                                  ', 'Calibri 24', 0,0)
    criar_label(frame_bandaid, '                                  ', 'Calibri 24', 1,0)


def create_charts_instructor():

    # deleta o frame_charts caso já exista
    children = frame_charts_parent.winfo_children()
    if children is not None and len(children) > 2 and children[2] is not None:
        children[2].destroy()

    from Authentication import CURRENT_USER
    from Models.Group import get_group
    from Events import trigger

    id = trigger('get_group_id')
    # print(f'trigger(\'get_group_name\'): {id}')

    group = get_group(id)

    frame_charts = criar_frame(frame_charts_parent, 0, 0)
    frame_charts.grid(sticky = 'news')
    frame_charts.columnconfigure(0, minsize = 0, weight = 1)
    frame_charts.rowconfigure(0, minsize = 0, weight = 1)

    print(f'get_group(id): {group}')
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from graficos import Charts

    figure1 = Charts.teams_media(group.id)
    canvas = FigureCanvasTkAgg(figure1, master = frame_charts)
    canvas.get_tk_widget().grid(row=0, column=0, sticky='wens')

    if group.leader_id == CURRENT_USER.id:

        figure2 = Charts.role_media(3, group.id)
        canvas = FigureCanvasTkAgg(figure2, master = frame_charts)
        canvas.get_tk_widget().grid(row=1, column=0, sticky='wens')
    if group.client_id == CURRENT_USER.id:

        figure2 = Charts.role_media(4, group.id)
        canvas = FigureCanvasTkAgg(figure2, master = frame_charts)
        canvas.get_tk_widget().grid(row=1, column=0, sticky='wens')

    figure3 = Charts.group_media_x_groups(group.id)
    canvas = FigureCanvasTkAgg(figure3, master = frame_charts)
    canvas.get_tk_widget().grid(row=2, column=0, sticky='wens')
