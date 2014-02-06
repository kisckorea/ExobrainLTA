'''
Created on 2014. 2. 6.

@author: Seongchan
'''

from operator import itemgetter

dic = {}
dic['a'] = 2
dic['b'] = 1
dic['c'] = 5
sortedx= sorted(dic.iteritems(), key=itemgetter(1), reverse=True)
print(sortedx)
sortedxx= dict(sortedx)
print sortedxx
