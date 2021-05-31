import nltk
from nltk.corpus import wordnet
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.chunk import RegexpParser
from nltk.corpus import stopwords
import gmaps
from ipywidgets.embed import embed_minimal_html
import googlemaps
import geocoder
import gmplot
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions
from bokeh.plotting import gmap
import spacy
import operator
from assistantv2 import geocodes
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
    hotwords = ['hotter', 'colder', 'raise', 'lower', 'degree', 'temperature', 'chilly', 'warm', 'temp']

    def process(self, sentence):
        vec = localVectorize(Ac(), sentence)
        lst = getTargetAc(sentence)

        if ('COMMAND' in lst.keys()) | ('DESIRE' in lst.keys()):
            if(vec['lower'] + vec['colder'] > vec['hotter'] + vec['raise']):
                return 'Lowering the temperature'
            else: return 'Raising the temperature'

        elif 'STATEMENT' in lst.keys():
            if(vec['chilly'] + vec['colder'] < vec['hotter'] + vec['warm']):
                return 'Lowering the temperature'
            else: return 'Raising the temperature'

        elif 'AMOUNT' in lst.keys():
            tagged = tkz(sentence)
            comp = False

            i = 0
            while tagged.iloc[i,1] != 'CD': i+=1
            if tagged.iloc[i-1,0].lower() == 'by': comp = True

            num = 0
            for tple in lst['AMOUNT']:
                if tple[1] == 'CD': num = int(tple[0])

            if ('AMOUNT COMP' in lst.keys()) | comp:
                if(vec['chilly'] + vec['colder'] > vec['hotter'] + vec['warm']):
                    return 'Lowering the temperature by ' + str(num) + ' degrees'
                else: return 'Raising the temperature by ' + str(num) + ' degrees'
            else:
                if(vec['lower'] + vec['colder'] > vec['hotter'] + vec['raise']):
                    return 'Setting the temperature to ' + str(num) + ' degrees'
                else: return 'Setting the temperature to ' + str(num) + ' degrees'
        else:
            return 'I\'m sorry, I didn\'t understand that'
class Navigation():
    name = 'Navigation'
    hotwords = ['direct', 'path', 'go']

    def process(self, sentence):
        addr = r'ADDR:{<TO><CD>*(<NNP.*>|<NN.*>)+}', 'ADDR'
        loc = findTarget(sentence, addr)
        gc = geocodes('Cupertino', loc)
        print('\t', gc)

        gmaps.configure(api_key='AIzaSyADV_UuSwm_E-woFGJ_fNZywJV4w7IKbuM')
        fig = gmaps.figure()
        layer = gmaps.directions.Directions(gc[1].latlng, gc[0].latlng ,mode='car')
        fig.add_layer(layer)
        embed_minimal_html('export2.html', views=[fig])

        return loc

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

def Factory(fn):
    dct = {
        'Ac': Ac,
        'Navigation': Navigation,
        'Music': Music,
        'Qmap': Qmap,
        'Qgoog': Qgoog,
        'Question': Question,
        'Qcar': Qcar,
    }
    return dct[fn]


