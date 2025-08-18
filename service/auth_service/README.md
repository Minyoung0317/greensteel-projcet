# Auth Service - Layered Architecture

## Migration Notes

### 🚀 레이어드 아키텍처 리팩터링 완료 (v3.0.0)

**변경 일자**: 2025-08-18  
**이전 버전**: v2.0.0 (Stream Architecture)  
**새로운 버전**: v3.0.0 (Layered Architecture)

#### 📁 새로운 폴더 구조

```
app/
├── www/                    # 프레젠테이션 계층
│   ├── deps.py            # 의존성 주입
│   ├── errors.py          # 에러 핸들링
│   ├── responses.py       # 표준 응답 모델
│   └── __init__.py
├── domain/                 # 도메인 계층
│   ├── entities/          # ORM 모델
│   │   ├── user.py
│   │   ├── company.py
│   │   └── stream.py
│   ├── schemas/           # Pydantic 스키마
│   ├── repositories/      # 데이터 접근 계층
│   ├── services/          # 비즈니스 로직
│   └── __init__.py
├── router/                 # 라우터 계층
│   ├── auth.py            # 인증 엔드포인트
│   ├── stream.py          # 스트림 엔드포인트
│   └── __init__.py
├── common/                 # 공통 모듈
│   ├── settings.py        # 설정 관리
│   ├── security.py        # 보안 유틸
│   ├── permissions.py     # 권한 관리
│   ├── db.py              # 데이터베이스 연결
│   ├── logger.py          # 로깅 설정
│   └── __init__.py
└── main.py                 # 앱 팩토리
```

#### 🔄 주요 변경사항

1. **레이어 분리**: www, domain, router, common 계층으로 명확한 책임 분리
2. **앱 팩토리 패턴**: `create_app()` 함수로 애플리케이션 생성
3. **의존성 주입**: 리포지토리와 서비스 레이어 간 의존성 주입
4. **표준 응답**: 일관된 에러 핸들링과 응답 형식
5. **절대 경로 import**: `app.` 접두사로 명확한 모듈 참조

#### ✅ 호환성 유지

- 모든 기존 엔드포인트 경로 유지
- 응답 스키마 및 상태코드 변경 없음
- 데이터베이스 스키마 변경 없음
- Docker 및 배포 스크립트 동일하게 동작

#### 🚀 부트스트랩

```bash
# 의존성 설치
pip install -r requirements.txt

# 로컬 실행
python main.py

# 또는 uvicorn으로 실행
uvicorn main:app --host 0.0.0.0 --port 8081 --reload
```

---

# 기존 README 내용

## About

greensteel.vercel.app
