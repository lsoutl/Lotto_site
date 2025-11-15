# Lotto Site (Django + Docker)

## 실행
```bash
docker compose up -d --build
# 접속: http://localhost:8000
# 로또 웹 사이트 구축 보고서

## 1. 개요
- 목적: Django와 Docker로 로또 구매/추첨/정산/조회 기능 구현
- 범위: Dev 서버(runserver), SQLite, 단위/통합 테스트

## 2. 아키텍처 개요
- Django(MVT), 앱: lotto
- DB: SQLite (dev)
- 컨테이너: server (python:3.13-slim 기반)

## 3. 개발 과정
- 모델 설계( Draw, Ticket )
- 구매 플로우(quick_pick, ManualPurchaseForm, views/urls/templates)
- 추첨/정산 커맨드(draw_lotto, settle_lotto)
- 결과 페이지(draw/<n>/result)
- 관리자 액션(추첨/정산)
- 테스트(services/commands/views) 통과

## 4. 실행·테스트 방법
(README 발췌)

## 5. 주요 코드/규칙
- 번호 저장: JSONField(list[int]) – 단순성과 학습 목적
- 정산 규칙: 6=1등, 5=2등, 4=3등, 3=4등, 그 외 0등(꽝)

## 6. 한계와 확장
- 보너스 번호 미적용 → score() 확장 가능
- 로그인/권한 개선(LoginRequiredMixin, 회원 가입)
- 정적 자원/배포(whitenoise, collectstatic) – 과제 범위 밖

## 7. 참고 문헌·용어
- Django 공식문서, Docker Docs
- 용어: MVT, JSONField, management command, runserver 등