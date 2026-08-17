from fastapi import FastAPI,Path,HTTPException
import json

app=FastAPI()

def load_data():
    with open('students.json','r') as f:
        data=json.load(f)
    
    return data

@app.get("/")
def hello():
    return "Student management system API"
@app.get("/about")
def about():
    return "A fully functional API to manage our student records"
@app.get("/view/{student_id}")
def view_students(student_id : str=Path(...,description="Student id of the student",example="S001")):
    data=load_data()
    
    if student_id in data:
        return data[student_id]
    else:
        raise HTTPException(status_code=404,detail='Student not found')