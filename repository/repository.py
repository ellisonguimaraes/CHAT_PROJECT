import sqlite3
from models.user import User
from models.message import Message
from models.check_message import CheckMessage


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
        cursor.execute("INSERT INTO Message (msg, date, id_user, is_recv, is_group) VALUES (?, ?, ?, ?, ?)",
                       (message.msg, message.date, message.id_user, message.is_recv, message.is_group))

        conn.commit()
        conn.close()

        return cursor.lastrowid

    @staticmethod
    def get_all():
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        all_messages = []

        cursor.execute("SELECT * FROM Message;")

        for m in cursor.fetchall():
            message = Message(m[0], m[1], m[2], m[3], m[4], m[5])
            all_messages.append(message)

        conn.close()

        return all_messages

    @staticmethod
    def update(message):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Message
            SET msg = ?, date = ?, id_user = ?, is_recv = ?, is_group = ?
            WHERE id = ?
        """, (message.msg, message.date, message.id_user, message.recv, message.is_group, message.id))

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


class CheckMessageRepository:
    @staticmethod
    def save(check):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO CheckMessage (id_user, id_message, is_check) VALUES (?, ?, ?)",
                       (check.id_user, check.id_message, check.is_check))

        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        all_checks = []

        cursor.execute("SELECT * FROM CheckMessage;")

        for m in cursor.fetchall():
            check = CheckMessage(m[0], m[1], m[2], m[3])
            all_checks.append(check)

        conn.close()

        return all_checks

    @staticmethod
    def update(check):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE CheckMessage
            SET is_check = ?
            WHERE id = ?
        """, (check.is_check, check.id))

        conn.commit()
        conn.close()

    @staticmethod
    def delete(id):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM CheckMessage
            WHERE id = ?
        """, (id,))

        conn.commit()
        conn.close()


if __name__ == "__main__":
    # Create Database
    conn = sqlite3.connect("../database.db")
    cursor = conn.cursor()

    # Create table User
    cursor.execute("""
        CREATE TABLE User (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(200) NOT NULL UNIQUE,
            ip VARCHAR(30) NOT NULL,
            port INTEGER NOT NULL,
            status INTEGER NOT NULL
        );
    """)

    # Create table Message
    cursor.execute("""
        CREATE TABLE Message (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            msg TEXT NOT NULL,
            date DATE NOT NULL,
            id_user INTEGER,
            is_recv INTEGER NOT NULL,
            is_group INTEGER NOT NULL,
            FOREIGN KEY(id_user) REFERENCES User(id)
        );
    """)

    # Create table CheckMessage
    cursor.execute("""
        CREATE TABLE CheckMessage (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER NOT NULL,
            id_message INTEGER NOT NULL,
            is_check INTEGER NOT NULL,
            FOREIGN KEY(id_user) REFERENCES User(id),
            FOREIGN KEY(id_message) REFERENCES Message(id)
        )
    """)

    conn.commit()
    conn.close()

