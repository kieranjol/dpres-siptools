from urllib import quote_plus, unquote_plus
from hashlib import md5

def encode_path(path, suffix='', prefix=''):
    return prefix + quote_plus(path) + suffix

def decode_path(path, suffix=''):
    path = unquote_plus(path)
    if path.endswith(suffix):
        path = path.replace(suffix, '', 1)
    return path 

def encode_id(id, suffix=''):
    #print encode_path(path, suffix, prefix) + " to " + md5(encode_path(path,
    #    suffix, prefix)).hexdigest()
    return '_' + md5(id).hexdigest()
