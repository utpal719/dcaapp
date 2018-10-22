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
from sklearn.metrics import silhouette_score

logging.basicConfig(level=logging.DEBUG)

def no_of_clusters(X):
    scores = []
    for i in range(2,16):
        kmeans = KMeans(n_clusters=i, random_state=10).fit(X)
        label = kmeans.labels_
        print(len(label))
        print('--------')
        print(len(X))
        sil_coeff = silhouette_score(X, label, metric='euclidean')
        scores.append(sil_coeff)
    index, value = max(enumerate(scores), key=operator.itemgetter(1))
    return (index+2,value)

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
        #Selecting rows having peak values
        #Min_Dist ->minimum distance between 2 peaks
        #thres ->adjust sensitivity of selecting peaks 
        index = peakutils.indexes(df[col_name],thres = 0.2, min_dist = 0.1)
        try:
            #[df['tmonth'][i],0] as it requires 2-D array
            # It will make clusters of months where we found peaks.
            n = 2
            kmc = KMeans(n_clusters = n, random_state = 10).fit([[df['tmonth'][i],0] for i in index]) 
            #select center of clusters   
            for i in range(n):
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
        print(onethird)
        print(twothird)
        ## converting value of month to its index in data to use in furthur calculations

        # for k in range(len(centers)):
        #     for i in range(len(df)):
        #         if df['tmonth'][i] > centers[k]:
        #             centers[k] = i
        #             break
        #     for j in range(i,len(df)):
        #         if df['tmonth'][j] > centers[k]:
        #             centers[k] = j
        #             break

        for i in range(len(df)):
            if df['tmonth'][i] > onethird:
                onethird = i
                break
        for j in range(i,len(df)):
            if df['tmonth'][j] > twothird:
                twothird = j
                break

        # print(onethird)
        # print(twothird)

        ####################################################################################3    
        interval = 10
        breakes = []

        # In gap of 10-10 values check for validation
        # Work only if their are existing +-40 values from onethird part else it will only check on onethird value.
        for center in centers:
            if center > 5 * interval and len(df) > center + 10 * interval:
                firstbreak = []
                for i in range(center-4*interval, center+8*interval,interval):
                    firstbreak.append(i)
            else:
                firstbreak = [center]
            breakes.append(firstbreak)



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
        
        #These check values for all different combinations of onethird and two third values
        for onethird in firstbreak:
            for twothird in secondbreak:
                errs = 0
                eqtns = []
                parameters = []
                #Now we will first take each segment and check all 4 equations.
                for x,y in zip([0,onethird,twothird],
                            [onethird,twothird,len(df)]):
                            params = []
                            #Add errors for all $ eqtns in this array.
                            errors = [float('inf'),float('inf'),float('inf'),float('inf')]
                            #Go through all equations
                            for i in range(len(equations)):
                                try:
                                    #print("going to call eqn %s"%i)
                                    params.append(op.curve_fit(equations[i],df['tmonth'][x:y],
                                                        df[col_name][x:y],[.5,1])[0])

                                except RuntimeError as rerr:
                                    print("runtime error: ",rerr)
                                    params.append(['error','error'])
                                except :
                                    print("exception occurs here", sys.exc_info()[0])
                                    params.append(['error','error'])
                                    #print('Well_'+str(well)+', equation_'+str(i+1)+' not suitable.')
                            #print("length params: ",len(params))
                            for e in range(4):
                                err = 0
                                if params[e][0]!='error':
                                    for i in range(x,y):
                                        err+=abs(df[col_name][i]-equations[e](df['tmonth'][i],params[e][0],params[e][1]))

                                    errors[e] = err

                                    
                            #Till now what we have is params and errors array in which their are values for all 4 equations  corresponding to a single segment.
                                    # params->[(a,b),(a,b),(a,b),(a,b)]   # errors-> [errorEQN1 , errorEQN2 ,errorEQN3, errorEQN4]
                            mini = 0

                            #Then select values corresponding to minimum error.
                            for i in range(1,4):
                                if errors[i]<errors[mini] :
                                    mini = i

                            #And save values corresponding to that index
                            #Now it will do for next segment and get total error of one combination of graph        
                            errs+=errors[mini]
                            eqtns.append(mini)
                            parameters.append(params[mini])


                        
                #At this points we are saving a best fit sets of equation for that particular onethird and twothird along with their errors and parameters.            
                break1.append(onethird)
                break2.append(twothird)
                par.append(parameters)
                eqtn.append(eqtns)
                total_error.append(errs)


        #Till now we have made arrays which store different combinations of equations,their total errors and parameters.
        #Now select the index with minimun total error and correspondingly select all the parameters from other arrays at same index point.
        #This will help us to get best segmentation point along with equations used for each segment.
        suit = 0
        error = float('inf')
        for i in range(len(total_error)):
            if total_error[i]<error:
                suit = i
                error = total_error[i]

        brkpoint1 = break1[suit]
        brkpoint2 = break2[suit]
        params = par[suit]
        eqns = eqtn[suit]
        ##################################################################################

        ##  Calculation remaining time of oil production

        
        last = df['tmonth'][len(df)-1]
        months_left = 0

        try:
            #Take 5% value of last segment starting part
            five_percent_of_max = equations[eqns[2]](df['tmonth'][brkpoint2],params[2][0],params[2][1])/20
        except:
            print("Error here!!!!!!!!!!!!!!!")
            print("Month: ",df['tmonth'][brkpoint2], " params[2][0]: ",params[2][0], " params[2][1]: ",params[2][1])

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
        for x,y,i,j in zip([0,brkpoint1,brkpoint2],[brkpoint1,brkpoint2,len(df)],eqns,range(3)):
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
        info.loc[0] = list(pd.Series([brkpoint1,brkpoint2,eqns[0],params[0][0],params[0][1],eqns[1],
                                        params[1][0],params[1][1],eqns[2],params[2][0],params[2][1],
                                        predicted_production,actual_production,predicted_production-actual_production,
                                        months_left,estimated_production]))

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