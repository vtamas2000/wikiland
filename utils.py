from typing import List
import string
import re
import numpy as np


def process_text(text: str) -> List[str]:

    """
    Processes the text so that only relevent words remain in it. Returns a list of the words in the text.
    """

    text = text.split('^')[0]
    text = re.sub(r'\[\d+\]', ' ', text)
    text = re.sub(r'\[\D+\]', ' ', text)
    text = text.replace('\n', ' ')
    text = text.replace('. ', 'y'*26)
    text = text.replace('.', 'z'*26)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.replace('–', '')
    text = text.replace('—', '')
    text = text.replace('×', '')
    text = text.replace('z'*26, '.')
    
    text = text.replace('y'*26, ' . ')
    text = text.lower()
    text_array = np.array(text.split(' '))
    text_array = list(text_array[text_array != ''])  # Removes the empty '' that come in after the splitting

    return text_array