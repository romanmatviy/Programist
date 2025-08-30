#!/usr/bin/env python3
"""
Скрипт для генерації sitemap.xml для сайту programist.matviy.pp.ua
Генерує URL-адреси за схемою /service/geo/city
"""

import os
import datetime
from xml.dom import minidom

# Базовий URL сайту
BASE_URL = "https://programist.matviy.pp.ua"

# Список сервісів
services = [
    "rozrobka-saitiv",
    "internet-magazin",
    "wordpress",
    "prestashop",
    "opencart",
    "laravel",
    "vue",
    "seo-optimizatsiya",
    "pidtrymka-saitiv",
    "crm-erp"
]

# Список гео (поки тільки Україна)
geos = ["ukraine"]

# Список міст
cities = [
    "kyiv",
    "lviv",
    "kharkiv",
    "odesa",
    "dnipro",
    "zaporizhzhia",
    "vinnytsia",
    "poltava",
    "chernivtsi",
    "cherkasy",
    "chernihiv",
    "zhytomyr",
    "ivano-frankivsk",
    "rivne",
    "lutsk",
    "ternopil",
    "mykolaiv",
    "khmelnytskyi",
    "sumy",
    "kropyvnytskyi",
    "uzhorod",
    "kryvyi-rih",
    "mariupol"
]

def generate_sitemap():
    """Генерує sitemap.xml файл"""
    
    # Створюємо XML документ
    doc = minidom.getDOMImplementation().createDocument(None, "urlset", None)
    root = doc.documentElement
    root.setAttribute("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    
    # Поточна дата для lastmod
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Додаємо головну сторінку
    add_url(doc, root, BASE_URL, "1.0", today, "daily")
    
    # Додаємо сторінки сервісів
    for service in services:
        service_url = f"{BASE_URL}/{service}"
        add_url(doc, root, service_url, "0.9", today, "weekly")
        
        # Додаємо сторінки сервіс/гео
        for geo in geos:
            geo_url = f"{service_url}/{geo}"
            add_url(doc, root, geo_url, "0.8", today, "weekly")
            
            # Додаємо сторінки сервіс/гео/місто
            for city in cities:
                city_url = f"{geo_url}/{city}"
                add_url(doc, root, city_url, "0.7", today, "weekly")
    
    # Зберігаємо XML файл
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(doc.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8"))
    
    print(f"Sitemap.xml згенеровано. Всього URL: {count_urls(doc)}")

def add_url(doc, root, loc, priority, lastmod, changefreq):
    """Додає URL до sitemap"""
    url_element = doc.createElement("url")
    
    # URL адреса
    loc_element = doc.createElement("loc")
    loc_text = doc.createTextNode(loc)
    loc_element.appendChild(loc_text)
    url_element.appendChild(loc_element)
    
    # Пріоритет
    priority_element = doc.createElement("priority")
    priority_text = doc.createTextNode(priority)
    priority_element.appendChild(priority_text)
    url_element.appendChild(priority_element)
    
    # Дата останньої модифікації
    lastmod_element = doc.createElement("lastmod")
    lastmod_text = doc.createTextNode(lastmod)
    lastmod_element.appendChild(lastmod_text)
    url_element.appendChild(lastmod_element)
    
    # Частота зміни
    changefreq_element = doc.createElement("changefreq")
    changefreq_text = doc.createTextNode(changefreq)
    changefreq_element.appendChild(changefreq_text)
    url_element.appendChild(changefreq_element)
    
    # Додаємо URL до кореневого елементу
    root.appendChild(url_element)

def count_urls(doc):
    """Підраховує кількість URL у sitemap"""
    return len(doc.getElementsByTagName("url"))

if __name__ == "__main__":
    generate_sitemap()