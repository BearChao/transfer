from flask import Blueprint

func = Blueprint('func', __name__)

from . import task_views,job_views,ipconfig_view