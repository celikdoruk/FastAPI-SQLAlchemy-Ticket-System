from models import CustomerORM, ShowORM, AvanueORM
from sqlalchemy.orm import Session
from typing import Any

class GenericRepository:
    def __init__(self, db: Session, model: Any):
        self.db = db
        self.model = model

    def get_all(self):
        return self.db.query(self.model).all()
    
    def get(self, id: int):
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def add(self, model):
        self.db.add(model)

        return model
    
    def delete(self, model):
        self.db.delete(model)

        return None

class CustomerRepository(GenericRepository):
    def __init__(self, db: Session):
        super().__init__(db, CustomerORM)

class ShowRepository(GenericRepository):
    def __init__(self, db: Session):
        super().__init__(db, ShowORM)

class AvanueRepository(GenericRepository):
    def __init__(self, db: Session):
        super().__init__(db, AvanueORM)



