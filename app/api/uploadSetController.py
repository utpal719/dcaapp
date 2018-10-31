from flask import jsonify, request, g, json, current_app, send_from_directory
from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import *
import pandas as pd
import io
import os
import datetime
import math
import pytz
from werkzeug.utils import secure_filename
from app.data_models.UploadSet import UploadSet
from app.data_models.Well import Well
from app.data_models.MeasurementFormat import MeasurementFormat
from app.data_models.WellOutputMeasurement import WellOutputMeasurement

ALLOWED_EXTENSIONS = set(['csv', 'prd'])
ALLOWED_COL_TYPES = set([
    "well_name",
    "read_date",
    "oil_production",
    "water_production",
    "gas_production",
    "co2_production",
    "water_injection",
    "co2_injection"])
ALLOWED_DATE_FORMATS = set([
    "%m/%d/%Y"])
ALLOWED_DATA_UNITS = set([
    "bbl/day"])

################################ post format ################################
# {
# 	"name" : "upload_27_0ct",
# 	"description" : "contains data of wells 101, 102, 103",
# 	"columns": [
# 		{
# 			"index" : 0,
# 			"type" : "well_name"
# 		},
# 		{
# 			"index" : 1,
# 			"type" : "read_date",
# 			"format" : "%m/%d/%Y"
# 		},
# 		{
# 			"index" : 2,
# 			"type" : "oil_production",
# 			"units" : "bbl/day"
# 		},
#         {
# 			"index" : 3,
# 			"type" : "water_production",
# 			"units" : "bbl/day"
# 		},
#         {
# 			"index" : 4,
# 			"type" : "gas_production",
# 			"units" : "bbl/day"
# 		},
#         {
# 			"index" : 5,
# 			"type" : "co2_production",
# 			"units" : "bbl/day"
# 		},
#         {
# 			"index" : 6,
# 			"type" : "water_injection",
# 			"units" : "bbl/day"
# 		},
#         {
# 			"index" : 7,
# 			"type" : "co2_injection",
# 			"units" : "bbl/day"
# 		}
# 	]
# }


@bp.route('/uploadsets/upload', methods=['POST'])
@token_auth.login_required
def uploadsetsUpload():

    UPLOAD_FOLDER = current_app.config.get('UPLOAD_FOLDER')

    try:
        if 'data' not in request.form:
            raise ValueError("data object is missing")

        postdata = json.loads(request.form["data"])

        uploadSetName = postdata.get("name", None)
        if uploadSetName is None:
            raise ValueError(
                "required parameter upload set name is not supplied")

        options = postdata.get("columns", None)
        if(options is None):
            raise ValueError(
                "required parameter columns array is not supplied")
    except Exception as ve:
        print(ve)
        return error_response(400, str(ve))

    try:
        if 'file' not in request.files:
            raise ValueError(
                "file field is missing. make sure that the name is file")

        file = request.files['file']
        if not file or file.filename == '' or not allowed_file(file.filename):
            raise ValueError(
                "file name is missing. make sure that the file name is not empty")

        filename = secure_filename(file.filename)
        file_ext = get_file_ext(filename)
        storedFileName = repr(
            datetime.datetime.utcnow().timestamp()) + '.' + file_ext
        file.save(os.path.join(UPLOAD_FOLDER, storedFileName))
    except Exception as IOException:
        return error_response(500, "unable to store the file.")

    try:
        uSet = UploadSet(
            Name=uploadSetName,
            CreatedDate=datetime.datetime.utcnow(),
            Description=postdata.get("description", None),
            UserId=g.current_user.id,
            FileName=filename,
            StoredFileName=storedFileName)
        db.session.add(uSet)
        db.session.commit()
    except Exception as ex:
        return error_response(500, "could not insert record into uploadset")

    try:
        if(file_ext == 'csv'):
            inputDataFrame = pd.read_csv(os.path.join(UPLOAD_FOLDER, storedFileName), skiprows=[
                                         0], skipinitialspace=True, header=None)
        elif(file_ext == 'prd'):
            inputDataFrame = pd.read_csv(os.path.join(UPLOAD_FOLDER, storedFileName), skiprows=[
                                         0], skipinitialspace=True, delim_whitespace=True, header=None, names=["well", "readdate", "oilrate", "waterrate", "gasrate"])
    except Exception as ex:
        return error_response(500, "unable to process data")

    colTable = {}
    wellNameColIndx = None
    readDateColIndx = None

    try:
        for idx, opt in enumerate(options):
            index = opt.get("index", None)
            if(index is None or math.isnan(index)):
                raise ValueError(
                    "required column parameter index is not supplied")
            if(index > len(inputDataFrame.columns) - 1 or index < 0):
                raise ValueError("index value : {} is invalid".format(index))

            colType = opt.get("type", None)
            if(colType is None or colType == ""):
                raise ValueError(
                    "required column parameter type is not supplied")
            if(colType not in ALLOWED_COL_TYPES):
                raise ValueError(
                    "column type {} is not supported".format(colType))

            if colType == "well_name":
                wellNameColIndx = index
            elif colType == "read_date":
                readDateColIndx = index
                date_fmt = opt.get("format", None)
                if(date_fmt is None or date_fmt == ""):
                    raise ValueError(
                        "required column parameter format for type date is not supplied")
                if date_fmt not in ALLOWED_DATE_FORMATS:
                    raise ValueError(
                        "date format {} is not supported".format(date_fmt))
                inputDataFrame[index] = inputDataFrame[index].apply(
                    lambda x: datetime.datetime.strptime(x, date_fmt))
            else:
                units = opt.get("units", None)
                if units is None:
                    raise ValueError(
                        "units for column type {} is not supplied".format(colType))
                if units not in ALLOWED_DATA_UNITS:
                    raise ValueError(
                        "units {} for type {} is not supported".format(units, colType))
                colTable[colType] = opt

        if wellNameColIndx is None:
            raise ValueError("column def for type well_name is not supplied")

        if readDateColIndx is None:
            raise ValueError("column def for type read_date is not supplied")

        if len(colTable) == 0:
            raise ValueError("no data columns are specified")

    except ValueError as ve:
        return error_response(400, str(ve))

    try:
        groupedDataFrame = inputDataFrame.groupby([wellNameColIndx])
        for wellName, wellDataPoints in groupedDataFrame:
            well = Well(
                Name=wellName,
                UserId=g.current_user.id,
                UploadSetId=uSet.Id)
            db.session.add(well)
            db.session.commit()

            for c, v in colTable.items():
                db.session.add(MeasurementFormat(
                    WellId=well.Id, MeasurementTypeId=c, Format=v.get("units")))
            db.session.commit()

            for index, dataPoint in wellDataPoints.iterrows():
                dateSupplied = dataPoint[readDateColIndx]
                dateSupplied = dateSupplied.replace(tzinfo=pytz.UTC)
                for col, value in colTable.items():
                    opVal = dataPoint[value.get("index")]
                    if not math.isnan(opVal):
                        db.session.add(WellOutputMeasurement(
                            Date=dateSupplied,
                            WellId=well.Id,
                            MeasurementTypeId=col,
                            Value=opVal))

            db.session.commit()
    except Exception as dbException:
        return error_response(500, str(dbException))

    response = jsonify(uSet.serialize)
    return response


@bp.route('/uploadsets/<int:id>/download', methods=['GET'])
@token_auth.login_required
def uploadSetsDownload(id):
    uSet = UploadSet.query.filter_by(Id=id).first()
    return send_from_directory(
        directory=current_app.config.get('UPLOAD_FOLDER'),
        filename=uSet.StoredFileName,
        as_attachment=True,
        attachment_filename=uSet.FileName)


@bp.route('/uploadsets/<int:id>', methods=['GET'])
@token_auth.login_required
def getUploadSet(id):
    uSet = UploadSet.query.filter_by(Id=id).one_or_none()
    if uSet is None:
        return not_found("not found")
    return jsonify(uSet.serialize)

@bp.route('/uploadsets/<int:id>', methods=['DELETE'])
@token_auth.login_required
def deleteUploadSet(id):
    uSet = UploadSet.query.filter_by(Id=id).one_or_none()
    if uSet is None:
        return not_found("not found")
    try:
        db.session.delete(uSet)
        db.session.commit()
    except Exception as dbException:
        return error_response(500, str(dbException))

    return jsonify(uSet.serialize)

@bp.route('/uploadsets', methods=['POST'])
@token_auth.login_required
def CreateUploadSet():
    try:
        data = request.get_json()
        name = data.get("name", None)
        if not name:
            raise ValueError("required field name is not supplied")
        if name is "":
            raise ValueError("name field cannot be empty")
    except Exception as ex:
        return bad_request(str(ex))

    try:
        uSet = UploadSet(
            Name=name,
            CreatedDate=datetime.datetime.utcnow(),
            Description=data.get("description", None),
            UserId=g.current_user.id,
            FileName=None,
            StoredFileName=None)
        db.session.add(uSet)
        db.session.commit()
    except Exception as ex:
        return error_response(500, "could not insert record into uploadset")
    
    return jsonify(uSet.serialize), 201


def allowed_file(filename):
    return '.' in filename and \
           get_file_ext(filename) in ALLOWED_EXTENSIONS


def get_file_ext(filename):
    return filename.rsplit('.', 1)[1].lower()
