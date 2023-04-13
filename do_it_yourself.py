import re


def sensor_state_counter(file, succes_test_dict: dict, failed_test_dict: dict):
    """function that counts the number of messages from handler for each sensor that is OK"""
    with open(file, 'r') as logfile:
        lines = logfile.readlines()
        for line in lines:
            line_big = re.search(r'BIG;\d{2};(\w{6}).*(\w{2});\'$', line)
            if line_big:
                sensor_id = line_big.group(1)
                sensor_state = line_big.group(2)
                if sensor_id in succes_test_dict:
                    succes_test_dict[sensor_id].append(sensor_state)
                else:
                    succes_test_dict[sensor_id] = [sensor_state]

    for key, val in list(succes_test_dict.items()):
        if 'DD' in val:
            failed_test_dict[key] = val
            del succes_test_dict[key]

    return succes_test_dict, failed_test_dict


if __name__ == '__main__':
    succes_test = {}
    failed_test = {}

    succes_test, failed_test = sensor_state_counter('app_2.log', succes_test, failed_test)

    print(f'_______________Failed test {len(failed_test)} devices________________')
    for id in failed_test.keys():
        print(f'Device {id} was removed')

    print(f'_______________Success test {len(succes_test)} devices________________')
    for id, cnt in succes_test.items():
        print(f'Device {id} sent {len(cnt)} statuses')
