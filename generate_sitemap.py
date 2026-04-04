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
    "nextjs",
    "nodejs",
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
    
    # Поточна дата та час для lastmod у форматі ISO 8601
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    
    urls = []
    
    # Додаємо головну сторінку
    urls.append(format_url(f"{BASE_URL}/", "1.00", now))
    
    # Додаємо факультативні сторінки
    if os.path.exists("faq.html"):
        urls.append(format_url(f"{BASE_URL}/faq.html", "0.80", now))
    
    # Додаємо сторінки сервісів
    for service in services:
        service_url = f"{BASE_URL}/{service}/"
        urls.append(format_url(service_url, "0.90", now))
        
        # Додаємо сторінки сервіс/гео
        for geo in geos:
            geo_url = f"{BASE_URL}/{service}/{geo}/"
            urls.append(format_url(geo_url, "0.85", now))
            
            # Додаємо сторінки сервіс/гео/місто
            for city in cities:
                city_url = f"{BASE_URL}/{service}/{geo}/{city}/"
                urls.append(format_url(city_url, "0.70", now))
    
    # Зберігаємо XML файл з точним форматуванням, яке просив користувач
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset\n'
    xml_content += '      xmlns="https://www.sitemaps.org/schemas/sitemap/0.9"\n'
    xml_content += '      xmlns:xsi="https://www.w3.org/2001/XMLSchema-instance"\n'
    xml_content += '      xsi:schemaLocation="https://www.sitemaps.org/schemas/sitemap/0.9\n'
    xml_content += '            https://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">\n'
    xml_content += "".join(urls)
    xml_content += "</urlset>"
    
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(xml_content)
    
    print(f"Sitemap.xml згенеровано. Всього URL: {len(urls)}")

def format_url(loc, priority, lastmod):
    """Форматує URL у XML блок з порядком: loc, lastmod, priority"""
    return f"""<url>
  <loc>{loc}</loc>
  <lastmod>{lastmod}</lastmod>
  <priority>{priority}</priority>
</url>
"""

def count_urls(doc):
    """Підраховує кількість URL у sitemap (залишено для сумісності, якщо треба)"""
    return len(doc.getElementsByTagName("url"))

if __name__ == "__main__":
    generate_sitemap()