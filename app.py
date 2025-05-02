import streamlit as st
import pandas as pd
import re
from datetime import datetime

@st.cache_data
def load_data():
    return pd.read_csv("date_store_final_safe.csv", encoding="cp932")

def extract_date(text):
    match = re.search(r"(20[2-6]\d?)年[^0-9]*(\d{1,2})月[^0-9]*(\d{1,2})日", text)
    if match:
        try:
            return datetime.strptime(f"{match.group(1)}/{int(match.group(2)):02d}/{int(match.group(3)):02d}", "%Y/%m/%d").strftime("%Y/%m/%d")
        except:
            return ""
    return ""

store_options = ["セブンイレブン", "ファミリーマート", "ローソン", "タクシー代", "チャージ代", "空欄"]

def main():
    st.title("領収書AI補助分類ツール")
    df = load_data()

    for i, row in df.iterrows():
        st.markdown(f"### No. {row['No']}")
        st.text_area("OCR元データ", row['元データ'], height=200)

        default_store = row['店名'] if row['店名'] in store_options else "空欄"
        store = st.selectbox("店名を選択してください", store_options, index=store_options.index(default_store), key=f"select_{i}")

        date_val = extract_date(row['元データ'])
        st.markdown(f"**抽出された日付**: `{date_val}`")
        st.markdown("---")

        df.at[i, '店名'] = store
        df.at[i, '日付'] = date_val

    if st.button("CSVをエクスポート"):
        df.to_csv("classified_receipts_final.csv", index=False, encoding="cp932")
        st.success("CSVファイルを出力しました。")

if __name__ == "__main__":
    main()
