from flask import Blueprint
from config import db
test = Blueprint('test', __name__)


@test.route("/")
def live():
    return "Up and running!"
