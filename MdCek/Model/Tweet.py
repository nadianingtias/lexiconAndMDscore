from bson.objectid import ObjectId


class Tweet(object):
    """A class for storing Project related information"""
    # constructor isi 5 parameter
    def __init__(self, id=None, username=None, date=None, text=None, tweet_id=None, state=None):
        if id is None:
            self._id = ObjectId()
        else:
            self._id = id
        self.username = username
        self.date = date
        self.text = text
        self.tweet_id = tweet_id
        self.state = state

    #konversi project itself into JSON form
    def get_as_json(self):
        """ Method returns the JSON representation of the Project object, yang mau disave di mongoDB"""
        return self.__dict__

    # method ini untuk membuat 1 instance baru, paramnya dari data json, di pecah dibikinkan objek
    @staticmethod
    def build_from_json(json_data):
        """ Method used to build Project objects from JSON data returned from MongoDB """
        if json_data is not None:
            try:
                return Tweet(json_data.get('_id', None),
                                 json_data['username'],
                                 json_data['date'],
                                 json_data['text'],
                                 json_data['tweet_id'],
                                 json_data['state']
                             )
            except KeyError as e:
                raise Exception("Key not found in json_data: {}".format(e))
        else:
            raise Exception("Tidak ada data untuk dijadikan Project")