from flask import jsonify, request, g, json
from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import error_response
import pandas as pd
import io
import datetime
from app.api.mldca import dodca

@bp.route('/upload', methods=['POST'])
@token_auth.login_required
def upload_csv():
    #Receive file 
    try:
        data = request.files['file']
    except:
        return error_response(400, "One or more required parameters are missing")

    data_opts = request.args.to_dict()

    """ has_delimiter = False
    try:
        delimiter_provided = data_opts['delimiter']
        has_delimiter = True
    except:
        has_delimiter = False """
    file_ext = data.filename.rsplit('.', 1)[1].lower()

    if(file_ext == 'csv'):
        print("has delimiter: %s"%delimiter_provided)
        df = pd.read_csv(io.BytesIO(data.read()), skiprows=[0], skipinitialspace=True, header=None)
    elif(file_ext == 'prd'):    
        df = pd.read_csv(io.BytesIO(data.read()), skiprows=[0], skipinitialspace=True, delim_whitespace=True, header=None, names=["well", "readdate", "oilrate", "waterrate", "gasrate"]) #, names=["Well", "Read_Date", "Oilrate", "Waterrate", "Gasrate"], index_col=False
    #df =  pd.read_csv(io.BytesIO(data.read()))
    
    column_order = json.loads(data_opts['columnOrder'])
    provided_names = []
    for o in column_order:
        provided_names.append(o['name'])
        df.rename(columns ={o['pos']: o['name']}, inplace =True)

    col_names = list(df.columns.values)

    for c_name in col_names:
        if c_name not in provided_names:
            df.drop([c_name], axis = 1, inplace = True)

    print(df[0:5])
    #Exclude empty fields
    df = df.dropna(subset=['oilrate'])
    #Correct indexes after dropping empty
    df = df.reset_index(drop=True)
    #Fill NA/NaN values with 0
    df = df.fillna(0)

    df['user'] = g.current_user.username
    df['datasetname'] = data.filename

    try:
        df.to_sql("casedata", con=db.engine, if_exists='replace', index=False)
    except:
        return error_response(400, "Unknown columns")
    resp = {
        'message': 'created'
    }

    response = jsonify(resp)
    response.status_code = 201
    return response

@bp.route('/process/dca', methods=['GET'])
@token_auth.login_required
def process_dca():
    try:
        data_opts = request.args.to_dict()
        well_name = data_opts['well_name']
        date_fmt = data_opts['date_fmt']
    except:
        return error_response(400, "One or more required parameters are missing")

    try:
        #df = pd.read_sql("select * from prodmetrics where user='{}' and AUTOMATION_NAME='{}'".format(g.current_user.username, well_name), con=db.engine, index_col='id')
        df = pd.read_sql("select * from casedata where user='{}' and well='{}'".format(g.current_user.username, well_name), con=db.engine)
    except:
        return error_response(400, "reading from table failed")
    #Rename columns ---> TODO: This should be user parametrized
    df.rename(columns={'well':'well','readdate':'date','oilrate':'prod'},inplace = True)

    """
    The month and year fields are captured depending on the date format supplied by user
    """
    month = []
    year = []
    try:
        #for i in df.index.values.tolist():
        for i in range(len(df)):
            dt = datetime.datetime.strptime(df['date'][i], date_fmt)
            month.append(dt.month)
            year.append(dt.year)

        df['year'] = year
        df['month'] = month
        del year,month

    except:
        return error_response(400, "Invalid date format")
    
    """ try:
        df.to_csv('data_well_wg.csv', index=False)
        df.to_sql("dataset", con=db.engine, if_exists='append', index=False)
    except:
        return error_response(400, "Unknown columns") """
    resp = dodca(df)
    """ resp = {
        'message': 'created'
    } """
    #print(resp)
    """ try:
        response = json.dumps(resp) #jsonify(resp)
    except:
        print('error converting to json')
        response = jsonify({})
    response['status_code'] = 200
    return jsonify(response) """

    response = jsonify(resp)
    response.headers.set("Content-Type", "application/json")
    return response