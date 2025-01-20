# earthquake-dash
Earthquake Information Visualization Platform




## api
https://wolfx.jp/apidoc


#### 中国地震台网 地震信息 JSON API

- 描述: 获取中国地震台网发布的最新地震信息，共50条
- HTTP GET API地址:https://api.wolfx.jp/cenc_eqlist.json

- WebSocket API地址:wss://ws-api.wolfx.jp/cenc_eqlist

| type      | cenc_eqlist                           |
| --------- | ------------------------------------- |
| No(1~50)  | 地震信息条目数，发布时间顺序          |
| type      | 信息类型，分为"automatic"和"reviewed" |
| time      | 发震时间                              |
| location  | 震源地                                |
| magnitude | 震级                                  |
| depth     | 震源深度                              |
| latitude  | 震源地纬度                            |
| longitude | 震源地经度                            |
| intensity | 最大烈度                              |
| md5       | 地震信息更新校验码                    |