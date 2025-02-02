# StarlightProto

Search for constellation's info.

# Use
```bash
for version 0.5


In Cli
$ cho-test search_c : 저장된 모든 국가명 검색
$ cho-test search_c --sub1 <'검색어(eng)'> : 일치 및 포함으로 국가명 검색

$ cho-test search_s : 저장된 모든 별자리명 검색
$ cho-test search_s --sub1 <'검색어(eng)'> : 일치 및 포함으로 별자리명 검색

$ cho-test find --sub1 <'국가명(eng)'> --sub2 <'별자리명(eng)'> : 
국가명 및 별자리명을 일치로 검색. 국가명은 대소문자를 구분하지 않음
ex: cho-test find --sub1 'South Korea' --sub2 'Leo'

In Python
$ pip install StarlightProto
>> import starlightproto.stella as ex
>> ex.select_act('your act', 'sub1', 'sub2')

example : ex.select_act('find', 'south korea', 'Leo')
          ex.select_act('search_c', 'korea')

```

# Dev
```bash
$ source .venv/bin/activate
$ pdm install
$ pdm add -dG eda jupyterlab

```

# Used tool
```bash

- GeoCoder : 국가명에 따른 위도, 경도, 시간 데이터를 반환 받기 위한 API
- Restcountries : 국가명 리스트를 받기 위한 API
- Amazon S3 : 별자리 위치 데이터 파일을 업로드. IAM을 이용한 권한 및 역할 설정 미숙으로 public 스토리지로 설정

```


# EDA
```bash
$ jupyter lab

```
