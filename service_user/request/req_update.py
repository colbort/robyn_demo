from typing import Optional

from pydantic import BaseModel, EmailStr, constr, model_validator


class ReqUpdate(BaseModel):
    email: Optional[EmailStr] = None  # 可选，合法的电子邮件地址
    phone_country_code: Optional[constr(min_length=1, max_length=5)] = None  # 可选，国家代码
    phone: Optional[constr(min_length=8, max_length=15)] = None  # 可选，电话号码
    nickname: Optional[constr(min_length=1, max_length=20)] = None  #
    avatar: Optional[constr(min_length=6, max_length=128)] = None  #
    password: Optional[constr(min_length=6, max_length=20)] = None  # 必须，密码长度约束
    captcha: str  # 必须，验证码

    # 自定义验证器：email 和 phone 至少需要一个
    @classmethod
    @model_validator(mode="before")
    def validate_contact(cls, value, info):
        values = info.data  # 获取所有字段值
        phone = values.get("phone")
        phone_country_code = values.get("phone_country_code")

        # 如果有 phone，则必须提供 phone_country_code
        if phone and not phone_country_code:
            raise ValueError("phone_country_code 不能为空")

        return value
