import requests
from bs4 import BeautifulSoup

URL = "https://castore.uz"
HOST = "https://castore.uz"

HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
}

def get_soup(link):
    response = requests.get(link, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def get_category():
    soup = get_soup(URL)
    categories = soup.find("div", class_="desc-catalog-block").find_all("div")
    data = [
        {
            "title": category.get_text().strip(),
            "link": HOST + category.find("div", class_="l-side-catalog-item").find("a").get("href")
            if category.find("div", class_="l-side-catalog-item") and category.find("div", class_="l-side-catalog-item").find("a")
            else None,
        }
        for category in categories
    ]
    return data

def get_products(category, link):
    soup = get_soup(link)
    sections = soup.find("div", class_="l-side-catalog-item")
    products = sections.find_all("div", class_="product_slider-card product js_gtm")
    print(products)
    data = []
    for product in products:
        title = product.find("a", class_="product_slider-name")
        price = product.find("div", class_="price")
        img = product.find("img")

        data.append({
            "Title": title.get_text().strip() if title else "N/A",
            "link": title.get("href").strip() if title and title.has_attr("href") else "N/A",
            "img": img.get("src").strip() if img and img.has_attr("src") else "N/A",
            "price": price.text.strip() if price else "N/A",
        })
    print(data)
    return data

get_products(get_category(), URL)
