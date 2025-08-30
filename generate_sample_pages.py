#!/usr/bin/env python3
"""
Скрипт для генерації прикладів SEO-сторінок для категорії "Розробка сайтів"
"""

import os
import shutil
import re
from generate_seo_pages import (
    services, geos, cities, PAGE_TEMPLATE, service_specific_content,
    service_descriptions, service_contents, service_accusative,
    generate_related_services, create_directory
)

# Базова директорія проекту
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_sample_pages():
    """Генерує приклади SEO-сторінок для категорії "Розробка сайтів" для кількох міст"""
    service_slug = "rozrobka-saitiv"
    service_name = services[service_slug]
    service_name_lower = service_name.lower()
    service_name_lower_acc = service_accusative.get(service_name_lower, service_name_lower)
    geo_slug = "ukraine"
    geo_name = geos[geo_slug]
    
    # Вибрані міста для прикладів
    sample_cities = ["kyiv", "lviv", "kharkiv", "odesa", "dnipro"]
    
    total_pages = 0
    
    for city_slug in sample_cities:
        city_data = cities[city_slug]
        city_name = city_data["name"]
        city_in = city_data["in"]
        
        # Створюємо директорію для міста
        city_dir = os.path.join(BASE_DIR, service_slug, geo_slug, city_slug)
        create_directory(city_dir)
        
        # Заповнюємо шаблон
        page_content = PAGE_TEMPLATE
        page_content = page_content.replace("{{ service_slug }}", service_slug)
        page_content = page_content.replace("{{ geo_slug }}", geo_slug)
        page_content = page_content.replace("{{ city_slug }}", city_slug)
        page_content = page_content.replace("{{ service_name }}", service_name)
        page_content = page_content.replace("{{ service_name_lower }}", service_name_lower)
        page_content = page_content.replace("{{ service_name_lower_acc }}", service_name_lower_acc)
        page_content = page_content.replace("{{ geo_name }}", geo_name)
        page_content = page_content.replace("{{ city_name }}", city_name)
        page_content = page_content.replace("{{ city_in }}", city_in)
        page_content = page_content.replace("{{ service_description }}", service_descriptions[service_slug])
        page_content = page_content.replace("{{ service_content }}", service_contents[service_slug])
        
        # Додаємо специфічний контент для сервісу
        specific_content = service_specific_content.get(service_slug, "")
        specific_content = specific_content.replace("{{ city_in }}", city_in)
        page_content = page_content.replace("{{ service_specific_content }}", specific_content)
        
        # Додаємо пов'язані послуги
        related_services = generate_related_services(service_slug, geo_slug, city_slug)
        page_content = page_content.replace("{{ related_services }}", related_services)
        
        # Зберігаємо файл
        index_path = os.path.join(city_dir, "index.html")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(page_content)
        
        total_pages += 1
        print(f"Згенеровано сторінку для міста {city_name}")
    
    print(f"Генерація завершена. Всього згенеровано {total_pages} прикладів SEO-сторінок.")

if __name__ == "__main__":
    generate_sample_pages()