# -*- coding: utf-8 -*-

from flask_script import Manager, Server

from app import create_app

app = create_app()
manager = Manager(app)

manager.add_command("serve", Server(host="0.0.0.0"))

if __name__ == '__main__':
    manager.run()

