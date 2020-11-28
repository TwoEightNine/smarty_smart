from flask import Flask, request, abort, render_template, redirect, url_for
from flask_cors import CORS
import utils
import logging
from src.controller import *
import colors
import json

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
CORS(app)

ctrl: Controller = GpioController()


def __create_state():
    return json.dumps({
        'temp': ctrl.get_temp(),
        'led_color': ctrl.get_led_color()
    })


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


@app.route("/")
def index():
    return render_template('ui.html', controller=ctrl, colors=colors.create_colors())


@app.route("/<path>")
def one_path(path):
    abort(400)


@app.route("/rgb", methods=["POST"])
def rgb():
    ctrl.set_led_color(request.form['rgb'])
    return redirect(url_for('index'))


@app.route('/api/state', methods=['GET'])
def api_state():
    return __create_state()


@app.route('/api/led_color', methods=['GET'])
def api_rgb():
    led_color = request.args.get('color')
    if led_color is None or len(led_color) != 6:
        abort(400)

    ctrl.set_led_color(led_color)
    return __create_state()


if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    app.run(threaded=True, host='0.0.0.0', port=1753)
