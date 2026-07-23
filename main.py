from fastapi import FastAPI
from pydantic import BaseModel
import json

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

def calculate_bmi(weight: float, height: float) -> float:
    height_m = height / 100  # cm를 m로 변환
    bmi = weight / (height_m ** 2)
    return round(bmi, 1)  # 소수점 1자리로 반올림

def classify_bmi(bmi: float) -> str:
    if bmi < 18.5:
        return "저체중"
    elif bmi <= 22.9:
        return "정상"
    elif bmi <= 24.9:
        return "과체중"
    else:
        return "비만"
    
def classify_bp(systolic: int, diastolic: int) -> str:
    if systolic >= 140 or diastolic >= 90:
        return "고혈압"
    elif systolic < 120 and diastolic < 80:
        return "정상"
    else:
        return "주의"
    
def classify_sugar(blood_sugar: int) -> str:
    if blood_sugar < 100:
        return "정상"
    elif blood_sugar <= 125:
        return "공복혈당장애"
    else:
        return "당뇨 의심"
    
def generate_warnings(bmi_category: str, bp_category: str, sugar_category: str) -> list:
    warnings = []

    if bmi_category == "비만":
        warnings.append("비만 위험 있습니다. 체중 관리가 필요합니다.")

    if bp_category == "고혈압":
        warnings.append("고혈압 위험이 있습니다. 병원 진료를 권장합니다.")

    if sugar_category == "당뇨 의심":
        warnings.append("당뇨 의심 수치입니다. 병원 진료를 권장합니다.")

    return warnings

def save_records():
    with open("data.json", "w") as f:
        json.dump(records, f)

def load_records():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# 기록을 저장할 서랍 (이제 파일에서 불러옴)
records = load_records()

@app.post("/records")
def create_record(record: RecordIn):
    new_record = record.dict()
    new_record["id"] = len(records) + 1
    
    bmi = calculate_bmi(record.weight, record.height)
    new_record["bmi"] = bmi
    
    bmi_category = classify_bmi(bmi)
    new_record["bmi_category"] = bmi_category
    
    bp_category = classify_bp(record.systolic, record.diastolic)
    new_record["bp_category"] = bp_category
    
    sugar_category = classify_sugar(record.blood_sugar)
    new_record["sugar_category"] = sugar_category
    
    warnings = generate_warnings(bmi_category, bp_category, sugar_category)
    new_record["warnings"] = warnings
    
    records.append(new_record)
    save_records()  # 기록을 파일에 저장
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
            save_records()  # 기록을 파일에 저장
            return {"message": "삭제되었습니다"}
        
    raise HTTPException(status_code=404, detail="기록을 찾을 수 없습니다")

@app.put("/records/{record_id}")
def update_record(record_id: int, record: RecordIn):
    for old_record in records:
        if record_id == old_record["id"]:
            updated_record = record.dict()
            updated_record["id"] = record_id
            
            bmi = calculate_bmi(record.weight, record.height)
            updated_record["bmi"] = bmi
            
            bmi_category = classify_bmi(bmi)
            updated_record["bmi_category"] = bmi_category
            
            bp_category = classify_bp(record.systolic, record.diastolic)
            updated_record["bp_category"] = bp_category
            
            sugar_category = classify_sugar(record.blood_sugar)
            updated_record["sugar_category"] = sugar_category
            
            warnings = generate_warnings(bmi_category, bp_category, sugar_category)
            updated_record["warnings"] = warnings
            
            records.remove(old_record)
            records.append(updated_record)
            save_records()  # 기록을 파일에 저장
            
            return updated_record
    
    raise HTTPException(status_code=404, detail="기록을 찾을 수 없습니다")

@app.get("/search")
def search_records(start: str, end: str):
    result = []
    
    for record in records:
        if start <= record["date"] <= end:
            result.append(record)
    
    return {"count": len(result), "data": result}

@app.get("/stats")
def get_stats():
    if len(records) == 0:
        return {"message": "기록이 없습니다"}
    
    weight_list = []
    for record in records:
        weight_list.append(record["weight"])
    
    avg_weight = sum(weight_list) / len(weight_list)
    
    return {
        "count": len(records),
        "avg_weight": round(avg_weight, 1)
    }