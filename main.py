from fastapi import FastAPI, Depends, HTTPException
from scrapper.scrapper import ProductScraper
from scrapper.database import FileDatabase
from utils.notifications import ConsoleNotifier
from utils.cache import RedisCache

app = FastAPI()


@app.get("/scrape")
def scrape_catalogue(pages_limit: int = 5, proxy: str = None):
    cache = RedisCache()
    db = FileDatabase(file_path="scraped_products.json")
    notifier = ConsoleNotifier()
    
    scraper = ProductScraper(cache=cache, db=db, notifier=notifier)
    
    scraped_count = scraper.scrape(pages_limit=pages_limit, proxy=proxy)
    
    return {"message": f"Scraped {scraped_count} products"}
