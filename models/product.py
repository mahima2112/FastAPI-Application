class Product:
    def __init__(self, name: str, price: float, image_url: str):
        self.name = name
        self.price = price
        self.image_url = image_url

    def __repr__(self):
        return f"Product(name={self.name}, price={self.price}, image_url={self.image_url})"
