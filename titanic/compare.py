'''
Created on Jul 8, 2013

@author: work
'''
import numpy as np
import csv as csv

def compare_results():
    
    f1=csv.reader(open("data/test_answers.csv","rb"))
    f2=csv.reader(open("results/test_results.csv","rb"))
    header = f1.next(); header = f2.next()
        
    data1 = [];
    for row in f1:
        data1.append(row)
    data1 = np.array(data1)
    
    data2 = [];
    for row in f2:
        data2.append(row)
    data2 = np.array(data2)
    
    same = 0.; diff = 0.
    for i,row in enumerate(data1):
        if int(row[1])==int(data2[i,1]):
            same +=1.
        else:
            diff +=1.
  
    #print "Correct:",same
    #print "False:",diff
    #print "Total:", float(same + diff)
    #print "Result:", float(same/(same+diff))
    return float(same/(same+diff))
