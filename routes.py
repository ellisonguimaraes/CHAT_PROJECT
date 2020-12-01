import requests
import datetime as dt
import threading as th
from flask import Flask, request, abort, render_template, redirect
from configure_data import MY_IP, MY_PORT, MY_NAME, TYPE_SERVICE
from repository.repository import MessageRepository, UserRepository, CheckMessageRepository
from models.message import Message
from models.check_message import CheckMessage


app = Flask("sd_chat", template_folder="templates", static_folder="static")


@app.route("/", methods=["GET"])
@app.route("/<id>", methods=["GET"])
def homepage(id=None):
    """
    Rotas de acesso as pages de conversa.
    :param id: ID do User na qual quer acessar a conversa.
    :return: Se id=None, a página de chat geral é retornada.
            Se id!=None, a página específica de um User é retornada
    """
    user_local = UserRepository.get_by_name(MY_NAME)

    # Return Users List, except the current user (Descending order ~ Users Online First)
    users = sorted([i for i in UserRepository.get_all() if i.name != MY_NAME + '.' + TYPE_SERVICE],
                   key=lambda x: x.status, reverse=True)

    # If id is none, return general chat page
    if id is None:
        messages = list(filter(lambda x: x.is_group == 1, MessageRepository.get_all()))
        return render_template('group_page.html', user_local=user_local, users=users, messages=messages)
    else:
        # If id is not none, return specific page
        user_other = UserRepository.get(id)

        if user_other is None:
            abort(400)

        # Get messages (by id_user)
        messages = list(filter(lambda x: x.id_user == user_other.id and x.is_group == 0, MessageRepository.get_all()))

        return render_template('index.html', user_local=user_local, users=users, messages=messages, user_other=user_other)


@app.route("/message/<name>", methods=["POST"])
@app.route("/message/<name>/<group>", methods=["POST"])
def message(name, group=None):
    """
    Método no qual outras aplicações enviarão os POST's, seja pro chat geral ou para o específico.
    Esse método formata o JSON até ser armazenado no banco de dados.
    :param name: Name service da pessoa que está realizando o POST nessa aplicação.
    :param group: Flag de identificação se a mensagem é para o Chat Geral. (se 1 é chat geral)
    :return: Retorna "OK" se o POST for realizado com sucesso, ou abort(400) se o usuário que enviar
                não fazer parte do Users.
    """
    body = request.get_json()
    user_sent = UserRepository.get_by_name(name)

    if user_sent is not None:
        m = Message(id=None,
                    msg=body['msg'],
                    date=dt.datetime.strptime(body['date'], "%Y-%m-%d %H:%M:%S.%f"),
                    id_user=user_sent.id,
                    is_recv=1)

        if group is not None:
            m.is_group = 1
        else:
            m.is_group = 0

        MessageRepository.save(m)

        return "OK"
    else:
        return abort(400)


@app.route("/send_message/<id_receiver>", methods=["POST"])
def send_message(id_receiver):
    """
    Método responsável por formatar e abrir uma thread para enviar o POST ao método message do outro User.
    :param id_receiver: ID do User que vai receber a mensagem.
    :return: Redirect('/' + id_receiver), ou seja, redireciona para a página do chat específica do usuário id_receiver
    """
    search_message = request.form["searchMessage"]
    user_receiver = UserRepository.get(id_receiver)

    m = Message(id=None,
                msg=search_message,
                date=dt.datetime.now(),
                id_user=id_receiver,
                is_recv=0,
                is_group=0)

    id_message = MessageRepository.save(m)

    message_dict = {
        'msg': m.msg,
        'date': str(m.date)
    }

    # Create thread with post_request method
    t = th.Thread(target=post_request,
                  args=(user_receiver.id,
                        id_message,
                        f'http://{user_receiver.ip}:{user_receiver.port}/message/' + MY_NAME,
                        message_dict))
    t.start()

    return redirect('/' + id_receiver)


@app.route("/send_message/group", methods=["POST"])
def send_message_group():
    """
    Método responsável por formatar e abrir uma thread para enviar o POST ao método message de TODOS os User's.
    :return: Redirect('/'), ou seja, redireciona para a página do chat GERAL.
    """
    search_message = request.form["searchMessage"]
    users_receiver = UserRepository.get_all()

    m = Message(id=None,
                msg=search_message,
                date=dt.datetime.now(),
                id_user=UserRepository.get_by_name(MY_NAME).id,
                is_recv=0,
                is_group=1)

    id_message = MessageRepository.save(m)

    message_dict = {
        'msg': m.msg,
        'date': str(m.date)
    }

    # Iterate all User's (except current user), create threads for each user.
    for u in [ur for ur in users_receiver if (ur.name != MY_NAME+'.'+TYPE_SERVICE)]:
        t = th.Thread(target=post_request,
                      args=(u.id,
                            id_message,
                            f'http://{u.ip}:{u.port}/message/' + MY_NAME + '/1',
                            message_dict))
        t.start()

    return redirect('/')


@app.template_filter()
def get_name(m):
    """
    Utilizado pela view.
    Este método recebe uma mensagem (tipo Message) e retorna o nome do serviço do usuário com base no
    id_user do Message.
    :param m: Receive Message
    :return: Return user NameService, based to Message(id_user).
    """
    return list(filter(lambda x: x.id == m.id_user, UserRepository.get_all()))[0].name.split('.')[0]


@app.template_filter()
def get_verification(m):
    """
    Utilizado pela view.
    Este método recebe uma mensagem (tipo Message), e retorna TRUE se todas as mensagens chegaram
    ao destinatário com sucesso, FALSE se uma única mensagem não chegou ao destinatário.
    :param m: Receive Message
    :return: Return:
        True ~ if all checks is True
        False ~ if as single check is false
    """
    checks = list(filter(lambda x: x.id_message == m.id, CheckMessageRepository.get_all()))

    for c in checks:
        if c.is_check != 1:
            return False

    return True


def post_request(id_user, id_message, url, message_dict):
    """
    Método executado pela thread para envio das mensagens via POST
    :param id_user: User Id
    :param id_message: Message Id
    :param url: Post URL
    :param message_dict: Data dictionary (JSON body)
    """
    try:
        res = requests.post(url, json=message_dict)
        if res.text.upper() == "OK":
            CheckMessageRepository.save(CheckMessage(None, id_user, id_message, 1))
        else:
            CheckMessageRepository.save(CheckMessage(None, id_user, id_message, 0))

        print(res.text)
    except:
        print(f"Não foi possível enviar a mensagem para o user: {id_user}")
        CheckMessageRepository.save(CheckMessage(None, id_user, id_message, 0))


def execute_server_flask():
    """
    Método de execução do app Flask (debug=False)
    """
    app.run(host=MY_IP, port=MY_PORT, debug=False)


if __name__ == "__main__":
    app.run(host=MY_IP, port=MY_PORT, debug=True)