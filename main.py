from fastapi import FastAPI, Path, HTTPException, Query, Body
import json
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from fastapi.responses import JSONResponse

app = FastAPI()
class Student(BaseModel):
    id: Annotated[str, Field(..., description="Student id of the student",example="S001")]
    name: Annotated[str, Field(..., description="Student name")]
    age: Annotated[int, Field(..., gt=0,lt=100, description="age of the student",example="12")]
    student_class: Annotated[int, Field(..., gt=0,lt=13)]
    roll: Annotated[int, Field(..., gt=0,lt=101)]
    Math_marks: Annotated[int, Field(..., gt=0,lt=101)]
    English_marks: Annotated[int, Field(..., gt=0,lt=101)]
    Science_marks: Annotated[int, Field(..., gt=0,lt=101)]
    phone: Annotated[str, Field(...,example="01700000000")]

class StudentUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None)]
    student_class: Annotated[Optional[int], Field(default=None)]
    roll: Annotated[Optional[int], Field(default=None)]
    Math_marks: Annotated[Optional[int], Field(default=None)]
    English_marks: Annotated[Optional[int], Field(default=None)]
    Science_marks: Annotated[Optional[int], Field(default=None)]
    phone: Annotated[Optional[str], Field(default=None)]

def load_data():
    with open('students.json','r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('students.json','w') as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return "Student Management System API"

@app.get("/about")
def about():
    return "A fully functional API to manage our student records"

@app.get("/view")
def view_students():
    data = load_data()
    return data


@app.get("/view/{student_id}")
def view_student_by_id(student_id: str = Path(..., description="Student id of the student",example="S001")):
    data = load_data()
    
    if student_id in data:
        return data[student_id]
    else:
        raise HTTPException(status_code=404, detail='Student not found')
    

@app.get("/sort")
def view_sorted_students(sorted_by: str = Query(..., description="Sort on the basis of class, age, roll, marks"), order: str = Query('asc', description="choose order: asc or desc")):
    
    valid_fields = ["age", "student_class", "roll", "Math_marks", "English_marks", "Science_marks",]

    if sorted_by not in valid_fields:
        raise HTTPException(status_code=404, detail=f'Invalid field, select from {valid_fields}')
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=404, detail="Choose between asc or desc")

    data = load_data()

    if order == 'asc':
        sorted_data = list(data.values())
        sorted_data.sort(key= lambda x: x[sorted_by])
        return sorted_data
    
    else:
        sorted_data = list(data.values())
        sorted_data.sort(key= lambda x: x[sorted_by], reverse=True)
        return sorted_data

@app.post("/create")
def create_student(student: Student):

    data = load_data()

    if student.id in data:
        raise HTTPException(status_code=400, detail="Student id already exists")

    data[student.id] = student.model_dump(exclude=["id"])

    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Student created successfully'})

@app.put("/edit/{student_id}")
def update_student(student_id: str, student: StudentUpdate):

    data = load_data()

    if student_id not in data:
        raise HTTPException(status_code=404, detail="Student not found")

    data[student_id].update(student.model_dump(exclude_unset=True))

    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Student updated successfully'})
@app.delete("/delete/{student_id}")
def delete_student(student_id: str):

    data = load_data()

    if student_id not in data:
        raise HTTPException(status_code=404, detail="Student not found")

    del data[student_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Student deleted successfully'})