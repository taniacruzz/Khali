from datetime import date
from Authentication import *


def create_test_data():
    from Settings import USERS_PATH, GROUPS_PATH, SPRINTS_PATH, TEAMS_PATH, RATINGS_PATH
    from CSV.CSVHandler import delete_csv

    delete_csv(USERS_PATH)
    delete_csv(GROUPS_PATH)
    delete_csv(SPRINTS_PATH)
    delete_csv(TEAMS_PATH)
    delete_csv(RATINGS_PATH)

    # cadastra o ADM
    register("A de Emmy",  "a@d.m",                None, None, 0,    custom_password='123')

    ni = ['', ' Second', ' Third', ' Fourth']
    ei = ['', 's', 't', 'f']

    # Cria 2 LdG e FC
    leader_ids = [register("Joao LG" +ni[i], ei[i]+"l@d.g", None, None, 1, custom_password='123') for i in range(2)]
    client_ids = [register("Clara FC"+ni[i], ei[i]+"c@c.c", None, None, 2, custom_password='123') for i in range(2)]

    # pra cada grupo
    for i in range(4):

        from Models.Group import create_group

        # cadastra time utilizando o id do lider do grupo e cliente recem cadastrados
        create_group("Grupo dos Devs"+ni[i], leader_ids[i//2], client_ids[i//2])

        from Models.Team import create_team

        # cria times no primeiro grupo
        t = [
            create_team("first team"+str(i), i),
            create_team("second team"+str(i), i),
            create_team("third team"+ni[i], i)
        ]

        #           nome             email                  grupo  time    role        senha
        # LTs
        register("Moacir LTum"+ni[i],      ei[i]+"lt1@o.com",         i,    t[0],    3,    custom_password='123')
        register("Maria LTdois"+ni[i],     ei[i]+"lt2@o.com",         i,    t[1],    3,    custom_password='123')
        register("Ana LTtres"+ni[i],       ei[i]+"lt3@o.com",         i,    t[2],    3,    custom_password='123')

        # POs
        register("Diego POum"+ni[i],       ei[i]+"po-um@o.com",       i,    t[0],    4,    custom_password='123')
        register("Caio POdois"+ni[i],      ei[i]+"po-dois@o.com",     i,    t[1],    4,    custom_password='123')
        register("Maira POtres"+ni[i],     ei[i]+"po-tres@o.com",     i,    t[2],    4,    custom_password='123')

        # devs
        register("Felipe Dev"+ni[i],       ei[i]+"d@e.v",             i,    t[0],    5,    custom_password='123')
        register("Dora Dev"+ni[i],         ei[i]+"dora@dev.com",      i,    t[0],    5,    custom_password='123')
        register("Lucas Dev"+ni[i],        ei[i]+"luc@dev.com",       i,    t[0],    5,    custom_password='123')
        register("Matheus Dev"+ni[i],      ei[i]+"mat@dev.dev",       i,    t[1],    5,    custom_password='123')
        register("Lais Dev"+ni[i],         ei[i]+"dev-lais@dev.com",  i,    t[1],    5,    custom_password='123')
        register("Lara Dev"+ni[i],         ei[i]+"dlara@dev.com",     i,    t[1],    5,    custom_password='123')
        register("Ignacio Dev"+ni[i],      ei[i]+"na-dev@dev.com",    i,    t[2],    5,    custom_password='123')
        register("Marcia Dev"+ni[i],       ei[i]+"marcia@dev.com",    i,    t[2],    5,    custom_password='123')
        register("Olga Dev"+ni[i],         ei[i]+"ol@dev.com",        i,    t[2],    5,    custom_password='123')

        from Models.User import get_users_of_team
        from Models.Team import get_teams_of_group
        from Models.Sprint import create_sprint
        from Models.Rating import create_rating
        from Models.id_criteria import criteria
        from random import randint

        # pega o id dos usuários do grupo i que foram cadrastados
        teams = [x.id for x in get_teams_of_group(i)]

        total_ratings = 5 * 4 * sum([len(get_users_of_team(t)) ** 2 for t in teams])
        current_rating_count = 0

        sprint_dates = [
            [date(2022, 8,  29), date(2022, 9,  18)],
            [date(2022, 9,  19), date(2022, 10,  9)],
            [date(2022, 10, 17), date(2022, 11,  14)],
            [date(2022, 11,  15), date(2022, 11, 27)]
        ]

        # pra cada sprint
        for sprint in range((4 * i), 4 + (4 * i)):

            # cria a sprint
            create_sprint(i, sprint_dates[sprint % 4][0], sprint_dates[sprint % 4][1], 5)

            for team_id in teams:
                users_of_team = [user.id for user in get_users_of_team(team_id)]

                # pra cada usuário do grupo
                for from_user_id in users_of_team:

                    # pra cada usuário do grupo novamente
                    for to_user_id in users_of_team:

                        # pra cada critério de avaliação
                        for criterio in range(len(criteria)):

                            # cria uma nota aleatória entre 1 (inclusivo) e 6 (exclusivo)
                            nota = randint(1, 5)

                            current_rating_count += 1
                            percent = (current_rating_count/(total_ratings))

                            # printa a avaliação que será criada
                            print(f'grupo {i}: {int(percent*100)}% |Criando avaliação teste: id({from_user_id}) avalia id({to_user_id}) na sprint {sprint} e critério {criterio} com a nota {nota}')

                            # cria a avaliação
                            create_rating(from_user_id, to_user_id, sprint, criterio, nota, 'feedback')


    # print do sucesso
    print("Geração de dados teste finalizada!")

