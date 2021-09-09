from db import Db
from mnemonic import Mnemonic

conn = Db()

def generate_mnemonic():
    m = Mnemonic('english')
    idx = 1
    all_words = set()
    while idx <= 10000:
        words = m.generate()
        if words in all_words:
            continue

        word_list = list(filter(bool, words.split(' ')))
        attributes = []
        for word_idx, word in enumerate(word_list):
            attributes.append({
                'trait_type': f'word {word_idx}',
                'value': word
            })

        nft = {
            'index': idx,
            'name': f'MLoot #{idx}',
            'description': f'MLoot #{idx}',
            'word_list': word_list,
            'attributes': attributes
        }
        conn.add_mloot(nft)
        idx += 1


if __name__ == '__main__':
    generate_mnemonic()