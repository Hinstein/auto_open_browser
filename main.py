import openWindow
import login
import csv_to_json


def main(value, input_value):
    response_data = openWindow.send_post_request(value['id'])
    driver_path = response_data['data']['driver']
    debugger_address = response_data['data']['http']
    print(driver_path)
    print(debugger_address)
    login.login(driver_path, debugger_address, value['password'], input_value)


