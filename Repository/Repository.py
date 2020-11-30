import sqlite3
from Models.User import User
from Models.Message import Message
from datetime import datetime


class UserRepository:
    @staticmethod
    def save(user):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO User (name, ip, port, status) VALUES (?, ?, ?, ?)",
                       (user.name, user.ip, user.port, user.status))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        all_users = []

        cursor.execute("SELECT * FROM User;")

        for l in cursor.fetchall():
            user = User(l[0], l[1], l[2], l[3], l[4])
            all_users.append(user)

        conn.close()

        return all_users

    @staticmethod
    def update(user):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE User
            SET name = ?, ip = ?, port = ?, status = ?
            WHERE id = ?
        """, (user.name, user.ip, user.port, user.status, user.id))

        conn.commit()
        conn.close()

    @staticmethod
    def delete(id):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM User
            WHERE id = ?
        """, (id,))

        conn.commit()
        conn.close()

    @staticmethod
    def get_by_name(name):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM User WHERE name LIKE ?", ("%" + name + "%",))
        result = cursor.fetchone()
        conn.close()

        if result is not None:
            return User(result[0], result[1], result[2], result[3], result[4])

        return None

    @staticmethod
    def get(id):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM User WHERE id == ?", (id,))
        result = cursor.fetchone()
        conn.close()

        if result is not None:
            return User(result[0], result[1], result[2], result[3], result[4])

        return None


class MessageRepository:
    @staticmethod
    def save(message):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Message (msg, date, id_user, recv) VALUES (?, ?, ?, ?)",
                       (message.msg, message.date, message.id_user, message.recv))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all(id:None):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        all_messages = []

        if id is None:
            cursor.execute("SELECT * FROM Message;")
        else:
            cursor.execute("SELECT * FROM Message WHERE id_user = ?", (id,))

        for l in cursor.fetchall():
            message = Message(l[0], l[1], l[2], l[3], l[4])
            all_messages.append(message)

        conn.close()

        return all_messages

    @staticmethod
    def update(message):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Message
            SET msg = ?, date = ?, id_user = ?, recv = ?
            WHERE id = ?
        """, (message.msg, message.date, message.id_user, message.recv, message.id))

        conn.commit()
        conn.close()

    @staticmethod
    def delete(id):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM Message
            WHERE id = ?
        """, (id,))

        conn.commit()
        conn.close()


if __name__ == "__main__":

    conn = sqlite3.connect("../database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE User (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(200) NOT NULL,
            ip VARCHAR(30) NOT NULL,
            port INTEGER NOT NULL,
            status INTEGER NOT NULL
        );
    """)

    cursor.execute("""
            CREATE TABLE Message (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                msg TEXT NOT NULL,
                date DATE NOT NULL,
                id_user INTEGER,
                recv INTEGER,
                FOREIGN KEY(id_user) REFERENCES User(id)
            );
    """)
    '''
    UserRepository.save(User(None, "Rebeca", "192.168.1.150", 4890, 0))
    UserRepository.save(User(None, "Ellison", "192.168.1.101", 5050, 1))

    MessageRepository.save(Message(None, "Olá, tudo bem?", datetime.now(), 1, 1))
    MessageRepository.save(Message(None, "To bem sim! e você?", datetime.now(), 1, 0))
    MessageRepository.save(Message(None, "Estou bem :3", datetime.now(), 1, 1))
    MessageRepository.save(Message(None, "Que ótimo!", datetime.now(), 1, 0))
    
    conn.commit()
    conn.close()
    '''
