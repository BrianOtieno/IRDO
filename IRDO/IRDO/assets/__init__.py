from flask import Blueprint

blueprint = Blueprint(
    'assets_blueprint',
    __name__,
    url_prefix='/assets',
    template_folder='/templates',
    static_folder='/static'
)

import IRDO.assets.routes
