'''
Created on Jul 8, 2013

@author: work
'''
import mlpy
import print_results as pr

def llc_solver(train_data,test_data):
    
    x, y = train_data[:,1::], train_data[:,0]
    x1, y1 = test_data[:,1::], test_data[:,0]
        
#    svm = mlpy.LibLinear(solver_type='l2r_l2loss_svc_dual', C=0.003) # ~83
    svm = mlpy.LibSvm(svm_type='nu_svc', kernel_type='poly',degree=4) # ~78
#    svm = mlpy.MaximumLikelihoodC()
#    svm = mlpy.ClassTree(minsize=200)
 
    svm.learn(x, y)
    val1 = svm.pred(x)
    val2 = svm.pred(x1)    
 
    pr.print_results(val2)
    
    count1 = 0.
    for i in range(len(val1)):
        if val1[i] == y[i]:
            count1 +=1.
        else:
            continue

    count2 = 0.
    for i in range(len(val2)):
        if val2[i] == y1[i]:
            count2 +=1.
        else:
            continue

    return [count1/len(val1),count2/len(val2)]