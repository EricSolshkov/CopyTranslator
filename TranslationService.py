import json
import random

from googletrans import Translator
import requests
import http
from hashlib import md5
from urllib import parse
from abc import ABC, abstractmethod


class TranslationService(ABC):
    @abstractmethod
    def __init__(self) -> None:
        self.name = "Abstract Service"
        pass

    @abstractmethod
    def translate(self, text: str) -> str:
        return "Abstract method should not be called."


class GoogleTrans(TranslationService):
    def __init__(self) -> None:
        super().__init__()
        self.translator = Translator()
        self.name = "GoogleTrans API"

    def translate(self, text: str) -> str:
        try:
            text = self.translator.translate(text, dest="zh-cn").text
            return text
        except Exception as e:
            return str(e)
        finally:
            return text


class BaiduTranslation(TranslationService):
    def __init__(self, app_id, key) -> None:
        super().__init__()
        self.app_id = app_id
        self.key = key
        self.name = "Baidu API"

    def translate(self, text: str) -> str:
        client = http.client.HTTPConnection("api.fanyi.baidu.com")
        salt = random.randint(114514, 1919810)
        sign = md5(f"{self.app_id}{text}{salt}{self.key}".encode("utf-8")).hexdigest()
        url = (f"/api/trans/vip/translate"
               f"?appid={str(self.app_id)}"
               f"&key={str(self.key)}"
               f"&q={parse.quote(text)}"
               f"&from=auto&to=zh"
               f"&salt={str(salt)}"
               f"&sign={str(sign)}")
        try:
            client.request("GET", url)
            response = client.getresponse()
            result = json.loads(response.read().decode("utf-8"))

            return result.get("trans_result", [{}])[0].get("dst", "")
        except Exception as e:
            return str(e)
        finally:
            client.close()
