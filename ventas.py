from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List
from datetime import datetime
from database import get_session
from models import VentaCreate, VentaUpdate, VentaResponse, VentaResponseWithAuto, AutoResponse
from repository import VentaRepository, AutoRepository

# Create router for ventas
router = APIRouter(prefix="/ventas", tags=["ventas"])

def get_venta_repository(session: Session = Depends(get_session)) -> VentaRepository:
    """Dependency to get venta repository"""
    return VentaRepository(session)

def get_auto_repository(session: Session = Depends(get_session)) -> AutoRepository:
    """Dependency to get auto repository"""
    return AutoRepository(session)

@router.post("/", response_model=VentaResponse, status_code=status.HTTP_201_CREATED)
def create_venta(
    venta: VentaCreate,
    repo: VentaRepository = Depends(get_venta_repository),
    auto_repo: AutoRepository = Depends(get_auto_repository)
) -> VentaResponse:
    """Create a new venta"""
    try:
        # Validate that auto exists
        db_auto = auto_repo.get_by_id(venta.auto_id)
        if not db_auto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Auto with id {venta.auto_id} not found"
            )
        
        # Validate fecha_venta is not in the future
        if venta.fecha_venta and venta.fecha_venta > datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Fecha de venta cannot be in the future"
            )
        
        db_venta = repo.create(venta)
        return VentaResponse.model_validate(db_venta)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating venta: {str(e)}"
        )

@router.get("/", response_model=List[VentaResponse])
def get_ventas(
    skip: int = Query(0, ge=0, description="Number of ventas to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of ventas to return"),
    repo: VentaRepository = Depends(get_venta_repository)
) -> List[VentaResponse]:
    """Get all ventas with pagination"""
    ventas = repo.get_all(skip=skip, limit=limit)
    return [VentaResponse.model_validate(venta) for venta in ventas]

@router.get("/{venta_id}", response_model=VentaResponse)
def get_venta(
    venta_id: int,
    repo: VentaRepository = Depends(get_venta_repository)
) -> VentaResponse:
    """Get venta by ID"""
    db_venta = repo.get_by_id(venta_id)
    if not db_venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Venta with id {venta_id} not found"
        )
    return VentaResponse.model_validate(db_venta)

@router.put("/{venta_id}", response_model=VentaResponse)
def update_venta(
    venta_id: int,
    venta_update: VentaUpdate,
    repo: VentaRepository = Depends(get_venta_repository),
    auto_repo: AutoRepository = Depends(get_auto_repository)
) -> VentaResponse:
    """Update venta by ID"""
    try:
        # Validate that auto exists if being updated
        if venta_update.auto_id:
            db_auto = auto_repo.get_by_id(venta_update.auto_id)
            if not db_auto:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Auto with id {venta_update.auto_id} not found"
                )
        
        # Validate fecha_venta is not in the future
        if venta_update.fecha_venta and venta_update.fecha_venta > datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Fecha de venta cannot be in the future"
            )
        
        db_venta = repo.update(venta_id, venta_update)
        if not db_venta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Venta with id {venta_id} not found"
            )
        return VentaResponse.model_validate(db_venta)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating venta: {str(e)}"
        )

@router.delete("/{venta_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_venta(
    venta_id: int,
    repo: VentaRepository = Depends(get_venta_repository)
) -> None:
    """Delete venta by ID"""
    success = repo.delete(venta_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Venta with id {venta_id} not found"
        )

@router.get("/auto/{auto_id}", response_model=List[VentaResponse])
def get_ventas_by_auto(
    auto_id: int,
    repo: VentaRepository = Depends(get_venta_repository),
    auto_repo: AutoRepository = Depends(get_auto_repository)
) -> List[VentaResponse]:
    """Get ventas by auto_id"""
    # Validate that auto exists
    db_auto = auto_repo.get_by_id(auto_id)
    if not db_auto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auto with id {auto_id} not found"
        )
    
    ventas = repo.get_by_auto_id(auto_id)
    return [VentaResponse.model_validate(venta) for venta in ventas]

@router.get("/comprador/{nombre}", response_model=List[VentaResponse])
def get_ventas_by_comprador(
    nombre: str,
    repo: VentaRepository = Depends(get_venta_repository)
) -> List[VentaResponse]:
    """Get ventas by comprador name (partial match)"""
    ventas = repo.get_by_comprador(nombre)
    return [VentaResponse.model_validate(venta) for venta in ventas]

@router.get("/{venta_id}/with-auto", response_model=VentaResponseWithAuto)
def get_venta_with_auto(
    venta_id: int,
    repo: VentaRepository = Depends(get_venta_repository),
    auto_repo: AutoRepository = Depends(get_auto_repository)
) -> VentaResponseWithAuto:
    """Get venta by ID with auto information included"""
    db_venta = repo.get_by_id(venta_id)
    if not db_venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Venta with id {venta_id} not found"
        )
    
    # Get auto information
    db_auto = auto_repo.get_by_id(db_venta.auto_id)
    
    venta_dict = VentaResponseWithAuto.model_validate(db_venta).model_dump()
    
    if db_auto:
        venta_dict['auto'] = AutoResponse.model_validate(db_auto).model_dump()
    
    return VentaResponseWithAuto.model_validate(venta_dict)

@router.get("/search/", response_model=List[VentaResponse])
def search_ventas(
    nombre_comprador: str = Query(None, min_length=2, description="Comprador name to search for"),
    precio_min: float = Query(None, ge=0, description="Minimum price"),
    precio_max: float = Query(None, ge=0, description="Maximum price"),
    fecha_desde: datetime = Query(None, description="Start date"),
    fecha_hasta: datetime = Query(None, description="End date"),
    repo: VentaRepository = Depends(get_venta_repository)
) -> List[VentaResponse]:
    """Search ventas by various filters"""
    # This would require additional repository method for complex search
    # For now, we'll get all and filter in Python (not efficient for large datasets)
    all_ventas = repo.get_all(limit=1000)
    filtered_ventas = []
    
    for venta in all_ventas:
        # Filter by nombre_comprador
        nombre_match = not nombre_comprador or nombre_comprador.lower() in venta.nombre_comprador.lower()
        
        # Filter by price range
        precio_match = True
        if precio_min is not None and venta.precio < precio_min:
            precio_match = False
        if precio_max is not None and venta.precio > precio_max:
            precio_match = False
        
        # Filter by date range
        fecha_match = True
        if fecha_desde and venta.fecha_venta < fecha_desde:
            fecha_match = False
        if fecha_hasta and venta.fecha_venta > fecha_hasta:
            fecha_match = False
        
        if nombre_match and precio_match and fecha_match:
            filtered_ventas.append(venta)
    
    return [VentaResponse.model_validate(venta) for venta in filtered_ventas]
