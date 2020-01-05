from pymongo import MongoClient

class WordList_sentic_Repository(object):
    """ Repository implementing CRUD operations on tweet collection in MongoDB """
    def __init__(self):
        self.client = MongoClient(host='localhost', port=27017)
        self.database = self.client['MDcek']
        self.collection = self.database.WordList_sentic

    def create(self, obj):
        if obj is not None:
            self.collection.insert(obj.get_as_json())
        else:
            raise Exception("Tidak ada yang disimpan, paramaternya masih None")

    def read(self, id=None):
        if id is None:
            return self.collection.find()
        else:
            return self.collection.find({"_id":id})

    def searchWord(self, name=None):
        if name is None:
            print("tanpa kueri nama")
            return self.collection.find()
        else:
            return self.collection.find({"word":name})

    def update(self, obj):
        if obj is not None:
            self.collection.save(obj.get_as_json())
        else:
            raise Exception("tidak bisa update, parameter projectnya tidak ada")

    def delete(self, obj):
        if obj is not  None:
            self.collection.remove(obj.get_as_json())
        else:
            raise Exception("tidak bisa delete, tidak ada param")