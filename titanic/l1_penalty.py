'''
Created on Jul 8, 2013

@author: work
'''
import numpy as np
import print_results as pr

from sklearn.linear_model import LogisticRegression
#from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier

def l1_penalty_solver(train_data,test_data,n_est,m_d):

    best = 0.0
    best_Output = []
    for j in [10**(x) for x in xrange(-3,-2,1)]:
        
        X, y = train_data[:,1::], train_data[:,0]
        x1, y1 = test_data[:,1::], test_data[:,0]
        
        # Set regularization parameter
        for C in range(10,11,1):
            # turn down tolerance for short training time
            #cls = svm.SVC(kernel='poly',degree=3).fit(X,y)
            cls = GradientBoostingClassifier(n_estimators=n_est,max_depth=m_d).fit(X,y)
            #cls = DecisionTreeClassifier().fit(X,y)
            #cls = LogisticRegression(C=C, penalty='l1', tol=j).fit(X, y)
            #cls = LogisticRegression(C=C, penalty='l2', tol=j).fit(X, y) 

            val1 = cls.predict(x1)
            #val1 = cls.predict(x1)
            val2 = val1 #cls.predict(x1)
                        
            count = 0.
            for i in range(len(val1)):
                if val1[i] == y1[i]:
                    count +=1.
                else:
                    continue
            result1 = count/len(val1)

            count = 0.
            for i in range(len(val2)):
                if val2[i] == y1[i]:
                    count +=1.
                else:
                    continue
            result2 = count/len(val2)
    
            if result1>best:
                best = result1
                best_Output = val1
            if result2>best:
                best = result2
                best_Output = val2
     
        
    pr.print_results(best_Output)
    #return best
    return [cls.score(X,y),cls.score(x1,y1)]
    

#        print("C=%d" % C)
#        print("Sparsity with L1 penalty: %.2f%%" % sparsity_l1_LR)
#        print("score with L1 penalty: %.4f" % clf_l1_LR.score(X, y))
#        print("Sparsity with L2 penalty: %.2f%%" % sparsity_l2_LR)
#        print("score with L2 penalty: %.4f" % clf_l2_LR.score(X, y))

