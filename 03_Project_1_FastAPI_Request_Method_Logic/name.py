# to run this type uvicorn name:app --reload
# CRUD operations

from fastapi import FastAPI

app = FastAPI()

students = [
    {"Title": "Roll Number 29", "Name": "Muzzamil Khalid", "Address": "Model Colony"},
    {"Title": "Roll Number 43", "Name": "Sami LQBT", "Address": "Flats"},
    {"Title": "Roll Number 09", "Name": "Hamza8", "Address": "Crossing Korangi"},
    {"Title": "Roll Number 32", "Name": "Moiz Green", "Address": "Sadar"},
    {"Title": "Roll Number 11", "Name": "Rayyan Kamleen", "Address": "Drig Road"},
    {"Title": "Roll Number 17", "Name": "Wajahat Mansoori", "Address": "Model Colony"},
]

@app.get("/names")
async def read_student():
    return students
