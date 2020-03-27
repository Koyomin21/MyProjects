import json
def new_user(user):
    with open('passed_test.json')as f:
        temp = json.load(f)

    users = dict(temp.items())

    users[user.name] = {"score" : user.score,"total" : user.total}

    with open('passed_test.json','w') as f:
        json.dump(users,f)
    

def get_questions():
    with open("questions.json")as file:
        templates = json.load(file)

    questions = list(templates.items())
    return questions


def send_res(user):
    with open('passed_test.json') as f:
        tmp = json.load(f)
    
    newUser = True
    
    for i in tmp.items():
        if i[0] == user.name:
            if i[1]['score'] < user.score:
                i[1]['score'] = user.score
                i[1]['total'] = user.total
            newUser = False
            break
    if newUser:
        new_user(user)
    else:
        result = dict(tmp.items())
        with open('passed_test.json','w') as f:
            json.dump(result,f)