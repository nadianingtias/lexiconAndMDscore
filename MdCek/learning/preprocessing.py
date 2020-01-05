import re


from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize, pos_tag

from collections import defaultdict

tag_map = defaultdict(lambda : wn.NOUN)
tag_map['J'] = wn.ADJ
tag_map['V'] = wn.VERB
tag_map['R'] = wn.ADV
stop_words =set(stopwords.words('english'))
porter = PorterStemmer()
wn_lemmater = WordNetLemmatizer()

regex_str = [
    # r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs
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

def printsep():
    print("--------------------------------------------------------------------------------------------------------------------")

if __name__ == '__main__':
    array =[10]
    print(array)

    level = ["NA", "least", "moderate", "most"]
    print(level[1])
    text =  "it @marie_brownsuga the fact that i procrastinator and still get shit done is the reason i can't stop procrastinating"

    # text = preprocess(text, True)
    # filtered_sentence = []
    # stemmed_token = []
    # lemmated_token = []
    # for w in text:
    #     # PREPROCESS - STOPWORD REMOVAL
    #     if w not in stop_words:
    #         filtered_sentence.append(w)
    #         stemmed_token.append(porter.stem(w))
    #         # lemmated_token.append(WordNetLemmatizer.lemmatize(w))
    #
    # print("hasil removal regex : {}".format(filtered_sentence))
    # print("hasil stemmed PORTER   : {}".format(stemmed_token))
    print("--------------------------------------------------------------------------------------------------------------------")

    #percobaan lematize dg wordnet- lebih bagus karena menggunkan param POS tag,
    text = "@coralineada i spoke with a number of developer from underrepresented groups and almost all of them said they"
    # tokens = word_tokenize(text)
    # token_2 = []
    # lemma_2 = []
    # for token, tag in pos_tag(tokens):
    #     lemma = wn_lemmater.lemmatize(token, tag_map[tag[0]])
    #     token_2.append(token)
    #     lemma_2.append(lemma)
    #     # print(token, "=>", lemma)
    # print("hasil token      : {}".format(token_2))
    # print("hasil lemma      : {}".format(lemma_2))


    print("--------------------------------------------------------------------------------------------------------------------")

    from senticnet.senticnet import SenticNet

    # sn = SenticNet()
    # word = 'smile'
    # concept_info = sn.concept(word)
    # print("concep_info : {}".format(concept_info))
    #
    # polarity_value = sn.polarity_value('love')
    # print("polarity_value : {}".format(polarity_value ))
    #
    # polarity_intense = sn.polarity_intense('love')
    # print("polarity_intense  : {}".format(polarity_intense ))
    #
    # moodtags = sn.moodtags('love')
    # print("moodtags : {}".format(moodtags ))
    #
    # semantics = sn.semantics('love')
    # print("semantics : {}".format(semantics ))
    #
    # sentics = sn.sentics('love')
    # print("sentics : {}".format(sentics ))
    #
    # printsep()
    #
    # concept_info = sn.concept('cry')
    # print("concep_info : {}".format(concept_info))
    #
    # polarity_value = sn.polarity_value('cry')
    # print("polarity_value : {}".format(polarity_value))
    #
    # polarity_intense = sn.polarity_intense('cry')
    # print("polarity_intense  : {}".format(polarity_intense))
    #
    # moodtags = sn.moodtags('cry')
    # print("moodtags : {}".format(moodtags))
    #
    # semantics = sn.semantics('cry')
    # print("semantics : {}".format(semantics))
    #
    # sentics = sn.sentics('cry')
    # print("sentics : {}".format(sentics))

    print(" SINONIM--------------------------------------------------------------------------------------------------------------------")

    # # First, you're going to need to import wordnet:
    from nltk.corpus import wordnet

    # Then, we're going to use the term "program" to find synsets like so:
    syns = wordnet.synsets("suicidal")

    # An example of a synset:
    print(syns[0].name())

    # Just the word:
    print(syns[0].lemmas()[0].name())

    # Definition of that first synset:
    print(syns[0].definition())

    # Examples of the word in use in sentences:
    print(syns[0].examples())

# ANTONYMS --------------------------
#     synonyms = []
#     antonyms = []
#     syns = wordnet.synsets("good")
#     for syn in syns:
#         for l in syn.lemmas():
#             synonyms.append(l.name())
#             if l.antonyms():
#                 antonyms.append(l.antonyms()[0].name())
#     # print(set(synonyms))
#     print(set(antonyms))
#     if len(antonyms)>0:
#         for i in range(len(antonyms)):
#             print(antonyms[i])

#POS TAG NLTK
    import nltk

    from nltk import word_tokenize, pos_tag

    text = "demand"
    nltk.pos_tag(text)
    print(nltk.pos_tag(text))

    tag_map = defaultdict(lambda: wordnet.NOUN)
    tag_map['J'] = wordnet.ADJ
    tag_map['V'] = wordnet.VERB
    tag_map['R'] = wordnet.ADV
    wn_lemmater = WordNetLemmatizer()

    tokens = word_tokenize(text)
    for token, tag in pos_tag(tokens):
        print("heyo")
        print(token)
        print(tag_map[tag[0]])

    # initialize A and B
    A = {1, 2, 3, 4, 5}
    B = {4, 5, 6, 7, 8}

    C = A.union(B)
    print(C)

    print("-------------------------------------------------------------------------------------------")
    from functools import reduce
    from itertools import groupby
    from operator import add, itemgetter


    def merge_records_by(key, combine):
        """Returns a function that merges two records rec_a and rec_b.
           The records are assumed to have the same value for rec_a[key]
           and rec_b[key].  For all other keys, the values are combined
           using the specified binary operator.
        """
        return lambda rec_a, rec_b: {
            k: rec_a[k] if k == key else combine(rec_a[k], rec_b[k])
            for k in rec_a
        }


    def merge_list_of_records_by(key, combine):
        """Returns a function that merges a list of records, grouped by
           the specified key, with values combined using the specified
           binary operator."""
        keyprop = itemgetter(key)
        return lambda lst: [
            reduce(merge_records_by(key, combine), records)
            for _, records in groupby(sorted(lst, key=keyprop), keyprop)
        ]


    a = [{'time': '25 APR', 'total': 10, 'high': 10},
         {'time': '26 APR', 'total': 5, 'high': 5}]

    b = [{'time': '24 APR', 'total': 10, 'high': 10},
         {'time': '26 APR', 'total': 15, 'high': 5}]
    merger = merge_list_of_records_by('time', add)
    hasil_merge = merger(a+b)
    print(hasil_merge)

    print("sinonim with thesaurus==================================================================")
    # from PyDictionary import PyDictionary
    #
    # dictionary = PyDictionary()
    # print(dictionary.synonym("good"))

    from thesaurus import Word

    w = Word('suicidal')
    syn = w.synonyms()
    print(syn)

    sn = SenticNet()
    try:
        concept_info_sinonim = sn.concept("suicidal")
        print(concept_info_sinonim)
    except Exception as e:
        print(e)