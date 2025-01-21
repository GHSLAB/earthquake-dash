import feffery_antd_components as fac
import feffery_leaflet_components as flc
from feffery_dash_utils.style_utils import style


from server import app
from config import MapConfig, AppConfig


from models.cenc_api import local_api

from callbacks import maps_c


def render():
    return flc.LeafletMap(
        [
            flc.LeafletMapListener(id="map-listener"),
            flc.LeafletMapAction(id="map-action"),
            flc.LeafletTileLayer(
                url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                opacity=0.5,
                id="tile-layer",
            ),
            flc.LeafletLayerGroup(id="click-incident-layer", zIndex=999),  # 点击事件
            flc.LeafletLayerGroup(id="click-incident-layer-radius", zIndex=99),
            flc.LeafletLayerGroup(  # circle marker
                [
                    flc.LeafletCircle(
                        # flc.LeafletTooltip(
                        #     f"{pnt['addtime']} {pnt['leve']}级",
                        #     permanent=False,
                        #     direction="right",
                        #     className="marker-group2",
                        # ),
                        center={
                            "lng": pnt["jingdu"],
                            "lat": pnt["weidu"],
                            "weight": float(pnt["leve"]) * 1000000,
                        },
                        pathOptions={
                            "color": "black",
                            "weight": 0,
                            # "dashArray": "5, 2, 5",
                            "fillOpacity": 0.01,
                            "fillColor": "blue",
                        },
                        radius=float(pnt["leve"]) ** 2 * 1000,
                    )
                    for pnt in local_api.get_cenc_data_dict()
                ],
                hidden=True,
                id={"type": "layer-group", "index": "circle marker"},
            ),
        ],
        minZoom=3,
        center=MapConfig.deafult_center,
        zoom=MapConfig.deafult_zoom,
        style=style(height="100%", width="100%", borderRadius="20px"),
    )
