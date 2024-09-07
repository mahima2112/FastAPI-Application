import requests
import time

def retry_request(url, headers, proxies=None, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            if response.status_code == 200:
                return response
        except requests.RequestException as e:
            print(f"Request failed: {str(e)}")
        time.sleep(delay)
    raise Exception(f"Failed to retrieve {url} after {retries} attempts")
