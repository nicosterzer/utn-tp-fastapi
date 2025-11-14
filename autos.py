from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List
from database import get_session
from models import AutoCreate, AutoUpdate, AutoResponse, AutoResponseWithVentas, VentaResponse
from repository import AutoRepository, VentaRepository

# Create router for autos
router = APIRouter(prefix="/autos", tags=["autos"])

def get_auto_repository(session: Session = Depends(get_session)) -> AutoRepository:
    """Dependency to get auto repository"""
    return AutoRepository(session)

def get_venta_repository(session: Session = Depends(get_session)) -> VentaRepository:
    """Dependency to get venta repository"""
    return VentaRepository(session)

@router.post("/", response_model=AutoResponse, status_code=status.HTTP_201_CREATED)
def create_auto(
    auto: AutoCreate,
    repo: AutoRepository = Depends(get_auto_repository)
) -> AutoResponse:
    """Create a new auto"""
    try:
        # Check if numero_chasis already exists
        existing_auto = repo.get_by_chasis(auto.numero_chasis)
        if existing_auto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Auto with numero_chasis '{auto.numero_chasis}' already exists"
            )
        
        db_auto = repo.create(auto)
        return AutoResponse.model_validate(db_auto)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating auto: {str(e)}"
        )

@router.get("/", response_model=List[AutoResponse])
def get_autos(
    skip: int = Query(0, ge=0, description="Number of autos to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of autos to return"),
    repo: AutoRepository = Depends(get_auto_repository)
) -> List[AutoResponse]:
    """Get all autos with pagination"""
    autos = repo.get_all(skip=skip, limit=limit)
    return [AutoResponse.model_validate(auto) for auto in autos]

@router.get("/{auto_id}", response_model=AutoResponse)
def get_auto(
    auto_id: int,
    repo: AutoRepository = Depends(get_auto_repository)
) -> AutoResponse:
    """Get auto by ID"""
    db_auto = repo.get_by_id(auto_id)
    if not db_auto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auto with id {auto_id} not found"
        )
    return AutoResponse.model_validate(db_auto)

@router.put("/{auto_id}", response_model=AutoResponse)
def update_auto(
    auto_id: int,
    auto_update: AutoUpdate,
    repo: AutoRepository = Depends(get_auto_repository)
) -> AutoResponse:
    """Update auto by ID"""
    try:
        # Check if numero_chasis already exists (if being updated)
        if auto_update.numero_chasis:
            existing_auto = repo.get_by_chasis(auto_update.numero_chasis)
            if existing_auto and existing_auto.id != auto_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Auto with numero_chasis '{auto_update.numero_chasis}' already exists"
                )
        
        db_auto = repo.update(auto_id, auto_update)
        if not db_auto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Auto with id {auto_id} not found"
            )
        return AutoResponse.model_validate(db_auto)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating auto: {str(e)}"
        )

@router.delete("/{auto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_auto(
    auto_id: int,
    repo: AutoRepository = Depends(get_auto_repository)
) -> None:
    """Delete auto by ID"""
    success = repo.delete(auto_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auto with id {auto_id} not found"
        )

@router.get("/chasis/{numero_chasis}", response_model=AutoResponse)
def get_auto_by_chasis(
    numero_chasis: str,
    repo: AutoRepository = Depends(get_auto_repository)
) -> AutoResponse:
    """Get auto by numero_chasis"""
    db_auto = repo.get_by_chasis(numero_chasis)
    if not db_auto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auto with numero_chasis '{numero_chasis}' not found"
        )
    return AutoResponse.model_validate(db_auto)

@router.get("/{auto_id}/with-ventas", response_model=AutoResponseWithVentas)
def get_auto_with_ventas(
    auto_id: int,
    repo: AutoRepository = Depends(get_auto_repository),
    venta_repo: VentaRepository = Depends(get_venta_repository)
) -> AutoResponseWithVentas:
    """Get auto by ID with ventas information included"""
    db_auto = repo.get_by_id(auto_id)
    if not db_auto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auto with id {auto_id} not found"
        )
    
    # Get ventas for this auto
    ventas = venta_repo.get_by_auto_id(auto_id)
    
    auto_dict = AutoResponseWithVentas.model_validate(db_auto).model_dump()
    auto_dict['ventas'] = [VentaResponse.model_validate(venta).model_dump() for venta in ventas]
    
    return AutoResponseWithVentas.model_validate(auto_dict)

@router.get("/search/", response_model=List[AutoResponse])
def search_autos(
    marca: str = Query(None, min_length=2, description="Marca to search for"),
    modelo: str = Query(None, min_length=2, description="Modelo to search for"),
    repo: AutoRepository = Depends(get_auto_repository)
) -> List[AutoResponse]:
    """Search autos by marca and/or modelo (partial match)"""
    # This would require additional repository method for search
    # For now, we'll get all and filter in Python (not efficient for large datasets)
    all_autos = repo.get_all(limit=1000)
    filtered_autos = []
    
    for auto in all_autos:
        marca_match = not marca or marca.lower() in auto.marca.lower()
        modelo_match = not modelo or modelo.lower() in auto.modelo.lower()
        
        if marca_match and modelo_match:
            filtered_autos.append(auto)
    
    return [AutoResponse.model_validate(auto) for auto in filtered_autos]
