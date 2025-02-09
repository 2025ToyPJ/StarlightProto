import streamlit as st
import starlightproto.stella as star
import requests
import json
import pandas as pd
import sys
import io

st.set_page_config(page_title='Search')

def capture_print_output(func, *args, **kwargs):
    buffer = io.StringIO()
    sys.stdout = buffer  # 표준 출력 변경
    func(*args, **kwargs)  # 함수 실행 (print() 내용이 buffer에 저장됨)
    sys.stdout = sys.__stdout__  # 원래 stdout으로 복구
    return buffer.getvalue().strip()


url = "https://restcountries.com/v3.1/all"
response = requests.get(url)
c_data = response.json()

country_list = sorted([country['name']['common'] for country in c_data])



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

stella_list = sorted(list(df['name']))

# 국가선택
countries = st.selectbox("관측국가 선택", country_list)

st.write("")
# 별자리선택
stella = st.selectbox("별자리 선택", stella_list)

search_button = st.button("Find")

st.divider()

if search_button:
    if countries and stella:
        output = capture_print_output(star.select_act, "find", countries, stella)
        st.write(output)
