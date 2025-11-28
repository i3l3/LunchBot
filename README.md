# LunchBot
나이스 API를 통해 학교 급식 정보를 불러와 인스타그램에 게시합니다.

## `.env` 파일 작성법
> `API_KEY`
나이스 급식 API 키입니다. 나이스 API 포털에서 얻을 수 있습니다.

> `OFCDC_CODE`
교육청 코드입니다. 나이스 API 포털에서 얻을 수 있습니다.

> `SCHOOL_CODE`
학교 코드입니다. 나이스 API 포털에서 얻을 수 있습니다.

> `INSTAGRAM_USERNAME` & `INSTAGRAM_PASSWORD`
게시물을 업로드할 계정의 아이디와 비밀번호입니다.

> `INSTAGRAM_AUTHOR`
게시물에 업로드될 때 추가될 사용자입니다.

## TODO
- [x] ~~로깅 기능~~
- [x] ~~새 디바이스로 로그인되었다는 알림 없애기 (쿠키?)~~
- [ ] 인스타그램 봇 감지 우회
- [ ] 비동기 전환