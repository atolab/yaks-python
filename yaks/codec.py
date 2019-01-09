from papero import *
from yaks.message import *
from yaks.encoding import *


def encode_raw_value(buf, v):
    buf.put_string(v.raw_format)
    buf.put_bytes(v.value.encode())


def decode_raw_value(buf, v):
    raw_format = buf.get_string()
    data = buf.get_bytes()
    return Value(data, encoding=Encoding.RAW, raw_format=raw_format)


def encode_json_value(buf, v):
    buf.put_string(v.value)


def decode_json_value(buf, v):
    data = buf.get_string()
    return Value(data, encoding=Encoding.JSON)


def encode_property_value(buf, v):
    encode_properties(buf, v.value)


def decode_property_value(buf, v):
    data = decode_properties(buf)
    return Value(data, encoding=Encoding.PROPERTY)


def encode_value(buf, v):
    buf.put(v.encoding)
    {
        Encoding.RAW: lambda v: encode_raw_value(buf, v),
        Encoding.JSON: lambda v: encode_json_value(buf, v),
        Encoding.PROPERTY: lambda v: encode_property_value(buf, v)
    }.get(v.encoding)(v)


def decode_value(buf):
    encoding = buf.get()
    v = {
        Encoding.RAW: lambda b: decode_raw_value(buf, b),
        Encoding.JSON: lambda b: decode_json_value(buf, b),
        Encoding.PROPERTY: lambda b: decode_property_value(buf, b)
    }.get(encoding)(buf)
    return v


def encode_key_value(buf, key, value):
    print("encoding key.value with key {}".format(key))
    buf.put_string(key)
    encode_value(buf,value)


def decode_key_value(buf):
    k = buf.get_string()
    v = decode_value(buf)
    return (k, v)


def encode_key_value_list(buf, kvs):
    encode_sequence(buf, kvs, encode_key_value)


def decode_key_value_list(buf):
    return decode_sequence(buf, decode_key_value)


def encode_header(buf, m):
    buf.put(m.mid)
    buf.put(m.flags)
    buf.put_vle(m.corr_id)
    if m.properties is not None:
        encode_properties(buf, m.properties)
    return buf


def decode_header(buf):
    mid = buf.get()
    flags = buf.get()
    corr_id = buf.get_vle()
    properties = None
    if Header.has_flag(flags, Header.P_FLAG):
        properties = decode_properties(buf)

    return Header(mid, corr_id, properties)


def encode_login(buf, m):
    encode_header(buf, m)


def encode_logout(buf, m):
    encode_header(buf, m)


def encode_workspace(buf, m):
    encode_header(buf, m)
    buf.put_string(str(m.path))


def encode_put(buf, m):
    encode_header(buf, m)
    encode_key_value_list(buf, m.kvs)


def encode_get(buf, m):
    encode_header(buf, m)
    buf.put_string(m.selector)


def encode_update(buf, m):
    encode_header(buf, m)
    encode_key_value_list(buf, m.kvs)


def encode_delete(buf, m):
    encode_header(buf, m)
    buf.put_string(m.path)


def encode_sub(buf, m):
    encode_header(buf, m)
    buf.put_string(m.selector)


def encode_unsub(buf, m):
    encode_header(buf, m)
    buf.put_string(m.subid)


def encode_reg_eval(buf, m):
    encode_header(buf, m)
    buf.put_string(m.path)


def encode_unreg_eval(buf, m):
    encode_header(buf, m)
    buf.put_string(m.path)


def encode_eval(buf, m):
    encode_header(buf, m)
    buf.put_string(m.selector)


def encode_values(buf, m):
    encode_header(buf, m)
    encode_key_value_list(buf, m.kvs)


def encode_ok(buf, m):
    encode_header(buf, m)


def encode_error(buf, m):
    encode_header(buf, m)


def decode_put(buf, header):
    properties = header.properties
    kvs = decode_key_value_list(buf)
    wsid = find_property(Message.WSID, properties)
    return PutM(wsid, kvs, properties)


def decode_get(buf, header):
    properties = header.properties
    wsid = find_property(Message.WSID, properties)
    selector = Selector(buf.get_string())
    return GetM(wsid, selector, properties)


def decode_update(buf, header):
    properties = header.properties
    kvs = decode_key_value_list(buf)
    wsid = find_property(Message.WSID, properties)
    return UpdateM(wsid, kvs, properties)


def decode_delete(buf, header):
    properties = header.properties
    wsid = find_property(Message.WSID, properties)
    path = buf.get_string()
    return DeleteM(wsid, path, properties)


def decode_sub(buf, header):
    properties = header.properties
    wsid = find_property(Message.WSID, properties)
    selector = Selector(buf.get_string())
    return SubscribeM(wsid, selector. properties)


def decode_unsub(buf, header):
    properties = header.properties
    wsid = find_property(Message.WSID, properties)
    subid = buf.get_string()
    return UnsubscribeM(wsid, subid, properties)


def decode_eval(buf, header):
    properties = header.properties
    wsid = find_property(Message.WSID, properties)
    selector = Selector(buf.get_string())
    return EvalM(wsid, selector, properties)


def decode_reg_eval(buf, header):
    properties = header.properties
    wsid = find_property(Message.WSID, properties)
    selector = Selector(buf.get_string())
    return RegisterEvalM(wsid, selector, properties)


def decode_unreg_eval(buf, header):
    properties = header.properties
    wsid = find_property(Message.WSID, properties)
    selector = Selector(buf.get_string())
    return UnregisterEvalM(wsid, selector, properties)


def decode_values(buf, header):
    kvs = decode_key_value_list(buf)
    return ValuesM.make(header, kvs)


def decode_ok(buf, header):
    return OkM.make(header)


def decode_error(buf, header):
    ec = buf.get()
    return ErrorM.make(header, ec)


def decode_message(buf):
    h = decode_header(buf)
    return {
        Message.OK: lambda h: decode_ok(buf, h),
        Message.ERROR: lambda h: decode_error(buf, h),
        Message.PUT: lambda h: decode_update(buf, h),
        Message.GET: lambda h: decode_get(buf, h),
        Message.UPDATE: lambda h: decode_update(buf, h),
        Message.DELETE: lambda h: decode_delete(buf, h),
        Message.SUB: lambda h: decode_sub(buf, h),
        Message.UNSUB: lambda h: decode_unsub(buf, h),
        Message.EVAL: lambda h: decode_eval(buf, h),
        Message.REG_EVAL: lambda h: decode_reg_eval(buf, h),
        Message.UNREG_EVAL: lambda h: decode_unreg_eval(buf, h),
        Message.VALUES: lambda h: decode_values(buf, h)

    }.get(h.mid)(h)


def encode_message(buf, m):
    {
        Message.LOGIN: lambda m: encode_login(buf, m),
        Message.LOGOUT: lambda m: encode_logout(buf, m),
        Message.WORKSPACE: lambda m: encode_workspace(buf, m),
        Message.PUT: lambda m: encode_put(buf, m),
        Message.GET: lambda m: encode_get(buf, m),
        Message.UPDATE: lambda m: encode_update(buf, m),
        Message.DELETE: lambda m: encode_delete(buf, m),
        Message.VALUES: lambda m: encode_values(buf, m),
        Message.SUB: lambda m: encode_sub(buf, m),
        Message.UNSUB: lambda m: encode_unsub(buf, m),
        Message.EVAL: lambda m: encode_eval(buf, m),
        Message.REG_EVAL: lambda m: encode_reg_eval(buf, m),
        Message.UNREG_EVAL: lambda m: encode_unreg_eval(buf, m),
        Message.OK: lambda m: encode_ok(buf, m),
        Message.ERROR: lambda m: encode_error(buf, m)
    }.get(m.mid)(m)
