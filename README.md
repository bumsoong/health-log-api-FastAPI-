# 마이 헬스 로그 API

매일의 건강 수치(몸무게, 키, 혈압, 혈당)를 기록하면 서버가 BMI를 자동으로 계산하고, 혈압·혈당 상태를 분류하며, 위험 수치에 대한 경고를 제공하는 개인용 건강 관리 API입니다. 누적된 기록을 기간별로 검색하고 평균 통계도 조회할 수 있습니다.

## 기능 목록

| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/records` | 건강 기록 추가 (BMI 계산, 혈압/혈당 분류, 경고 메시지 자동 생성) |
| GET | `/records` | 전체 기록 조회 (개수 포함) |
| GET | `/records/{record_id}` | 기록 단건 조회 (없으면 404) |
| PUT | `/records/{record_id}` | 기록 수정 (계산 항목 재산출) |
| DELETE | `/records/{record_id}` | 기록 삭제 |
| GET | `/search?start=&end=` | 날짜 범위로 기록 검색 |
| GET | `/stats` | 평균 체중 등 통계 조회 |

### 자동 계산 항목

기록을 추가하거나 수정하면 아래 항목이 자동으로 함께 저장됩니다.

- `bmi`, `bmi_category` (저체중 / 정상 / 과체중 / 비만)
- `bp_category` (정상 / 주의 / 고혈압)
- `sugar_category` (정상 / 공복혈당장애 / 당뇨 의심)
- `warnings` (비만·고혈압·당뇨 의심 시 경고 메시지 목록)

## 실행 방법

### 로컬 실행

```bash
# 가상환경 생성 및 활성화
python -m venv venv
venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload
```

브라우저에서 `http://127.0.0.1:8000/docs` 접속하면 API 문서와 테스트 화면을 확인할 수 있습니다.

### Docker 실행

```bash
# 이미지 빌드
docker build -t health-log-api .

# 컨테이너 실행
docker run -d -p 8000:8000 health-log-api
```

브라우저에서 `http://127.0.0.1:8000/docs` 접속하면 동일하게 확인할 수 있습니다.

## 기술 스택

- **Language**: Python 3.11
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Validation**: Pydantic
- **Container**: Docker
- **Data Storage**: JSON 파일 (`data.json`)

## 데이터 저장 방식

기록은 서버 메모리가 아닌 `data.json` 파일에 저장되어, 서버를 재시작해도 기존 기록이 유지됩니다. 서버 시작 시 `data.json`이 없으면 빈 상태로 자동 초기화됩니다.

## 프로젝트 구조

```
health-log-api/
├── main.py              # API 코드
├── requirements.txt      # 필요 패키지 목록
├── Dockerfile             # Docker 이미지 빌드 설계도
├── .dockerignore          # Docker 빌드 제외 목록
├── .gitignore              # Git 제외 목록 (venv, data.json 등)
└── README.md
```

## 참고 사항

- 본 프로젝트의 BMI·혈압·혈당 분류 기준은 학습 목적으로 단순화된 값이며, 실제 의학적 진단으로 사용할 수 없습니다.
- 이 프로젝트는 FastAPI 학습용 미니 프로젝트로 제작되었습니다.
