import os
from datetime import datetime

from symspellpy.symspellpy import SymSpell

class Item:
    requesterID: str = ""
    usePool: bool = False
    fixEncoding: bool = True
    decodeHTML: bool = True
    decodeUnicode: bool = True
    fixSpelling: bool = True
    splitDictVersion: str = "latest"
    splitCompoundWords: bool = True
    stripRepeatedCharacters: bool = True
    stripSpecialCharacters: str = ""
    maskNumbers: bool = False
    reattachPrefixes: bool = False
    text: list


sym_split = {}
for f in os.listdir("./split_dictionaries"):
    if f.endswith('.txt'):
        dict_name = f[0 : len(f) - 4]
        sym_split[dict_name] = None


def load_dictionary(dict_name):
    sym_split[dict_name] = SymSpell(0)
    dictionary_path = os.path.join(os.path.dirname(__file__), "split_dictionaries/" + dict_name + ".txt")
    if not sym_split[dict_name].load_dictionary(dictionary_path, term_index = 0, count_index = 1):
        print("ERROR: Dictionary [", dict_name , "] not found!")
        return False
    return True



def read_post(item: Item):
    start_time = datetime.now()

    # Check for Requester ID
    if not item.requesterID:
        return "ERROR: Missing flag: `requesterID`.  This should either be your VMware email address, or, if this is an automated request from a system, then this should be the name of the system.  Thank you."

    # Check for a valid dictionary name
    if not item.splitDictVersion in sym_split:
        return "ERROR: Invalid dictionary name.  Please `GET /dictionaries` for the list of available dictionaries."

    if item.usePool:
        # NOTE: Need ~1GB per process
        cpuCount = query_cpu()
        # Create an array such that each element of the array has one of the strings to be corrected and all flags
        params = vars(item)
        textWithFlags = list()
        for string in item.text:
            obj = {}
            obj['text'] = string
            for flag in params.keys():
                if (flag != 'text'):
                    obj[flag] = params[flag]
            textWithFlags.append(obj)
        # Multiprocess the text array with flags
        with Pool(cpuCount) as p:
            textWithFlags = p.map(fix, textWithFlags)
        # Copy the results back
        for i in range(len(textWithFlags)):
            item.text[i] = textWithFlags[i]['text']

    else:
        # Check if the requested dictionary has already been loaded
        if sym_split[item.splitDictVersion] == None:
            loaded = load_dictionary(item.splitDictVersion)
            if not loaded:
                return "ERROR: Failed to load dictionary [ " + item.splitDictVersion + " ].  Please inform a system administrator!"

        for i in range(len(item.text)):
            # Fix encoding problems
            if item.fixEncoding:
                item.text[i] = ftfy.fix_text(item.text[i], normalization='NFKC')
            # Decode HTML
            if item.decodeHTML:
                item.text[i] = decodeHTML(item.text[i])
            # Decode Unicode
            if item.decodeUnicode:
                item.text[i] = decodeUnicode(item.text[i])
            # Strip Repeated Characters
            if item.stripRepeatedCharacters:
                item.text[i] = regex_repeated_characters.fix(item.text[i])
            # Strip Special Characters
            if item.stripSpecialCharacters:
                item.text[i] = stripSpecialCharacters(item.text[i])
            # Custom Expansion(ignored in jinyu version)
            # if item.splitCompoundWords:
            #    item.text[i] = customExpansion(item.text[i])
            # Fix Spelling
            if item.fixSpelling:
                item.text[i] = fixSpelling(item.text[i])
            # Split Compound Words
            if item.splitCompoundWords:
                item.text[i] = splitCompoundWords(item.text[i], item.splitDictVersion)
            # Reattach prefixes
            if item.reattachPrefixes:
                item.text[i] = reattachPrefixes(item.text[i])
            # Mask Numbers
            if item.maskNumbers:
                item.text[i] = maskNumbers(item.text[i])
            # Clean up whitespace
            item.text[i] = cleanWhiteSpace(item.text[i])

    # Save stats
    if (not background_tasks == None):
        background_tasks.add_task(saveStats, item, datetime.now() - start_time)

    # Return cleansed strings
    return item
