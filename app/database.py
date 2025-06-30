from sqlmodel import create_engine, Session
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# 환경 변수에서 데이터베이스 URL 가져오기
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL 환경 변수가 설정되지 않았습니다.")

# 데이터베이스 엔진 생성
# echo=True는 SQL 쿼리를 콘솔에 출력하여 디버깅에 도움을 줍니다.
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """
    SQLModel에 정의된 모든 테이블을 데이터베이스에 생성합니다.
    """
    from app.models import SQLModel # models.py에서 SQLModel을 임포트하여 metadata에 접근
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    FastAPI 의존성 주입을 위한 데이터베이스 세션 제너레이터.
    요청이 들어올 때마다 새 세션을 생성하고, 응답 후 닫습니다.
    """
    with Session(engine) as session:
        yield session