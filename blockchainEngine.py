import time
import datetime
import json
from blockchain import BlockChain
from pprint import pprint as print
from multiprocessing import Process

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

username = 'AleksandrT'
password ='080901'	
init = BlockChain(username=username, password=password, base_url = 'https://b1.ahmetshin.com/restapi/')
init.get_version_file()



def getTaskResult(data_json, id, count):
            #print("задача задана:")
            hash = init.get_hash_object(json.dumps(data_json))
            result_hash = init.make_hash(hash)
            #print("задача решена:" + result_hash)
            data = {
                'type_task':'BlockTaskUser_Solution',
                'id':id,
                'hash':result_hash
            }
            res = init.send_task(data)
            print("результат")
            print(res)
            time.sleep(15)
            count = count - 1



start = True
if __name__ == '__main__':

    while start:
        count = 0
        time.sleep(1)
        print(f'sleep {str(datetime.datetime.now())}')
        print("счетчик:" + str(count))
        result = init.get_task().json()
        # проверяем какие задачи поступили на решение
        if result['tasks']:
            for i in result['tasks']:
            #создаем процессы   
                id = i['id']
                data_json = i['data_json']  
                if not i['status_solution'] and count < 5:
                    count = count + 1
                    p = Process(target=getTaskResult, args=(data_json, id, count))
                    p.start()
                    #getTaskResult(data_json, id)

