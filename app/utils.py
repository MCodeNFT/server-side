import json
import re

import requests
from consts import vnlp_api, model_api
from typing import Union, List
from urllib import request, parse


def fetch_api(url: str, method: str = 'GET', params: dict = {}, body: dict = {}, raw: bool = False, retry: int = 3):
    full_url = url
    if params:
        full_url = f'{url}/{parse.urlencode(params)}'
    try:
        if method == 'GET':
            res = requests.get(full_url)
        else:
            res = requests.post(full_url, json=body)
    except Exception as e:
        print(e)
        if retry > 0:
            return fetch_api(url, method, params, body, raw, retry - 1)
        else:
            return {}
    if raw:
        return res.text
    else:
        return res.json()


def get_vnlp_process_lines(lines: [str]) -> Union[None, List[str]]:
    body = {
        'text': lines,
        'fixSpelling': False,
        'usePool': True,
        'stripSpecialCharacters': 'all',
        'requesterID': 'jinyuj'
    }
    res = fetch_api(vnlp_api, method='POST', body=body)
    return res.get('text', [])


def get_pcc_from_model(raw_lines: [str]) -> str:
    body = {
        'lines': raw_lines
    }
    # res = fetch_api(model_api, method='POST', body=body)
    # return res.get('pcc')
    return 'XYZ'


def match_loop_output_regex(lines: [str], loop_output_regex: [[str]])-> bool:
    def lines_with_single_regex(lines: [str], regex: str) -> bool:
        for line in lines:
            if not re.fullmatch(regex, line):
                return False
        return True

    def lines_with_n_regex(lines: [str], regex_list: [str]) -> bool:
        for regex in regex_list:
            if not lines_with_single_regex(lines, regex):
                return False
        return True

    for loop_regex in loop_output_regex:
        if lines_with_n_regex(lines, loop_regex):
            return True
    return False
