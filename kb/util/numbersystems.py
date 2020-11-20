ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyz'


def encode(n):
    try:
        return ALPHABET[n]
    except IndexError:
        raise Exception('cannot encode %s' % n)


def dec_to_base(dec=0, base=36):
    if dec < base:
        return encode(dec)
    else:
        return dec_to_base(dec // base, base) + encode (dec % base)