from flask import jsonify, request
from app.api import bp
import pandas as pd
import io
import datetime

@bp.route('/upload', methods=['POST'])
def upload_csv():
    #Receive file 
    data = request.files['file']
    data_opts = request.args.to_dict() #request.form.get('date_fmt')
    date_fmt = data_opts['date_fmt']
    
    df =  pd.read_csv(io.BytesIO(data.read()))
    
    #Exclude empty fields
    df = df.dropna(subset=['OIL_PROD'])
    #Correct indexes after dropping empty
    df = df.reset_index(drop=True)
    #Fill NA/NaN values with 0
    df = df.fillna(0)
    #Rename columns ---> TODO: This should be user parametrized
    df.rename(columns={'AUTOMATION_NAME':'well','BOOK_DATE':'date','OIL_PROD':'prod'},inplace = True)

    """
    The month and year fields are captured depending on the date format supplied by user
    """
    month = []
    year = []

    for i in range(len(df)):
        dt = datetime.datetime.strptime(df['date'][i], date_fmt)
        month.append(dt.month)
        year.append(dt.year)

    df['year'] = year
    df['month'] = month
    del year,month
    """
    Added month and year columns to the dataframe - this is being used in the next stage
    """
    #Sort by well-name or identifier and reset indexes
    df.sort_values('well',inplace = True)
    df = df.reset_index(drop=True)

    index = [1]
    welldict = {1:df['well'][0]}

    for i in range(1,len(df)):
        if df['well'][i] != df['well'][i-1]:    #When we reach a different well
            index.append(index[-1]+1)           #Increment index number
            welldict[index[-1]] = df['well'][i]
        else:
            index.append(index[-1])             #For same well, use same index number

    df['index'] = index


    #dftemp = pd.DataFrame(columns = df.columns)
    wells = [pd.DataFrame(columns = df.columns) for i in range(len(df['index'].value_counts())+1)]

    for i in range(len(df)):
        wells[df['index'][i]].loc[len(wells[df['index'][i]])] = df.iloc[i]

    for well in wells:
        well.reset_index(inplace=True,drop=True)

    for i in range(1,len(wells)):
        wells[i].to_csv('data_well_'+str(i)+'.csv')
    
    resp = {
        'data': 'created'
    }
    response = jsonify(resp)
    response.status_code = 201
    return response