from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="마이 헬스 로그 API", version="1.0")

# 건강 기록 데이터 양식(문진표)
class RecordIn(BaseModel) :
    date : str
    weight : float
    height : float
    systolic : int
    diastolic : int
    blood_sugar : int
    steps : int = 0
    sleep_hours : float = 0.0
    memo : str = ""

# 기록을 저장할 서랍 (지금은 그냥 리스트)
records = []

@app.post("/records")
def create_record(record: RecordIn):
    new_record = record.dict()          # 받은 데이터를 딕셔너리로 변환
    new_record["id"] = len(records) + 1  # 간단한 id 부여 (1번, 2번...)
    
    records.append(new_record)
    
    return new_record

@app.get("/records")
def get_records() :
    return {
        "count" : len(records),
        "data" : records
    }

from fastapi import HTTPException  # 맨 위에 이 줄 추가 필요

@app.get("/records/{record_id}")
def get_record(record_id: int):
    for record in records:
        if record_id == record["id"]:
            return record
    
    raise HTTPException(status_code=404, detail="기록을 찾을 수 없습니다")

@app.delete("/records/{record_id}")
def delete_record(record_id: int):
    for record in records:
        if record_id == record["id"]:
            records.remove(record)
            return {"message": "삭제되었습니다"}
    
    raise HTTPException(status_code=404, detail="기록을 찾을 수 없습니다")