import nltk
from nltk.corpus import wordnet
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.chunk import RegexpParser
from nltk.corpus import stopwords
import spacy

simlex = pd.read_csv('./project/restructured/data/SimLex-999.txt', sep='\r' ,delimiter='\t')

verbs = pd.read_csv('./project/restructured/data/SimVerb-3500.txt', sep='\r' ,delimiter='\t', header=None)
verbs.columns = ['word1', 'word2', 'pos', 'similarity', 'notes']

def tkz(sentence):
    tags = nltk.pos_tag(nltk.word_tokenize(sentence))
    df = pd.DataFrame(tags)
    df.columns = ['word', 'tag']
    return df

def lemmatizeDF(data):
        for i in range (len(data)):
            w = WordNetLemmatizer().lemmatize(data[i].lower())
            data[i] = w

def verbSearch(tagged, htw, j):
    m = 0
    verbsearch = verbs[
        ((verbs['word1'] == tagged.iloc[j,0].lower()) | (verbs['word1'] == htw[0].lower())) &
        ((verbs['word2'] == tagged.iloc[j,0].lower()) | (verbs['word2'] == htw[0].lower()))
        ]    
    if(not(len(verbsearch) == 0)):
        m = max(verbsearch['similarity'])
        
    if(not(m == 0)):
        return 1
    else:
        return 0

def synSearch(tagged, htw, j):
    m = 0
    syns = []
    for syn in wordnet.synsets(htw[0]):
        for l in syn.lemmas():
            syns.append(l.name())
    if(tagged.iloc[j,0].lower() in syns):
        m = 1
    return m

def wordSearch(tagged, htw, j):
    stem1 = SnowballStemmer('english').stem(tagged.iloc[j,0])
    stem2 = SnowballStemmer('english').stem(htw[0])
    if( stem1 == stem2 ):
        return 1
    return 0

# funcs will be a list filled with one object of each function class
def vectorize(funcs, sentence):
    tagged = tkz(sentence)
    lemmatizeDF(tagged.word)
    v = {}
    for f in funcs:
        v[f.name] = 0

    for f in funcs:
        for htw in f.hotwords:
            m = 0
            for j in range(0, tagged.shape[0]):
                vm = verbSearch(tagged, [htw], j)
                sm = synSearch(tagged, [htw], j)
                wm = wordSearch(tagged, [htw], j)
                m += max(vm, sm, wm)
            v[f.name] += m
    return v
                    
def findTarget(string, regtuple):
    chunker = RegexpParser(regtuple[0])
    tr = chunker.parse(nltk.pos_tag(nltk.word_tokenize(string)))

    subtr = 0
    for t in tr.subtrees(filter=lambda x: x.label() == regtuple[1]):
        subtr = t

    ret = ''
    if(subtr != 0):
        for node in subtr:
            if(node[1].lower() not in stopwords.words('english')):
                ret += node[0] + ' '
    return ret

def getSong(string):
    start = string.lower().find('play')
    end = string.lower().find('on')
    if(end == -1):
        end = string.lower().find('by')
    if(not(end == -1)): 
        return string[start+4:end]
    return string[start+4:]

def hasSubject(sentence):

    spcy = spacy.load('en_core_web_sm')
    doc=spcy(sentence)

    #sub_toks = [(tok,tok.dep_,) for tok in doc]

    hasSubj = False
    for tok in doc:
        if(tok.dep_ == 'nsubj'):
            hasSubj = True
    return hasSubj

def getTargetAc(sentence):
    grammar = '''
        DESIRE: {<VB.*|MP><PRP>}
        COMMAND: {<JJR|VB.*><PRP|DT>}
        STATEMENT: {<PRP><VBZ|VBP><RB>?<RB|JJ>}
        AMOUNT: {<CD><NNS>?}
        cmp1: {<IN><AMOUNT>}
        cmp2: {<AMOUNT><VB.*|NN.*>}

    '''
    chunker = nltk.RegexpParser(grammar)
    t = chunker.parse(nltk.pos_tag(nltk.word_tokenize(sentence)))

    lst = {}
    target = 0
    category = ''
    for tree in t.subtrees():
        if tree.label() == 'cmp1':
            target = (tree.leaves())
            category = 'cmp1'
            lst[category] = target
        elif tree.label() == 'cmp2':
            target = (tree.leaves())
            category = 'cmp2'
            lst[category] = target
        elif tree.label() == 'AMOUNT':
            target = (tree.leaves())
            category = 'AMOUNT'
            lst[category] = target
        elif tree.label() == 'COMMAND': 
            target = (tree.leaves())
            category = 'COMMAND'
            lst[category] = target
        elif tree.label() == 'DESIRE': 
            target = (tree.leaves())
            category = 'DESIRE'
            lst[category] = target
        elif tree.label() == 'STATEMENT': 
            target = (tree.leaves())
            category = 'STATEMENT'
            lst[category] = target
        
    return lst

def localVectorize(obj, sentence):
    tagged = tkz(sentence)
    lemmatizeDF(tagged.word)
    v = {}
    for htw in obj.hotwords:
        m = 0
        for j in range(0, tagged.shape[0]):
            vm = verbSearch(tagged, [htw], j)
            sm = synSearch(tagged, [htw], j)
            wm = wordSearch(tagged, [htw], j)
            m += max(vm, sm, wm)
        v[htw]  = m
    return v

