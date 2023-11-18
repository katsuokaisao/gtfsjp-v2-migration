import re

# https://www.soumu.go.jp/main_sosiki/joho_tsusin/top/tel_number/q_and_a.html#q2
# 0から始まる市外局番込の10桁の番号
# [2-9]から始まる市外局番を含まない5~8桁の番号
# 市外局番と市内局番は各1~4桁、合わせると5桁 になる
# 携帯電話とPHSは「070」、「080」又は「090」から始まる11桁の番号
# 市外局番、市内局番の境目で区切りが入る可能性がある 03-1234-1234
# 区切りが市内局番を()で囲む可能性がある 03(1234)1234
# フリーダイヤルは0120から始まる4桁3桁3桁

# 固定電話の番号

# 市外局番と市内局番の間にハイフンを入れて表記した場合
# 0X-XXXX-XXXX
# 0XX-XXX-XXXX
# 0XXX-XX-XXXX
# 0XXXX-X-XXXX

# 市外局番と市内局番の間に括弧を入れて表記した場合
# 0(X)XXXX-XXXX
# 0(XX)XXX-XXXX
# 0(XXX)XX-XXXX
# 0(XXXX)X-XXXX

landline_phone_number_with_hyphen_re = re.compile(r'^0(\d-\d{4}|\d{2}-\d{3}|\d{3}-\d{2}|\d{4}-\d)-\d{4}$')
landline_phone_number_with_bracket_re = re.compile(r'^0(\(\d\)\d{4}|\(\d{2}\)\d{3}|\(\d{3}\)\d{2}|\(\d{4}\)\d)-\d{4}$')
landline_phone_number_re = re.compile(r'^0\d{9}$')


def is_valid_landline_phone(phone):
    if landline_phone_number_with_hyphen_re.match(phone):
        return True
    if landline_phone_number_with_bracket_re.match(phone):
        return True
    if landline_phone_number_re.match(phone):
        return True
    return False
