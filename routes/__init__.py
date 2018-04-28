from flask import Blueprint
routes = Blueprint('routes', __name__)

from .nixie import *
from .happiness import *