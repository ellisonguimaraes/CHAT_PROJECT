from flask import Flask, request, abort, render_template, redirect
import requests
from configure_data import *
from Repository.Repository import MessageRepository, UserRepository
from Models.Message import Message
import datetime as dt
from random import choice
from Models.User import User


app = Flask("sd_chat", template_folder="Templates", static_folder="static")


@app.route("/", methods=["GET"])
@app.route("/<id>", methods=["GET"])
def homepage(id=None):
    users = [i for i in UserRepository.get_all() if i.name != MY_NAME + '.' + TYPE_SERVICE]

    if id is None:
        return render_template('index_empty.html', users=users)

    else:
        user = UserRepository.get(id)

        if user is None:
            abort(400)

        messages = MessageRepository.get_all(user.id)

        return render_template('index.html', users=users, user=user, messages=messages)


@app.route("/<id>", methods=["POST"])
def send_message(id):
    search_message = request.form["searchMessage"]
    date = dt.datetime.now()

    if search_message:
        message = Message(None, search_message, date, id, 0)

        message_dict = {
            'msg': message.msg,
            'date': str(message.date)
        }

        user = UserRepository.get(id)

        res = requests.post(f'http://{user.ip}:{user.port}/message/' + MY_NAME, json=message_dict)

        print(res.text)

        MessageRepository.save(message)

    return redirect('/'+id)


@app.route("/message/<name>", methods=["POST"])
def message(name):
    body = request.get_json()
    user = UserRepository.get_by_name(name)

    if user is not None:
        m = Message(None, body['msg'], dt.datetime.strptime(body['date'], "%Y-%m-%d %H:%M:%S.%f"), user.id, 1)
        MessageRepository.save(m)
        return "OK"
    else:
        return abort(400)


if __name__ == "__main__":
    app.run(host=MY_IP, port=MY_PORT, debug=True)
