class DeliveryExceptionNotFoundError(Exception):

    def __init__(self):
        super().__init__(
            "Delivery exception not found."
        )


class InactiveDeliveryExceptionError(Exception):

    def __init__(self):
        super().__init__(
            "Delivery exception is inactive."
        )


class OverlappingDeliveryExceptionError(Exception):

    def __init__(self):
        super().__init__(
            "An active delivery exception already exists for the selected date range."
        )


class InvalidDateRangeError(Exception):

    def __init__(self):
        super().__init__(
            "End date cannot be earlier than start date."
        )


class PastDateNotAllowedError(Exception):

    def __init__(self):
        super().__init__(
            "Delivery exceptions cannot be created for past dates."
        )