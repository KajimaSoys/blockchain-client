import time, datetime, json, urllib3
from blockchain import BlockChain
from pprint import pprint as print

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

username = 'AysheR'
password ='RehsyA'

init = BlockChain(username=username, password=password, base_url='https://b1.ahmetshin.com/restapi/')

init.get_version_file()


def main():
    try:
        while True:
            time.sleep(2)
            print(f'sleep {str(datetime.datetime.now())}')

            # Получаем цепочки какие есть, и сохраняем у себя локально
            result = init.get_chains()
            # print(result.json())

            # получаем задачи, которые надо решить
            result = init.get_task().json()
            print(result)

            # проверяем какие задачи поступили на решение
            if result['tasks']:
                # print(result)
                for item in result['tasks']:
                    id = item['id']
                    data_json = item['data_json']
                    hash = init.get_hash_object(json.dumps(data_json))
                    result_hash = init.make_hash(hash)
                    data = {
                        'type_task': 'BlockTaskUser_Solution',
                        'id': id,
                        'hash': result_hash
                    }

                    result = init.send_task(data)
                    print(result.json())

    except KeyboardInterrupt:
        return True


if __name__ == "__main__":
    main()