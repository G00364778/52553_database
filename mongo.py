import pymongo

mongoclient = None

def connect():
    global mongoclient
    #print('client_before: ',mongoclient)
    mongoclient = pymongo.MongoClient()
    mongoclient.admin.command('ismaster')
    print('client_connect: ',mongoclient)

def find():
    db = mongoclient["proj"]
    docs = db["docs"]
    query = {"car":{"$exists":"true"}}
    cars = docs.find(query)
    for car in cars:
        print(car)

def insert():
    db = mongoclient["proj"]
    docs = db["docs"]
    newDoc = {"_id":7, "car":{"reg":"99-D-69674", "enginesize":1.0}}

    docs.insert_one(newDoc)

def main():
    if (not mongoclient):
        try:
            connect()
        except Exception as e:
            print('Error', e)

if __name__ == "__main__":
    main()
    find()
    #insert()

