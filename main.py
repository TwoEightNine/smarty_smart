from flask import Flask, request, abort, send_file
from flask_sqlalchemy import SQLAlchemy
import utils
import json
import logging
import os
import cry
from keys import *

HOST = 'localhost'
PORT = 1753

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'smarty.db')
db_uri = 'sqlite:///%s' % db_path
app.config.from_pyfile('app.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)


class SeedStorage(db.Model):

    seed = db.Column('seed', db.String(32), primary_key=True)
    time_stamp = db.Column('time_stamp', db.Integer)

    def __init__(self, seed):
        self.seed = seed
        self.time_stamp = utils.get_time()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '[%s (%d)]' % (self.seed, self.time_stamp)

    def is_expired(self):
        return utils.get_time() - self.time_stamp > utils.SEED_EXPIRATION_TIME


class EventStorage(db.Model):

    id = db.Column('id', db.Integer, primary_key=True)
    event = db.Column('event', db.String(20))
    ip = db.Column('ip', db.String(16))
    time_stamp = db.Column('time_stamp', db.Integer)

    def __init__(self, event, ip):
        self.event = event
        self.ip = ip
        self.time_stamp = utils.get_time()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '%d: %s from %s at %s\n' % (
            self.id,
            self.event.ljust(20),
            self.ip.ljust(16),
            utils.get_ui_time(self.time_stamp)
        )


def log_table():
    try:
        print(SeedStorage.query.all())
        print(EventStorage.query.all())
    except Exception as e:
        print(e)


def is_token_valid(token):
    try:
        seed_val = cry.decrypt(token)
    except Exception as e:
        return False
    if not utils.does_seed_match_alphabet(seed_val):
        return False
    seed = SeedStorage.query.filter_by(seed=seed_val).first()
    return seed is not None and not seed.is_expired()


def save_event(event):
    event = EventStorage(event, request.remote_addr)
    db.session.add(event)
    db.session.flush()
    db.session.commit()


@app.errorhandler(Exception)
def exception_handler(e):
    print(e)
    return utils.get_error_by_code(500)


@app.errorhandler(500)
@app.errorhandler(502)
@app.errorhandler(405)
@app.errorhandler(404)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(400)
def error_handler(e):
    print(e)
    code, _ = utils.get_error_data(e)
    return utils.get_error_by_code(code)


@app.route("/getSeed")
def get_seed():
    save_event('getSeed')
    while True:
        seed_val = utils.get_random_seed()
        if SeedStorage.query.filter_by(seed=seed_val).count() == 0:
            break
    seed = SeedStorage(seed_val)
    print(cry.encrypt(seed_val))
    db.session.add(seed)
    db.session.flush()
    db.session.commit()
    return utils.RESPONSE_FORMAT % utils.as_str(seed_val)


@app.route("/execute", methods=['POST'])
def execute():
    save_event('execute')
    data = request.form
    if TOKEN not in data:
        return utils.get_extended_error_by_code(1, TOKEN)
    token = data[TOKEN]
    if not is_token_valid(token):
        abort(401)
    return utils.RESPONSE_1


log_table()

if __name__ == "__main__":
    db.create_all()
    db.init_app(app)
    app.logger.setLevel(logging.DEBUG)
    app.run(threaded=True, host=HOST, port=PORT)
