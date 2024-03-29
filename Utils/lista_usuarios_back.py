
# função para acessar os users
def get_users(user, group_id):
    if user == None: return

    from Models.Role import get_role
    from Models.User import get_users_of_team, get_users_of_group
    from Models.Rating import get_ratings
    from Models.Sprint import current_rating_period, next_rating_period
    from Models.Group import get_group

    sprint = current_rating_period(group_id)
    if sprint == None: 
        sprint = next_rating_period(group_id)
    if sprint == None: return [[], []]
    

    #pego o nome e funções da pessoa que logou
    role = get_role(user.role_id)
    
    #lista com as linhas da tabela ratings que correspondem a avaliações do usuário logado
    ratings = get_ratings(from_user_id=user.id, sprint_id=sprint.id)

    # for rating in ratings:
    #     print(rating)

    # ratings = get_ratings_from_user(user.id)
    grade_submitted = []
    grade_to_submit = []
    
    if user.role_id in [3, 4, 5]:
        # retorna lista com todos os usuários que são do mesmo time que o logado
        rate_users = get_users_of_team(user.team_id)
        
        for member in rate_users:
            if ratings is None or len(ratings) < 1:
                grade_to_submit.append(member)
                continue
            for rating in ratings:
                if member.id == rating.to_user_id:
                    grade_submitted.append(member)
                    break
            else:
                grade_to_submit.append(member)
        return [grade_to_submit, grade_submitted]

    group = get_group(group_id)
    role = get_role(1) if group.leader_id == user.id else get_role(2) if group.client_id == user.id else None
    if role is None: return

    rate_users = get_users_of_group(group_id)
    for group_member in rate_users:
        if group_member.role_id not in role.permissions_rate or group_member.team_id == '': continue
        if ratings is None or len(ratings) < 1:
            grade_to_submit.append(group_member)
            continue
        for rating in ratings:
            if group_member.id == rating.to_user_id and rating.value != '':
                grade_submitted.append(group_member)
                break
        else:
            grade_to_submit.append(group_member)
    return [grade_to_submit, grade_submitted]



def get_feedbacks(user_id, sprint_id):
    feedbacks = []
    from Models.Rating import get_ratings
    ratings = get_ratings(to_user_id=user_id, sprint_id=sprint_id)
    for rating in ratings:
        feedback = []
        if rating.value <= 3:
            feedback.append(rating.criteria_id)
            feedback.append(rating.comment)
            feedbacks.append(feedback)
    return feedbacks





















