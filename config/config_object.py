class ConfigObject:
    """通用配置对象类，将字典转换为嵌套类属性，并映射顶层属性"""

    def __init__(self, config_dict):
        # 遍历字典的键值对
        for key, value in config_dict.items():
            keys = key.split(".")
            current = self
            for sub_key in keys[:-1]:
                if not hasattr(current, sub_key):
                    setattr(current, sub_key, ConfigObject({}))
                current = getattr(current, sub_key)
            setattr(current, keys[-1], value)

        # 动态将顶层嵌套属性映射为顶层直接属性
        existing_keys = list(self.__dict__.keys())  # 创建属性名的副本
        for key in existing_keys:
            attr = getattr(self, key)
            if isinstance(attr, ConfigObject):  # 仅映射嵌套对象
                for nested_key, nested_value in attr.__dict__.items():
                    # 将嵌套的属性映射到顶层
                    setattr(self, f"{nested_key}", nested_value)

    def __call__(self):
        """实现可调用行为，返回自身或其他操作"""
        return self

    def __repr__(self):
        return f"<ConfigObject {self.__dict__}>"
