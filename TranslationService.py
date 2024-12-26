from googletrans import Translator


class TranslationService:
    def __init__(self) -> None:
        pass

    def request_translation(self, text: str) -> str:
        translator = Translator()
        return translator.translate(text, dest='zh-cn').text
