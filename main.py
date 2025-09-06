from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services import CRUDServices, GeneralServices
from repositories import CustomerRepository, ShowRepository, AvanueRepository
import schemas

app = FastAPI()

@app.get("/", response_model=list[schemas.CustomerReadList])
def get_customers(db: Session = Depends(get_db)):
    rows = CustomerRepository(db).get_all()
    return rows

@app.get("/customer/{customer_id}", response_model=schemas.Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    rows = CustomerRepository(db).get(customer_id)
    return rows

@app.get("/shows/", response_model=list[schemas.ShowReadList])
def get_shows(db: Session = Depends(get_db)):
    rows = ShowRepository(db).get_all()
    return rows

@app.get("/show/{show_id}", response_model=schemas.Show)
def get_show(show_id: int, db: Session = Depends(get_db)):
    row = ShowRepository(db).get(show_id)
    return row

@app.get("/avanues/", response_model=list[schemas.AvanueReadList])
def get_avanues(db: Session = Depends(get_db)):
    row = AvanueRepository(db).get_all()
    return row

@app.get("/avanue/{avanue_id}", response_model=schemas.Avanue)
def get_avanue(avanue_id: int, db: Session = Depends(get_db)):
    row = AvanueRepository(db).get(avanue_id)
    return row

@app.post("/add/customer/", response_model=schemas.Customer)
def add_customer(customer: schemas.CustomerAdd, db: Session = Depends(get_db)):
    try:
        result = CRUDServices.CustomerService(db).enroll_customer(customer)
        return result
    except Exception as e:
        raise HTTPException(404, f"{e}")

@app.post("/add/show/", response_model=schemas.Show)
def add_show(show: schemas.ShowAdd, db: Session = Depends(get_db)):
    try:
        result = CRUDServices.ShowService(db).enroll_show(show)
        return result
    except Exception as e:
        raise HTTPException(404, f"{e}")

@app.post("/add/avanue/", response_model=schemas.Avanue)
def add_avanue(avanue: schemas.AvanueAdd, db: Session = Depends(get_db)):
    try:
        result = CRUDServices.AvanueService(db).enroll_avanue(avanue)
        return result
    except Exception as e:
        raise HTTPException(404, f"{e}")

@app.post("/general_services/enroll_customer_to_show/", response_model=schemas.Message)
def enroll_customer_to_show(customer_id: int, show_id: int, db: Session = Depends(get_db)):
    try:
        result = GeneralServices(db).enroll_customer_to_show(customer_id, show_id)
        return result
    except Exception as e:
        raise HTTPException(404, f"{e}")

@app.post("/general_services/show_to_avanue/", response_model=schemas.Message)
def enroll_show_to_avanue(show_id: int, avanue_id: int, db: Session = Depends(get_db)):
    try:
        result = GeneralServices(db).enroll_show_to_avanue(show_id, avanue_id)
        return result
    except Exception as e:
        raise HTTPException(404, f"{e}")

@app.patch("/update/customer/{customer_id}", response_model=schemas.Customer)
def update_customer(id: int, customer: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    try:
        result = CRUDServices.CustomerService(db).update_customer(id, customer)
        return result
    except Exception as e:
        raise HTTPException(404, f"{e}")

@app.patch("/update/show/{show_id}", response_model=schemas.Show)
def update_show(id: int, show: schemas.ShowUpdate, db: Session = Depends(get_db)):
    try:
        result = CRUDServices.ShowService(db).update_show(id, show)
        return result
    except Exception as e:
        raise HTTPException(404, f"{e}")

@app.patch("/update/avanue/{avanue_id}", response_model=schemas.Avanue)
def update_avanue(id: int, avanue: schemas.AvanueUpdate, db: Session = Depends(get_db)):
    try:
        result = CRUDServices.AvanueService(db).update_avanue(id, avanue)
        return result
    except Exception as e:
        raise HTTPException(404, f"{e}")

@app.delete("/delete/customer/{customer_id}", response_model=schemas.Message)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    try:
        result = CRUDServices.CustomerService(db).delete_customer(customer_id)
        return result
    except Exception as e:
        raise HTTPException(404, f"{e}")
    
@app.delete("/delete/show/{show_id}", response_model=schemas.Message)
def delete_show(show_id: int, db: Session = Depends(get_db)):
    try:
        result = CRUDServices.ShowService(db).delete_show(show_id)
        return result
    except Exception as e:
        raise HTTPException(404, f"{e}")

@app.delete("/delete/avanue/{avanue_id}", response_model=schemas.Message)
def delete_avanue(avanue_id: int, db: Session = Depends(get_db)):
    try:
        result = CRUDServices.AvanueService(db).delete_avanue(avanue_id)
        return result
    except Exception as e:
        raise HTTPException(404, f"{e}")

    
@app.delete("/general_services/remove_customer_from_show/", response_model=schemas.Message)
def delete_customer_from_show(customer_id: int, show_id: int, db: Session = Depends(get_db)):
    try:
        result = GeneralServices(db).remove_customer_from_show(customer_id, show_id)
        return result
    except Exception as e:
        raise HTTPException(404, f"{e}")
    
@app.delete("/general_services/remove_show_from_avanue", response_model=schemas.Message)
def delete_Show_from_avanue(show_id: int, avanue_id: int, db: Session = Depends(get_db)):
    try:
        result = GeneralServices(db).delete_show_from_avanue(show_id, avanue_id)
        return result
    except Exception as e:
        raise HTTPException(404, f"{e}")
    


