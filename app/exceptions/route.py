from app.exceptions.base import BusinessException


class DuplicateRouteCodeError(BusinessException):
    """Raised when the route code already exists."""

    def __init__(self, route_code: str):

        super().__init__(
            f"Route code '{route_code}' already exists."
        )


class DuplicateRouteNameError(BusinessException):
    """Raised when the route name already exists."""

    def __init__(self, route_name: str):

        super().__init__(
            f"Route name '{route_name}' already exists."
        )


class RouteNotFoundError(BusinessException):
    """Raised when a route cannot be found."""

    def __init__(self):

        super().__init__(
            "Route not found."
        )