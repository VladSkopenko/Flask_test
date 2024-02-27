from flask import Flask, render_template, request, jsonify, send_from_directory
import json
from datetime import datetime
import logging
import os

app = Flask(__name__)
logging.basicConfig(level="DEBUG")


@app.route("/home")
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/message.html")
@app.route("/message", methods=["POST", "GET"])
def message():
    if request.method == 'POST':
        try:
            request_data = request.data.decode()
            save_data(request_data)
            return jsonify({"message": "Data saved successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == "GET":
        return render_template("message.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404


@app.route('/static/logo.png')
def send_logo():
    return send_from_directory('static', 'logo.png')


@app.route('/static/<path:filename>')
def send_css(filename):
    return send_from_directory('static/css', filename)


def save_data(data):
    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        new_data = {current_time: {key: value for key, value in [el.split('=') for el in data.split('&')]}}

        file_path = "storage/data.json"

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = {}
        except ValueError:
            existing_data = {}

        existing_data.update(new_data)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=2)

        if os.path.exists(file_path):
            logging.info(f"Data saved to {file_path}")
        else:
            logging.error("Data was not saved")

    except ValueError as error:
        logging.error(f"ValueError_11: {error}")
    except OSError as oser:
        logging.error(f"OSError: {oser}")

if __name__ == "__main__":
    app.run(debug=True)
