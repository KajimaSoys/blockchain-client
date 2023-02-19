from fastapi import FastAPI
import uvicorn
from blockchain import BlockChain
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


link_client = 'https://b1.ahmetshin.com/static/blockchain.py'

username = 'AysheR'
password ='RehsyA'
# username = 'testEngine5'
# password ='12345'
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


class MessageDataEncrypted(MessageData):
    private_key : str

    class Config:
        orm_mode = True


class MessageDecrypt(BaseModel):
    private_key: str
    action : str
    curlid : str
    random_key : str
    random_number : str
    secret_text : str

    class Config:
        orm_mode = True


@app.get("/coins")
def read_root():
    result = init.check_coins()

    return result.json()


@app.get("/chains")
def read_root():
    result = init.get_chains()
    response = result.json()

    return response


@app.get("/userHash")
async def userHash():
    return init.hach_user



@app.get('/get_task')
def get_task():
    result = init.get_task()

    return result.json()


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
def send_task(dataType: MessageDataEncrypted):
    data = {
        'type_task': dataType.type_task,
        'from_hach': dataType.from_hach,
        'to_hach': dataType.to_hach,
        'message': init.encrypt({
            'private_key': dataType.private_key,
            'text': dataType.message
        }).json()
    }
    result = init.send_task(data)

    return result.json()


@app.post('/decrypt_message')
def decrypt_message(dataType: MessageDecrypt):
    data = {
        'private_key': dataType.private_key,
        'encrypted_object': {
            'action': dataType.action,
            'curlid': dataType.curlid,
            'random_key': dataType.random_key,
            'random_number': dataType.random_number,
            'secret_text': dataType.secret_text
            }
    }
    result = init.decrypt(data)

    return result.json()


if __name__ == "__main__":
    uvicorn.run('server:app', port=8000, host="127.0.0.1", reload=True)