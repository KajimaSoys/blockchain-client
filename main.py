from typing import Union
from fastapi import FastAPI
import uvicorn
from blockchain import BlockChain
from pydantic import BaseModel
import json
from pprint import pprint as print
from fastapi.middleware.cors import CORSMiddleware
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


link_client = 'https://b1.ahmetshin.com/static/blockchain.py'

username = 'testEngine6'
password ='12345'
# username = 'AleksandrT'
# password ='080901'
init = BlockChain(username=username, password=password, base_url = 'https://b1.ahmetshin.com/restapi/')

init.get_version_file()


app = FastAPI()
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://localhost:63342"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/coins")
def read_root():
    result = init.check_coins()
    return result.json()

@app.get("/chains")
def read_root():
    result = init.get_chains()
    response = result.json()
    
    for block in response['chains']['block_active']:
        if 'data_json' in block:
            for data in block['data_json']:
                if 'message' in data['data_json']:
                    if isinstance((data['data_json']['message']), str):
                        pass
                    else:
                        if (data['data_json']['from_hach'] == '10fa511f879707980af0f16720bcc5e20a2b720a888200a0697f749aed56eb07' and  data['data_json']['to_hach'] == '92ac7967c50052c20619118e1783e28f88ca9f14767e982085815982a8920325') or (data['data_json']['from_hach'] == '92ac7967c50052c20619118e1783e28f88ca9f14767e982085815982a8920325' and  data['data_json']['to_hach'] == '10fa511f879707980af0f16720bcc5e20a2b720a888200a0697f749aed56eb07'):
                            data['data_json']['message_before'] = data['data_json']['message']
                            ans = init.decrypt({
                                'private_key': 'SashaBest',
                                'encrypted_object': data['data_json']['message']
                            }).json()

                            if ans['success']:
                                data['data_json']['message'] = ans['message']
                            else:
                                data['data_json']['message'] = 'decrypt error'

    
    return response

@app.get("/userHash")
async def userHash():
    return init.hach_user



@app.get('/get_task')
def get_task():
    result = init.get_task()
    return result.json()


class DataType(BaseModel):
    type_task : str
    from_hach : str
    to_hach : str
    count_coins : int

    class Config:
        orm_mode = True 

class MessageData(BaseModel):
    type_task : str
    from_hach : str
    to_hach : str
    message : str

    class Config:
        orm_mode = True 

@app.post('/send_task')
def send_task(dataType: DataType):
    data = {
        'type_task': dataType.type_task,
        'from_hach': dataType.from_hach,
        'to_hach': dataType.to_hach,
        'count_coins': dataType.count_coins
    }
    result = init.send_task(data)
    return result.json()

@app.post('/send_message')
def send_task(dataType: MessageData):
    data = {
        'type_task': dataType.type_task,
        'from_hach': dataType.from_hach,
        'to_hach': dataType.to_hach,
        'message': dataType.message
    }
    result = init.send_task(data)
    return result.json()

@app.post('/send_message_encrypted')
def send_task(dataType: MessageData):
    data = {
        'type_task': dataType.type_task,
        'from_hach': dataType.from_hach,
        'to_hach': dataType.to_hach,
        'message': init.encrypt({
            'private_key':'SashaBest',
            'text': dataType.message
        }).json()
    }
    result = init.send_task(data)
    return result.json()

if __name__ == "__main__":
    uvicorn.run('main:app', port=8000, host="127.0.0.1", reload=True)