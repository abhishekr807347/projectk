import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def scrape_product_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    product_description = soup.find("div", class_="product-description").text.strip()
    asin = soup.find("span", text="ASIN").find_next("span").text.strip()
    manufacturer = soup.find("span", text="Manufacturer").find_next("span").text.strip()

    return {
        "Description": product_description,
        "ASIN": asin,
        "Product Description": product_description,
        "Manufacturer": manufacturer
    }


def scrape_product_listing(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    products = []
    product_tags = soup.find_all("div", class_="product")

    for product_tag in product_tags:
        product_url = product_tag.find("a", class_="product-url")["href"]
        product_name = product_tag.find("h2", class_="product-title").text.strip()
        product_price = product_tag.find("span", class_="product-price").text.strip()
        product_rating = product_tag.find("span", class_="product-rating").text.strip()
        num_reviews = product_tag.find("span", class_="product-reviews").text.strip()

        product_details = scrape_product_details(product_url)
        product_info = {
            "Product URL": product_url,
            "Product Name": product_name,
            "Product Price": product_price,
            "Rating": product_rating,
            "Number of Reviews": num_reviews,
            **product_details
        }
        products.append(product_info)
        time.sleep(1)  

    return products

if __name__ == "__main__":
   
   
    product_list = []
    for page_number in range(1, 21):
        url_to_scrape = f"URL_TO_PRODUCT_LISTING&page={page_number}"
        product_list.extend(scrape_product_listing(url_to_scrape))

    
    df = pd.DataFrame(product_list)
    df.to_csv("product_data.csv", index=False)

    print("Scraping and CSV export complete!")
