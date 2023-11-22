def is_valid_longitude(longitude):
    try:
        # 経度の値が浮動小数点数に変換可能か確認
        lon = float(longitude)
        # 経度の範囲が -180 から 180 に収まっているか確認
        if -180.0 <= lon <= 180.0:
            return True
        else:
            return False
    except ValueError:
        return False

def is_valid_latitude(latitude):
    try:
        # 緯度の値が浮動小数点数に変換可能か確認
        lat = float(latitude)
        # 緯度の範囲が -90 から 90 に収まっているか確認
        if -90.0 <= lat <= 90.0:
            return True
        else:
            return False
    except ValueError:
        return False