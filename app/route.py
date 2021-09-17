import random

from flask import Blueprint, jsonify
from exception import APIParamError
from model import MCode
from utils import get_image

router_bp = Blueprint('router', __name__)


@router_bp.route('/mcode/<int:_token_id>')
def nft(_token_id):
    if _token_id < 0 or _token_id > 9999:
        raise APIParamError()

    mcode = MCode.query.filter(MCode.index == _token_id).scalar()
    image = get_image(mcode.word_list)
    mcode = {
        'name': mcode.name,
        'description': mcode.description,
        'image': image,
        'image_data': image,
        'attributes': mcode.attributes,
    }
    return jsonify(mcode)


@router_bp.route('/mcode/random/<int:n>')
def random_n(n):
    idx = random.randint(1, 10000 - n + 1)
    models = MCode.query.filter(MCode.index.in_(tuple(list(range(idx, idx+n))))).all()
    mcodes = []
    for model in models:
        mcodes.append({
            'id': model.index,
            'word_list': model.word_list
        })
    return jsonify(mcodes)
