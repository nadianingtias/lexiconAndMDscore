from bson.objectid import ObjectId


class TrainData(object):
    """A class for storing Project related information"""
    # constructor isi 2 parameter
    def __init__(self, id=None, username=None, tweet=None, cleanTweet=None, selfScore=None, negSentiScore=None,
                 negEmo=None, MDscore=None, label =None):
        if id is None:
            self._id = ObjectId()
        else:
            self._id = id
        self.username = username
        self.tweet = tweet
        self.cleanTweet = cleanTweet
        self.selfScore = selfScore
        self.negSentiScore = negSentiScore
        self.negEmo = negEmo
        self.MDscore = MDscore
        self.label = label

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
                return TrainData(json_data.get('_id', None),
                                 json_data['tweet'],
                                 json_data['cleanTweet'],
                                 json_data['selfScore'],
                                 json_data['negSentiScore'],
                                 json_data['negEmo'],
                                 json_data['MDscore'],
                                 json_data['label']
                             )
            except KeyError as e:
                raise Exception("Key not found in json_data: {}".format(e))
        else:
            raise Exception("Tidak ada data untuk dijadikan Data Entry")
