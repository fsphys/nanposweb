from hashlib import sha256


def format_currency(value, factor=100):
    return '{:.2f} €'.format(value / factor).replace('.', ',')


def check_hash(hashed, value):
    hashed_value = sha256(value.encode('utf-8')).hexdigest()

    if hashed == hashed_value:
        return True
    else:
        return False


def calc_hash(value):
    return sha256(value.encode('utf-8')).hexdigest()
