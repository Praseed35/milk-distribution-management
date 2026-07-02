class CustomerNotFoundError(Exception):

    def __init__(self):
        super().__init__(
            "Customer not found."
        )


class DuplicatePrimaryPhoneError(Exception):

    def __init__(self, phone: str):
        super().__init__(
            f"Primary phone '{phone}' already exists."
        )


class DuplicateCustomerCodeError(Exception):

    def __init__(self, customer_code: str):
        super().__init__(
            f"Customer code '{customer_code}' already exists."
        )

class SamePhoneNumberError(Exception):

    def __init__(self):
        super().__init__(
            "Primary phone and alternate phone cannot be the same."
        )