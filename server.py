import dash

from config import AppConfig

app = dash.Dash(
    __name__,
    compress=True,
    suppress_callback_exceptions=True,
)

app.title = AppConfig.app_title
