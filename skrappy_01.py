import pyrebase
import sys_constants
from urllib import parse

config = sys_constants.getAdminKeys()

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

def LoginAsAdmin():
    global user
    user = auth.sign_in_with_email_and_password('kesavaprasadarul@outlook.com','95123456')
    return user

def RefreshToken(user):
    return auth.refresh(user['refreshToken'])

def GetCurrentQueueDeprecated(userY):
    #userY = RefreshToken(userY)
    Queue = db.child('users').child(userY['localId']).child('items').get(userY['idToken']).val()
    return Queue

def GetCurrentQueueFromId(id):
    #userY = RefreshToken(userY)
    Queue = db.child('users').child(id).child('items').get(user['idToken']).val()
    return Queue

def AddItemToQueue(userId,url,id,registeredPrice,triggerPrice):
    payload = {'url': url, 'registeredPrice': registeredPrice, 'triggerPrice': triggerPrice}
    db.child('users').child(userId).child('items').child(id).set(payload, user['idToken'])
    AddItemToGlobalQueue(id)


def AddItemToGlobalQueue(id):
    queue = db.child('g_queue').child('amazon').get(user['idToken']).val()
    queueList = str(queue).split(',')
    if (not queueList.__contains__(str(id))):
        queue = queue + "," + str(id)
    payload = {"amazon":queue}
    db.child('g_queue').update(payload,user['idToken'])

def ParseIDfromURL(url):
    parse_url = parse.urlsplit(url)
    params = parse_url.path.split('/')
    for i in range(len(params)):
        if params[i] == "dp":
            return params[i + 1]
    return None

LoginAsAdmin()