'''
Created on Jul 7, 2013

@author: work
'''
import csv as csv
import numpy as np

def import_data(file_name):

    csv_file = csv.reader(open('data/'+file_name+'.csv','rb'))
    header = csv_file.next()
    
    data = []
    for row in csv_file:
        data.append(row)
    data = np.array(data)

# input extra column due to missing survival data
    if file_name == "test":
        data = np.insert(data,1,'0',axis=1)

    
    '''Assign passenger names to int
    Mr.=0; Mrs.=1; Miss.=2;Rev.=3;Master.=4
    '''
    number_passengers = np.size(data[0::,0].astype(np.float))
    for row in range(number_passengers):
        name = str(data[row,3]).split()
        for word in name:
            if word=="Mr." or word=="Don." or word=="Major." or word=="Col." or word=="Jonkheer.":
                data[row,3]="0"
            elif word=="Mrs." or word=="Mrs" or word=="Mme.":
                data[row,3]='1'
            elif word=="Miss." or word=="Ms." or word=="Mlle.":
                data[row,3]='1'
            elif word=="Sir." or word=="Countess." or word=="Lady.":
                data[row,3]='1'
            elif word=="Master.":
                data[row,3]='2'
            elif word=="Rev." or word=="Dr." or word=="Capt.":
                data[row,3] = '0'
            else:
                continue

        sex=str(data[row,4])
        if sex.lower()=="male":
            data[row,4] = '0'
        elif sex.lower()=="female":
            data[row,4] = '1'
        else:
            data[row,4] = '2'
    
    # Handle missing data or exceptions to the above assignments
    for row in range(number_passengers):
        try:
            float(data[row,3])
        except:
            data[row,3]='3'
    
    #Calculate average age per title (i.e. "Mr."=0,..)
    age = np.array(np.zeros(np.size(np.unique(data[:,3]))))#[0.,0.,0.,0.,0.])
    total = np.array(np.zeros(np.size(np.unique(data[:,3]))))#[0.,0.,0.,0.,0.])
    for row in range(number_passengers):
        try:
            indx = np.int32(data[row,3])
            age[indx]+=np.float(data[row,5])
            total[indx]+=1.
        except:
            continue
    for i in range(np.size(age)):
        if total[i] == 0:
            age[i] = 0
        else:
            age[i] /= float(total[i])
    

    # Assign average age to missing value corresponding to title
    for row in range(number_passengers):
        try:
            data[row,5] = np.str(np.int32(data[row,5]))
        except:
            indx = np.int32(data[row,3])
            data[row,5]=np.str(np.int32(age[indx]))
        finally:
            val = np.int32(data[row,5])
            if val<=14:
                data[row,5] = '0'
            elif val>14 and val<=25:
                data[row,5] = '1'
            elif val>25 and val<=40:
                data[row,5] = '1'
            elif val>40 and val<=60:
                data[row,5] = '1'
            else: 
                data[row,5] = '2'
            #data[row,5] = np.str(int(data[row,5])/14)

        # Number of Siblings/Spouses
        try:
            data[row,6] = np.str(np.int32(data[row,6]))
        except:
            data[row,6] = '0'
        finally:
            val = np.int32(data[row,6])
            if val==0 or val>2:
                data[row,6] = '0'
            elif val == 1 or val == 2:
                data[row,6] = '1'
            else:
                data[row,6] = '0'
                
        # Number of Parents/Children
        try:
            data[row,7] = np.str(np.int32(data[row,7]))
        except:
            data[row,7] = '0'
        finally:
            val = np.int32(data[row,7])
            if val==0 or val>3:
                data[row,7] = '0'
            elif val == 1 or val == 2 or val == 3:
                data[row,7] = '1'
            else:
                data[row,7] = '0'   

    
    # Scanning through ticket number
        try:
            float(data[row,8])
        except:
            ticket=str(data[row,8]).split()
            for i in ticket:
                try:
                    data[row,8] = np.str(int(i))
                except:
                    continue
    
    # Assign ticket number to small integers based on values
    for row in range(number_passengers):
        try:
            val = np.float(data[row,8])
            if val<100000:
                data[row,8] = '0'
            elif val>=100000 and val<200000:
                data[row,8] = '0'
            elif val>=200000 and val<300000:
                data[row,8] = '0'
            elif val>=300000 and val<500000:
                data[row,8] = '1'
            else:
                data[row,8] = '1'
        except:
            data[row,8] = '0'
    
    # Verify cabin fare + change to integer
    for row in range(number_passengers):
        try:
            data[row,9] = np.int32(float(data[row,9]))
        except:
            data[row,9] = str(np.int32(9 * (4-data[row,2].astype(int))**1.5))
        finally:
            val = float(data[row,9])
            if val<=9:
                data[row,9] = '0'
            elif val>9 and val<=20:
                data[row,9] = '1'
            elif val>20 and val<=30:
                data[row,9] = '1'
            elif val>30 and val<=53:
                data[row,9] = '1'
            elif val>53 and val<=100:
                data[row,9] = '2'
            else: 
                data[row,9] = '2'
        
    
    # Cabin number
    for row in range(number_passengers):
        try:
            cabin = np.str(data[row,10])[0]
            for i in cabin:
                if i.lower()=='a':
                    data[row,10] = '0'
                elif i.lower()=='b':
                    data[row,10] = '0'
                elif i.lower()=='c':
                    data[row,10] = '0'
                elif i.lower()=='d':
                    data[row,10] = '0'
                elif i.lower()=='e':
                    data[row,10] = '1'
                elif i.lower()=='f':
                    data[row,10] = '1'
                elif i.lower()=='g':
                    data[row,10] = '1'
                else:
                    data[row,10] = '1'
                break
        except:
            data[row,10] = '2'
            continue
    
    # Point of embarkment classification
    for row in range(number_passengers):
        try:
            port = np.str(data[row,11])
            if port.lower() == 'c':
                data[row,11] = '0'
            elif port.lower() == 'q':
                data[row,11] = '1'
            elif port.lower() == 's':
                data[row,11] = '2'
            else:
                data[row,11] = '2'
        except:
            data[row,11] = '2'
            continue
    
    c = csv.writer(open('data/'+file_name+"_mod.csv", "wb"))
    for row in data:
        c.writerow(row)
    
    return data


