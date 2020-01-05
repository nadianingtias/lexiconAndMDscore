import itertools


from MdCek.DBRepository.UserTweetRepository import UserTweetRepository as UserTweetDepRepo
from MdCek.DBRepository.UserTweetNormalRepository import UserTweetNormalRepository as UserTweetNormRepo


from MdCek.DBRepository.WordList_depression_Repository import WordList_depressionRepository as wordlist_dep_repo
from MdCek.DBRepository.WordList_positive_depression_Repository import WordList_positive_depressionRepository as wordlist_pos_dep_repo
from MdCek.DBRepository.TrainData_Repository import TrainData_Repository as TrainDataRepo

from MdCek.Model.WordList import WordList as WordList
from MdCek.Model.TrainData import TrainData as TrainData
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
            wordList_depRepo.create(newWord)
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
            wordList_pos_depRepo.create(newWord)
    print("{} Words of positive word list FOUND".format(counter))


def sendArrayOfTrainDataToDB(arrayTrainData):
    trainDataRepo = TrainDataRepo()
    counter = 0
    for trainData in arrayTrainData:
        trainDataRepo.create(trainData)
        counter = counter + 1
        print("berhasil masukkan {} kata".format(counter))

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

self_words = ['my', 'myself', 'i', "i'", 'self', 'am', 'me', 'id', "i'd", "'d", "ain", "ain't",
                  "i'll", 'im', "i'm", "ive","i've",
                  "mine", "own", 'myselves', 'ourselves', "'ve"]
negation_words = ['no', 'not', 'mustn', "wouldn't", "aren't", "hasn't", 'wasn', 'don',
                      "isn't", 'won', "won't", "didn't", "couldn't", "weren't", 'nor', 'neither', "'t"]
def updateStopWords(stop_words):
    to_extend = ['x', 'y', 'r', 'e', 's', 'm', 'hi', 'yet', 'may', 'oh', 'due', 'to',
                 'day', 'days', 'weeks', 'week',
                 'being', 'months', 'way', ]
    stop_words = stop_words.union(to_extend)

    # print(stop_words)
    to_remove = ['instead']
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


def initArrayNol(length):
    arrayNol = []
    for i in range(length):
        arrayNol.append(0)

    print("panjang array : {}".format(len(arrayNol)))
    return arrayNol

hiRiskWord = ['Absolutely', 'All', 'Always', 'Complete', 'Completely',
              'Constant', 'Constantly', 'Definitely', 'Entire', 'Ever',
              'Every', 'Everyone', 'Everything', 'Full', 'Must',
               'Never', 'Nothing', 'Totally', 'Whole',
                  'fault',
                  # 'fine',
                  'tired', 'alone', 'neg', 'care',
                  'suicide', 'suicidal']

if __name__ == '__main__':
    negation_word =["not", "no", "none", "never", "neither", "nor"]

    #START FROM THIS
    #DEPRESSION DATA SOURCE
    userDepressionRepo = UserTweetDepRepo()
    trainDepression = userDepressionRepo.read()

    #NORMAL DATA SOURCE
    userNormalRepo = UserTweetNormRepo()
    trainNormal = userNormalRepo.read()

    #persiapan masukkan wordlist ke DB
    counter = 0
    wordObject = WordList()

    state = "DEPRESSION"
    wordList_depRepo = wordlist_dep_repo()
    state = "DEPRESSION"
    wordList_pos_depRepo = wordlist_pos_dep_repo()

    import sys
    #menghentikan jalannya program
    # sys.exit()

    # PREPROCESSING
    print(stop_words)

    #METHOD - mengupdate kata2 untuk menyeleksi kata yang  perlu saja
    stop_words = updateStopWords(stop_words)

    # ------------------------------------------------------------SENTICNET
    from MdCek.DBRepository.WordList_sentic_Repository import WordList_sentic_Repository
    from MdCek.Model.WordList_sentic import WordList_sentic
    import pprint
    from senticnet.senticnet import SenticNet

    wordSenticRepo = WordList_sentic_Repository()
    sn = SenticNet()
    existWordlistDepression = wordList_depRepo.read()
    wordSenticListDB = wordSenticRepo.read()
    #-------------------------------------------------------------------------

    wordSenticList = set()
    for word in wordSenticListDB:
        wordSenticList.add(word['word'])
    # print("kata word sentic : {}".format(wordSenticList))

    counterUser = 0
    counterTweets = 0
    sumLemmaToken = 0
    sumToken = 0
    sumHasil = 0
    ALL_filtered_sentence = []
    arrayTweet = []
    arrayCleanTweet = []
    arrayUsername = []

    arraySelfScore = []
    arraySentiScore = []
    arrayMDScore = []
    arrayMDScore2 = []
    arrayNegativityScore = []
    arrayNegativityScore2 = []
    arrayAbsolutistScore = []


    for trainUser in trainDepression:
    # for trainUser in trainNormal:
        username = trainUser['username']

        counterUser += 1
        print("{}. User : {}".format(counterUser, username))
        userTweets = trainUser['tweets']
        # print(userTweets)
        # 2. masing2 user punya banyak tweets, tweets per user dibaca per rownya
        sum = 0
        sumMDScore = 0 #. untuk menyimpad MD score per user
        for tweet in userTweets:
            # START
            if sum <1 :
                counterTweets = counterTweets + 1
                #ALL DATA
                # sum = sum + 1
                text = tweet['sentence']['text']

                #2nd - SENTIMEN KALIMAT - check
                print(tweet['sentence'])
                sentiScore = tweet['sentence']['negSentiment']
                arraySentiScore.append(sentiScore)

                print("--------tweet-----------")
                # print("raw tweet                    : {}".format(text))
                arrayTweet.append(text)
                arrayUsername.append(username)
                # print("sentiment negatif : {}".format(sentiScore))
                text = getFivePreprocess(text) #NUMBER, LINK, MENTION, # sign (removal), Dont (conversion)

                #PREPROCESS - lemmatization by wordnet NLTK
                wn_lemmater = WordNetLemmatizer()
                # text = "@coralineada i spoke with a number of developer from underrepresented groups and almost all of them said they"
                tokens = word_tokenize(text)
                token_2 = []
                lemma_2 = []
                for token, tag in pos_tag(tokens):
                    lemma = wn_lemmater.lemmatize(token, tag_map[tag[0]])
                    # print("heyo")
                    # print(tag_map[tag[0]])
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

                # for w in filtered_sentence :


                # ALL_filtered_sentence.append(filtered_sentence)
                if(len(lemma_2)!=len(word_tokens)):
                    print("FIND ME - membuktikan proses cleanbyregex telah mengurangi kata yang tidak jelas(noise)")
                # print("{} token : {}".format(len(word_tokens), word_tokens))
                #  print("{} hasil : {} ".format(len(filtered_sentence),filtered_sentence))
                sumToken = sumToken + len(word_tokens)
                sumHasil  = sumHasil + len(filtered_sentence)

                # 1st - SELF REFERENCES - check
                selfScore = False
                for word in filtered_sentence:
                    if word in self_words:
                        selfScore = True;
                        break
                arraySelfScore.append(selfScore)

                #5 - ABSOLUTIST - check
                absolutistScore = False
                absoluteWord = ['Absolutely', 'All', 'Always', 'Complete', 'Completely',
                                'Constant', 'Constantly', 'Definitely', 'Entire', 'Ever',
                                'Every', 'Everyone', 'Everything', 'Full', 'Must',
                                'Never', 'Nothing', 'Totally', 'Whole']
                for word in filtered_sentence:
                    if word in absoluteWord:
                        absolutistScore = True;
                        break
                arrayAbsolutistScore.append(absolutistScore)

                MDScore = 0
                NegativityScore = 0
                temNegScore = 0
                # print("{} hasil preprocess tweet        : {} ".format(len(filtered_sentence),filtered_sentence))
                arrayCleanTweet.append(filtered_sentence)

                for word in filtered_sentence:
                    # if word in absoluteWord:
                    #     absolutist = True
                    if word in wordSenticList:
                        findWord  = wordSenticRepo.searchWord(word)
                        # print("MD score for             : {}".format(word))
                        MDScore = MDScore + 1
                        for fw in findWord:
                            sentics = fw['senticnet']['sentics']
                            # print("kata : {}, nilai senticsnya : {}".format(word, sentics))
                            # print("sentics negativity : {}".format(abs(float(sentics['sensitivity']))))
                            temNegScore = temNegScore + ( -1 * abs(float(sentics['sensitivity'])))
                            if(float(sentics['pleasantness'])<0):
                                # print("sentics pleasantness : {}".format(sentics['pleasantness']))
                                temNegScore = temNegScore +  float(sentics['pleasantness'])
                            if(float(sentics['aptitude'])<0):
                                # print("sentics aptitude : {}".format(sentics['aptitude']))
                                temNegScore = temNegScore + float(sentics['aptitude'])
                            # print("findWord : {}".format(sentics))

                NegativityScore = temNegScore
                arrayNegativityScore.append(NegativityScore)
                arrayMDScore.append(MDScore) #array untuk menyimpan semua MD score dari tweet2 user
                # arrayAbsolutist.append(absolutist)
                if(MDScore != 0):
                    arrayMDScore2.append(MDScore)
                if (NegativityScore != 0):
                    arrayNegativityScore2.append(NegativityScore)

                print("#SKOR Self Reference              : {}".format(selfScore))
                print("#SKOR negative sentiscore         : {}".format(sentiScore))
                print("#SKOR Negativity Emotion          : {}".format(NegativityScore))
                print("#SKOR Mental Disorder             : {}".format(MDScore)) #MDscore =  menympan nilai MD score per tweet
                import pandas as pd
                item =
                data = [['tom', 10], ['nick', 15], ['juli', 14]]
                sumMDScore = sumMDScore + MDScore
            else: break

        # print("User {} memiliki MDscore         : {}".format(username, sumMDScore))
    print("========================================outlier removal")
    import numpy as np

    arrayMDScoreSorted = arrayNegativityScore2;
    arrayMDScoreSorted.sort()

    print(arrayMDScoreSorted)
    # arrayMDScoreSorted arrayNegativityScore2

    lenMDscore = len(arrayMDScoreSorted)
    print("len : {}".format(lenMDscore))
    print("Q1 len array of MD Score : {} ".format(arrayMDScoreSorted[int((lenMDscore+1)*1/4)]))
    print("Q2 len array of MD Score : {} ".format(arrayMDScoreSorted[int((lenMDscore+1)/2)]))
    print("Q3 len array of MD Score : {} ".format(arrayMDScoreSorted[int((lenMDscore+1)*3/4)]))

    q1 = arrayMDScoreSorted[int((lenMDscore+1)*1/4)]
    q2 = arrayMDScoreSorted[int((lenMDscore+1)/2)]
    q3 = arrayMDScoreSorted[int((lenMDscore+1)*3/4)]

    interquartile = q3 - q1
    batasOutlierBawah = q1 - (1.5 * interquartile)
    batasOutlierAtas = q3 + (1.5 * interquartile)
    #jadi batas bawah pengambilan range adalah -2
    print(" Batas outlier bawah : {}".format(batasOutlierBawah))
    #jadi batas atas pengambilan range adalah 6
    print(" Batas outlier atas : {}".format(batasOutlierAtas))

    if(batasOutlierBawah < arrayMDScoreSorted[0]):
        batasBawah = arrayMDScoreSorted[0]
    else:
        batasBawah = batasOutlierBawah
    if(batasOutlierAtas > arrayMDScoreSorted[len(arrayMDScoreSorted)-1]):
        batasAtas = arrayMDScoreSorted[len(arrayMDScoreSorted)-1]
    else:
        batasAtas = batasOutlierAtas

    print("RULE penggolongan ===============================================")
    # maxRangeMD = arrayMDScore[len(arrayMDScore)-1] - arrayMDScore[0]

    maxRangeMD = batasAtas - batasBawah
    arrayLabel = initArrayNol(len(arraySelfScore)) #akan diisi {NA,least, moderate, most}
    level = ["NA","least","moderate", "most"]
    # =========DENGAN MDSCORE
    # print(level[1])
    # for i in range(len(arrayMDScore)):
    #     # if arraySelfScore[i] == None:
    #     if arraySelfScore[i] != True:
    #         arrayLabel[i] = level[0]
    #         print(arrayLabel[i])
    #     else:
    #         if arraySentiScore[i] > 0:  #kalimat bersentimen Negatif
    #             if arrayNegativityScore[i] !=0 : #tingkat sadnessnya ADA
    #                 if arrayMDScore[i] < maxRangeMD/3:
    #                     arrayLabel[i] = level[2]    #MODERATE 1
    #                 else:
    #                     arrayLabel[i] = level[3]    #MOST 2
    #             else: #tingkat sadnesnya tidak ada
    #                 print("kalimatnya tidak mengandung sadness")
    #                 if arrayMDScore[i] < maxRangeMD/3:
    #                     arrayLabel[i] = level[1]    #LEAST 3
    #                 elif arrayMDScore[i] < (maxRangeMD/3*2):
    #                     arrayLabel[i] = level[2]    #MODERATE 4
    #                 else:
    #                     arrayLabel[i] = level[3]    #MOST 5
    #         else: #kalimat bersentimen positif
    #             print("kalimat nya positif")
    #             if arrayNegativityScore[i] != 0: #tingkat sadnessnya ADA
    #                 if arrayMDScore[i] < maxRangeMD/3:
    #                     arrayLabel[i] = level[1]    #LEAST 6
    #                 else:
    #                     arrayLabel[i] = level[2]    #MODERATE 7
    #             else: #tingkat sadnesnya tidak ada
    #                 print("kalimatnya tidak mengandung sadness")
    #                 if arrayMDScore[i] < maxRangeMD/3:
    #                     arrayLabel[i] = level[1]    #LEAST 8
    #                 elif arrayMDScore[i] < (maxRangeMD/3*2):
    #                     arrayLabel[i] = level[1]    #LEAST 9
    #                 else:
    #                     arrayLabel[i] = level[2]    #MODERATE 10


    print("len selfscore : {} \n len neg sentiscore : {} \n len MD score : {} \n len negativity score : {} \n len mdscore : {}"
          .format(len(arraySelfScore), len(arraySentiScore), len(arrayMDScore), len(arrayNegativityScore), len(arrayLabel)))

    # =========DENGAN negEMO
    # for i in range(len(arrayNegativityScore)):
    #     #versi dengan SELF REF
    #     if arraySelfScore[i] != True:
    #     #versi tanpa self ref
    #     # if arraySelfScore[i] == None:
    #         arrayLabel[i] = level[0]
    #         print(arrayLabel[i])
    #     else:
    #         if arraySentiScore[i] > 0:  #kalimat bersentimen Negatif
    #             if arrayNegativityScore[i] !=0 : #tingkat sadnessnya ADA
    #                 if arrayNegativityScore[i] *-1 < (maxRangeMD/3):
    #                     arrayLabel[i] = level[2]    #MODERATE 1
    #                 else:
    #                     arrayLabel[i] = level[3]    #MOST 2
    #             else: #tingkat sadnesnya tidak ada
    #                 print("kalimatnya tidak mengandung sadness")
    #                 if arrayNegativityScore[i] *-1 < (maxRangeMD/3):
    #                     arrayLabel[i] = level[1]    #LEAST 3
    #                 elif arrayNegativityScore[i] *-1 < (maxRangeMD/3*2):
    #                     arrayLabel[i] = level[2]    #MODERATE 4
    #                 else:
    #                     arrayLabel[i] = level[3]    #MOST 5
    #         else: #kalimat bersentimen positif
    #             print("kalimat nya positif")
    #             if arrayNegativityScore[i] != 0: #tingkat sadnessnya ADA
    #                 if arrayNegativityScore[i] *-1 < (maxRangeMD/3):
    #                     arrayLabel[i] = level[1]    #LEAST 6
    #                 else:
    #                     arrayLabel[i] = level[2]    #MODERATE 7
    #             else: #tingkat sadnesnya tidak ada
    #                 print("kalimatnya tidak mengandung sadness")
    #                 if arrayNegativityScore[i] *-1 < (maxRangeMD/3):
    #                     arrayLabel[i] = level[1]    #LEAST 8
    #                 elif arrayNegativityScore[i] *-1 < (maxRangeMD/3*2)*-1:
    #                     arrayLabel[i] = level[1]    #LEAST 9
    #                 else:
    #                     arrayLabel[i] = level[2]    #MODERATE 10
    #

    # =========DENGAN negEmo range + MDscore if
    #negEmo dg MDcek dulu
    for i in range(len(arrayNegativityScore)):
    #versi dengan SELF REF
        if arraySelfScore[i] != True:
        #versi tanpa self ref
        # if arraySelfScore[i] == None:
            arrayLabel[i] = level[0]
            print(arrayLabel[i])
        else:
            if arraySentiScore[i] > 0:  #kalimat bersentimen Negatif
                if arrayMDScore[i] !=0 : #tingkat MDscorenya ADA
                    if arrayNegativityScore[i] *-1 < (maxRangeMD/3):
                        arrayLabel[i] = level[2]    #MODERATE 1
                    else:
                        arrayLabel[i] = level[3]    #MOST 2
                else: #tingkat MDscorenya tidak ada
                    print("kalimatnya tidak mengandung sadness")
                    if arrayNegativityScore[i] *-1 < (maxRangeMD/3):
                        arrayLabel[i] = level[1]    #LEAST 3
                    elif arrayNegativityScore[i] *-1 < (maxRangeMD/3*2):
                        arrayLabel[i] = level[2]    #MODERATE 4
                    else:
                        arrayLabel[i] = level[3]    #MOST 5
            else: #kalimat bersentimen positif
                print("kalimat nya positif")
                if arrayMDScore[i] != 0: #tingkat MDscore nya ADA
                    if arrayNegativityScore[i] *-1 < (maxRangeMD/3):
                        arrayLabel[i] = level[1]    #LEAST 6
                    else:
                        arrayLabel[i] = level[2]    #MODERATE 7
                else: #tingkat MDscore nya tidak ada
                    print("kalimatnya tidak mengandung sadness")
                    if arrayNegativityScore[i] *-1 < (maxRangeMD/3):
                        arrayLabel[i] = level[1]    #LEAST 8
                    elif arrayNegativityScore[i] *-1 < (maxRangeMD/3*2)*-1:
                        arrayLabel[i] = level[1]    #LEAST 9
                    else:
                        arrayLabel[i] = level[2]    #MODERATE 10

    print("= show tweet + label ===============================================================")
    arrayObjTraindata = []

    for i in range(len(arrayMDScore)):
        tempObj = TrainData(None, arrayUsername[i], arrayTweet[i], arrayCleanTweet[i], arraySelfScore[i],
                            arraySentiScore[i], arrayNegativityScore[i], arrayMDScore[i], arrayLabel[i])
        # pprint.pprint(tempObj.__dict__)
        arrayObjTraindata.append(tempObj)

    sendArrayOfTrainDataToDB(arrayObjTraindata)

    print("================================================================")
    print("Array Self Score : {}".format(arraySelfScore))
    print("Array Senti Score : {}".format(arraySentiScore))
    print("Array MDscore : {}".format(arrayMDScore))
    print("Array Negative Emotion Score : {}".format(arrayNegativityScore))

    # print("Array MDscore : {}".format(sortedMDScore))

    from collections import Counter

    print("=================================================================")
    arraySelfScore.sort()
    CounterValueSelfScore = Counter(arraySelfScore)
    print("Kemunculan SelfScore  : {}".format(CounterValueSelfScore))
    print("=================================================================")
    arraySentiScore.sort()
    CounterValueSentiScore = Counter(arraySentiScore)
    print("Kemunculan Negative SentiScore  : {}".format(CounterValueSentiScore))
    print("Array Negative Sentiscore highest : {}".format(arraySentiScore[len(arraySentiScore) - 1]))
    print("Array Negative Sentiscore lowest: {}".format(arraySentiScore[0]))
    print("=================================================================")

    arrayNegativityScore.sort()
    CounterValueNegativityScore = Counter(arrayNegativityScore)
    print("Kemunculan Negativity Score  : {}".format(CounterValueNegativityScore))
    print("Array Negativity Score highest : {}".format(arrayNegativityScore[len(arrayNegativityScore) - 1]))
    print("Array Negativity Score lowest: {}".format(arrayNegativityScore[0]))

    print("=================================================================")

    arrayMDScore.sort()
    CounterValueMDScore = Counter(arrayMDScore)
    print("Kemunculan MDScore  : {}".format(CounterValueMDScore))
    print("Array MDscore highest : {}".format(arrayMDScore[len(arrayMDScore) - 1]))
    print("Array MDscore lowest: {}".format(arrayMDScore[0]))

    print("=================================================================")
    print(arrayLabel)
    # arrayLabel.sort()
    CounterValueLabel= Counter(arrayLabel)
    print("Kemunculan LABEL  : {}".format(CounterValueLabel))
    print("Array MDscore highest : {}".format(arrayLabel[len(arrayLabel) - 1]))
    print("Array MDscore lowest: {}".format(arrayLabel[0]))

    print("=================================================================")
    print("jumlah user depresi : {}\n jumlah tweet yang dipreproses : {}".format(counterUser, counterTweets))
    print("Jumlah Token lemma : {}".format(sumLemmaToken))
    print("Jumlah Token Awal : {}".format(sumToken))
    print("Jumlah Token Hasil : {}".format(sumHasil))

    # ALL_filtered_sentence =
    # PREPROCESSING - make unique token lemma
    ALL_unique_word = []
    # ALL_unique_word = getUniqueWord(ALL_filtered_sentence)
    #ALL_unique_word adalah daftar kata yang sudah direduce kemunculannya berkali2 hingga muncul daftar kata unique

    # PREPROCESSING - FILTER ONLY RECOGNIZED WORD with sentiword dictionary
    only_recognized_words = []
    # only_recognized_words = getRecognizedWordnet(ALL_unique_word)
    # only_recognized_words adalah daftar kata unique yang sudah ditest di wordnet telah ter recognized








