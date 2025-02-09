# 필요 패키지 import
from astropy.coordinates import EarthLocation, AltAz, SkyCoord
from astropy.time import Time
import numpy as np
import typer
import json
import pandas as pd
from astropy import units as u
from opencage.geocoder import OpenCageGeocode
import requests
from datetime import datetime
import pytz


#opencage api key
API_KEY = "5084bf0c7cba459d9b8fef23da253bd7"
geocoder = OpenCageGeocode(API_KEY)


#국가명 가져오기
url = "https://restcountries.com/v3.1/all"
response = requests.get(url)
c_data = response.json()

countries = [country['name']['common'] for country in c_data]

# S3에서 별자리 정보 json 가져오기
# IAM 권한 및 역할 설정 미숙으로 퍼블릭 S3로 운영
url_s = 'https://cho-stella-bucket.s3.ap-northeast-2.amazonaws.com/starloc.json'
response_s = requests.get(url_s)

if response_s.status_code == 200:
    data = json.loads(response_s.text)

#기존 로컬 경로 기반 코드
#JSON 파일 경로
#file_path = "starloc.json"
#with open(file_path, 'r') as file:
   # data = json.load(file)

#별자리 정보 추출
constellations = []
for name, loc in data.items():
    ra = loc.get('ra', None)
    de = loc.get('de', None)
    kor = loc.get('korean', None)
    constellations.append({'name': name, 'ra': ra, 'de': de, 'kor': kor})

df = pd.DataFrame(constellations)

#test 데이터
#countries = ["korea", "korea2"]
#constellations = ["Leo", "Leo2"]

# 첫 입력에 따른 행동 구분
def select_act(keyword: str, sub1: str=None, sub2: str=None):
    if keyword == "search_c":
        search_c_act(sub1)
    elif keyword == "search_s":
        search_s_act(sub1)
    elif keyword == "find":
        find_act(sub1, sub2)

# 저장된 국가 검색 함수
def search_c_act(sub1: str=None):
    if sub1:
        result = [country for country in countries if sub1.lower() in country.lower()]
        if result:
            print(f"{sub1}에 대한 검색 결과 : {result}")
            return result
        else: 
            print("검색 결과가 없습니다")
            return None
    else:
        #print(f"저장된 국가 리스트 : {countries}")
        return print(f"저장된 국가 리스트 : \n{countries}")

# 저장된 별자리 검색 함수
def search_s_act(sub1: str=None):
    if sub1:
        result = [stella for stella in df['name'] if sub1.lower() in stella.lower()]
        if result:
            print(f"{sub1}에 대한 검색 결과 : {result}")
        else: print("검색 결과가 없습니다")
    else:
        print(f"저장된 별자리 리스트 : \n{df[['name', 'kor']]}")

def find_act(sub1_location: str, sub2_constellation: str):
    
    # 사용자 정보 입력
    country = geocoder.geocode(sub1_location)
    annotations = country[0]['annotations']['timezone']['name']

    latitude = country[0]['geometry']['lat']
    longitude = country[0]['geometry']['lng']
    altitude = 0 #고도는 0으로 통일
    ra = str(df[df['name']==sub2_constellation]['ra'].iloc[0])
    de = str(df[df['name']==sub2_constellation]['de'].iloc[0])

    # 현지 시간 추출
    local_time = datetime.now()
    local_tz = pytz.timezone(annotations)
    localized_time = local_tz.localize(local_time)
    utc_time = localized_time.astimezone(pytz.UTC)
    utc_time_str = utc_time.strftime("%Y-%m-%d %H:%M:%S")

    date_time = Time(utc_time_str)

    #관측 위치 설정
    location = EarthLocation(lat=latitude, lon=longitude, height=altitude)

    #시각에 따른 관측 천구 생성
    observation_time = Time(date_time)
    altaz_frame = AltAz(obstime=observation_time, location=location) #관측 천구

    #별자리 위치 정보 전달
    constellation = SkyCoord(ra=ra, dec=de, frame="icrs", unit=(u.deg, u.deg))

    #관측 위치에 따른 별자리의 고도와 방위각 계산
    altaz = constellation.transform_to(altaz_frame)
    altitude = altaz.alt.deg #고도
    azimuth = altaz.az.deg #방위각

    #결과 출력
    if not is_observable(latitude, constellation.dec.deg):
        print("현 위치에서 해당 별자리는 관측되지 않습니다")
        return("현 위치에서 해당 별자리는 관측되지 않습니다")
    else:
        if altitude > 0:
            direction = get_direction(azimuth)
            print(f"현재 별자리는 {direction}쪽 하늘에 떠 있습니다. (고도: {altitude:.2f}°, 방위각: {azimuth:.2f}°)v")
            return f"현재 별자리는 {direction}쪽 하늘에 떠 있습니다. (고도: {altitude:.2f}°, 방위각: {azimuth:.2f}°)"
        else :
            delta_time = 0
            while altitude <= 0:
                delta_time += 1
                future_time = observation_time + delta_time / 1440
                altaz_frame_future = AltAz(obstime=future_time, location=location)
                altaz_future = constellation.transform_to(altaz_frame_future)
                altitude = altaz_future.alt.deg

                if delta_time > 1440:
                    print("현 위치에서 해당 별자리는 오늘 관측할 수 없습니다, Err")
                    return("현 위치에서 해당 별자리는 오늘 관측할 수 없습니다, Err")
                    break

            if altitude > 0:
                print(f"해당 별자리는 {delta_time//60}시 {delta_time%60}분 후에 떠오릅니다.")
                return(f"해당 별자리는 {delta_time//60}시 {delta_time%60}분 후에 떠오릅니다.")


#별자리 방위 방향 결정
def get_direction(azimuth):
    if 0 <= azimuth < 45 or 315 <= azimuth <= 360:
        return "북"
    elif 45 <= azimuth < 135:
        return "동"
    elif 135 <= azimuth < 225:
        return "남"
    elif 225 <= azimuth < 315:
        return "서"


#별자리 관측 가능 여부 확인
def is_observable(latitude, dec):
    #북반구
    if latitude >= 0 :
        max_dec = 90
        min_dec = latitude - 90
    #남반구
    else :
        max_dec = latitude + 90
        min_dec = -90
    return min_dec <= dec <= max_dec


def entry_point():
    typer.run(select_act)
