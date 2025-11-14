from abc import ABC, abstractmethod
from typing import List, Optional
from sqlmodel import Session, select
from models import Persona, PersonaCreate, PersonaUpdate, Pais, PaisCreate, PaisUpdate, Auto, AutoCreate, AutoUpdate, Venta, VentaCreate, VentaUpdate

class PersonaRepositoryInterface(ABC):
    """Interface for Persona repository"""
    
    @abstractmethod
    def create(self, persona: PersonaCreate) -> Persona:
        pass
    
    @abstractmethod
    def get_by_id(self, persona_id: int) -> Optional[Persona]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Persona]:
        pass
    
    @abstractmethod
    def update(self, persona_id: int, persona_update: PersonaUpdate) -> Optional[Persona]:
        pass
    
    @abstractmethod
    def delete(self, persona_id: int) -> bool:
        pass

class PersonaRepository(PersonaRepositoryInterface):
    """Repository for Persona entity using SQLModel"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, persona: PersonaCreate) -> Persona:
        """Create a new persona"""
        db_persona = Persona.model_validate(persona)
        self.session.add(db_persona)
        self.session.commit()
        self.session.refresh(db_persona)
        return db_persona
    
    def get_by_id(self, persona_id: int) -> Optional[Persona]:
        """Get persona by ID"""
        statement = select(Persona).where(Persona.id == persona_id)
        return self.session.exec(statement).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Persona]:
        """Get all personas with pagination"""
        statement = select(Persona).offset(skip).limit(limit)
        return self.session.exec(statement).all()
    
    def update(self, persona_id: int, persona_update: PersonaUpdate) -> Optional[Persona]:
        """Update persona by ID"""
        db_persona = self.get_by_id(persona_id)
        if not db_persona:
            return None
        
        # Update only provided fields
        persona_data = persona_update.model_dump(exclude_unset=True)
        for key, value in persona_data.items():
            setattr(db_persona, key, value)
        
        self.session.add(db_persona)
        self.session.commit()
        self.session.refresh(db_persona)
        return db_persona
    
    def delete(self, persona_id: int) -> bool:
        """Delete persona by ID"""
        db_persona = self.get_by_id(persona_id)
        if not db_persona:
            return False
        
        self.session.delete(db_persona)
        self.session.commit()
        return True


class PaisRepositoryInterface(ABC):
    """Interface for Pais repository"""
    
    @abstractmethod
    def create(self, pais: PaisCreate) -> Pais:
        pass
    
    @abstractmethod
    def get_by_id(self, pais_id: int) -> Optional[Pais]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Pais]:
        pass
    
    @abstractmethod
    def update(self, pais_id: int, pais_update: PaisUpdate) -> Optional[Pais]:
        pass
    
    @abstractmethod
    def delete(self, pais_id: int) -> bool:
        pass


class PaisRepository(PaisRepositoryInterface):
    """Repository for Pais entity using SQLModel"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, pais: PaisCreate) -> Pais:
        """Create a new pais"""
        db_pais = Pais.model_validate(pais)
        self.session.add(db_pais)
        self.session.commit()
        self.session.refresh(db_pais)
        return db_pais
    
    def get_by_id(self, pais_id: int) -> Optional[Pais]:
        """Get pais by ID"""
        statement = select(Pais).where(Pais.id == pais_id)
        return self.session.exec(statement).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Pais]:
        """Get all paises with pagination"""
        statement = select(Pais).offset(skip).limit(limit)
        return self.session.exec(statement).all()
    
    def update(self, pais_id: int, pais_update: PaisUpdate) -> Optional[Pais]:
        """Update pais by ID"""
        db_pais = self.get_by_id(pais_id)
        if not db_pais:
            return None
        
        # Update only provided fields
        pais_data = pais_update.model_dump(exclude_unset=True)
        for key, value in pais_data.items():
            setattr(db_pais, key, value)
        
        self.session.add(db_pais)
        self.session.commit()
        self.session.refresh(db_pais)
        return db_pais
    
    def delete(self, pais_id: int) -> bool:
        """Delete pais by ID"""
        db_pais = self.get_by_id(pais_id)
        if not db_pais:
            return False
        
        self.session.delete(db_pais)
        self.session.commit()
        return True


class AutoRepositoryInterface(ABC):
    """Interface for Auto repository"""
    
    @abstractmethod
    def create(self, auto: AutoCreate) -> Auto:
        pass
    
    @abstractmethod
    def get_by_id(self, auto_id: int) -> Optional[Auto]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Auto]:
        pass
    
    @abstractmethod
    def update(self, auto_id: int, auto_update: AutoUpdate) -> Optional[Auto]:
        pass
    
    @abstractmethod
    def delete(self, auto_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_by_chasis(self, numero_chasis: str) -> Optional[Auto]:
        pass


class AutoRepository(AutoRepositoryInterface):
    """Repository for Auto entity using SQLModel"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, auto: AutoCreate) -> Auto:
        """Create a new auto"""
        db_auto = Auto.model_validate(auto)
        self.session.add(db_auto)
        self.session.commit()
        self.session.refresh(db_auto)
        return db_auto
    
    def get_by_id(self, auto_id: int) -> Optional[Auto]:
        """Get auto by ID"""
        statement = select(Auto).where(Auto.id == auto_id)
        return self.session.exec(statement).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Auto]:
        """Get all autos with pagination"""
        statement = select(Auto).offset(skip).limit(limit)
        return self.session.exec(statement).all()
    
    def update(self, auto_id: int, auto_update: AutoUpdate) -> Optional[Auto]:
        """Update auto by ID"""
        db_auto = self.get_by_id(auto_id)
        if not db_auto:
            return None
        
        # Update only provided fields
        auto_data = auto_update.model_dump(exclude_unset=True)
        for key, value in auto_data.items():
            setattr(db_auto, key, value)
        
        self.session.add(db_auto)
        self.session.commit()
        self.session.refresh(db_auto)
        return db_auto
    
    def delete(self, auto_id: int) -> bool:
        """Delete auto by ID"""
        db_auto = self.get_by_id(auto_id)
        if not db_auto:
            return False
        
        self.session.delete(db_auto)
        self.session.commit()
        return True
    
    def get_by_chasis(self, numero_chasis: str) -> Optional[Auto]:
        """Get auto by numero_chasis"""
        statement = select(Auto).where(Auto.numero_chasis == numero_chasis)
        return self.session.exec(statement).first()


class VentaRepositoryInterface(ABC):
    """Interface for Venta repository"""
    
    @abstractmethod
    def create(self, venta: VentaCreate) -> Venta:
        pass
    
    @abstractmethod
    def get_by_id(self, venta_id: int) -> Optional[Venta]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Venta]:
        pass
    
    @abstractmethod
    def update(self, venta_id: int, venta_update: VentaUpdate) -> Optional[Venta]:
        pass
    
    @abstractmethod
    def delete(self, venta_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_by_auto_id(self, auto_id: int) -> List[Venta]:
        pass
    
    @abstractmethod
    def get_by_comprador(self, nombre: str) -> List[Venta]:
        pass


class VentaRepository(VentaRepositoryInterface):
    """Repository for Venta entity using SQLModel"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, venta: VentaCreate) -> Venta:
        """Create a new venta"""
        db_venta = Venta.model_validate(venta)
        self.session.add(db_venta)
        self.session.commit()
        self.session.refresh(db_venta)
        return db_venta
    
    def get_by_id(self, venta_id: int) -> Optional[Venta]:
        """Get venta by ID"""
        statement = select(Venta).where(Venta.id == venta_id)
        return self.session.exec(statement).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Venta]:
        """Get all ventas with pagination"""
        statement = select(Venta).offset(skip).limit(limit)
        return self.session.exec(statement).all()
    
    def update(self, venta_id: int, venta_update: VentaUpdate) -> Optional[Venta]:
        """Update venta by ID"""
        db_venta = self.get_by_id(venta_id)
        if not db_venta:
            return None
        
        # Update only provided fields
        venta_data = venta_update.model_dump(exclude_unset=True)
        for key, value in venta_data.items():
            setattr(db_venta, key, value)
        
        self.session.add(db_venta)
        self.session.commit()
        self.session.refresh(db_venta)
        return db_venta
    
    def delete(self, venta_id: int) -> bool:
        """Delete venta by ID"""
        db_venta = self.get_by_id(venta_id)
        if not db_venta:
            return False
        
        self.session.delete(db_venta)
        self.session.commit()
        return True
    
    def get_by_auto_id(self, auto_id: int) -> List[Venta]:
        """Get ventas by auto_id"""
        statement = select(Venta).where(Venta.auto_id == auto_id)
        return self.session.exec(statement).all()
    
    def get_by_comprador(self, nombre: str) -> List[Venta]:
        """Get ventas by comprador name (partial match)"""
        statement = select(Venta).where(Venta.nombre_comprador.ilike(f"%{nombre}%"))
        return self.session.exec(statement).all()
