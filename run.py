from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from os import environ



from app import create_app, db

app = create_app()

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)



def start_ngrok():
    from pyngrok import ngrok

    url = ngrok.connect(5000)
    print("Starting Ngrok URL tunnel please wait..")
    print("http url tunnel for ngrok: {}".format(url))


if __name__ == '__main__':
    manager.run()
