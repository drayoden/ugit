import hashlib
import os

GIT_DIR = '.ugit'

def init():
    os.makedirs(GIT_DIR)
    os.makedirs(f'{GIT_DIR}/objects')
    print(f'initialized empty ugit repo in {os.getcwd()}/{GIT_DIR}')

def hash_object(data, type_='blob'):
    obj = type_.encode() + b'\x00' + data
    oid = hashlib.sha1(obj).hexdigest()
    with open(f'{GIT_DIR}/objects/{oid}', 'wb') as out:
        out.write(obj)
    return oid

def get_object(oid, expected='blob'):
    with open(f'{GIT_DIR}/objects/{oid}', 'rb') as f:
        obj = f.read()

    first_null = obj.index(b'\x00')
    type_ = obj[:first_null].decode()   # type string before null byte
    content = obj[first_null + 1:]      # remaining data after the null byte

    
    # -- assert is used for debug only
    # if expected is not None:
    #    assert type_ == expected, f'Expected {exptected}, got {type_}'  
    # return content

    # -- alternate from above using 'raise'
    if expected is not None and type_ != expected:
        raise ValueError(f'Expected {exptected}, got {type_}' )
    return content