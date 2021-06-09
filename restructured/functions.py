import nltk
from nltk.corpus import wordnet
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.chunk import RegexpParser
from nltk.corpus import stopwords
import spacy
import operator
import re
from assistantv2 import getSong
from assistantv2 import hasSubject
from assistantv2 import findTarget
from assistantv2 import getTargetAc
from assistantv2 import localVectorize
from assistantv2 import vectorize
from assistantv2 import tkz
from q import Qgoog
from q import Qmap
from q import Qcar

# This function will be used to classify the 
def classifier2(funcs, sentence):
    v = vectorize(funcs, sentence)
    if(v['Qgoog'] == max(v.values())): return Factory('Qgoog')
    temp = max(v.items(), key=operator.itemgetter(1))[0]
    return Factory(temp)


class Ac():
    name = 'Ac'
    hotwords = ['hotter', 'colder', 'raise', 'lower', 'degree', 'temperature', 'chilly', 'warm', 'temp', 'warmer', 'cooler']

    def process(self, sentence):
        vec = localVectorize(Ac(), sentence)
        lst = getTargetAc(sentence)

        hot = vec['hotter'] + vec['raise'] + vec['warm'] + vec['warmer']
        cold = vec['colder'] + vec['lower'] + vec['chilly'] + vec['cooler']
        
        if 'AMOUNT' in lst.keys():
            num = 0
            for tple in lst['AMOUNT']:
                if tple[1] == 'CD': num = int(tple[0])

            if 'cmp1' in lst.keys():
                if(cold > hot):
                    return 'Lowering the temperature by ' + str(num) + ' degrees'
                else: return 'Raising the temperature by ' + str(num) + ' degrees'
            elif 'cmp2' in lst.keys():
                if(cold > hot):
                    return 'Lowering the temperature by ' + str(num) + ' degrees'
                else: return 'Raising the temperature by ' + str(num) + ' degrees'                
            else:
                if(cold > hot):
                    return 'Setting the temperature to ' + str(num) + ' degrees'
                else: return 'Setting the temperature to ' + str(num) + ' degrees'
        elif ('COMMAND' in lst.keys()) | ('DESIRE' in lst.keys()):
            if(cold > hot):
                return 'Lowering the temperature'
            else: return 'Raising the temperature'

        elif 'STATEMENT' in lst.keys():
            if(cold < hot):
                return 'Lowering the temperature'
            else: return 'Raising the temperature'
        else:
            return 'I\'m sorry, I didn\'t understand that'

class Navigation():
    name = 'Navigation'
    hotwords = ['direct', 'path', 'go']

    def process(self, sentence):
        addr = r'ADDR:{<TO><CD>*(<NNP.*>|<NN.*>)+}', 'ADDR'
        loc = findTarget(sentence, addr)
        return 'Getting directions to' + loc

class Music():
    name = 'Music'
    hotwords = ['play', 'spotify', 'music', 'raise', 'lower', 'volume']
        
    def process(self, sentence):
        s = getSong(sentence)
        return ('Playing' + s)

class Question():
    name = 'Question'
    hotwords = ['What', 'Where', 'How', 'When', 'Are']

    def process(self, sentence):
        obj = classifier2([Qgoog(), Qmap(), Qcar()], sentence)
        return obj.process(obj, sentence)

class Lights():
    name = 'Lights'
    rooms = ['living room', 'garage', 'kitchen', 'bedroom']
    hotwords = ['room', 'lights', 'on', 'off', 'dim', 'bright', 'brighter', 'dimmer', 'brighten'] + rooms
    def process(self, sentence):
        v = localVectorize(Lights(), sentence)
        r = ''
        ret = ''
        for room in self.rooms:
            if re.findall(room, sentence) != [] : r = room + ' '
        if ((v['dim'] == 1) | (v['dimmer'] == 1)):
            ret = 'Dimming '
        elif (((v['bright'] == 1) | (v['brighter'] == 1)) | (v['brighten'] == 1)):
            ret = 'Brightening '
        elif v['on'] == 1:
            ret = 'Turning On '
        elif v['off'] == 1:
            ret = 'Turning off '
        return ret + r + 'lights'



def Factory(fn):
    dct = {
        'Ac': Ac,
        'Navigation': Navigation,
        'Music': Music,
        'Qmap': Qmap,
        'Qgoog': Qgoog,
        'Question': Question,
        'Qcar': Qcar,
        'House': Lights
    }
    return dct[fn]


