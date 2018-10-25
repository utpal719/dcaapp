import sys
from flask import jsonify, json
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
from datetime import datetime as time
import math
#scientific python library:- used for curve fitting
import scipy.optimize as op
##Finding Peaks
import peakutils
from sklearn.cluster import KMeans
import operator
import logging
import itertools
from sklearn.metrics import silhouette_score
import copy

logging.basicConfig(level=logging.DEBUG)

def eq1(x,a,b):
    #print("calling eqn 1")
    try:
        val = b*pow(np.array(x),-a)
    except:
        print("error in eq 1")
    return b*pow(np.array(x),-a)

def eq2(x,a,b):
    #print("calling eqn 2")
    try:
        val = a+b/(10*np.log(1+b*np.array(x)))
    except:
        print("error in eq 2")
    return a+b/(10*np.log(1+b*np.array(x)))

def eq3(x,a,b):
    #print("calling eqn 3")
    try:
        val = a/(1+ b*np.array(x))
    except:
        print("error in eq 3")
    return a/(1+ b*np.array(x))

def eq4(x,a,b):
    #print("calling eqn 4")
    try:
        val = (a+b*np.array(x)*(np.log(x)-1))/(np.array(x)*pow(np.log(x),2))
    except:
        print("error in eq 4")
    return (a+b*np.array(x)*(np.log(x)-1))/(np.array(x)*pow(np.log(x),2))

def no_of_clusters(X,n=15):
    scores = []
    for i in range(2,n+1):
        kmeans = KMeans(n_clusters=i, random_state=10).fit(X)
        label = kmeans.labels_
        sil_coeff = silhouette_score(X, label, metric='euclidean')
        scores.append(sil_coeff)
    index, value = max(enumerate(scores), key=operator.itemgetter(1))
    return (index+2,value)


def dodca(df):
    print(df.head())
    np.seterr(divide='print')
    time_start = time.now()
    cols = ['segment1','segment2','eq1','p1_a','p1_b','eq2','p2_a','p2_b','eq3','p3_a','p3_b',
        'predicted_production','actul_production','difference','months_left','est_prod']
    
    info = pd.DataFrame(columns = cols)
    totalprod = 0
    
    for i in df['prod']:
        num = float(i)
        totalprod += int(num)

    df = df.sort_values(['year','month'])
    percentile95 = df['prod'].quantile(0.95)
    percentile05 = df['prod'].quantile(0.05)

    ##  DELETING THE OUTLIERS 
    #Only in case of large datasets - deleting outliers for small datasets will affect the equations
    if df.shape[0] > 150:
        df = df[df['prod']<percentile95]
        df = df[df['prod']>percentile05]
        ##
        #reset index/make row order wise
        df = df.reset_index(drop=True)

    ## make new column counting total no. of months
    totalmonth = []

    for i in range(len(df)):
        totalmonth.append(df['month'][i]+12*(df['year'][i] - df['year'].min()))   
    
    df['tmonth'] = totalmonth
    #print(df[['month','year','tmonth']])
    del totalmonth

    ##    NORMALISATION OF PRODUCTION DATA
    ##
    ##    maxi = max(df['prod'])
    ##    nprod = []
    ##    ##normalising production
    ##    for i in range(len(df)):
    ##        nprod.append( float(df['prod'][i]/maxi))
    ##
    ##    df['actualprod'] = df['prod']
    ##    del df['prod']
    ##    df['prod'] = nprod

    
    """This might not be necessary for all datasets"""
    ##  Calculating cumulative production
    cprod = [df['prod'][0]]
    for i in range(1,len(df)):
        cprod.append(cprod[-1]+df['prod'][i])
    df['cprod'] = cprod
    del cprod

    """This might not be necessary for all datasets"""

    """Three time period segments have been assumed. This should be decided based on the data"""
    ## Lets take default values of (time/period) segmentation point as:-
    onethird = int(df['tmonth'][len(df)-1]/3)
    twothird = int(2*df['tmonth'][len(df)-1]/3)
    centers = []

    #Start loop here:
    focus_cols = ["prod", "waterrate", "gasrate"]

    master = {
        "prod": {},
        "waterrate": {},
        "gasrate": {}
    }

    for col_name in focus_cols:
        print('--------------------')
        print(col_name)
        print('+-------------------')
        #Selecting rows having peak values
        #Min_Dist ->minimum distance between 2 peaks
        #thres ->adjust sensitivity of selecting peaks 
        index = peakutils.indexes(df[col_name],thres = 0.2, min_dist = 0.1)
        try:
            #[df['tmonth'][i],0] as it requires 2-D array
            # It will make clusters of months where we found peaks.
            XX = [[df['tmonth'][i],0] for i in index]
            nc, val = no_of_clusters(XX)
            kmc = KMeans(n_clusters = nc, random_state = 10).fit(XX) 
            #select center of clusters   
            for i in range(nc):
                centers.append(kmc.cluster_centers_[i][0])

            # centers = [kmc.cluster_centers_[0][0],kmc.cluster_centers_[1][0]]
            centers.sort()
            onethird,twothird = centers[0],centers[1]
            #print("onethird: %s, twothird: %s"%(onethird,twothird))
        except :
            #If k-means not work it takes previous default values
            #print('kmeans not done in well'+str(i))
            pass

        # print(centers)
        # print(onethird)
        # print(twothird)
        ## converting value of month to its index in data to use in furthur calculations

        for k in range(len(centers)):
            for i in range(len(df)):
                if df['tmonth'][i] > centers[k]:
                    centers[k] = i
                    break

        # for i in range(len(df)):
        #     if df['tmonth'][i] > onethird:
        #         onethird = i
        #         break
        # for j in range(i,len(df)):
        #     if df['tmonth'][j] > twothird:
        #         twothird = j
        #         break

        # print(onethird)
        # print(twothird)

        ####################################################################################3    
        interval = 10
        breakes = []
        stamp = 0

        # In gap of 10-10 values check for validation
        # Work only if their are existing +-40 values from onethird part else it will only check on onethird value.
        for center in centers:
            if center > 5 * interval+stamp and len(df) > center + 5 * interval:
                firstbreak = []
                for i in range(center-5*interval, center+5*interval,interval):
                    firstbreak.append(i)
            else:
                firstbreak = [center]
            breakes.append(firstbreak)
            stamp = center



        # if onethird >5*interval and len(df)>onethird+10*interval:
        #     firstbreak = []
        #     #will store -40,-30,-20,-10,0,10,20,30,40 from onethird value in firstbreak array.
        #     for i in range(onethird-4*interval,onethird+5*interval,interval):
        #         firstbreak.append(i)
        # else :
        #     firstbreak = [onethird]

        # if twothird >5*interval+onethird and len(df)>twothird+5*interval:
        #     secondbreak = []
        #     #will store -40,-30,-20,-10,0,10,20,30,40 from twothird value in secondbreak array.
        #     for i in range(twothird-5*interval,twothird+5*interval,interval):
        #         secondbreak.append(i)
        # else :
        #     secondbreak = [twothird]

        ################################################################################ 
        #firstbread = [3], secondbreak = [10]
        #Array of equations
        equations = [eq1,eq2,eq3,eq4]
        suitable = []
        graphcolor = {1:'r',2:'g',3:'b',4:'y'}

        #print('Well_'+str(well)+'...')
        total_error = []
        break1 = []
        break2 = []
        par = []
        eqtn = []
        break_points = []
        
        #These check values for all different combinations of onethird and two third values

        # for rows in range(len(center)):
        # print('----------------')
        # print(breakes)

        combinations = []

        for com in itertools.product(*breakes):
            combinations.append(com)


        
        for combination in combinations:
            errs = 0
            eqtns = []
            parameters = []
            
            com = [b for b in combination]
            com1 = copy.deepcopy(com)
            com2 = copy.deepcopy(com)
            com1.insert(0,0)
            com2.append(len(df))

            for x,y in zip(com1,com2):
                params = []
                errors = [float('inf'),float('inf'),float('inf'),float('inf')]
                for i in range(len(equations)):
                    try:
                        params.append(op.curve_fit(equations[i],df['tmonth'][x:y],
                                                            df['prod'][x:y],[.5,1])[0])
                    except :
                        params.append(['error','error'])
                            
                for e in range(4):
                    err = 0
                    if params[e][0]!='error':
                        for i in range(x,y):
                            err+=abs(df['prod'][i]-equations[e](df['tmonth'][i],params[e][0],params[e][1]))

                        errors[e] = err
                mini = 0
                for i in range(1,4):
                    if errors[i]<errors[mini] :
                        mini = i   
                errs+=errors[mini]
                eqtns.append(mini)
                parameters.append(params[mini]) 

            par.append(parameters)
            eqtn.append(eqtns)
            total_error.append(errs)

            inside = []
            for index, value in enumerate(combination):
                inside.append(value)
                
            break_points.append(inside)
        num_each_tuple = len(break_points[0])
        compl = []
        for inx in range(num_each_tuple):
            vals = []
            for index_bkpt in range(len(break_points)):
                vals.append(break_points[index_bkpt][inx])
            compl.append(vals)

        break_points = copy.deepcopy(compl)

        #Till now we have made arrays which store different combinations of equations,their total errors and parameters.
        #Now select the index with minimun total error and correspondingly select all the parameters from other arrays at same index point.
        #This will help us to get best segmentation point along with equations used for each segment.
        suit = 0
        error = float('inf')
        for i in range(len(total_error)):
            if total_error[i]<error:
                suit = i
                error = total_error[i]

        bkpoints = []

        for idx in range(num_each_tuple):
            bkpoints.append(break_points[idx][suit])

        params = par[suit]
        eqns = eqtn[suit]
        ##################################################################################

        ##  Calculation remaining time of oil production

        
        last = df['tmonth'][len(df)-1]
        months_left = 0

        try:
            #Take 5% value of last segment starting part
            five_percent_of_max = equations[eqns[2]](df['tmonth'][bkpoints[-1]],params[2][0],params[2][1])/20
        except:
            print("Error here!!!!!!!!!!!!!!!")
            #print("Month: ",df['tmonth'][bkpoints[-1]], " params[2][0]: ",params[2][0], " params[2][1]: ",params[2][1])

        #Calculating the total months till production exceeds
        while equations[eqns[2]](last+months_left,params[2][0],
                        params[2][1])>equations[eqns[2]](last+months_left+1,
                                                    params[2][0],params[2][1]) > five_percent_of_max and months_left<=100:
            months_left += 1
        
        #Store those months in array called predict
        predict = []
        for i in range(1,months_left):
            predict.append(i+last)

        master[col_name] = {
            'decline': [],
            'eqn': [],
            'color': [],
            'predict': {}
        }
        predicted_production = 0
        actual_production = 0
        estimated_production = 0 #in next 100 months
        ##  PLOTTING THE DATA
        #plt.figure()

        #x->start point  y->end point  i->which equation to use  j->It indicates which segment part.
        for x,y,i,j in zip([0,*bkpoints],[*bkpoints,len(df)],eqns,range(3)):
            #Plot curves
            #plt.plot(df['tmonth'][x:y],equations[i](df['tmonth'][x:y],params[j][0],params[j][1]),c=graphcolor[i+1])
            master[col_name]['decline'].append(df['tmonth'][x:y].values.tolist()) #.to_json(orient='values')
            tdf = pd.Series(equations[i](df['tmonth'][x:y],params[j][0],params[j][1]))
            master[col_name]['eqn'].append(tdf.tolist()) #.to_json(orient='values')
            master[col_name]['color'].append(graphcolor[i+1])
            predicted_production += sum(equations[i](df['tmonth'][x:y],params[j][0],params[j][1]))
            actual_production += sum(df[col_name][x:y])

        #Ploting for future months stored in predict array.
        #'i' will be continue from last part so it will represent last segment
        #plt.plot(predict,equations[i](predict,params[j][0],params[j][1]),c=graphcolor[i+1])
        try:
            prdf = pd.Series(equations[i](predict,params[j][0],params[j][1]))
            master[col_name]['predict'] = {
                'x': pd.Series(predict).tolist(), #.to_json(orient='values')
                'y': prdf.tolist() #.to_json(orient='values')
            }
        except:
            print('error mapping predict')
        #Future cummulative production
        estimated_production = sum(equations[i](predict,params[j][0],params[j][1]))

        #Fill the empty data frame that we have made in starting
        # info.loc[0] = list(pd.Series([brkpoint1,brkpoint2,eqns[0],params[0][0],params[0][1],eqns[1],
        #                                 params[1][0],params[1][1],eqns[2],params[2][0],params[2][1],
        #                                 predicted_production,actual_production,predicted_production-actual_production,
        #                                 months_left,estimated_production]))

        #plot the original points and save figure
        #plt.scatter(df['tmonth'],df['prod'],s=3)
        try:
            master[col_name]['datapoints'] = {
                'x': df['tmonth'].values.tolist(), #.to_json(orient='records'),
                'y': df[col_name].values.tolist() #.to_json(orient='records')
            }
        except:
            print("Error mapping scatter")
        
        centers = []
        #plt.savefig('graph_well_'+str(0)+'.png')
        #plt.close('all')
        
        #print()
        #print()
        #print(master['predict'])

        #info.to_csv('wells_info.csv')
        """ colss = ['prod', 'month', 'year']
        ff = pd.DataFrame(columns = colss)
        ff = df[['prod', 'month', 'year']]
        ff.to_csv('ex-data.csv') """
        #print('Duration: {}'.format(time.now()-time_start))

    #End loop here:

    return master