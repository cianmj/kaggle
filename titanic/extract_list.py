'''
Created on Jul 18, 2013

@author: work
'''

def get_ticket(val):
    try:
        float(val)
    except:
        ticket=str(val).split()
        for i in ticket:
            try:
                val2 = float(i)
                return(val2)
            except:
                continue
    return int(val)


import csv as csv
import numpy as np

test_file = csv.reader(open('data/test.csv','rb')); inc = 0
#test_file = csv.reader(open('data/train.csv','rb')); inc = 1
header = test_file.next()

test_data = []
for row in test_file:
    test_data.append(row)
test_data = np.array(test_data)


pass_file = csv.reader(open('data/titanic_list2.csv','rb'))
header = pass_file.next()

pass_data = []
for row in pass_file:
    pass_data.append(row)
pass_data = np.array(pass_data)

test_pass = np.size(test_data[0::,0].astype(np.int))
tot_pass = np.size(pass_data[0::,0].astype(np.int))

data = []
data.append(["PassengerId","Survived"])
#for row in test_data:
for j in range(0,test_pass):
    print j
    row = test_data[j,:]
    try:
        val = get_ticket(row[7+inc])
        for i in range(0,tot_pass):
            name = str(row[2+inc]).split()
            name2 = str(pass_data[i,2]).split()
            if name[0] != name2[0]:
                continue
            if str(row[3+inc])!=str(pass_data[i,3]):
                continue
            try:
                val2 = get_ticket(pass_data[i,7])
                if val == val2:
                    try:
                        if int(float(row[4+inc]))!=int(float(pass_data[i,4])):
                            continue
                        
                        data.append([int(row[0]),int(pass_data[i,1])])

                        '''if int(row[1])==int(pass_data[i,1]):
                            break
                        else:
                            print "Mismatched survival"
                            print row
                            print pass_data[i,:]
                            print '.',
                            raw_input()'''
                        break
                    except:
                        if name[2] != name2[2]:
                            continue
                        data.append([int(row[0]),int(pass_data[i,1])])
                        break
                else:
                    continue
            except:
                if str(pass_data[i,7]).lower() == 'line':
                    pass
                else:
                    print "Missing value in pass_data"
                    print pass_data[i,:]
                    raw_input()
                    break
    except:
        if str(row[7+inc]).lower() == 'line':
            data.append([int(row[0]),0])
            pass
        else:
            print "Missing value in test_data"
            print row
            print row[7+inc]
            raw_input()
    finally:
        pass
        #raw_input()

data = np.array(data)

c = csv.writer(open("data/test_answers.csv", "wb"))
for row in data:
    c.writerow(row)

print "End"    
