from typing import Dict
import json
import math


def calculate_movement(raw) -> Dict:
    WHEEL_DIAMETER = 5.6  # cm
    MAIN_AXIS_LENGTH = 12.0  # cm

    motor_1_path = []  # in rad
    motor_2_path = []  # in rad

    robot_orientation = 0.0  # in rad
    robot_position_x = 0.0  # in cm
    robot_position_y = 0.0  # in cm

    distance_traveled_wheel_1 = 0.0  # in cm
    distance_traveled_wheel_2 = 0.0  # in cm

    data_length = min(len(raw['motor_1']), len(raw["motor_2"]))
    data = {'motor_1': [], 'motor_2': [], 'position': [], 'orientation': []}

    for i in range(data_length):
        if i == 0:
            distance_traveled_wheel_1 = (WHEEL_DIAMETER * math.pi * raw['motor_1'][i]['motor_pos']) / (2 * math.pi)
            distance_traveled_wheel_2 = (WHEEL_DIAMETER * math.pi * raw['motor_2'][i]['motor_pos']) / (2 * math.pi)
        else:
            distance_traveled_wheel_1 = (WHEEL_DIAMETER * math.pi *
                                         (raw['motor_1'][i]['motor_pos'] - raw['motor_1'][i-1]['motor_pos'])) / (2 * math.pi)
            distance_traveled_wheel_2 = (WHEEL_DIAMETER * math.pi *
                                         (raw['motor_2'][i]['motor_pos'] - raw['motor_2'][i-1]['motor_pos'])) / (2 * math.pi)

        delta_distance = (distance_traveled_wheel_1 + distance_traveled_wheel_2) / 2
        delta_angle = (distance_traveled_wheel_1 - distance_traveled_wheel_2) / MAIN_AXIS_LENGTH

        robot_orientation = robot_orientation + delta_angle
        robot_position_x = robot_position_x + delta_distance * math.sin(robot_orientation)
        robot_position_y = robot_position_y + delta_distance * math.cos(robot_orientation)

        data['motor_1'].append({'motor_pos': raw['motor_1'][i]['motor_pos'], 'time': raw['motor_1'][i]['time']})
        data['motor_2'].append({'motor_pos': raw['motor_2'][i]['motor_pos'], 'time': raw['motor_2'][i]['time']})
        data['position'].append({'x': robot_position_x, 'y': robot_position_y})
        data['orientation'].append(robot_orientation)

    return data


# with open("codes/server/data/25042021_15:45:21_raw.json", "r") as f:
#     data = json.load(f)

# print(calculate_movement(data))
