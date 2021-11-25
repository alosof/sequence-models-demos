import numpy as np
import string


vocab = list(string.digits) + list(string.ascii_lowercase) + ['.', ' ', '\'']
index_to_char = {index: vocab[index] for index in range(len(vocab))}
char_to_index = {char: index for index, char in index_to_char.items()}

def one_hot_encode(text, char_to_index=char_to_index):
    indices = [char_to_index[c] for c in text]
    one_hot_encoding = np.zeros((len(indices), len(char_to_index)))
    for i in range(len(indices)):
        one_hot_encoding[i, indices[i]] = 1
    return one_hot_encoding

def one_hot_decode(encoding, index_to_char=index_to_char):
    result = ""
    for e in encoding:
        result = result + index_to_char[list(e).index(1)]
    return result

def pick_char(preds, temperature=1.0, do_sample=True, index_to_char=index_to_char):
    # Avec sampling
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    # Sans sampling
    preds = np.reshape(preds, (1, preds.shape[0]))
    if do_sample:
        return index_to_char[np.argmax(probas)]
    else:
        return index_to_char[np.argmax(preds)]
