# -*- coding: utf-8 -*-
import hashlib
import hmac
from datetime import datetime


def get_authorization(timestamp: int, params: dict, secret_id: str, secret_key: str) -> str:
    '''
    :说明
        获取Header中的authorization参数

    :参数
        * timestamp：时间戳
        * params：上报data内容
        * secret_id：腾讯API内容
        * secret_key：腾讯API内容

    :返回
        * authorization：Header中的authorization参数
    '''
    service = "nlp"
    host = "nlp.tencentcloudapi.com"

    algorithm = "TC3-HMAC-SHA256"
    date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")

    # ************* 步骤 1：拼接规范请求串 *************
    http_request_method = "POST"
    canonical_uri = "/"
    canonical_querystring = ""
    ct = "application/json"
    payload = params
    canonical_headers = f"content-type:{ct}\nhost:{host}\n"
    signed_headers = "content-type;host"
    hashed_request_payload = hashlib.sha256(
        payload.encode("utf-8")).hexdigest()
    canonical_request = (http_request_method + "\n" + canonical_uri + "\n" +
                         canonical_querystring + "\n" + canonical_headers +
                         "\n" + signed_headers + "\n" + hashed_request_payload)

    # ************* 步骤 2：拼接待签名字符串 *************
    credential_scope = date + "/" + service + "/" + "tc3_request"
    hashed_canonical_request = hashlib.sha256(
        canonical_request.encode("utf-8")).hexdigest()
    string_to_sign = (algorithm + "\n" + str(timestamp) + "\n" +
                      credential_scope + "\n" + hashed_canonical_request)

    # ************* 步骤 3：计算签名 *************

    secret_date = _sign(("TC3" + secret_key).encode("utf-8"), date)
    secret_service = _sign(secret_date, service)
    secret_signing = _sign(secret_service, "tc3_request")
    signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"),
                         hashlib.sha256).hexdigest()

    # ************* 步骤 4：拼接 Authorization *************
    authorization = (algorithm + " " + "Credential=" + secret_id + "/" +
                     credential_scope + ", " + "SignedHeaders=" +
                     signed_headers + ", " + "Signature=" + signature)

    return authorization


def _sign(key, msg):
    '''
    计算签名摘要函数
    '''
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()
