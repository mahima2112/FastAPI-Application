import requests
from bs4 import BeautifulSoup
import time
from utils.retry import retry_request
from models.product import Product

class ProductScraper:
    def __init__(self, cache, db, notifier):
        self.cache = cache
        self.db = db
        self.notifier = notifier
        self.base_url = "https://dentalstall.com/shop/"
    
    def scrape(self, pages_limit: int, proxy: str = None):
        headers = {"User-Agent": "Mozilla/5.0"}
        proxies = {"http": proxy, "https": proxy} if proxy else None
        products = []
        for page in range(1, pages_limit + 1):
            url = f"{self.base_url}?page={page}"
            try:
                response = retry_request(url, headers=headers, proxies=proxies)
                soup = BeautifulSoup(response.text, "lxml")
                
                product_elements = soup.find_all("div", class_="product")
                for product_element in product_elements:
                    product = self.extract_product_info(product_element)
                    if product and not self.cache.is_cached(product):
                        products.append(product)
                        self.cache.cache_product(product)
                        self.db.save_product(product)
            except Exception as e:
                print(f"Failed to scrape page {page}: {str(e)}")
        
        self.notifier.notify(len(products))
        return len(products)
    
    def extract_product_info(self, element):
        try:
            name = element.find("h2").text
            price = float(element.find("span", class_="price").text.replace("$", ""))
            image_url = element.find("img")["src"]
            product = Product(name=name, price=price, image_url=image_url)
            return product
        except Exception as e:
            print(f"Error extracting product: {e}")
            return None
