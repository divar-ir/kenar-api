import httpx

from kenar.errors import APIException, HTTPException


def merge_headers(original_hdr, new_hdr):
    return original_hdr | new_hdr if new_hdr is not None else original_hdr


def mask_secret(key:str) -> str:
    if len(key) < 6:
        return '*' * 4
    return key[:2] + '*' * (len(key) - 4) + key[-2:]


def _request(client: httpx.Client, url: str, method: str, data):
    content = data.json() if data is not None else ''
    try:
        resp = client.request(
            method=method,
            url=url,
            content=content
        )
        if resp.status_code == httpx.codes.OK:
            return resp
        raise APIException({"code": resp.status_code, "message": resp.text})
    except httpx.RequestError as e:
        raise HTTPException(e) from None

