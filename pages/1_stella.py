import streamlit as st
import starlightproto.stella as star
import requests
import json
import pandas as pd
import sys
import io

st.set_page_config(page_title='Stella')

url_s = 'https://cho-stella-bucket.s3.ap-northeast-2.amazonaws.com/starloc.json'
response_s = requests.get(url_s)

if response_s.status_code == 200:
    data = json.loads(response_s.text)

constellations = []
for name, loc in data.items():
    ra = loc.get('ra', None)
    de = loc.get('de', None)
    kor = loc.get('korean', None)
    constellations.append({'name': name, 'ra': ra, 'de': de, 'kor': kor})

df = pd.DataFrame(constellations)


st.title("저장된 별자리 목록")

st.write()
st.dataframe(df[['name', 'kor']])
