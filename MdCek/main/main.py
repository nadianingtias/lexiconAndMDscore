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

    # ------------------------------------------------------------SENTICNET
    from MdCek.DBRepository.WordList_sentic_Repository import WordList_sentic_Repository
    from MdCek.Model.WordList_sentic import WordList_sentic
    import pprint
    from senticnet.senticnet import SenticNet

    wordSentic = WordList_sentic_Repository()
    sn = SenticNet()
    print("-----------------------------------------membaca wordlist depresion yang sudah ada dari NLTK dan textblob")
    # EXISTING WORDLIST NEGATIVE

    existWordlistDepression = wordList_depRepo.read()

    lemmaOfExistWordlist = []
    conceptExist = []
    conceptExistNegative = []
    objsConceptExistNegative = []

    conceptExistPositive = []
    objsConceptExistPositive = []
    sisa = 0

    # print("Jumlah existing wordlist : {} ".format(len(existWordlistDepression)))
    #here it is
    for wordExist in existWordlistDepression:
        word = wordExist['word']
        tokens = word_tokenize(word)

        for token, tag in pos_tag(tokens):
            lemma = wn_lemmater.lemmatize(token, tag_map[tag[0]])
            print("lemma asli : {}".format(lemma))
            if lemma not in lemmaOfExistWordlist:
                lemmaOfExistWordlist.append(lemma)  # 685 lemma unique ditemukan dari DB
                try:
                    syns = wordnet.synsets(lemma)
                    concept_info = sn.concept(lemma)
                    concept_info_origin = concept_info

                    conceptExist.append(concept_info)
                    #word dimasukkan ke dalam objek
                    senticwordObj = WordList_sentic()
                    senticwordObj = WordList_sentic(None,lemma,concept_info) #OBJEK WORD ASLI

                    if (float(concept_info['polarity_intense']) < 0): #TERBUKTI NEGATIF
                        # print(concept_info['polarity_intense'])
                        # conceptExistNegative.append(concept_info)
                        objsConceptExistNegative.append(senticwordObj)
                    elif (float(concept_info['polarity_intense']) > 0): #TIDAK - di senticnet
                        # SINONIM
                        # cek SINONIM di wordnet jika tidak dinyatakan -
                        print("lemma positif masuk di - : {}".format(lemma))
                        sinonim = getSinonim(lemma)
                        concept_info_sinonim = sn.concept(sinonim)

                        #JIKA SINONIMNYA NEG MAKA KATA ITU NEG
                        if (float(concept_info_sinonim['polarity_intense']) < 0):
                            #telah menemukan 8 kata yang harus dibawa negatif (84 - 76)
                            print("lemma negatif ditemukan lagi : {}".format(sinonim))
                            # conceptExistNegative.append(concept_info)

                            #INPUT SINONIM MASUK NEGATIF
                            # senticwordObj = WordList_sentic(None, sinonim, concept_info_sinonim)
                            # objsConceptExistNegative.append(senticwordObj)
                            # print("INI ->")
                            # pprint.pprint(senticwordObj.__dict__)

                            #INPUT KATA LEMA ORIGIN MASUK NEGATIF
                            senticwordObj = WordList_sentic(None, lemma, concept_info_sinonim)
                            objsConceptExistNegative.append(senticwordObj)
                            # print("INI ->")
                            # pprint.pprint(senticwordObj.__dict__)

                        #JIKA SINONIMNYA JUGA POS, COBA CARI ANTONIMNYA
                        elif (float(concept_info['polarity_intense']) > 0): #masih tidak dinyatakan - cari antonimnya
                            # ANTONIM
                            print("sinonim LEMMA ORIGIN masih positif: {}".format(sinonim))
                            antonyms = getAntonimss(lemma)
                            print(set(antonyms))

                            if len(antonyms) > 0: #KETEMU ANTONIMNYA
                                print(antonyms[0]) #INI adalah antonim yang akan dicari
                                concept_info_antonym = sn.concept(antonyms[0])  #mencari concept dar antonimnya
                                if (float(concept_info_antonym['polarity_intense']) < 0): #BUKTI SALAH LETAK, antonimnya neg, lmma asli sungguh +
                                    # conceptExistPositive.append(concept_info_origin)
                                    senticwordObj = WordList_sentic(None, lemma, concept_info_origin)
                                    objsConceptExistPositive.append(senticwordObj)

                                elif (float(concept_info_antonym['polarity_intense']) > 0):  # proses 6
                                    print("ADA ANTONIM yang positif")  #artinya dia masih NEGATIF kata lemma asalnya
                                    text = antonyms[0]
                                    tokens = word_tokenize(text)
                                    for token, tag in pos_tag(tokens):
                                        print("heyo")
                                        print(token)
                                        pos = tag_map[tag[0]]
                                        print(tag_map[tag[0]])
                                    if pos != 'n':
                                        # 7. REVERSE DULU - TODO
                                        # reverse_concept = getReverseConcept(concept_info_antonym)
                                        reverse_concept = concept_info_antonym
                                        print("ADA ANTONIM yang positif dan bukan NOUN")
                                        # 8. MASUKKAN NEGATIF
                                        # conceptExistNegative.append(reverse_concept)
                                        # senticwordObj = WordList_sentic(None, sinonim, reverse_concept)
                                        # objsConceptExistNegative.append(senticwordObj)

                                        senticwordObj = WordList_sentic(None, lemma, reverse_concept)
                                        objsConceptExistNegative.append(senticwordObj)
                                    else:
                                        sisa = sisa + 1
                                else:
                                    senticwordObj = WordList_sentic(None, lemma, concept_info_origin)
                                    objsConceptExistPositive.append(senticwordObj)
                            else:
                                print("tidak ada antonim")
                                # sinonim2 = syns[0].lemmas()[0].name()
                                # concept_info = sn.concept(sinonim2)

                                # conceptExistPositive.append(concept_info_origin)
                                senticwordObj = WordList_sentic(None, lemma, concept_info_origin)
                                objsConceptExistPositive.append(senticwordObj)
                        else:
                            senticwordObj = WordList_sentic(None, lemma, concept_info_origin)
                            objsConceptExistPositive.append(senticwordObj)
                    else:
                        senticwordObj = WordList_sentic(None, lemma, concept_info_origin)
                        objsConceptExistPositive.append(senticwordObj)
                except Exception as e:
                    print(e)

    print("Jumlah lemma dari existing wordlist : {} ".format(len(lemmaOfExistWordlist)))
    print("Jumlah lemma di senticnet dari existing wordlist : {} ".format(len(conceptExist)))
    print("Jumlah lemma negatif di senticnet dari existing wordlist : {} ".format(len(conceptExistNegative)))
    print("--Jumlah lemma negatif di senticnet dari existing wordlist : {} ".format(len(objsConceptExistNegative)))
    print("Jumlah lemma positif di senticnet dari existing wordlist : {} ".format(len(conceptExistPositive)))
    print("Jumlah lemma positif di senticnet dari existing wordlist : {} ".format(len(objsConceptExistPositive)))
    print("sisa : {} ".format(sisa))

    print("-------------------------------------------")

    for word in wordSentic.read():
        print("word ")
        pprint.pprint(word)

    tambahanKataNegatif  = objsConceptExistNegative
    print("jumlah kata negatif tambahan dari NLTK n textblob : {}".format(len(tambahanKataNegatif)))
    for i in range(len(tambahanKataNegatif)):
        # print(" HALO -> : {}".format(tambahanKataNegatif[i].word))
        word = tambahanKataNegatif[i].word
        cursor = wordSentic.searchWord(tambahanKataNegatif[i].word)
        ada = False
        for data in cursor:
            ada = True
        if ada:
            # print("ada yg sama di {}".format(i))
            print("ada yg sama di {}".format(i))
        elif ada != True:
            try:
                print("ada yg tidak sama di  {}".format(i))
                concept_info = sn.concept(word)
                senticwordObj = WordList_sentic(None, word, concept_info)

                if float(senticwordObj.senticnet['polarity_intense'])<0:
                    #CREATE in DB
                    print("sudah create 13 instance negatif baru")
                    # wordSentic.create(senticwordObj)
                else:
                    pprint.pprint("ini masih positive {}".format(senticwordObj.__dict__))
                    #CARI SINONIM YUKS
                    sinonim = getSinonim(word)
                    concept_info_sinonim = sn.concept(sinonim)
                    if float(concept_info_sinonim['polarity_intense'])<0:
                        pprint.pprint("{} ini positive ketemu negatifnya {}".format(word,concept_info_sinonim))
                        senticwordObj = WordList_sentic(None, word, concept_info_sinonim)
                        # CREATE in DB
                        print("sudah create 5 instance negatif baru")
                        # wordSentic.create(senticwordObj)

                    else:
                        print("bandel positif wkwk")
                        print(sinonim)
                    # cek sinonim
            except Exception as e:
                print(e)
            # wordSentic.create(senticwordObj)

    print("----------------------------------------- membaca wordlist depresion from 0")
    sumSenticnetWord = 0;
    # negSenticnetWord = 0;
    objsConceptNegative = []
    objsConceptPositive = []

    conceptAll = []
    i  = 0

    for i in range(len(only_recognized_words)):

        # print(type(only_recognized_words[i]))
        # print(only_recognized_words[i])
        word = only_recognized_words[i]

        # concept_info = SenticNet.concept(word)
        # print("concep_info {} : {}".format(word, concept_info))
        try:
            concept_info = sn.concept(word)
            # print("concep_info {} : {}".format(word, concept_info))
            senticwordObj = WordList_sentic()
            senticwordObj = WordList_sentic(None, word, concept_info)  # OBJEK WORD ASLI

            if (float(concept_info['polarity_intense']) < 0): #jika bermuatan negatif
                print(concept_info['polarity_intense'])
                conceptAll.append(concept_info)
                # negSenticnetWord = negSenticnetWord + 1
                objsConceptNegative.append(senticwordObj)

                #!!!!!!!!! PROSES MASUKKAN DB
                # wordSentic.create(senticwordObj)
            else:
                sinonim = getSinonim(word) #WITH WORDNET

                concept_info_sinonim = sn.concept(sinonim)

                # JIKA SINONIMNYA NEG MAKA KATA ITU NEG
                if (float(concept_info_sinonim['polarity_intense']) < 0): #JIKA sinonimnya bersentimen negatif
                    cursor = wordSentic.searchWord(word) #dicari dulu apakah sudah ada di DB, jika belum CREATE NEW
                    ada = False
                    for data in cursor:
                        pprint.pprint(word)
                        ada = True
                    if ada == True:
                        print("ada nih")
                    else:
                        sinonim2 = getSinonim(sinonim)
                        concept_info_sinonim2 = sn.concept(sinonim2)
                        if (float(concept_info_sinonim2['polarity_intense']) < 0):

                            print("tidak ada : {} {}".format(sinonim, sinonim2))
                            senticwordObj = WordList_sentic(None, word, concept_info_sinonim2)

                            pprint.pprint("{} ini sudah ketemu negatifnya {}".format(word, concept_info_sinonim2))
                            # !!!!!!!!! PROSES MASUKKAN DB
                            # wordSentic.create(senticwordObj) #CREATE - menambahkan word ke dalam wordlist dg nilai SINONIM
                            objsConceptNegative.append(senticwordObj)
                else:
                    print("word {} : sinonim {} -> memang positif {}".format(word, sinonim, concept_info_sinonim['polarity_intense']))
                    objsConceptPositive.append(senticwordObj)
            sumSenticnetWord = sumSenticnetWord + 1
        except Exception as e :
            print(e)
            # print("An exception occurred")
        i = i+1


    print("Total wordlist  : {}".format(sumSenticnetWord))
    print("Total wordlist negatif : {}".format(len(objsConceptNegative)))

    # ------------------------------------------------------------SENTICNET gabungan

    # unionConcept= []
    # unionConcept = conceptAll
    # print("konsep ALL : {}".format(conceptAll))
    # print("konsep Exist NEGATIVE: {}".format(conceptExistNegative))
    # i = 0
    # tambahan = 0
    # for i in range(len(conceptExistNegative)):
    #     if conceptExistNegative[i] not in unionConcept:
    #         unionConcept.append(conceptExistNegative[i])
    #         print(conceptExistNegative[i])
    #         tambahan = tambahan + 1
    #     i = i+1
    #
    # print("Total wordlist gabungan  : {}".format(len(unionConcept)))
    # print("tambahan kata dari existing wordlist : {}:".format(tambahan))


    # ------------------------------------------------------------SENTICNET gabungan NEGATIF
    # unionObjNegatif = []
    # unionObjNegatif = objsConceptNegative
    # tambahan = 0
    # for i in range(len(objsConceptExistNegative)):
    #     if objsConceptExistNegative[i] not in unionObjNegatif:
    #         unionObjNegatif.append(objsConceptExistNegative[i])
    #         print(objsConceptExistNegative[i])
    #         tambahan = tambahan+1
    #     i = i+1
    #
    # print("Total wordlist gabungan  : {}".format(len(unionObjNegatif)))
    # print("tambahan kata dari existing wordlist : {}:".format(tambahan))

    # ------------------------------------------------------------SENTICNET gabungan NEGATIF
    # unionObjNegatif = ()
    # unionObjNegatif = objsConceptExistNegative + objsConceptNegative
    # unionObjNegatif = set(unionObjNegatif)
    # print("Total wordlist gabungan  : {}".format(len(unionObjNegatif)))
    #
    #
    # objsConceptNegativeSet = objsConceptExistNegativeSet = set
    #
    # objsConceptNegativeSet = set(objsConceptNegative)
    # objsConceptExistNegativeSet = set(objsConceptExistNegative)
    # print("total awal konsep all : {}".format(len(objsConceptNegativeSet)))
    # print("total awal konsep exist : {}".format(len(objsConceptExistNegativeSet)))
    # objsConceptNegativeSet.union(objsConceptExistNegative)
    # print("total akhir : {}".format(len(objsConceptNegativeSet)))

    #---------------------------------------------------------------------------
    # from functools import reduce
    # from itertools import groupby
    # from operator import add, itemgetter
    #
    #
    # def merge_records_by(key, combine):
    #     """Returns a function that merges two records rec_a and rec_b.
    #        The records are assumed to have the same value for rec_a[key]
    #        and rec_b[key].  For all other keys, the values are combined
    #        using the specified binary operator.
    #     """
    #     return lambda rec_a, rec_b: {
    #         k: rec_a[k] if k == key else combine(rec_a[k], rec_b[k])
    #         for k in rec_a
    #     }
    #
    # def merge_list_of_records_by(key, combine):
    #     """Returns a function that merges a list of records, grouped by
    #        the specified key, with values combined using the specified
    #        binary operator."""
    #     keyprop = itemgetter(key)
    #     return lambda lst: [
    #         reduce(merge_records_by(key, combine), records)
    #         for _, records in groupby(sorted(lst, key=keyprop), keyprop)
    #     ]
    #
    # merger = merge_list_of_records_by('time', add)
    # hasil_merge = merger(objsConceptExistNegative + objsConceptNegative)
    # print("total hasil merge : {}".format(hasil_merge) )