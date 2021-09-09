import base64
from typing import List


def get_image(word_list: List[str]) -> str:
    s = '<svg xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMinYMin meet" viewBox="0 0 350 350"><style>.base { fill: white; font-family: serif; font-size: 14px; }</style><rect width="100%" height="100%" fill="black" />'
    y = 20
    for word in word_list:
        s += f'<text x="10" y="{y}" class="base">{word}</text>'
        y += 20
    s += '</svg>'
    return f'data:image/svg+xml;base64,{base64.b64encode(s.encode()).decode()}'
