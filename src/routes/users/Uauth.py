
import redis
import jwt
from config import db
import config
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, make_response
from routes.users import token_required
from routes import API_required, Uhash, Phash, verifyPass, SetOTP

user = Blueprint('user', __name__)


@user.route("/signup",  methods=['POST'])
@API_required
def signup():
    try:
        if not request or not request.json:
            return make_response(jsonify(error="Requirements Missing REQUIRED"), 400)

        req = dict(request.json)
        MobileNum = req.get("MobileNum")
        # FirstName = req.get("FirstName")
        # address = req.get("addr")
        if not MobileNum:
            return make_response(jsonify(error="Requirements Missing REQUIRED"), 400)

        UniqueNum = Uhash(MobileNum)

        SetOTP(MobileNum)
        # return make_response(jsonify(error="Ivalid Number to send OTP"), 400)
        return make_response(jsonify(success=True), 200)
    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(error=e), 401)


@user.route("/Validate-signup",  methods=['POST'])
@API_required
def ValidateSingnup():
    try:
        if not request or not request.json:
            return make_response(jsonify(error="Requirements Missing REQUIRED"), 400)
        req = dict(request.json)

        MobileNum = req.get("MobileNum")
        OTP = int(req.get("OTP"))
        FirstName = req.get("FirstName")
        address = req.get("addr")
        Age = req.get("age")
        gender = req.get("gender")

        if not MobileNum or not FirstName or not address or not OTP or not Age or not gender:
            return make_response(jsonify(error="Requirements Missing REQUIRED"), 400)
        r = redis.Redis(host='localhost', port=6379, db=0)
        rOTP = int(r.get(MobileNum))
        if not rOTP:
            return make_response(jsonify(error="No user Registered"), 400)
        if OTP != rOTP:
            return make_response(jsonify(error="Wrong OTP"), 400)
        UniqueNum = Uhash(MobileNum)
        useOBJ = {
            "_id": UniqueNum,
            "FirstName": FirstName,
            "address": address,
            "MobileNum": MobileNum,
            "age": Age,
            "gender": gender,
            "Services": {
                "CovidXray": [],
                "CovidCT": [],
                "Tuber": [],
                "Malaria": []
            }
        }
        db.users.insert_one(useOBJ)
        return make_response(jsonify(success=True), 200)

    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(error=e), 401)


@user.route("/Validate-Login",  methods=['POST'])
@API_required
def ValidateSingnin():
    try:
        if not request or not request.json:
            return make_response(jsonify(error="Requirements Missing REQUIRED"), 400)
        req = dict(request.json)
        MobileNum = req.get("MobileNum")
        OTP = int(req.get("OTP"))
        if not MobileNum or not OTP:
            return make_response(jsonify(error="Requirements Missing REQUIRED"), 400)
        r = redis.Redis(host='localhost', port=6379, db=0)
        rOTP = int(r.get(MobileNum))
        if OTP != rOTP:
            return make_response(jsonify(error="Wrong OTP"), 400)

        UniqueNum = Uhash(MobileNum)
        useOBJ = db.users.find_one({"_id": UniqueNum})

        token = jwt.encode({
            'public_id': useOBJ["_id"],
            'exp': datetime.utcnow() + timedelta(weeks=2)
        }, config.SECRET_KEY).decode('utf-8')
        return make_response(jsonify(success=True, token=str(token), user=useOBJ), 200)

    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(error=e), 401)


# default route to authenticate or for init after re-opening client
@user.route('/init', methods=['GET'])
@token_required
@API_required
def init(current_user):
    return make_response(jsonify(message="Valid session"), 200)


@user.route('/del-acct', methods=['DELETE'])
@token_required
@API_required
def DelAccount(current_user):
    try:
        db.users.delete_one({"_id": current_user['_id']})
        return make_response(jsonify(accountDel=True))
    except Exception as e:
        print(e,  e.__traceback__.tb_lineno)
        return make_response(jsonify(error=e), 401)
