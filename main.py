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
    ip = db.Column('ip', db.String(16))
    time_stamp = db.Column('time_stamp', db.Integer)

    def __init__(self, seed, ip):
        self.seed = seed
        self.ip = ip
        self.time_stamp = utils.get_time()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '[%s %s (%s)]' % (self.seed, self.ip, utils.get_ui_time(self.time_stamp))

    def is_expired(self):
        return utils.get_time() - self.time_stamp > utils.SEED_EXPIRATION_TIME

    def does_ip_match(self, ip):
        return self.ip == ip


class EventStorage(db.Model):

    id = db.Column('id', db.Integer, primary_key=True)
    event = db.Column('event', db.String(20))
    ip = db.Column('ip', db.String(16))
    asserted = db.Column('asserted', db.Integer)
    time_stamp = db.Column('time_stamp', db.Integer)

    def __init__(self, event, ip, asserted):
        self.event = event
        self.ip = ip
        self.asserted = asserted
        self.time_stamp = utils.get_time()

    def __repr__(self):
        return '%d: %s from %s (%s) at %s\n' % (
            self.id,
            self.event.ljust(20),
            self.ip.ljust(16),
            'asserted  ' if self.asserted == 1 else 'unasserted',
            utils.get_ui_time(self.time_stamp)
        )

    def __str__(self):
        return json.dumps(self.as_ui_obj())

    def as_ui_obj(self):
        return {
            'id': self.id,
            'event': self.event,
            'ip': self.ip,
            'asserted': self.asserted,
            'time_stamp': self.time_stamp
        }


def log_table():
    try:
        print(SeedStorage.query.all())
        print(EventStorage.query.all())
    except Exception as e:
        print(e)


def is_token_valid(token):
    try:
        seed_val = cry.decrypt(token)
    except Exception:
        return False
    if not utils.does_seed_match_alphabet(seed_val):
        return False
    seed = SeedStorage.query.filter_by(seed=seed_val).first()
    if seed is None:
        return False
    expired = seed.is_expired()
    matches_ip = seed.does_ip_match(request.remote_addr)
    if expired:
        db.session.delete(seed)
        db.session.commit()
    return not expired and matches_ip


def save_event(event, asserted):
    event = EventStorage(event, request.remote_addr, 1 if asserted else 0)
    db.session.add(event)
    db.session.flush()
    db.session.commit()


def assert_and_save(event):
    data = request.headers
    asserted = TOKEN in data and is_token_valid(data[TOKEN])
    save_event(event, asserted)
    if not asserted:
        abort(401)


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
    save_event('getSeed', 1)
    while True:
        seed_val = utils.get_random_seed()
        if SeedStorage.query.filter_by(seed=seed_val).count() == 0:
            break
    seed = SeedStorage(seed_val, request.remote_addr)
    print(cry.encrypt(seed_val))
    db.session.add(seed)
    db.session.flush()
    db.session.commit()
    return utils.RESPONSE_FORMAT % utils.as_str(seed_val)


@app.route("/getEvents", methods=['POST'])
def get_events():
    assert_and_save('getEvents')
    events = [ev.as_ui_obj() for ev in EventStorage.query.order_by(EventStorage.time_stamp.desc()).limit(100).all()]
    return utils.RESPONSE_FORMAT % json.dumps(events)


@app.route("/execute", methods=['POST'])
def execute():
    assert_and_save('execute')
    return utils.RESPONSE_1


log_table()

if __name__ == "__main__":
    db.create_all()
    db.init_app(app)
    app.logger.setLevel(logging.DEBUG)
    app.run(threaded=True, host=HOST, port=PORT)
