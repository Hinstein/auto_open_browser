import json

import bit_browser_request
import browser_operate


def main(value, input_value):
    response_data = bit_browser_request.send_post_request(value['id'])
    driver_path = response_data['data']['driver']
    debugger_address = response_data['data']['http']
    print(driver_path)
    print(debugger_address)
    browser_operate.login(driver_path, debugger_address, value['metamask'], input_value)
