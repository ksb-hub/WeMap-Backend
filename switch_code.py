import pyproj

def utmk_to_wgs84(utmk_x, utmk_y):
    transformer = pyproj.Transformer.from_crs("epsg:5178", "epsg:4326")
    lat, lon = transformer.transform(utmk_x, utmk_y)
    return (lat, lon)


def response_XY(XY_dict):
    X_list = XY_dict['X_list']
    Y_list = XY_dict['Y_list']

    length = len(X_list)

    XY_geo = []
    for X, Y in zip(X_list, Y_list):
        XY_geo.append(utmk_to_wgs84(X, Y))

    return XY_geo
    # lat, lon = utmk_to_wgs84(utmk_x, utmk_y)

# 사용 예시
# utmk_x = 961114.519726
# utmk_y = 1942887.59712

