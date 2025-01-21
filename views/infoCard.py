from dash import html
import dash

import feffery_antd_components as fac
import feffery_leaflet_components as flc
from feffery_dash_utils.style_utils import style

from dash.dependencies import Input, Output, ALL

import pandas as pd

from server import app
from models.cenc_api import local_api
from callbacks import infocard_c


def get_ceic_id(url: str):
    return url.replace(".html", "").replace("https://news.ceic.ac.cn/", "")


def earthquake_tag_color(data):
    level = float(data)

    if level < 4:
        return "green"
    elif 4 <= level < 5:
        return "yellow"
    elif 5 <= level < 6:
        return "orange"
    else:
        return "red"


def render():
    return html.Div(
        [
            fac.AntdAffix(  # 最新消息固定在顶部
                fac.AntdCard(
                    children=[
                        fac.AntdFlex(
                            [
                                fac.AntdTag(
                                    content=f"{local_api.get_first_cenc_data()['leve']}级",
                                    color=earthquake_tag_color(
                                        local_api.get_first_cenc_data()["leve"]
                                    ),
                                    bordered=True,
                                    style=style(fontSize=16, fontWeight="bold"),
                                ),
                                fac.AntdTag(
                                    content=f"坐标 {local_api.get_first_cenc_data()['jingdu']},{local_api.get_first_cenc_data()['weidu']}",
                                    bordered=True,
                                ),
                                fac.AntdTag(
                                    content=f"深度 {local_api.get_first_cenc_data()['shendu']}km",
                                    bordered=True,
                                ),
                            ],
                            justify="space-between",
                            style=style(width="100%"),
                        )
                    ],
                    title=local_api.get_first_cenc_data()["weizhi"],
                    bordered=True,
                    hoverable=True,
                    style=style(
                        margin=10,
                        boxShadow="0px 0px 8px 5px rgba(0, 0, 0, 0.5)",
                    ),
                    id={
                        "type": "incident-card-grid-click",
                        "index": get_ceic_id(local_api.get_first_cenc_data()["tourl"]),
                    },
                    extraLink={
                        "content": local_api.get_first_cenc_data()["addtime"],
                        "href": local_api.get_first_cenc_data()["tourl"],
                    },
                ),
                # offsetTop=10,
                target="info-card-container",
            ),
            fac.AntdFlex(
                [
                    (
                        fac.AntdCard(
                            children=[
                                fac.AntdFlex(
                                    [
                                        fac.AntdTag(
                                            content=f"{data['leve']}级",
                                            color=earthquake_tag_color(data["leve"]),
                                            bordered=True,
                                            style=style(fontSize=16, fontWeight="bold"),
                                        ),
                                        fac.AntdTag(
                                            content=f"位置 {data['jingdu']},{data['weidu']}",
                                            bordered=True,
                                        ),
                                        fac.AntdTag(
                                            content=f"深度 {data['shendu']}km",
                                            bordered=True,
                                        ),
                                    ],
                                    justify="space-between",
                                    style=style(width="100%"),
                                )
                            ],
                            id={
                                "type": "incident-card-grid-click",
                                "index": get_ceic_id(data["tourl"]),
                            },
                            extraLink={"content": data["addtime"], "href": data["tourl"]},
                            title=data["weizhi"],
                            bordered=True,
                            hoverable=True,
                            size="small",
                            style=style(marginTop=5, marginBottom=5, marginLeft=10, marginRight=10),
                        )
                    )
                    for data in local_api.get_cenc_data_without_first_row()
                ],
                vertical=True,
            ),
        ],
        id="info-card-container",
        style=style(
            height="100%",
            width="calc(100%-10)",
            maxHeight="100%",
            overflowY="auto",
            paddingRight=10,
        ),
    )


# 点击卡片回调函数缩放至对应范围
@app.callback(
    [
        Output("message-container", "children"),
        Output("map-action", "mapActionConfig"),
        Output("click-incident-layer", "children"),
        Output("click-incident-layer-radius", "children"),
    ],
    Input({"type": "incident-card-grid-click", "index": ALL}, "nClicks"),
    prevent_initial_call=True,
)
def card_click_callback(nClicks):
    # 获取当前点击的 incident_id
    incident_id = dash.ctx.triggered_id["index"]
    current_incident = pd.DataFrame(local_api.get_cenc_data())

    # 筛选出包含 incident_id 的行
    filtered_incident = current_incident[current_incident["tourl"].str.contains(incident_id)]

    # 计算坐标范围
    boundradius = 0.5
    minx = float(filtered_incident["jingdu"]) - boundradius
    maxx = float(filtered_incident["jingdu"]) + boundradius
    miny = float(filtered_incident["weidu"]) - boundradius
    maxy = float(filtered_incident["weidu"]) + boundradius

    bound_dict = {
        "type": "fly-to-bounds",
        "bounds": {"minx": minx, "miny": miny, "maxx": maxx, "maxy": maxy},
    }

    return [
        fac.AntdMessage(content=f"ID：{incident_id}"),  # 显示消息
        bound_dict,  # 缩放至对应范围
        flc.LeafletMarker(  # 显示点击的点
            flc.LeafletPopup(
                fac.AntdFlex(
                    [
                        fac.AntdTitle(
                            filtered_incident["weizhi"],
                            level=5,
                            style=style(marginTop=0, width="100%"),
                        ),
                        fac.AntdText(filtered_incident["addtime"], italic=True),
                        fac.AntdText(filtered_incident["leve"]),
                    ],
                    vertical=True,
                ),
                width=200,
            ),
            position={"lng": filtered_incident["jingdu"], "lat": filtered_incident["weidu"]},
        ),
        flc.LeafletCircle(  # 显示点击的点的半径
            center={
                "lng": filtered_incident["jingdu"],
                "lat": filtered_incident["weidu"],
            },
            pathOptions={
                "color": "black",
                "weight": 3,
                "dashArray": "5, 2, 5",
                "fillOpacity": 0.2,
                "fillColor": "red",
            },
            radius=float(filtered_incident["leve"]) ** 2 * 1000,
        ),
    ]
