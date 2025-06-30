from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="블로그 API",
    description="간단한 블로그 API 예제입니다.",
    version="0.0.1",
)

# Pydantic 모델 정의
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# 임시 데이터베이스 (실제 DB는 다음 강의에서 연동)
fake_items_db = {}
next_item_id = 1

@app.get("/")
async def read_root():
    """
    루트 경로에 대한 간단한 메시지를 반환합니다.
    """
    return {"message": "안녕하세요! FastAPI 블로그 API입니다."}

@app.get("/items/{item_id}", summary="특정 아이템 조회")
async def read_item(item_id: int):
    """
    경로 매개변수를 사용하여 특정 아이템을 조회합니다.
    - **item_id**: 조회할 아이템의 고유 ID
    """
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다.")
    return fake_items_db[item_id]

@app.get("/items/", summary="아이템 목록 조회 (쿼리 매개변수)")
async def read_items(skip: int = 0, limit: int = 10):
    """
    쿼리 매개변수를 사용하여 아이템 목록을 페이지네이션하여 조회합니다.
    - **skip**: 건너뛸 아이템의 수
    - **limit**: 반환할 아이템의 최대 수
    """
    return list(fake_items_db.values())[skip : skip + limit]

@app.post("/items/", summary="새로운 아이템 생성")
async def create_item(item: Item):
    """
    새로운 아이템을 생성합니다.
    - **item**: 생성할 아이템의 정보 (이름, 설명, 가격, 세금)
    """
    global next_item_id
    new_item = item.model_dump() # Pydantic v2 이후 .dict() 대신 .model_dump() 사용
    new_item["id"] = next_item_id
    fake_items_db[next_item_id] = new_item
    next_item_id += 1
    return {"message": "아이템이 성공적으로 생성되었습니다.", "item": new_item}

# FastAPI 자동 문서화 확인:
# 개발 서버 실행 후 브라우저에서 http://127.0.0.1:8000/docs 또는 http://127.0.0.1:8000/redoc 접속