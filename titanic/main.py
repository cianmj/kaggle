'''
Created on Jul 8, 2013

@author: work
'''
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import itertools as itt
import csv as csv

import data_processing as dp
import forest as fr
import l1_penalty as l1
#import mlpy_llc as mlpy
import compare as compare
import neutral_network as nn

def map_feature(x):
    """ Add polynomial features to x in order to reduce high bias.
    """
    m, n = x.shape
    out = x

    # Add quodratic features.
    for i in range(n):
        for j in range(i, n):
            out = np.hstack((out, x[:, i].reshape(m, 1) * x[:, j].reshape(m, 1)))

    # Add cubic features.
    for i in range(n):
        for j in range(i, n):
            for k in range(j, n):
                out = np.hstack(
                    (out, x[:, i].reshape(m, 1) * x[:, j].reshape(m, 1) * x[:, k].reshape(m, 1)))
    return out


def scale_data(x):
    """ Scale data with zero mean and unit variance.
    """
    mu = x.mean(axis=0)
    sigma = x.std(axis=0)
    x = (x - mu) / sigma
    return (x, mu, sigma)


def calculate_distribution(x):
    dist = []
    for i in range(1,x.shape[1]):
        bins = np.bincount(x[:,i])
        counts = np.array(np.zeros(bins.shape[0]))
        for j in range(0,np.size(x[:,i])):
            if x[j,0]==1:
                counts[x[j,i]]+=1
        for j in range(0,np.size(counts)):
            if bins[j]==0 or counts[j]==0:
                counts[j]=0.
            else:
                counts[j]/=bins[j]
        dist.append(counts)
    return np.array(dist)

def combinations_with_replacement(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    if not n and r:
        return
    indices = [0] * r
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != n - 1:
                break
        else:
            return
        indices[i:] = [indices[i] + 1] * (r - i)
        yield tuple(pool[i] for i in indices)



if __name__ == '__main__':

# Read in data
    for i in range(0,1):
        file_train = "train"
        data0 = np.array(dp.import_data(file_train))
        data0 = data0.astype(np.int)
        
        file_test = "test"
        test_data0 = np.array(dp.import_data(file_test))
        test_data0 = test_data0.astype(np.int)
		
        out_best=csv.writer(open("results/best_results.csv","wb"))
        best_result = 0.
        best_val = []
        ival = range(1,11)
        print(ival)
        c = [1,2,6,8,10] 
        for n_est in range(23,24,1):
            maxd = n_est%50 + 1
        #for c in combinations_with_replacement(ival,10):
            print(c)       
            #Slice select data out (i.e. passenger numbers)
            data = sp.delete(data0,0,1); test_data = sp.delete(test_data0,0,1)
            for i in range(len(data[0])-1,0,-1):
                if i in c:
                    continue
                else:
                    data = sp.delete(data,i,1)
                    test_data = sp.delete(test_data,i,1)
            '''
        	# Normalize data in each column (i.e. feature scaling)
            for i in range(1,len(data[0])):
                data[:,i] = 10.*(data[:,i] - np.mean(data[:,i]))/np.std(data[:,i])
                test_data[:,i] = 10.*(test_data[:,i] - np.mean(test_data[:,i]))/np.std(test_data[:,i])
           '''
           # Divide into training and test data (or import test data)
            test = True
            if test:
                cut = 1. * np.size(data[:,0])
            else:
                cut = .7 * np.size(data[:,0])
            train_data = data[:cut,0:]        
            if not test:
                test_data = data[cut:,0:]
                print(np.mean(data[:,0]))
                print(calculate_distribution(train_data))
            
            map_feature(train_data); map_feature(test_data)
            train_data_scale,mu,sigma = scale_data(train_data[:,1:])
            train_data = np.column_stack((train_data[:,0],train_data_scale))
            test_data = np.column_stack((test_data[:,0],(test_data[:,1:]-mu)/sigma))
    
            if test:
                fr.forest_solver(train_data,test_data,n_est)
                #mlpy.llc_solver(train_data,test_data)
                #l1.l1_penalty_solver(train_data,test_data,n_est,maxd)
                #nn.neutral_net(train_data,test_data,n_est,maxd)        
                result = compare.compare_results()
                #exit()
            else:
                print(l1.l1_penalty_solver(train_data,test_data))

            if result>best_result:
                best_result = result
                best_val = c
                out_best.writerow([best_result,best_val,n_est,maxd])


        print("Best Results:")
        print(best_result)
        print(best_val)
        exit()

        xp = []; yp = []
        for i in range(1,9):
            cut2 = int(cut*0.1*i)
            train_data = data[:cut2,0:]
            xp.append(cut2)
            yp.append(fr.forest_solver(train_data,test_data))
            #yp.append(l1.l1_penalty_solver(train_data,test_data))
            #yp.append(mlpy.llc_solver(train_data,test_data))
            #yp.append(nn.neutral_net(train_data,test_data))
            print(yp[i-1])
        xp = np.array(xp); yp = np.array(yp)
        
        plt.figure(2)
        plt.plot(xp,yp[:,0]);plt.plot(xp,yp[:,1])
        plt.axis([0, 600, 0.6, 1])
        plt.show()
 
    

        
