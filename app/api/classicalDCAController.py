from flask import jsonify, request, g, json
from app import db
from app.response_models import dcaVMs
from app.api import bp
from app.api import dca
from app.api.auth import token_auth
from app.api.errors import error_response
import io
import datetime
import pandas as pd
import numpy as np


################################ post format ################################
# [{
#     "mode": "exponential",
#     "a": 0.002,
#     "ref": "OIL_q_t_exp",
#     "qi": 100,
#     "tSpan": 100,
#     "tStep": 0.5
# },
#     {
#     "datasource": "oilrate",
#     "mode": "harmonic",
#     "a": 0.002,
#     "ref": "OIL_q_t_har"
# },
#     {
#     "qi": 5000,
#     "mode": "hyperbolic",
#     "a": 0.002,
#     "tSpan": 100,
#     "tStep": 1,
#     "n": 0.8
# },
#     {
#     "datasource": "oilrate",
#     "mode": "cumulative",
#     "ref": "OIL_Q"
# },
#     {
#     "datasource": "oilrate",
#     "mode": "cumulative",
#     "ref": "WATER_Q"
# }]
@bp.route('/classical/dca/<wellName>', methods=['POST'])
def test_dca(wellName):
    supported_modes = ["cumulative", "exponential", "harmonic", "hyperbolic"]

    try:
        options = request.get_json()
    except Exception as ex:
        print(ex)
        return error_response(400, "One or more required parameters are missing")

    try:
        feedDf = pd.read_sql("select readdate, oilrate, waterrate, gasrate from casedata where user='{}' and well='{}'".format(
            'dcaappa', wellName), con=db.engine)
    except:
        return error_response(400, "reading from table failed")

    try:
        date_fmt = "%m/%d/%Y"
        date_arr = []

        for i in range(len(feedDf)):
            dt = datetime.datetime.strptime(feedDf['readdate'][i], date_fmt)
            date_arr.append(dt)

        feedDf['date'] = date_arr
        feedDf.sort_values(by=['date'], ascending=True, inplace=True)

        feedDf.drop(columns=['readdate'], inplace=True)
    except:
        return error_response(500, "error reading date field")

    output = []
    try:
        for idx, opt in enumerate(options):
            ref = opt.get("ref", idx)

            try:
                mode = opt.get("mode", None)
                if(mode is None):
                    raise ValueError("required parameter mode is not supplied")
                if(not(mode in supported_modes)):
                    raise ValueError("mode {} is not supported".format(mode))

                datasource = opt.get("datasource", None)
                if(datasource is not None and datasource not in feedDf.columns):
                    raise ValueError(
                        "datasource {} could not be found".format(datasource))

                qiOverride = opt.get("qi", None)
                if(qiOverride is None and datasource is None):
                    raise ValueError(
                        "either qi or datasource must be supplied")

                t = opt.get("tSpan", None)
                if(t is None and datasource is None):
                    raise ValueError(
                        "tSpan cannot be empty when datasource is not supplied")

                if(t is not None and t < 1):
                    raise ValueError("value of t must be greater than 0")

                if(datasource is not None and len(feedDf) == 0):
                    raise ValueError(
                        "no data is available for the supplied criteria")

                tStep = opt.get("tStep", 1)
                if(tStep <= 0):
                    raise ValueError("value of tStep must be greater than 0")

                a = opt.get("a", None)
                n = opt.get("n", None)

                dca_result = []
                qiOverride = qiOverride if qiOverride is not None else feedDf[datasource][0]

                outputDf = pd.DataFrame()
                outputDf["time"] = feedDf["date"] if datasource is not None else np.arange(
                    1, t, tStep)

                inputDf = pd.DataFrame()
                if(datasource is not None):
                    inputDf["time"] = feedDf["date"]
                    inputDf["value"] = feedDf[datasource]

                pearsonr = 0.0
                tIntervals = len(outputDf)

                if(mode == "cumulative"):
                    if(datasource is None):
                        raise ValueError(
                            "required parameter datasource is not supplied")
                    dca_result = dca.cumulative(feedDf[datasource])
                else:
                    dca_result = dca.calc(
                        qiOverride, tIntervals, mode, a=a, n=n)
                    pearsonr = dca.r2(
                        feedDf[datasource], dca_result) if datasource is not None else pearsonr

                outputDf["value"] = dca_result
                output_dict = outputDf.to_dict('records')
                input_dict = inputDf.to_dict('records')

                result = {}
                if(mode == "cumulative"):
                    result = dcaVMs.cumulative_resp_model(
                        mode=mode,
                        wellName=wellName,
                        datasource=datasource,
                        input=input_dict,
                        output=output_dict,
                        ref=ref)

                if(mode == "exponential"):
                    result = dcaVMs.exponential_resp_model(
                        mode=mode,
                        wellName=wellName,
                        datasource=datasource,
                        input=input_dict,
                        output=output_dict,
                        qi=qiOverride,
                        a=a,
                        t=t,
                        tStep=tStep,
                        pearsonr=pearsonr,
                        ref=ref)

                if(mode == "harmonic"):
                    result = dcaVMs.exponential_resp_model(
                        mode=mode,
                        wellName=wellName,
                        datasource=datasource,
                        input=input_dict,
                        output=output_dict,
                        qi=qiOverride,
                        a=a,
                        t=t,
                        tStep=tStep,
                        pearsonr=pearsonr,
                        ref=ref)

                if(mode == "hyperbolic"):
                    result = dcaVMs.exponential_resp_model(
                        mode=mode,
                        wellName=wellName,
                        datasource=datasource,
                        input=input_dict,
                        output=output_dict,
                        qi=qiOverride,
                        a=a,
                        t=t,
                        n=n,
                        tStep=tStep,
                        pearsonr=pearsonr,
                        ref=ref)

                output.append(result)

            except ValueError as ve:
                print(ve)
                result = {
                    "ref": ref,
                    "error": {
                        "message": str(ve)
                    }
                }
                output.append(result)

    except Exception as ex:
        print(ex)
        return error_response(500, str(ex))

    response = jsonify(output)
    response.headers.set("Content-Type", "application/json")

    return response
