# 인스타그램 태그 수집기
인스타그램 태그 페이지의 최신 글의 태그를 수집합니다. Google App Engine에서 동작하며 매 1분마다 랜덤함 샘플 데이터를 수집하도록 구현되었습니다.
https://www.instagram.com/robots.txt 에 명시되어 있는 규칙을 준수합니다.

## 설치
1. app.yaml 파일에서 application 수정

  ```
  application: <your app engine id>
  ```
2. library 설치

  ```
  $ pip install -t lib -r requirements.txt
  ```

## 동작
Google App Engine 으로 프로젝트 실행하면 1분마다 /crawl 작업을 수행합니다.
http://project-domain/crawl 페이지를 접속하면 직접 실행할 수 있습니다.

1. 처음에는 지정된 기본 태그(먹스타그램, 일상 등등)의 페이지에서 최신 글의 태그를 수집합니다.
2. 수집된 태그 중에 랜덤하게 태그를 뽑아서 다음 수집에 사용합니다.


## 수집된 태그 다운로드
아래 app-id 부분에 적절한 id를 넣어 실행하세요.
```
$ appcfg.py download_data --url=https://<app-id>.appspot.com/_ah/remote_api \
                        --kind=TagText_Sampling \
                        --config_file=bulkloader.yaml \
                        --filename=tags.txt \
                        --batch_size=50 --num_threads=12
$ ls tags.txt
```
