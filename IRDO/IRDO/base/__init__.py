from flask import Blueprint

blueprint = Blueprint(
    'base_blueprint',
    __name__,
    url_prefix='/base',
    template_folder='/templates',
    static_folder='/static'
)

import IRDO.base.routes
