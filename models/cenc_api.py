import json
import requests
import pandas as pd
import toml

# 读取 TOML 文件
with open("./api.toml", "r") as toml_file:
    api = toml.load(toml_file)


class CencAPI:

    id = api["apihz"]["id"]
    key = api["apihz"]["key"]
    # API URL
    url = f"https://cn.apihz.cn/api/tianqi/dizhen.php?id={id}&key={key}"

    response = requests.get(url)
    data = response.json()

    @classmethod
    def get_cenc_time(cls):
        return cls.data["time2"]

    @classmethod
    def get_cenc_data(cls):
        return cls.data["data"]

    @classmethod
    def get_cenc_data_df(cls):
        return pd.DataFrame(cls.data["data"])


class local_api:

    with open("./data/cenc.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    @classmethod
    def get_cenc_time(cls):
        return cls.data["time2"]

    @classmethod
    def get_cenc_data(cls):
        return cls.data["data"]

    @classmethod
    def get_cenc_data_dict(cls):
        return pd.DataFrame(cls.data["data"]).to_dict("records")

    @classmethod
    def get_cenc_normal_data_dict(cls):
        return pd.DataFrame(cls.data["data"]).to_dict("records")

    @classmethod
    def get_first_cenc_data(cls):
        if cls.data["data"]:
            return cls.data["data"][0]
        else:
            return None

    @classmethod
    def get_cenc_data_without_first_row(cls):
        return pd.DataFrame(cls.data["data"]).iloc[1:].to_dict("records")
