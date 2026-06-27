from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.route import (
    RouteCreate,
    RouteResponse,
    RouteUpdate
)

from app.services import route_service

from app.exceptions.route import (
    DuplicateRouteCodeError,
    DuplicateRouteNameError,RouteNotFoundError
)


router = APIRouter(
    prefix="/routes",
    tags=["Routes"]
)

@router.post(
    "/",
    response_model=RouteResponse
)
def create_route(
    route: RouteCreate,
    db: Session = Depends(get_db)
):
    try:

        return route_service.create(
        db,
        route
        )
    except DuplicateRouteCodeError as e:

     raise HTTPException(
        status_code=400,
        detail=str(e)
    )

    except DuplicateRouteNameError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get(
    "/",
    response_model=list[RouteResponse]
)
def get_routes(
    db: Session = Depends(get_db)
):

    return route_service.get_all(
        db
    )

@router.get(
    "/{route_id}",
    response_model=RouteResponse
)
def get_route(
    route_id: int,
    db: Session = Depends(get_db)
):

    try:

        return route_service.get_by_id(
            db,
            route_id
        )

    except RouteNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    
@router.put(
    "/{route_id}",
    response_model=RouteResponse
)
def update_route(
    route_id: int,
    route: RouteUpdate,
    db: Session = Depends(get_db)
):
    try:
        return route_service.update_by_id(
            db,
            route_id,
            route
            )
    except RouteNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except DuplicateRouteCodeError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except DuplicateRouteNameError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.delete(
    "/{route_id}",
    response_model=RouteResponse
)

def delete_route(
    route_id:int,
    db:Session=Depends(get_db)
):
    try:
        return route_service.delete_by_id(
                db,
                route_id
                )
    except RouteNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )