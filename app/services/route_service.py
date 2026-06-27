from sqlalchemy.orm import Session

from app.models.route import Route
from app.schemas.route import RouteCreate,RouteUpdate

from app.exceptions.route import (
    DuplicateRouteCodeError,
    DuplicateRouteNameError,RouteNotFoundError
)


def create(
    db: Session,
    route: RouteCreate
) -> Route:
    """
    Create a new delivery route.

    Args:
        db: SQLAlchemy database session.
        route: Route creation data.

    Returns:
        Newly created Route.

    Raises:
        DuplicateRouteCodeError:
            If the route code already exists.
        DuplicateRouteNameError:
            If the route name already exists.
    """

    existing_route_code = (
        db.query(Route)
        .filter(
            Route.route_code == route.route_code
        )
        .first()
    )

    if existing_route_code:
        raise DuplicateRouteCodeError(
            route.route_code
        )

    existing_route_name = (
        db.query(Route)
        .filter(
            Route.route_name == route.route_name
        )
        .first()
    )

    if existing_route_name:
        raise DuplicateRouteNameError(
            route.route_name
        )

    new_route = Route(
        route_code=route.route_code,
        route_name=route.route_name,
        description=route.description
    )

    db.add(new_route)

    db.commit()

    db.refresh(new_route)

    return new_route

def get_all(
    db: Session
) -> list[Route]:
    """
    Retrieve all active routes.

    Args:
        db: SQLAlchemy database session.

    Returns:
        List of active routes.
    """

    routes = (
        db.query(Route)
        .filter(
            Route.is_active == True
        )
        .all()
    )

    return routes

def get_by_id(
    db: Session,
    route_id: int
) -> Route:
    """
    Retrieve a route by ID.

    Args:
        db: SQLAlchemy database session.
        route_id: Route ID.

    Returns:
        Route

    Raises:
        RouteNotFoundError
    """

    route = (
        db.query(Route)
        .filter(
            Route.id == route_id,
            Route.is_active == True
        )
        .first()
    )

    if not route:
        raise RouteNotFoundError()

    return route

def update_by_id(
        db:Session,
        route_id:int,
        route:RouteUpdate
)-> Route:
    
    route_to_update = (
        db.query(Route)
        .filter(
            Route.id == route_id,
            Route.is_active == True
        )
        .first()
    )

    if not route_to_update:
        raise RouteNotFoundError()
    
    existing_route_code=(
        db.query(Route).filter(
    Route.route_code == route.route_code,
    Route.id != route_id
    ).first()
)

    if existing_route_code:
        raise DuplicateRouteCodeError(route.route_code)
    
    existing_route_name=(
        db.query(Route).filter(
    Route.route_name == route.route_name,
    Route.id != route_id
    ).first())

    if existing_route_name:
        raise DuplicateRouteNameError(route.route_name)
        
    route_to_update.route_code = route.route_code
    route_to_update.route_name = route.route_name
    route_to_update.description = route.description
    
    db.commit()
    db.refresh(route_to_update)

    return route_to_update

def delete_by_id(
    db: Session,
    route_id: int
) -> Route:
    
    route_to_delete = (
        db.query(Route)
        .filter(
            Route.id == route_id,
            Route.is_active == True
        )
        .first()
    )

    if not route_to_delete:
        raise RouteNotFoundError()
    
    route_to_delete.is_active = False

    db.commit()
    db.refresh(route_to_delete)

    return route_to_delete