from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class PersonaBase(SQLModel):
    """Base model for Persona"""
    nombre: str = Field(max_length=100, description="Nombre de la persona")
    apellido: str = Field(max_length=100, description="Apellido de la persona")  
    edad: int = Field(ge=0, le=150, description="Edad de la persona")
    pais_id: Optional[int] = Field(default=None, foreign_key="pais.id", description="ID del país")

class Persona(PersonaBase, table=True):
    """Persona table model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationship with pais
    pais: Optional["Pais"] = Relationship(back_populates="personas")

class PersonaCreate(PersonaBase):
    """Model for creating a new persona"""
    pass

class PersonaUpdate(BaseModel):
    """Model for updating persona"""
    nombre: Optional[str] = Field(None, max_length=100, description="Nombre de la persona")
    apellido: Optional[str] = Field(None, max_length=100, description="Apellido de la persona")
    edad: Optional[int] = Field(None, ge=0, le=150, description="Edad de la persona")
    pais_id: Optional[int] = Field(None, description="ID del país")

class PersonaResponse(PersonaBase):
    """Model for persona response"""
    id: int

class PersonaResponseWithPais(PersonaResponse):
    """Model for persona response with pais information"""
    pais: Optional["PaisResponse"] = None


# País models
class PaisBase(SQLModel):
    """Base model for Pais"""
    nombre: str = Field(max_length=100, description="Nombre del país", unique=True)

class Pais(PaisBase, table=True):
    """Pais table model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationship with personas
    personas: List["Persona"] = Relationship(back_populates="pais")

class PaisCreate(PaisBase):
    """Model for creating a new pais"""
    pass

class PaisUpdate(BaseModel):
    """Model for updating pais"""
    nombre: Optional[str] = Field(None, max_length=100, description="Nombre del país")

class PaisResponse(PaisBase):
    """Model for pais response"""
    id: int


# Auto models
class AutoBase(SQLModel):
    """Base model for Auto"""
    marca: str = Field(max_length=100, description="Marca del vehículo")
    modelo: str = Field(max_length=100, description="Modelo específico del vehículo")
    año: int = Field(ge=1900, le=2025, description="Año de fabricación")
    numero_chasis: str = Field(max_length=50, description="Número único de identificación del chasis", unique=True)

class Auto(AutoBase, table=True):
    """Auto table model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationship with ventas
    ventas: List["Venta"] = Relationship(back_populates="auto")

class AutoCreate(AutoBase):
    """Model for creating a new auto"""
    pass

class AutoUpdate(BaseModel):
    """Model for updating auto"""
    marca: Optional[str] = Field(None, max_length=100, description="Marca del vehículo")
    modelo: Optional[str] = Field(None, max_length=100, description="Modelo específico del vehículo")
    año: Optional[int] = Field(None, ge=1900, le=2025, description="Año de fabricación")
    numero_chasis: Optional[str] = Field(None, max_length=50, description="Número único de identificación del chasis")

class AutoResponse(AutoBase):
    """Model for auto response"""
    id: int

class AutoResponseWithVentas(AutoResponse):
    """Model for auto response with ventas information"""
    ventas: List["VentaResponse"] = []


# Venta models
class VentaBase(SQLModel):
    """Base model for Venta"""
    nombre_comprador: str = Field(max_length=200, description="Nombre completo del comprador")
    precio: float = Field(gt=0, description="Precio de venta del vehículo")
    auto_id: int = Field(foreign_key="auto.id", description="Referencia al auto vendido")
    fecha_venta: datetime = Field(default_factory=datetime.now, description="Fecha y hora de la venta")

class Venta(VentaBase, table=True):
    """Venta table model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationship with auto
    auto: Optional["Auto"] = Relationship(back_populates="ventas")

class VentaCreate(BaseModel):
    """Model for creating a new venta"""
    nombre_comprador: str = Field(max_length=200, description="Nombre completo del comprador")
    precio: float = Field(gt=0, description="Precio de venta del vehículo")
    auto_id: int = Field(description="Referencia al auto vendido")
    fecha_venta: Optional[datetime] = Field(default_factory=datetime.now, description="Fecha y hora de la venta")

class VentaUpdate(BaseModel):
    """Model for updating venta"""
    nombre_comprador: Optional[str] = Field(None, max_length=200, description="Nombre completo del comprador")
    precio: Optional[float] = Field(None, gt=0, description="Precio de venta del vehículo")
    auto_id: Optional[int] = Field(None, description="Referencia al auto vendido")
    fecha_venta: Optional[datetime] = Field(None, description="Fecha y hora de la venta")

class VentaResponse(VentaBase):
    """Model for venta response"""
    id: int

class VentaResponseWithAuto(VentaResponse):
    """Model for venta response with auto information"""
    auto: Optional["AutoResponse"] = None