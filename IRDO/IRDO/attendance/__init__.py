from flask import Blueprint

blueprint = Blueprint(
    'attendance_blueprint',
    __name__,
    url_prefix='/attendance',
    template_folder='/templates',
    static_folder='/static'
)

import IRDO.attendance.routes
