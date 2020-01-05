from bson.objectid import ObjectId


class WordList_sentic(object):
    """A class for storing Project related information"""
    # constructor isi 2 parameter
    def __init__(self, id=None, word=None, senticnet=None):
        if id is None:
            self._id = ObjectId()
        else:
            self._id = id
        self.word = word
        self.senticnet = senticnet

    #konversi project itself into JSON form
    def get_as_json(self):
        """ Method returns the JSON representation of the Project object, yang mau disave di mongoDB"""
        return self.__dict__

    # method ini untuk membuat 1 instance baru, paramnya dari data json, di pecah dibikinkan objek
    @staticmethod
    def build_from_json(json_data):
        """ Method used to build WordList objects from JSON data returned from MongoDB """
        if json_data is not None:
            try:
                return WordList_sentic(json_data.get('_id', None),
                                 json_data['word'],
                                 json_data['sentic']
                             )
            except KeyError as e:
                raise Exception("Key not found in json_data: {}".format(e))
        else:
            raise Exception("Tidak ada data untuk dijadikan Data Entry")
