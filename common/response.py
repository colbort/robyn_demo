import decimal
from typing import Any

from pydantic import BaseModel
from robyn.types import JSONResponse


# 返回结果统一格式
class ResponseModel(BaseModel):
    code: int
    message: str
    data: Any = None


def convert_decimal_to_float(data):
    """递归地将数据中的 decimal.Decimal 转换为 float"""
    if isinstance(data, dict):
        return {key: convert_decimal_to_float(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_decimal_to_float(item) for item in data]
    elif isinstance(data, decimal.Decimal):
        return float(data)
    return data


# 成功返回
def success(data: Any = None, message: str = "请求成功") -> ResponseModel:
    resp = ResponseModel(code=200, message=message, data=convert_decimal_to_float(data))
    return JSONResponse(resp.model_dump())


# 失败返回
def fail(code: int = 400, message: str = "请求失败") -> ResponseModel:
    resp = ResponseModel(code=code, message=message)
    return JSONResponse(resp.model_dump())


# 异常返回
def error(message: str = "服务器内部错误") -> ResponseModel:
    resp = ResponseModel(code=500, message=message)
    return JSONResponse(resp.model_dump())
