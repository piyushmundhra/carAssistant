from functions import Factory
from functions import Ac
from functions import Navigation
from functions import Music
from functions import Qgoog
from functions import Qmap
from functions import Question
from assistantv2 import vectorize
from assistantv2 import localVectorize
from assistantv2 import getTargetAc
import operator

# Before I use a machine learning classifier, I am going to make a quite naive classification algorithm. 
# Once I have collected enough data, I will implement a deep learning/machine learning classifier
def classifier(funcs, sentence):
    v = vectorize(funcs, sentence)
    temp = max(v.items(), key=operator.itemgetter(1))[0]
    return Factory(temp)

def harness(l):
    while(1>0):
        s = input()
        if (s.lower() == 'exit') | (s.lower() == 'end'): break
        else: 
            obj = classifier(lst, s)
            print(obj.process(obj,s), '\n')

ac = Ac()
navi = Navigation()
music = Music()
question = Question()
lst = [ac, navi, music, question]

print('\n')

harness(lst)