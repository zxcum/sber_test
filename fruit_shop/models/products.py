class Product:
    def __init__(self):
        self.quantity: int
        self.name: str


class Fruit(Product):
    pass


class Pear(Fruit):
    def __init__(self):
        super().__init__()
        self.name = "Pear"

    def __str__(self):
        return self.name


class Apple(Fruit):
    def __init__(self):
        super().__init__()
        self.name = "Apple"

    def __str__(self):
        return self.name


class Orange(Fruit):
    def __init__(self):
        super().__init__()
        self.name = "Orange"

    def __str__(self):
        return self.name


class Tangerine(Fruit):
    def __init__(self):
        super().__init__()
        self.name = "Tangerine"

    def __str__(self):
        return self.name


class Pineapple(Fruit):
    def __init__(self):
        super().__init__()
        self.name = "Pineapple"

    def __str__(self):
        return self.name
