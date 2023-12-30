from sqlalchemy.orm import Session
from schemas.sucursalSchema import SucursalSchema, SucursalEditSchema
from models.sucursal import Sucursal
from fastapi import HTTPException, status
from models.office import Office
from sqlalchemy import desc, func, and_

def get_sucursal_all(db: Session, limit: int = 100, offset: int = 0):
    try:
        sucursales = (
            db.query(Sucursal, func.count(Office.id).label("count_offices"))
            .outerjoin(Office, and_(Office.sucursal_id == Sucursal.id, Office.removed == 0))
            .filter(Sucursal.removed == 0)
            .group_by(Sucursal.id)
            .order_by(desc(Sucursal.id))
            .offset(offset)
            .limit(limit)
            .all()
        )
        result = []
        for sucursal in sucursales:
            sucursal[0].count_offices = sucursal[1]
            result.append(sucursal[0])

        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Error al obtener sucursal sucursal {e}")
    #return db.query(Sucursal).offset(skip).limit(limit).all()

def count_sucursal(db: Session):
    try:
        return db.query(Sucursal).filter(Sucursal.removed == 0).count()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Error al contar sucursales {e}")

def get_sucursal_by_id(db: Session, sucursal_id: int):
    try:
        return db.query(Sucursal).filter(Sucursal.id == sucursal_id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Error al obtener sucursales por id {e}")

def get_sucursal_by_id_company(db: Session, company_id: int, limit: int = 100, offset: int = 0):
    try:
        sucursales = (
            db.query(Sucursal, func.count(Office.id).label("count_offices"))
            .outerjoin(Office, and_(Office.sucursal_id == Sucursal.id, Office.removed == 0))
            .filter(Sucursal.company_id == company_id, Sucursal.removed == 0)
            .group_by(Sucursal.id)
            .order_by(desc(Sucursal.id))
            .offset(offset)
            .limit(limit)
            .all()
        )
        result = []
        for sucursal in sucursales:
            sucursal[0].count_offices = sucursal[1]
            result.append(sucursal[0])
        print(result)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Error al obtener sucursal sucursal {e}")
    #return db.query(Sucursal).filter(Sucursal.company_id == company_id).all()

def create_sucursal(db: Session, sucursal: SucursalSchema):
    try:
        _sucursal = Sucursal(
            description=sucursal.description,
            number = sucursal.number,
            address = sucursal.address,
            region = sucursal.region,
            city = sucursal.city,
            commune=sucursal.commune,
            company_id=sucursal.company_id
        )

        db.add(_sucursal)
        db.commit()
        db.refresh(_sucursal)
        return _sucursal
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"Error creando sucursal {e}")

def update_sucursal(db: Session, sucursal_id: int, sucursal: SucursalEditSchema):

    try:
        sucursal_to_edit = db.query(Sucursal).filter(Sucursal.id == sucursal_id).first()
        if sucursal_to_edit:
            sucursal_to_edit.description = sucursal.description
            sucursal_to_edit.number = sucursal.number
            sucursal_to_edit.address = sucursal.address

            db.commit()
            sucursal_edited = get_sucursal_by_id(db, sucursal_id)
            return sucursal_edited
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sucursal no encontrada")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error editando sucursal: {e}")

def delete_sucursal(db: Session, sucursal_id: int):
    try:
        sucursal_to_delete = db.query(Sucursal).filter(Sucursal.id == sucursal_id).first()
        if sucursal_to_delete:
            sucursal_to_delete.removed = 1
            db.commit()
            return sucursal_id
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sucursal con id {sucursal_id} no encontrada")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error eliminando sucursal: {e}")