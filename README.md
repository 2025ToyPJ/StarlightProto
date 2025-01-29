# StarlightProto

Search for constellation's info.

# Use
```bash
for version 0.2


In Cli
$ cho-test search_c : 저장된 모든 국가명 검색
$ cho-test search_c --sub1 <'검색어(eng)'> : 일치 및 포함으로 국가명 검색

$ cho-test search_s : 저장된 모든 별자리명 검색
$ cho-test search_s --sub1 <'검색어(eng)'> : 일치 및 포함으로 별자리명 검색

$ cho-test find --sub1 <'국가명(eng)'> --sub2 <'별자리명(eng)'> : 
국가명 및 별자리명을 일치로 검색. 국가명은 대소문자를 구분하지 않음
ex: cho-test find --sub1 'South Korea' --sub2 'Leo'

```

# Dev
```bash
$ source .venv/bin/activate
$ pdm install
$ pdm add -dG eda jupyterlab

```

# EDA
```bash
$ jupyter lab

```
