'''
Created on Jul 8, 2013

@author: work
'''

def print_results(val):

    f = open("results/test_results.csv","w")
    f.write("PassengerId,Survived\n")
    for i in range(len(val)):
        f.write(str(892+i)+','+str(int(val[i]))+'\n')
    f.close()
