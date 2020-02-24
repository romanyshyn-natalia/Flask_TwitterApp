from flask import Flask, redirect, url_for, request, render_template, abort
import create_map

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/get_name', methods=["POST"])
def get_name():
    name = request.form.get("name")
    create_map.main(name)
    return render_template(name + "_map.html")


if __name__ == '__main__':
    app.run(debug=True)
