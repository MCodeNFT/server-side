import logging
import urllib.request

from flask import Blueprint, request, jsonify
from flask import current_app as app
from exception import APIParamError
from model import Log, db
from utils import get_vnlp_process_lines, match_loop_output_regex, get_pcc_from_model

router_bp = Blueprint('router', __name__)


@router_bp.route('/', methods=['POST'])
def analyze():
    # get param url
    try:
        j = request.get_json()
        url = j.get('url', '')
        lines = j.get('lines', [])
        assert url or lines
    except Exception as e:
        logging.error(e)
        raise APIParamError()

    # get lines from url
    if url and not lines:
        try:
            with urllib.request.urlopen(url) as r:
                lines = r.readlines()
                lines = [i.decode() for i in lines]
        except Exception as e:
            logging.error(f'error {e}, url: {url}')
            raise

    # strip: \n
    lines = list(filter(bool, [i.strip() for i in lines]))
    print(f'origin lines: {lines}')

    # pre process
    #   todo: replace path, vm_name

    # call vnlp api to
    processed_log = get_vnlp_process_lines(lines)
    print(f'processed_log: {processed_log}')

    # post vnlp process
    #   todo: extract regex

    # if lines are recognized
    #    fetch loop_output_regex with is_tmp=false
    loop_logs = Log.query.filter(Log.loop_output_regex != '{}').filter_by(is_temp=False).all()
    loop_regex = [loop.loop_output_regex for loop in loop_logs]
    print(f'loop_regex: {loop_regex}')
    matched = match_loop_output_regex(lines, loop_regex)
    if matched:
        pcc = get_pcc_from_model(lines)
        return jsonify({
            'pcc': pcc
        })

    log = {
        'url': url,
        'raw_log': lines,
        'processed_log': processed_log
    }
    log_model = Log(**log)
    db.session.add(log_model)
    db.session.commit()

    # check duplication before create loop project

    return jsonify({
        'pcc': 'unknown'
    })
