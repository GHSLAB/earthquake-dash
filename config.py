class AppConfig:
    # 应用标签页title
    app_title: str = "地震速报可视化"
    # 调试模式端口
    debug_port: int = 8000


class MapConfig:
    # 默认中心
    deafult_center: tuple = [26, 113]
    deafult_zoom: int = 5
