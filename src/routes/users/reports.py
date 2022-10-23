""""
Handles reports/cases uploaded by citizens

"""
import mimetypes
import enum
import uuid
import json
from datetime import datetime
from config import db
from Logic_objects import location as loc
from ML_workspace import model, CovidCT, CovidXray, Tuber
# from Logic_objects import file_server
from flask import Blueprint, request, make_response, jsonify

# from routes.users import token_required
from routes import API_required, token_required


file = Blueprint('file', __name__)


@file.route("/new-CovidCT",  methods=['POST'])
@token_required
@API_required
def new_CovidCT(current_user):
    if not current_user:
        return make_response(jsonify({
            'message': 'unable to find user '
        }), 400)
    try:
        if not request or not request.json:
            return make_response(jsonify(error="Requirements Missing REQUIRED"), 400)
        resp = dict(request.json)
        ImgID = resp.get("ImgID")
        if not ImgID:
            return make_response(jsonify(error="No IMAGE ID"), 400)
        Covid = CovidCT.CovidCT(ImgID)
        # print(Covid is "True", Covid, "True")
        if Covid.__repr__() is "True":
            print(Covid)
            response = Covid.Predict()
            if response == "error":
                return make_response(jsonify(error="Error Source"), 400)
            print(current_user, ".dockerignore")
            current_user["Services"]["CovidCT"].append({
                "date": str(datetime.now()),
                "result": response,
                "ImgFile": ImgID
            })
            newObj = db.users.update_one({"_id": current_user["_id"]}, {
                "$set": {"Services": current_user["Services"]}
            })

            return make_response(jsonify(success=True, result=response), 200)
        else:
            return make_response(jsonify(error="Improper Image ID"), 400)
    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(uploaded="fail", file_id=None, error=e), 403)


@file.route("/new-CovidXray",  methods=['POST'])
@token_required
@API_required
def new_CovidXray(current_user):
    if not current_user:
        return make_response(jsonify({
            'message': 'unable to find user'
        }), 400)
    try:
        if not request or not request.json:
            return make_response(jsonify(error="Requirements Missing REQUIRED"), 400)
        resp = dict(request.json)
        ImgID = resp.get("ImgID")
        Covid = CovidXray.CovidXray(ImgID)
        if Covid.__repr__():
            response = Covid.Predict()
            if response == "error":
                return make_response(jsonify(error="Error Source"), 400)
            current_user["Services"]["CovidXray"].append(
                {
                    "date": str(datetime.now()),
                    "result": response,
                    "ImgFile": ImgID
                }
            )
            newObj = db.users.update_one({"_id": current_user["_id"]}, {
                "$set": {"Services": current_user["Services"]}
            })

            return make_response(jsonify(success=True, result=response), 200)
        else:
            return make_response(jsonify(error="Improper Image ID"), 400)
        return make_response(jsonify(success=True), 200)
    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(uploaded="fail", file_id=None, error=e), 403)


@file.route("/new-Tuber",  methods=['POST'])
@token_required
@API_required
def new_Tuber(current_user):
    if not current_user:
        return make_response(jsonify({
            'message': 'unable to find user '
        }), 400)
    try:
        if not request or not request.json:
            return make_response(jsonify(error="Requirements Missing REQUIRED"), 400)
        resp = dict(request.json)
        ImgID = resp.get("ImgID")
        Covid = Tuber.Tuber(ImgID)
        if Covid.__repr__():
            response = Covid.Predict()
            if response == "error":
                return make_response(jsonify(error="Error Source"), 400)
            print(current_user, "TRYYY")
            current_user["Services"]["Tuber"].append(
                {
                    "date": str(datetime.now()),
                    "result": response,
                    "ImgFile": ImgID
                }
            )
            newObj = db.users.update_one({"_id": current_user["_id"]}, {
                "$set": {"Services": current_user["Services"]}
            })

            return make_response(jsonify(success=True, result=response), 200)
        else:
            return make_response(jsonify(error="Improper Image ID"), 400)
        return make_response(jsonify(success=True), 200)
    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(uploaded="fail", file_id=None, error=e), 403)


@file.route("/GetCases",  methods=['POST'])
@token_required
@API_required
def getCases(current_user):
    if not current_user:
        return make_response(jsonify({
            'message': 'unable to find user '
        }), 400)
    try:
        if not request or not request.json:
            return make_response(jsonify(error="Requirements Missing REQUIRED"), 400)
        resp = dict(request.json)
        Type = resp.get("Type")
        if Type not in ["CovidXray", "CovidCT", "Tuber", "Malaria"]:
            return make_response(jsonify(error="Impropr TYPE"), 400)
        return make_response(jsonify(success=True, result=current_user["Services"][Type]), 200)
    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(uploaded="fail", file_id=None, error=e), 403)
