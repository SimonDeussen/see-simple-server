import json
from flask import Flask
from flask import request, jsonify
from datetime import datetime
from os import path

from ev3_standard import calculate_movement

app = Flask(__name__)

real_path = path.realpath(__file__)
dir_path = path.dirname(real_path)


@app.route('/log_ev3_standard', methods=['POST'])
def log_data():
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H:%M:%S")
    file_name_raw = f"{dir_path}/data/{dt_string}_raw.json"
    file_name_full = f"{dir_path}/data/{dt_string}_full.json"

    request_data = json.loads(request.get_json())

    with open(file_name_raw, "w") as file:
        file.write(json.dumps(request_data, indent=4))

    print(f"Received experiment data and saved as {file_name_raw}")

    with open(file_name_full, 'w') as file:
        data = calculate_movement(request_data)
        file.write(json.dumps(data, indent=4))

    print(f"Calculated full movement data and saved as: {file_name_full}")

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(host="0.0.0.0")
