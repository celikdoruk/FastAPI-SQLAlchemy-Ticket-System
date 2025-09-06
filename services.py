from sqlalchemy.orm import Session
from repositories import CustomerRepository, ShowRepository, AvanueRepository
from models import CustomerORM, ShowORM, AvanueORM
import schemas

class CRUDServices:
    class CustomerService:
        def __init__(self, db: Session):
            self.db = db
            self.repo = CustomerRepository(db)

        def enroll_customer(self, payload: schemas.CustomerAdd):
            if not payload.age or not payload.name: 
                raise ValueError("Please provide name and age for the customer.")
            
            if not (5 <= payload.age <= 120):
                raise ValueError("The age for customer must be between 5 and 120 maximum.")
            
            customer = CustomerORM(
                name = payload.name,
                age = payload.age
            )

            self.repo.add(customer)
            self.db.commit()
            self.db.refresh(customer)

            return customer


        def delete_customer(self, id: int):
            customer = self.repo.get(id)
            if not customer:
                raise ValueError("Customer is not in the repository.")
            
            self.repo.delete(customer)
            self.db.commit()

            return {"message": "Customer has been removed succesfully."}

        
        def update_customer(self, id: int, payload: schemas.CustomerUpdate):
            current_customer = self.repo.get(id)
            if not current_customer:
                raise ValueError("Customer is not in the repository.")
            
            changes = payload.model_dump(exclude_none=True)

            if "name" in changes:
                current_customer.name = changes["name"]
            if "age" in changes:
                if not  (5 <= changes["age"] <= 120):
                    raise ValueError("The new age must be between 5 and 120.")
                current_customer.age = changes["age"]
            
            self.db.commit()
            self.db.refresh(current_customer)

            return current_customer


    class ShowService:
        def __init__(self, db: Session):
            self.db = db
            self.repo = ShowRepository(db)

        def enroll_show(self, payload: schemas.ShowAdd):
            if not payload.title or not payload.age_limit or not payload.head_count:
                raise ValueError("Please pass in the necassery information.")
            
            show = ShowORM(
                title = payload.title,
                age_limit = payload.age_limit,
                head_count = payload.head_count
            )

            self.repo.add(show)
            self.db.commit()
            self.db.refresh(show)

            return show

        def delete_show(self, id: int):
            show = self.repo.get(id)
            if not show:
                raise ValueError("Show is not in the repository.")

            self.repo.delete(show)   
            self.db.commit()

            return {"message": "The show has been deleted."}

        def update_show(self, id: int, payload: schemas.ShowUpdate):
            show = self.repo.get(id)
            if not show:
                raise ValueError("The show is not in the repository.")

            changes = payload.model_dump(exclude_none=True) 
            max_headcount = 50000
            max_age_limit = 25

            if "title" in changes:
                show.title = changes["title"]
            if "age_limit" in changes:
                if not changes["age_limit"] > max_age_limit:
                    show.age_limit = changes["age_limit"]
            if "head_count" in changes:
                if not changes["head_count"] > max_headcount:
                    show.head_count = changes["head_count"]
            
            self.db.commit()
            self.db.refresh(show)

            return show
        

    class AvanueService:
        def __init__(self, db: Session):
            self.db = db
            self.repo = AvanueRepository(db)

        def enroll_avanue(self, payload: schemas.AvanueAdd):
            if payload.name is None or payload.availability is None:
                raise ValueError("Please provide the required details.")
            
            avanue = AvanueORM(
                name = payload.name,
                availability = payload.availability
            )

            self.repo.add(avanue)
            self.db.commit()
            self.db.refresh(avanue)

            return avanue
        
        def delete_avanue(self, id: int):
            avanue = self.repo.get(id)
            if not avanue:
                raise ValueError("The avanue is not in the repository.")
            
            self.repo.delete(avanue)
            self.db.commit()

            return {"message": "The avanue has been deleted succesfully."}
        
        def update_avanue(self, id: int, payload: schemas.AvanueUpdate):
            avanue = self.repo.get(id)
            if not avanue:
                raise ValueError("The avanue is not in the repository.")
            
            changes = payload.model_dump(exclude_none=True)

            if "name" in changes:
                avanue.name = changes["name"]
            if "availability" in changes:
                avanue.availability = changes["availability"]
            
            self.db.commit()
            self.db.refresh(avanue)

            return avanue


class GeneralServices:
    def __init__(self, db: Session):
        self.db = db
        self.repo_customer = CustomerRepository(db)
        self.repo_show = ShowRepository(db)
        self.repo_avanue = AvanueRepository(db)
    
    def enroll_customer_to_show(self, customer_id: int, show_id: int):
        customer = self.repo_customer.get(customer_id)
        show = self.repo_show.get(show_id)

        if not customer or not show:
            raise ValueError("Customer or show not found in repositories. Check your ids.")
        
        if customer.age < show.age_limit:
            raise ValueError(f"The customer with id {customer.id} is not old enough to attend to show with id {show.id}.")
        
        if customer in show.customer_list:
            raise ValueError(f"Customer {customer.id} is already admitted to the show {show.id}")
        
        if show.head_count <= 0:
            raise ValueError(f"Show {show.id} is full.")

        show.customer_list.append(customer)
        show.head_count -= 1

        self.db.commit()
        self.db.refresh(show)

        return {"message": f"Customer {customer.id} admitted to show {show.id}"}
    
    def remove_customer_from_show(self, customer_id: int, show_id: int):
        customer = self.repo_customer.get(customer_id)
        show = self.repo_show.get(show_id)

        if not customer or not show:
            raise ValueError("Customer or show not found in repositories. Check your ids.")
        
        if customer not in show.customer_list:
            raise ValueError(f"Customer {customer.id} not admitted to the show {show.id}")
        
        show.customer_list.remove(customer)
        show.head_count += 1
        
        self.db.commit()
        self.db.refresh(show)

        return {"message": f"Customer {customer.id} removed from the show {show.id}"}
    
    def enroll_show_to_avanue(self, show_id: int, avanue_id: int):
        show = self.repo_show.get(show_id)
        avanue = self.repo_avanue.get(avanue_id)

        if show in avanue.show_list:
            raise ValueError(f"The show {show.id} is already admitted to the avanue {avanue.id}")

        if avanue.availability is False:
            raise ValueError(f"The avanue {avanue.id} is not availabile!")
        
        if show.avanue_id == avanue.id:
            raise ValueError(f"Show {show.id} alread in avanue {avanue.id}")
        
        if show.avanue_id is not None:
            raise ValueError(f"Show {show.id} is already assigned to avanue {show.avanue_id}")

        avanue.show_list.append(show)

        self.db.commit()
        self.db.refresh(avanue)

        return {"message": f"Show {show.id} is admitted to avanue {avanue.id}"}

    def delete_show_from_avanue(self, show_id: int, avanue_id: int):
        show = self.repo_show.get(show_id)
        avanue = self.repo_avanue.get(avanue_id) 

        if not avanue or not show:
            raise ValueError("Customer or show not found in repositories. Check your ids.")
        
        if show not in avanue.show_list:
            raise ValueError(f"Show {show.id} not found in the avanue {avanue.id}")
        
        show.avanue = None

        self.db.commit()
        self.db.refresh(show)

        return {"message": f"Show {show.id} is deleted from avanue {avanue.id}"}
