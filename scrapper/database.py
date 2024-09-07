import json

class FileDatabase:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save_product(self, product):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        
        data.append({
            "product_title": product.name,
            "product_price": product.price,
            "path_to_image": product.image_url
        })
        
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)
