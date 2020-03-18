from flask import Flask, request, abort, render_template, redirect, url_for
import utils
import logging
import controller
import colors

PUSH_TITLE = "says Smarty"
HOST = '0.0.0.0'
PORT = 1753

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
ctrl = controller.Controller()


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
    return render_template('ui.html', controller=ctrl)


@app.route("/<path>")
def one_path(path):
    abort(400)


@app.route("/colors")
def colors_list():
    return render_template('rgb.html', colors=colors.create_colors())


@app.route("/light", methods=["POST"])
def light():
    ctrl.toggle_light()
    return redirect(url_for('index'))


@app.route("/amp", methods=["POST"])
def amp():
    ctrl.toggle_amp()
    return redirect(url_for('index'))


@app.route("/rgb", methods=["POST"])
def rgb():
    ctrl.set_led(request.form['rgb'])
    return redirect(url_for('colors_list'))


if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    app.run(threaded=True, host=HOST, port=PORT)
