class MilkTypeNotFoundError(Exception):

    def __init__(self):
        super().__init__("Milk type not found.")


class DuplicateMilkTypeNameError(Exception):

    def __init__(self, name: str):
        super().__init__(
            f"Milk type '{name}' already exists."
        )


class DuplicateQuantityError(Exception):

    def __init__(self, quantity_ml: int):
        super().__init__(
            f"Milk type with quantity '{quantity_ml} ml' already exists."
        )


class InactiveMilkTypeError(Exception):

    def __init__(self):
        super().__init__(
            "Milk type is inactive."
        )