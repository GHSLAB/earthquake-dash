from dash import html
import feffery_antd_components as fac
import feffery_utils_components as fuc
import feffery_leaflet_components as flc
import feffery_antd_charts as fact

from feffery_dash_utils.style_utils import style

from dash.dependencies import Input, Output

# 配置
from server import app
from config import AppConfig, MapConfig

import random

# 组件
from views import infoCard, maps

from models.cenc_api import local_api

from callbacks import maps_c

## 主要布局
app.layout = html.Div(
    [
        # fuc.FefferyGeolocation(id="geolocation"),
        # html.Pre(id="geolocation-output"),
        html.Div(id="message-container"),
        fac.AntdRow(
            [
                fac.AntdCol(
                    [
                        fac.AntdRow([maps.render()], style=style(height="80%")),
                        fac.AntdRow(
                            fact.AntdLine(
                                data=[
                                    {
                                        "date": f"{i['addtime']}",
                                        "level": float(i["leve"]),
                                    }
                                    for i in reversed(local_api.get_cenc_data_dict())
                                ],
                                xField="date",
                                yField="level",
                                xAxis={"label": None},
                                yAxis={
                                    "min": 2,
                                    "max": 8,
                                },
                                smooth=True,
                                slider={},
                                # tooltip={"field": "weizhi"},
                                # width=1500,
                                # height=200,
                                style=style(
                                    position="absolute",
                                    width="100%",
                                    height="90%",
                                    left=0,
                                    bottom=0,
                                    marginRight="10px",
                                    # margin="10 auto",
                                ),
                            ),
                            style=style(width="100%", height="20%", position="relative", bottom=0),
                        ),
                    ],
                    span=18,
                    style=style(padding="10px", height="100%"),
                ),
                fac.AntdCol(
                    [infoCard.render()],
                    span=6,
                    # style=style(paddingTop="10px", paddingBottom="10px", paddingRight="20px"),
                ),
            ],
            style=style(height="100%"),
        ),
    ],
    style=style(width="100%", height="100vh", backgroundColor="#F2F2F2"),
)


if __name__ == "__main__":
    app.run(port=AppConfig.debug_port, debug=True)  # 调试模式
    # app.run(host="0.0.0.0", debug=False) # 生产模式
