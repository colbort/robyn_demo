import json
import os
from typing import Dict


class Translator:
    _translations: Dict[str, Dict[str, str]] = {}  # 缓存语言数据
    _default_lang: str = "en"  # 默认语言
    _translations_path: str = "../locales"  # 翻译文件目录

    @classmethod
    def set_locales(cls, path: str):
        if path:
            cls._translations_path = path

    @classmethod
    def load_translation(cls, lang: str):
        """
        加载指定语言的翻译文件到缓存
        """
        if lang in cls._translations:  # 如果缓存中已存在，直接返回
            return cls._translations[lang]

        try:
            file_path = os.path.join(cls._translations_path, f"{lang}.json")
            with open(file_path, "r", encoding="utf-8") as file:
                cls._translations[lang] = json.load(file)
        except FileNotFoundError:
            # 如果找不到语言文件，回退到默认语言
            if lang != cls._default_lang:
                return cls.load_translation(cls._default_lang)
            else:
                raise Exception(f"Default language file '{cls._default_lang}.json' is missing!")
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse JSON file for language '{lang}': {e}")

        return cls._translations[lang]

    @classmethod
    def get_translation(cls, key: str, lang: str = "en") -> str:
        """
        获取指定语言的翻译内容
        """
        translations = cls.load_translation(lang)  # 加载语言数据
        return translations.get(key, key)  # 如果没有匹配的 key，则返回原始 key

    @classmethod
    def set_default_language(cls, lang: str):
        """
        设置默认语言
        """
        cls._default_lang = lang
