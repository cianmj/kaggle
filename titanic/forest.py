'''
Created on Jul 8, 2013

@author: work
'''
from sklearn.ensemble import RandomForestClassifier
import print_results as pr

def forest_solver(train_data,test_data,n_est):
    best = 0.0
    best_Output = []
    for i in [x**2 for x in range(1,2)]:

        X = train_data[0::,1::]
        y = train_data[0::,0]
        
        Xt = test_data[0::,1::]
        yt = test_data[0::,0]

        Forest = RandomForestClassifier(n_estimators = n_est,random_state=93758) # = 100
        Forest = Forest.fit(X,y)
        Output = Forest.predict(Xt)
    
        result = Forest.score(Xt,yt)

        if result>best:
            best = result
            best_Output = Output

      
    pr.print_results(best_Output)
    return [Forest.score(X,y), Forest.score(Xt,yt)]
    #return best
