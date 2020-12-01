import requests
import datetime as dt
import threading as th
from flask import Flask, request, abort, render_template, redirect
from configure_data import MY_IP, MY_PORT, MY_NAME, TYPE_SERVICE
from repository.repository import MessageRepository, UserRepository
from models.message import Message


app = Flask("sd_chat", template_folder="templates", static_folder="static")


@app.route("/", methods=["GET"])
@app.route("/<id>", methods=["GET"])
def homepage(id=None):
    user_local = UserRepository.get_by_name(MY_NAME)

    users = sorted([i for i in UserRepository.get_all() if i.name != MY_NAME + '.' + TYPE_SERVICE],
                   key=lambda x: x.status, reverse=True)

    if id is None:
        messages = list(filter(lambda x: x.is_group == 1, MessageRepository.get_all()))
        return render_template('group_page.html', user_local=user_local, users=users, messages=messages)
    else:
        user_other = UserRepository.get(id)

        if user_other is None:
            abort(400)

        messages = list(filter(lambda x: x.id_user == user_other.id and x.is_group == 0, MessageRepository.get_all()))

        return render_template('index.html', user_local=user_local, users=users, messages=messages, user_other=user_other)


@app.route("/message/<name>", methods=["POST"])
@app.route("/message/<name>/<group>", methods=["POST"])
def message(name, group=None):
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
    search_message = request.form["searchMessage"]

    m = Message(id=None,
                msg=search_message,
                date=dt.datetime.now(),
                id_user=id_receiver,
                is_recv=0,
                is_group=0)

    message_dict = {
        'msg': m.msg,
        'date': str(m.date)
    }

    user_receiver = UserRepository.get(id_receiver)

    if user_receiver.status == 1:
        res = requests.post(f'http://{user_receiver.ip}:{user_receiver.port}/message/' + MY_NAME, json=message_dict)
        print(res.text)

        MessageRepository.save(m)

    return redirect('/' + id_receiver)


@app.route("/send_message/group", methods=["POST"])
def send_message_group():
    search_message = request.form["searchMessage"]

    m = Message(id=None,
                msg=search_message,
                date=dt.datetime.now(),
                id_user=UserRepository.get_by_name(MY_NAME).id,
                is_recv=0,
                is_group=1)

    message_dict = {
        'msg': m.msg,
        'date': str(m.date)
    }

    users_receiver = UserRepository.get_all()

    for u in [ur for ur in users_receiver if (ur.name != MY_NAME+'.'+TYPE_SERVICE) and ur.status == 1]:
        t = th.Thread(target=post_request, args=(u, message_dict))
        t.start()

    MessageRepository.save(m)

    return redirect('/')


@app.template_filter()
def get_name(m):
    return list(filter(lambda x: x.id == m.id_user, UserRepository.get_all()))[0].name.split('.')[0]


def post_request(u, message_dict):
    res = requests.post(f'http://{u.ip}:{u.port}/message/' + MY_NAME + '/1', json=message_dict)
    print(res.text)


def execute_server_flask():
    app.run(host=MY_IP, port=MY_PORT, debug=False)


if __name__ == "__main__":
    app.run(host=MY_IP, port=MY_PORT, debug=True)