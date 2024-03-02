from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas import CategoryBase, CategoryResponse, CategoryUpdate
from app.models.models import Category as CategoryModel
from app.dependencies import get_current_user
from app.services.database import get_db

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=CategoryResponse)
async def create_category(
    category: CategoryBase,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
):
    db_category = await CategoryModel.create(
        db, **category.model_dump(), user_id=current_user_id
    )
    return db_category


@router.get("/", response_model=list[CategoryResponse])
async def read_categories(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
):
    categories = await CategoryModel.get_all(
        db, user_id=current_user_id, skip=skip, limit=limit
    )
    return categories


@router.get("/{category_id}", response_model=CategoryResponse)
async def read_category(
    category_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
):
    category = await CategoryModel.get(
        db, category_id=category_id, user_id=current_user_id
    )
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: str,
    category: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
):
    updated_category = await CategoryModel.update(
        db, category_id=category_id, user_id=current_user_id, **category.model_dump()
    )
    if not updated_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return updated_category


@router.delete("/{category_id}", response_model=CategoryResponse)
async def delete_category(
    category_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
):
    deleted_category = await CategoryModel.delete(
        db, category_id=category_id, user_id=current_user_id
    )
    if not deleted_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return deleted_category
