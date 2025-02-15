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

    @model_validator(mode="after")
    def validate_contact(self):
        phone = self.phone
        phone_country_code = self.phone_country_code

        if phone and not phone_country_code:
            raise ValueError("phone_country_code 不能为空")
        if phone_country_code and not phone:
            raise ValueError("phone 不能为空")

        avatar = self.avatar
        if avatar and not (avatar.startswith("http://") or avatar.startswith("https://")):
            raise ValueError("avatar 必须以 http:// 或 https:// 开头")

        return self
