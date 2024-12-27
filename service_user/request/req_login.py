from typing import Optional

from pydantic import BaseModel, EmailStr, constr, model_validator


class ReqLogin(BaseModel):
    email: Optional[EmailStr] = None  # 可选，合法的电子邮件地址
    phone_country_code: Optional[constr(min_length=1, max_length=5)] = None  # 可选，国家代码
    phone: Optional[constr(min_length=8, max_length=15)] = None  # 可选，电话号码
    username: Optional[constr(min_length=3)] = None  # 用户名
    password: constr(min_length=6, max_length=20)  # 必须，密码长度约束

    @classmethod
    @model_validator(mode="before")
    def validate_contact(cls, value, info):
        values = info.data  # 获取所有字段值
        email = values.get("email")
        phone = values.get("phone")
        phone_country_code = values.get("phone_country_code")
        username = values.get('username')

        if not email and not phone and not username:
            raise ValueError("email, phone, username 至少需要一个")

        if phone and not phone_country_code:
            raise ValueError("phone_country_code 不能为空")

        return value
