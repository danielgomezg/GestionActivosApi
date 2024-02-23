from models import article
from models.article import Article
# from database import engine
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pathlib import Path
from sqlalchemy.orm import Session
from database import get_db
from crud.article import (get_article_all, get_article_by_id, create_article, update_article, delete_article,
                          get_article_by_id_company, get_image_url, search_article_by_company, get_article_by_company_and_code)
from schemas.articleSchema import ArticleSchema, ArticleEditSchema
from schemas.schemaGenerico import Response, ResponseGet
from crud.company import get_company_by_id
from crud.category import get_category_by_id
from fastapi.responses import FileResponse
from crud.user import  get_user_disable_current
from typing import Tuple

router = APIRouter()
#article.Base.metadata.create_all(bind=engine)

@router.get("/article/{id}")
def get_article(id: int, db: Session = Depends(get_db), current_user_info: Tuple[str, str] = Depends(get_user_disable_current)):
    name_user, expiration_time = current_user_info
    # Se valida la expiracion del token
    if expiration_time is None:
        return Response(code="401", message="token-exp", result=[])

    result = get_article_by_id(db, id)
    if result is None:
        return Response(code="404", result=[], message="Articulo no encontrada").model_dump()
    return Response(code="200", result=result, message="Articulo encontrado").model_dump()

@router.get('/articles')
def get_articles(db: Session = Depends(get_db), current_user_info: Tuple[str, str] = Depends(get_user_disable_current), limit: int = 25, offset: int = 0):
    name_user, expiration_time = current_user_info
    # print("Tiempo de expiración: ", expiration_time)
    # Se valida la expiracion del token
    if expiration_time is None:
        return Response(code="401", message="token-exp", result=[])

    result, count = get_article_all(db, limit, offset)
    #return result
    if not result:
        return ResponseGet(code= "404", result = [], limit= limit, offset = offset, count = 0).model_dump()
    return ResponseGet(code= "200", result = result, limit= limit, offset = offset, count = count).model_dump()

@router.get('/articles/company/{id_company}')
def get_articles_por_company(id_company: int, db: Session = Depends(get_db), current_user_info: Tuple[str, str] = Depends(get_user_disable_current), limit: int = 25, offset: int = 0):
    name_user, expiration_time = current_user_info
    # print("Tiempo de expiración: ", expiration_time)
    # Se valida la expiracion del token
    if expiration_time is None:
        return Response(code="401", message="token-exp", result=[])

    result, count = get_article_by_id_company(db, id_company, limit, offset)
    if not result:
        return ResponseGet(code= "404", result = [], limit= limit, offset = offset, count = 0).model_dump()
    return ResponseGet(code= "200", result = result, limit= limit, offset = offset, count = count).model_dump()


@router.get('/articles/search/{company_id}')
def search_articles(company_id: int, search: str, db: Session = Depends(get_db), current_user_info: Tuple[str, str] = Depends(get_user_disable_current), limit: int = 25, offset: int = 0):
    name_user, expiration_time = current_user_info
    if expiration_time is None:
        return Response(code="401", message="token-exp", result=[])

    result, count = search_article_by_company(db, search, company_id, limit, offset)
    if not result:
        return ResponseGet(code="200", result=[], limit=limit, offset=offset, count=0).model_dump()
    return ResponseGet(code="200", result=result, limit=limit, offset=offset, count=count).model_dump()

@router.post("/image_article")
def upload_image(file: UploadFile = File(...), current_user_info: Tuple[str, str] = Depends(get_user_disable_current)):
    try:
        id_user, expiration_time = current_user_info
        # print("Tiempo de expiración: ", expiration_time)
        # Se valida la expiracion del token
        if expiration_time is None:
            return Response(code="401", message="token-exp", result=[])

        upload_folder = Path("files") / "images_article"
        upload_folder.mkdir(parents=True, exist_ok=True)  # Crea el directorio si no existe
        photo_url = get_image_url(file, upload_folder)
        return Response(code="201", message="Foto guardada con éxito", result=photo_url).model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {e}")

@router.post('/article')
def create(request: ArticleSchema, db: Session = Depends(get_db), current_user_info: Tuple[str, str] = Depends(get_user_disable_current)):
    name_user, expiration_time = current_user_info
    #print("Tiempo de expiración: ", expiration_time)
    # Se valida la expiracion del token
    if expiration_time is None:
        return Response(code="401", message="token-exp", result=[])

    if(len(request.name) == 0):
        return  Response(code = "400", message = "Nombre no valido", result = [])

    if(len(request.code) == 0):
        return  Response(code = "400", message = "Codigo no valido", result = [])

    article_code = get_article_by_company_and_code(db, request.company_id, request.code)
    if article_code:
        return Response(code="400", message="Codigo de articulo ya ingresado", result=[])

    # id_category = get_category_by_id(db, request.category_id)
    # if not id_category:
    #     return Response(code="400", message="id categoria no valido", result=[])

    id_company = get_company_by_id(db, request.company_id)
    if(not id_company):
        return Response(code="400", message="id compania no valido", result=[])

    _article = create_article(db, request, name_user)
    return Response(code = "201", message = f"Articulo {_article.name} creado", result = _article).model_dump()

@router.put('/article/{id}')
def update(request: ArticleEditSchema, id: int, db: Session = Depends(get_db), current_user_info: Tuple[str, str] = Depends(get_user_disable_current)):
    name_user, expiration_time = current_user_info
    # Se valida la expiracion del token
    if expiration_time is None:
        return Response(code="401", message="token-exp", result=[])

    if(len(request.name) == 0):
        return  Response(code = "400", message = "Nombre no valido", result = [])

    if(len(request.code) == 0):
        return  Response(code = "400", message = "Codigo no valido", result = [])

    article_code = get_article_by_company_and_code(db, request.company_id, request.code)
    if article_code and id is not article_code.id:
        return Response(code="400", message="Codigo de barra ya ingresado", result=[])

    # id_category = get_category_by_id(db, request.category_id)
    # if not id_category:
    #     return Response(code="400", message="id categoria no valido", result=[])

    _article = update_article(db, id,  request, name_user)
    return Response(code = "201", message = f"Articulo {_article.name} editado", result = _article).model_dump()

@router.delete('/article/{id}')
def delete(id: int, db: Session = Depends(get_db), current_user_info: Tuple[str, str] = Depends(get_user_disable_current)):
    name_user, expiration_time = current_user_info
    # print("Tiempo de expiración: ", expiration_time)
    # Se valida la expiracion del token
    if expiration_time is None:
        return Response(code="401", message="token-exp", result=[])

    _article = delete_article(db, id, name_user)
    return Response(code = "201", message = f"Articulo con id {id} eliminado", result = _article).model_dump()


@router.get("/image_article/{image_path}")
async def get_image(image_path: str):
    image = Path("files") / "images_article" / image_path
    if not image.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image)