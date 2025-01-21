import dash

from dash.dependencies import Input, Output, ALL

from server import app

import json


@app.callback(
    Output({"type": "layer-group", "index": "circle marker"}, "hidden"),
    [
        Input("map-listener", "_bounds"),
        Input("map-listener", "_zoom"),
    ],
    # prevent_initial_call=True,
)
def map_listener(map_bounds, zoom_level):
    print(map_bounds)
    if zoom_level > 7:
        return False
    else:
        return True
    # return _bounds


# # 监听地理定位
# @app.callback(Output("geolocation-output", "children"), Input("geolocation", "geoLocationInfo"))
# def geolocation_demo(geoLocationInfo):
#     return json.dumps(geoLocationInfo, ensure_ascii=False, indent=4)
