import jwt



def decode_token(token: str):

    try:
        decoded_token = jwt.decode(token, "secret_key", algorithms="HS256")

        return f'Bearer {decoded_token}'
    except jwt.ExpiredSignatureError as je:
        raise je