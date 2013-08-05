'''
Created on Jul 16, 2013

@author: work
'''
import numpy as np
import print_results as pr
import pybrain

from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SupervisedDataSet
from pybrain.datasets.classification import ClassificationDataSet
from pybrain.structure.modules import SoftmaxLayer
from pybrain.structure.modules import SigmoidLayer
#from pybrain.tools.xml.networkwriter import NetworkWriter
#from pybrain.tools.xml.networkreader import NetworkReader

def neutral_net(train_data,test_data,n_est,maxd):
    
    #ds = SupervisedDataSet(len(train_data[0,:])-1,1)
    ds = ClassificationDataSet(len(train_data[0,:])-1,1,nb_classes=2,class_labels=['Lived','Died'])
    X=[];y=[]; X1=[]; y1=[]
    for row in range(0,len(train_data[:,0])):
        X.append(train_data[row,1:].astype(int))
        y.append([train_data[row,0].astype(int)])
        #ds.addSample(train_data[row,1:].astype(int),train_data[row,0].astype(int))
    #for row in range(0,len(test_data[:,0])):
    #    X.append(test_data[row,1:].astype(int))
    #    y.append([test_data[row,0].astype(int)])

    X=np.array(X); y=np.array(y)
    ds.setField('input',X)
    ds.setField('target',y)

    ds._convertToOneOfMany(bounds=[0,1])  # only for classification

    #net = buildNetwork(len(train_data[0,:])-1,100, 1)
    read = False
    if read:
        #net = NetworkReader.readFrom('10_200.xml')  # hiddenclass=SigmoidLayer
		pass
    else:
        net = buildNetwork(ds.indim,maxd,ds.outdim,bias=True,hiddenclass=SigmoidLayer,outclass=SoftmaxLayer)#SoftmaxLayer)        
        trainer = BackpropTrainer(net,dataset=ds,verbose=False,learningrate=0.01,momentum=0.1,weightdecay=0.01)
        trainer.trainUntilConvergence(maxEpochs=n_est,continueEpochs=10,validationProportion=0.3)
        #NetworkWriter.writeToFile(net, '10_200.xml')

    tot = 0.
    for a,b in zip(X,y):
        val = net.activate(a)
        tot+=int((val[0] > val[1] and b==0) or (val[0]<val[1] and b==1))
        '''num = int((net.activate(a)<0.5 and b<0.5) or (net.activate(a)>0.5 and b>0.5))
        tot+=num'''
        
    for row in range(0,len(test_data[:,0])):
        X1.append(test_data[row,1:].astype(int))
        y1.append([test_data[row,0].astype(int)])
    X1=np.array(X1); y1=np.array(y1)
    
    tot1 = 0.
    output = []
    for a,b in zip(X1,y1):
        val = net.activate(a)
        tot1+=int((val[0] > val[1] and b==0) or (val[0]<val[1] and b==1))
        output.append(int(val[0]<val[1]))
        '''num = int((net.activate(a)<0.5 and b<0.5) or (net.activate(a)>0.5 and b>0.5))
        tot1+=num
        output.append(int(net.activate(a)>0.5))'''

    pr.print_results(output)
    
        
    return [tot/len(y),tot1/len(y1)]
