import random

from flask import Blueprint, jsonify
from exception import APIParamError
from model import MLoot
from utils import get_image

router_bp = Blueprint('router', __name__)


@router_bp.route('/mloot/<int:_token_id>')
def nft(_token_id):
    if _token_id <= 0 or _token_id > 10000:
        raise APIParamError()

    mloot = MLoot.query.filter(MLoot.index == _token_id).scalar()
    mloot = {
        'name': mloot.name,
        'description': mloot.description,
        'image': get_image(mloot.word_list),
        'attributes': mloot.attributes,
    }
    return jsonify(mloot)


@router_bp.route('/mloot/random/<int:n>')
def random3(n):
    idx = random.randint(1, 10000 - n + 1)
    models = MLoot.query.filter(MLoot.index.in_(tuple(list(range(idx, idx+n))))).all()
    mloots = []
    for model in models:
        mloots.append({
            'id': model.index,
            'word_list': model.word_list
        })
    return jsonify(mloots)