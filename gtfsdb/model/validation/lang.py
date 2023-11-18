import pycountry


def is_valid_language_code(code, use_iso639_1=True):
    """指定された言語コードが有効かどうかをチェックする関数"""
    if use_iso639_1:
        # ISO 639-1 に基づく2文字の言語コードを検証
        try:
            return bool(pycountry.languages.get(alpha_2=code))
        except KeyError:
            return False
    else:
        # ISO 639-2 に基づく3文字の言語コードを検証
        try:
            return bool(pycountry.languages.get(alpha_3=code))
        except KeyError:
            return False
