import uuid
import base64


def get_compress_uuid():
    data = uuid.uuid4()
    data = str(data)
    data = data.replace('-', '')
    data = base64.b64encode(data.encode())
    data = data.decode()
    data = data.strip('=\n')
    return data
