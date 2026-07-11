class CustomerSubscriptionNotFoundError(Exception):

    def __init__(self):
        super().__init__(
            "Customer subscription not found."
        )


class DuplicateSubscriptionError(Exception):

    def __init__(self):
        super().__init__(
            "An active subscription already exists for the selected customer, milk type, and shift."
        )