import pyrebase

config = {
    #confidential config keys here
};

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()



def LoginAsAdmin():
    user = auth.sign_in_with_email_and_password('kesavaprasadarul@outlook.com','95123456')
    return user

def RefreshToken(user):
    return auth.refresh(user['refreshToken'])

def GetCurrentQueue(userY):
    #userY = RefreshToken(userY)
    Queue = db.child('users').child(userY['localId']).child('items').get(userY['idToken']).val()
    return Queue

def AddItemToQueue(userX,url,id,registeredPrice,triggerPrice):
    payload = {'url': url, 'registeredPrice': registeredPrice, 'triggerPrice': triggerPrice}
    db.child('users').child(userX['localId']).child('items').child(id).set(payload, userX['idToken'])
    AddItemToGlobalQueue(userX,id)


def AddItemToGlobalQueue(userX,id):
    queue = db.child('g_queue').child('amazon').get(userX['idToken']).val()
    queueList = str(queue).split(',')
    if (not queueList.__contains__(str(id))):
        queue = queue + "," + str(id)
    payload = {"amazon":queue}
    db.child('g_queue').update(payload,userX['idToken'])



user = LoginAsAdmin()
AddItemToQueue(user,"https://amazon.in/dp/95123",95123,142, 95)
print(GetCurrentQueue(user))