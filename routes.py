from flask import Flask, request, abort, render_template
from main import MY_IP, MY_PORT
from Repository.Repository import MessageRepository, UserRepository
from Models.Message import Message
import datetime as dt
from random import choice
from Models.User import User


app = Flask("sd_chat", template_folder="Templates", static_folder="static")

"""
@app.route("/", methods=["GET"])
def homepage():
    users_list = UserRepository.get_all()
    return render_template('index.html', users=users_list)
"""
@app.route("/<id>", methods=["GET"])
def homepage(id):
    users = UserRepository.get_all()

    user = UserRepository.get(id)

    if user is None:
        abort(400)

    messages = MessageRepository.get_all(user.id)

    return render_template('index.html', users=users, user=user, messages=messages)


@app.route("/message/<name>", methods=["POST"])
def message(name):
    body = request.get_json()
    user = UserRepository.get_by_name(name)

    if user is not None:
        m = Message(None, body['msg'], dt.datetime.strptime(body['date'], "%Y-%m-%d %H:%M:%S.%f"), user.id)
        MessageRepository.save(m)
        return "OK"
    else:
        return abort(400)


if __name__ == "__main__":
    app.run(host=MY_IP, port=MY_PORT, debug=True)