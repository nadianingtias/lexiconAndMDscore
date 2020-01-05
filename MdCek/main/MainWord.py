import itertools


from MdCek.DBRepository.UserTweetRepository import UserTweetRepository as UserTweetDepRepo
from MdCek.DBRepository.WordList_depression_Repository import WordList_depressionRepository as wordlist_dep_repo
from MdCek.DBRepository.WordList_positive_depression_Repository import WordList_positive_depressionRepository as wordlist_pos_dep_repo
from MdCek.Model.WordList import WordList as WordList
import nltk
import string
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk import word_tokenize, pos_tag

from collections import defaultdict

tag_map = defaultdict(lambda : wordnet.NOUN)
tag_map['J'] = wordnet.ADJ
tag_map['V'] = wordnet.VERB
tag_map['R'] = wordnet.ADV
wn_lemmater = WordNetLemmatizer()
stop_words =set(stopwords.words('english'))
pStemmer = PorterStemmer()

import re


def getNegWordList(trainDepression):
    NegWordList = []
    counterUser = 0
    # 1. read depresi user total 38 user, read normal user total 38
    for trainUser in trainDepression:
        counterUser += 1
        userTweets = trainUser['tweets']
        # print(userTweets)
        # 2. masing2 user punya banyak tweets, tweets per user dibaca per rownya
        for tweet in userTweets:
            # print(tweet['annotation'])
            # 3. masing2 row tweet punya atribut annotation,
            annotationOfEachTweet = tweet['annotation']
            # print(annotationOfEachTweet['negAnno'])
            NegWord = annotationOfEachTweet['negAnno']
            for Word in NegWord:
                if Word != None:
                    # print(Word)
                    # NegWordList.append(Word)
                    NegWordList.append(Word)
    return NegWordList

def getPosWordList(trainDepression):
    PosWordList = []
    counterUser = 0
    # 1. read depresi user total 38 user, read normal user total 38
    for trainUser in trainDepression:
        counterUser += 1
        userTweets = trainUser['tweets']
        # print(userTweets)
        # 2. masing2 user punya banyak tweets, tweets per user dibaca per rownya
        for tweet in userTweets:
            # print(tweet['annotation'])
            # 3. masing2 row tweet punya atribut annotation,
            annotationOfEachTweet = tweet['annotation']
            # print(annotationOfEachTweet['negAnno'])
            PosWord = annotationOfEachTweet['posAnno']
            for Word in PosWord:
                if Word != None:
                    # print(Word)
                    # NegWordList.append(Word)
                    PosWordList.append(Word)
    return PosWordList

def sendWordListToDB(NegWordList):
    counter = 0

    for word in NegWordList:
        print(type(word))
        counter = counter + 1
        print(word)
        existWord = wordList_depRepo.searchWord(word)
        isExist = False
        count = 0
        for successresult in existWord:
            print("akan tambah counter")
            isExist = True
            objWord = wordObject.build_from_json(successresult)
            idWord = objWord._id
            countWord = objWord.count + 1
        #jika ada di dalam DB
            if idWord :
                # //update
                print("updating word dengan id : {} ".format(idWord))
                updateWord = WordList(idWord, word, countWord, state)
                wordList_depRepo.update(updateWord)
        #jika tidak ada di dalam DB
        if not isExist:
            print("new word!!")
            isExist = False
            count = 1
            newWord = WordList(None, word, count, state)
            #!!!!!!!!!masuk ke DB
            # wordList_depRepo.create(newWord)
    print("{} words of negative word list FOUND".format(counter))

def sendPosWordListToDB(PosWordList):
    counter = 0
    # wordPosObject = WordList()

    for word in PosWordList:
        print(type(word))
        counter = counter + 1
        print(word)
        existWord = wordList_pos_depRepo.searchWord(word)
        isExist = False
        count = 0
        for successresult in existWord:
            print("akan tambah counter")
            isExist = True
            objWord = wordObject.build_from_json(successresult)
            idWord = objWord._id
            countWord = objWord.count + 1
        #jika ada di dalam DB
            if idWord :
                # // update
                print("updating word dengan id : {} ".format(idWord))
                updateWord = WordList(idWord, word, countWord, state)
                wordList_pos_depRepo.update(updateWord)
        #jika tidak ada di dalam DB
        if not isExist:
            print("new word!!")
            isExist = False
            count = 1
            newWord = WordList(None, word, count, state)
            #!!!!!! masuk ke DB
            # wordList_pos_depRepo.create(newWord)
    print("{} Words of positive word list FOUND".format(counter))


regex_str = [
    # r'<[^>]+>',  # HTML tags
    # r'(?:@[\w_]+)',  # @-mentions
    # r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    # r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs
    # r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    # r'(?:\S)'  # anything else
]
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)
def preprocess(param, lowercase=False):
    tokens = tokenize(param)
    if lowercase:
        tokens = [token.lower() for token in tokens]
    return tokens


def updateStopWords(stop_words):
    to_extend = ['x', 'y', 'r', 'e','s', 'm', 'hi', 'yet', 'may', 'oh', 'due', 'to',
                 'day', 'days', 'weeks', 'week',
                 'being', 'months', 'way', ]
    stop_words = stop_words.union(to_extend)

    # print(stop_words)

    to_remove = ['instead']

    self_words = ['my', 'myself', 'i', "i'", 'self', 'am', 'me', 'id', "i'd", "'d", "ain", "ain't"
                                                                               "i'll", 'im', "i'm", "ive", "i've",
                  "mine", "own", 'myselves', 'ourselves', "'ve"]
    negation_words = ['no','not', 'mustn', "wouldn't", "aren't", "hasn't", 'wasn', 'don',
                      "isn't", 'won', "won't", "didn't", "couldn't", "weren't", 'nor', 'neither',"'t"]
    stop_words = stop_words.difference(to_remove)
    stop_words = stop_words.difference(self_words)
    stop_words = stop_words.difference(negation_words)
    # print(stop_words)
    return  stop_words


def getRecognizedWordnet(ALL_unique_word):
    recognized_words = []
    for word in ALL_unique_word:
        if word:  # check if empty string
            if wordnet.synsets(word):
                # print(word)
                recognized_words.append(word)  # only keep recognized words
    print("{} word have been recognized by WORDNET dictionary : {}".format(len(recognized_words),
                                                                           recognized_words))
    #only_recognized_words adalah daftar kata unique yang sudah ditest di wordnet telah ter recognized
    return recognized_words


def getUniqueWord(ALL_filtered_sentence):
    ALL_unique = []
    for w in ALL_filtered_sentence:
        if w not in ALL_unique:
            ALL_unique.append(w)
    # print("Unique Words : {}".format(len(ALL_unique_word)))
    return ALL_unique


def getNumberRemoval(text):
    # PREPROCESS - NUMBER REMOVAL
    text = re.sub(r'\d+', '', text)
    # print("Number removal: {}".format(text))
    return text


def getMentionLinkHashtagRemoval(text):
    # PREPROCESS - MENTION REMOVAL , LINK, HASHTAG sign REMOVAL
    text = re.sub(r'@\w+ ?|http\S+|#', '', text)
    # print("Mention, Link, hashtag sign removal: {}".format(text))
    return text


def getNTConversion(text):
    # PREPROCESS - n't conversion
    # text  = re.sub('n''t+$', " not", text)
    text = re.sub("n't\s*|don$", " not ", text)
    # print(" n't conversion: {}".format(text))
    return text


def getFivePreprocess(text):
    text = getNumberRemoval(text)  # PREPROCESS - NUMBER REMOVAL
    # PREPROCESS - PUNCTUATION REMOVAL (have done at prev preprocess)
    # text = text.translate(string ("", ""), string.punctuation)
    text = getMentionLinkHashtagRemoval(text)  # PREPROCESS - MENTION REMOVAL , LINK, HASHTAG sign REMOVAL
    text = getNTConversion(text)  # PREPROCESS - n't conversion
    # PREPROCESS - OVERWRITE (data dari DB sudah recognize by wordnet and corrected by textblob)
    # text = ''.join(''.join(s)[:] for _, s in itertools.groupby(text))
    return text


def getSinonim(lemma):
    syns = wordnet.synsets(lemma)
    sinonim = syns[0].lemmas()[0].name()
    return sinonim


def getAntonimss(lemma):
    syns = wordnet.synsets(lemma)  # yg jadi acuan antonim tetap lemma awal
    synonyms = []
    antonyms = []
    for syn in syns:
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    return antonyms


if __name__ == '__main__':
    #START FROM THIS
    userDepressionRepo = UserTweetDepRepo()
    trainDepression = userDepressionRepo.read()

    # METHOD - Mendapatkan semua daftar kata negatif dari DB (lib vader dan pattern)
    # NegWordList = getNegWordList(trainDepression)

    # METHOD - Mendapatkan semua daftar kata positif dari DB (lib vader dan pattern)
    # PosWordList = getPosWordList(trainDepression)

    #persiapan masukkan wordlist ke DB
    counter = 0
    wordObject = WordList()

    state = "DEPRESSION"
    wordList_depRepo = wordlist_dep_repo()
    # METHOD - memuat wordlist negatif ke dalam collection baru
    # sendWordListToDB(NegWordList)


    state = "DEPRESSION"
    wordList_pos_depRepo = wordlist_pos_dep_repo()
    # METHOD - memuat wordlist positif ke dalam collection baru
    # sendPosWordListToDB(PosWordList)

    import sys
    #menghentikan jalannya program
    # sys.exit()

    # PREPROCESSING
    # print(stop_words)

    #METHOD - mengupdate kata2 untuk menyeleksi kata yang  perlu saja
    stop_words = updateStopWords(stop_words)


    counterUser = 0
    counterTweets = 0
    sumLemmaToken = 0
    sumToken = 0
    sumHasil = 0
    ALL_filtered_sentence = []
    for trainUser in trainDepression:
        counterUser += 1
        userTweets = trainUser['tweets']
        # print(userTweets)
        # 2. masing2 user punya banyak tweets, tweets per user dibaca per rownya
        sum = 0
        for tweet in userTweets:
            # START
            if sum <1 :
                counterTweets = counterTweets + 1
                #ALL DATA
                # sum = sum + 1
                text = tweet['sentence']['text']
                print("-------------------------------------")
                text = getFivePreprocess(text) #NUMBER, LINK, MENTION, # sign (removal), Dont (conversion)

                #PREPROCESS - lemmatization by wordnet NLTK
                wn_lemmater = WordNetLemmatizer()
                # text = "@coralineada i spoke with a number of developer from underrepresented groups and almost all of them said they"
                tokens = word_tokenize(text)
                token_2 = []
                lemma_2 = []
                for token, tag in pos_tag(tokens):
                    lemma = wn_lemmater.lemmatize(token, tag_map[tag[0]])
                    print("heyo")
                    print(tag_map[tag[0]])
                    token_2.append(token)
                    lemma_2.append(lemma)
                sumLemmaToken = sumLemmaToken + len(tokens)
                # print("hasil token      : {}".format(token_2))
                # print("hasil lemma     {} : {}".format(len(lemma_2),lemma_2))
                text = ' '.join(lemma_2)

                # PREPROCESS - #LOWERCASE ALL
                                #TOKEN NEEDED TYPE (word)
                word_tokens = cleanByRegex = preprocess(text, True)
                # print("clean by regex : {}".format(cleanByRegex))
                # word_tokens = lemma_2   #lemma 2 - digunakan jika tidak menggunakan tahap preprocess by regEx

                filtered_sentence = []
                for w in word_tokens:
                    # PREPROCESS - STOPWORD REMOVAL
                    if w not in stop_words:
                        filtered_sentence.append(w) #untuk tampilan per tweet
                        ALL_filtered_sentence.append(w) #untuk mencari kata dari seluruh data training

                # ALL_filtered_sentence.append(filtered_sentence)
                if(len(lemma_2)!=len(word_tokens)):
                    print("FIND ME - membuktikan proses cleanbyregex telah mengurangi kata yang tidak jelas(noise)")
                # print("{} token : {}".format(len(word_tokens), word_tokens))
                #  print("{} hasil : {} ".format(len(filtered_sentence),filtered_sentence))
                sumToken = sumToken + len(word_tokens)
                sumHasil  = sumHasil + len(filtered_sentence)
            else: break

    print("jumlah user depresi : {}\n jumlah tweet yang dipreproses : {}".format(counterUser, counterTweets))
    print("Jumlah Token lemma : {}".format(sumLemmaToken))
    print("Jumlah Token Awal : {}".format(sumToken))
    print("Jumlah Token Hasil : {}".format(sumHasil))

    #MEMBANGUN LEXICON DARI DATA KAMI
    # ALL_filtered_sentence =
    # PREPROCESSING - make unique token lemma
    ALL_unique_word = []
    ALL_unique_word = getUniqueWord(ALL_filtered_sentence)
    #ALL_unique_word adalah daftar kata yang sudah direduce kemunculannya berkali2 hingga muncul daftar kata unique

    # PREPROCESSING - FILTER ONLY RECOGNIZED WORD with sentiword dictionary
    only_recognized_words = []
    only_recognized_words = getRecognizedWordnet(ALL_unique_word)
    #only_recognized_words adalah daftar kata unique yang sudah ditest di wordnet telah ter recognized


    # untuk mencari frekuensi kemunculan kata (menggunakan list asli, bukan list kata unik)
    from nltk.probability import FreqDist
    fdist = FreqDist(ALL_filtered_sentence)
    print("fdist : {}".format(fdist))
    print(fdist.most_common(200))