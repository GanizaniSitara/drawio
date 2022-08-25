import base64, zlib
from urllib.parse import quote, unquote, quote_plus

# functions courtesy of
# https://stackoverflow.com/questions/46351275/using-pako-deflate-with-python
# TODO: refactor
def js_encode_uri_component(data):
    return quote(data, safe='~()*!.\'')

def js_decode_uri_component(data):
    return unquote(data)

def js_string_to_byte(data):
    return bytes(data, 'iso-8859-1')

def js_bytes_to_string(data):
    return data.decode('iso-8859-1')

def js_btoa(data):
    return base64.b64encode(data)

def js_atob(data):
    return base64.b64decode(data)

def pako_deflate_raw(data):
    compress = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -15, memLevel=8,strategy=zlib.Z_DEFAULT_STRATEGY)
    compressed_data = compress.compress(data)
    compressed_data += compress.flush()
    return compressed_data

def pako_inflate_raw(data):
    decompress = zlib.decompressobj(-15)
    decompressed_data = decompress.decompress(data)
    decompressed_data += decompress.flush()
    return decompressed_data

def decode_diagram_data(data):
    data = js_atob(data)
    data = pako_inflate_raw(data)
    data = data.decode()
    data = unquote(data)
    return data

def encode_diagram_data(data):
    # https://stackoverflow.com/questions/33547976/using-python-quote-plus-with-slashes
    data = quote(data, safe='~()*!.\'')
    data = data.encode()
    data = pako_deflate_raw(data)
    data = js_btoa(data)
    return data

def encode_stencil(data):
    # https://stackoverflow.com/questions/33547976/using-python-quote-plus-with-slashes
    data = quote(data, safe='~()*!.\'')
    data = data.encode()
    data = pako_deflate_raw(data)
    data = js_btoa(data)
    data = data.decode("utf-8")
    return data






