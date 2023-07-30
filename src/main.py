import io
from base64 import b64encode

import pandas as pd
import plotly.express as px
import streamlit as st


def _get_html_bytes(fig):
    buffer = io.StringIO()
    fig.write_html(buffer)

    return buffer.getvalue()


def main():
    st.set_page_config(layout="wide")
    st.header("2021年度北海道ふるさと納税の寄付１件あたり返礼品送付費用")

    # 自治体の座標
    df_government = pd.read_csv("data/r0401puboffice_utf8.csv", sep="\t")
    # 送料
    df_postage = pd.read_csv("data/2021年度北海道ふるさと納税の寄付１件あたり返礼品送付費用.csv")

    st.write("送料")
    st.write(df_postage)

    df_postage = pd.merge(df_postage, df_government, how="left", left_on="市町村", right_on="name")

    # 地図に表示
    fig = px.scatter_mapbox(
        # データフレームおよび緯度・経度の設定
        data_frame=df_postage,
        lat="lat",
        lon="long",
        size="1件あたり送付費用",
        color="1件あたり送付費用",
        # カーソルを当てるとホバーする情報を与えます
        hover_data=["順位", "市町村", "1件あたり送付費用"],
        size_max=15,
        zoom=6,
        height=700,
        width=1200,
        color_continuous_scale=px.colors.sequential.Jet,
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    # グラフを描画
    st.plotly_chart(fig, use_container_width=True, theme=None)

    html_bytes = _get_html_bytes(fig)
    st.download_button(
        "Download",
        data=html_bytes,
        file_name="export.html",
        mime="html",
    )


if __name__ == "__main__":
    main()
