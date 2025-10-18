#!/usr/bin/env python3
"""
Скрипт для генерації всіх статичних SEO-сторінок за схемою /service/geo/city
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

def generate_all_static_pages():
    """Генерує всі статичні SEO-сторінки для всіх комбінацій service/geo/city"""
    total_pages = 0
    
    # Створюємо індексні сторінки для сервісів
    for service_slug, service_name in services.items():
        service_dir = os.path.join(BASE_DIR, service_slug)
        create_directory(service_dir)
        
        # Генеруємо індексну сторінку для сервісу
        generate_service_index_page(service_slug, service_name)
        total_pages += 1
        
        # Для кожного гео
        for geo_slug, geo_name in geos.items():
            geo_dir = os.path.join(service_dir, geo_slug)
            create_directory(geo_dir)
            
            # Генеруємо індексну сторінку для гео
            generate_geo_index_page(service_slug, service_name, geo_slug, geo_name)
            total_pages += 1
            
            # Для кожного міста
            for city_slug, city_data in cities.items():
                # Генеруємо сторінку для міста
                generate_city_page(service_slug, service_name, geo_slug, geo_name, city_slug, city_data)
                total_pages += 1
                
                # Виводимо прогрес кожні 10 сторінок
                if total_pages % 10 == 0:
                    print(f"Згенеровано {total_pages} статичних сторінок...")
    
    print(f"Генерація завершена. Всього згенеровано {total_pages} статичних сторінок.")

def generate_service_index_page(service_slug, service_name):
    """Генерує індексну сторінку для сервісу"""
    service_name_lower = service_name.lower()
    service_name_lower_acc = service_accusative.get(service_name_lower, service_name_lower)
    
    # Шаблон для індексної сторінки сервісу
    template = """<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ service_name }} | Програміст Роман (RomanDev)</title>
    <meta name="description" content="Професійні послуги: {{ service_name_lower }}. {{ service_description }} Замовте {{ service_name_lower_acc }} у програміста Романа.">
    
    <!-- Canonical -->
    <link rel="canonical" href="https://programist.matviy.pp.ua/{{ service_slug }}/">
    
    <!-- Favicon -->
    <link rel="icon" href="/img/favicon.ico" type="image/x-icon">
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    
    <!-- Styles -->
    <link rel="stylesheet" href="/css/style.css?ver=1">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{{ service_name }} | Програміст Роман (RomanDev)">
    <meta property="og:description" content="Професійні послуги: {{ service_name_lower }}. {{ service_description }} Замовте {{ service_name_lower_acc }} у програміста Романа.">
    <meta property="og:url" content="https://programist.matviy.pp.ua/{{ service_slug }}/">
    <meta property="og:type" content="website">
    <meta property="og:image" content="/img/og-image.jpg">
</head>
<body>
    <!-- Header -->
    <header>
        <div class="container header-container">
            <a href="/" class="logo">RomanDev</a>
            <nav>
                <ul>
                    <li><a href="/#services">Послуги</a></li>
                    <li><a href="/#portfolio">Портфоліо</a></li>
                    <li><a href="/#about">Про мене</a></li>
                    <li><a href="/#contact">Контакти</a></li>
                </ul>
            </nav>
            <button class="mobile-menu-toggle">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>
    </header>

    <!-- Main Content -->
    <main>
        <div class="container">
            <!-- Breadcrumbs -->
            <div class="breadcrumbs" data-schema="BreadcrumbList">
                <a href="/">Головна</a> <span>></span> 
                <span>{{ service_name }}</span>
            </div>
            
            <!-- SEO Content -->
            <div class="seo-content">
                <h1>{{ service_name }} – професійно під ключ</h1>
                
                <div data-schema="LocalBusiness" 
                     data-name="Програміст Роман" 
                     data-description="Професійні послуги: {{ service_name_lower }}" 
                     data-city="Україна" 
                     data-region="Україна">
                </div>
                
                <div data-schema="Service" 
                     data-service-type="{{ service_name }}" 
                     data-city="Україна" 
                     data-description="Професійні послуги: {{ service_name_lower }}. {{ service_description }}">
                </div>
                
                <p>Потрібні професійні послуги: {{ service_name_lower }}? Програміст Роман пропонує повний спектр послуг для вашого бізнесу. {{ service_content }} Замовляючи {{ service_name_lower_acc }}, ви отримуєте ефективне рішення, яке приносить результат.</p>
                
                <h2>Послуги: {{ service_name_lower }}</h2>
                <p>Як професійний розробник, я пропоную широкий спектр послуг для бізнесу. Моя мета – створити не просто {{ service_name_lower_acc }}, а ефективний інструмент для залучення клієнтів та збільшення продажів. Кожен проект розробляється з урахуванням специфіки вашого бізнесу та потреб цільової аудиторії.</p>
                
                {{ service_specific_content }}
                
                <h2>Технології, які я використовую</h2>
                <p>У роботі я використовую сучасні технології та фреймворки:</p>
                <ul>
                    <li><strong>Laravel</strong> – потужний PHP-фреймворк для створення складних веб-додатків</li>
                    <li><strong>WordPress</strong> – найпопулярніша CMS для створення сайтів різної складності</li>
                    <li><strong>PrestaShop</strong> – спеціалізована платформа для створення інтернет-магазинів</li>
                    <li><strong>OpenCart</strong> – гнучка система для електронної комерції</li>
                    <li><strong>Vue.js</strong> – прогресивний JavaScript-фреймворк для створення інтерактивних інтерфейсів</li>
                </ul>
                
                <h2>Переваги замовлення послуг у мене</h2>
                <p>Обираючи мої послуги, ви отримуєте ряд переваг:</p>
                <ul>
                    <li>Індивідуальний підхід до кожного проекту</li>
                    <li>Оптимальне співвідношення ціни та якості</li>
                    <li>Дотримання термінів виконання</li>
                    <li>Підтримка після завершення проекту</li>
                    <li>Можливість подальшого розвитку проекту</li>
                </ul>
                
                <h2>Етапи роботи</h2>
                <p>Процес роботи включає наступні етапи:</p>
                <ol>
                    <li><strong>Аналіз вимог</strong> – визначення цілей, аудиторії та функціоналу</li>
                    <li><strong>Прототипування</strong> – створення структури та макетів</li>
                    <li><strong>Дизайн</strong> – розробка унікального візуального оформлення</li>
                    <li><strong>Розробка</strong> – реалізація функціоналу</li>
                    <li><strong>Тестування</strong> – перевірка працездатності</li>
                    <li><strong>Запуск</strong> – розміщення та налаштування</li>
                    <li><strong>Підтримка</strong> – подальший розвиток та обслуговування</li>
                </ol>
                
                <h2>SEO-оптимізація</h2>
                <p>Всі мої проекти створюються з урахуванням вимог пошукових систем. Це дозволяє досягти високих позицій у результатах пошуку за ключовими запитами, пов'язаними з вашим бізнесом. SEO-оптимізація включає:</p>
                <ul>
                    <li>Технічну оптимізацію</li>
                    <li>Створення SEO-friendly структури</li>
                    <li>Оптимізацію швидкості завантаження</li>
                    <li>Адаптивний дизайн для мобільних пристроїв</li>
                    <li>Налаштування мета-тегів та мікророзмітки</li>
                </ul>
                
                <h2>Вартість послуг</h2>
                <p>Ціна послуг залежить від складності проекту, необхідного функціоналу та термінів виконання. Для отримання точної вартості, зв'яжіться зі мною для безкоштовної консультації. Я пропоную конкурентні ціни на послуги, зберігаючи високу якість виконання.</p>
                
                <h2>{{ service_name }} за регіонами</h2>
                <p>Я надаю послуги з {{ service_name_lower }} у різних регіонах:</p>
                <ul class="regions-list">
                    <li><a href="/{{ service_slug }}/ukraine">{{ service_name }} в Україні</a></li>
                </ul>
            </div>
        </div>
        
        <!-- CTA Section -->
        <section class="cta-section">
            <div class="container">
                <h2>Готові замовити {{ service_name_lower_acc }}?</h2>
                <p>Зв'яжіться зі мною для безкоштовної консультації та оцінки вашого проекту</p>
                <a href="/#contact" class="btn">Замовити консультацію</a>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer>
        <div class="container">
            <div class="footer-container">
                <div class="footer-col">
                    <h3>Послуги</h3>
                    <ul>
                        <li><a href="/rozrobka-saitiv/ukraine">Розробка сайтів</a></li>
                        <li><a href="/internet-magazin/ukraine">Інтернет-магазини</a></li>
                        <li><a href="/wordpress/ukraine">WordPress розробка</a></li>
                        <li><a href="/laravel/ukraine">Laravel розробка</a></li>
                        <li><a href="/crm-erp/ukraine">CRM/ERP системи</a></li>
                        <li><a href="/seo-optimizatsiya/ukraine">SEO-оптимізація</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h3>Міста</h3>
                    <ul>
                        <li><a href="/{{ service_slug }}/ukraine/kyiv">Київ</a></li>
                        <li><a href="/{{ service_slug }}/ukraine/lviv">Львів</a></li>
                        <li><a href="/{{ service_slug }}/ukraine/kharkiv">Харків</a></li>
                        <li><a href="/{{ service_slug }}/ukraine/odesa">Одеса</a></li>
                        <li><a href="/{{ service_slug }}/ukraine/dnipro">Дніпро</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h3>Контакти</h3>
                    <ul>
                        <li>Телефон: <a href="tel:+380938800822">+38 (093) 88-00-822</a></li>
                        <li>Email: <a href="mailto:info@matviy.pp.ua">info@matviy.pp.ua</a></li>
                    </ul>
                </div>
            </div>
            <div class="copyright">
                &copy; 2025 Програміст Роман. Всі права захищені.
            </div>
        </div>
    </footer>

    <!-- Scripts -->
    <script src="/js/main.js?ver=1"></script>
</body>
</html>
"""
    
    # Заповнюємо шаблон
    page_content = template
    page_content = page_content.replace("{{ service_slug }}", service_slug)
    page_content = page_content.replace("{{ service_name }}", service_name)
    page_content = page_content.replace("{{ service_name_lower }}", service_name_lower)
    page_content = page_content.replace("{{ service_name_lower_acc }}", service_name_lower_acc)
    page_content = page_content.replace("{{ service_description }}", service_descriptions[service_slug])
    page_content = page_content.replace("{{ service_content }}", service_contents[service_slug])
    
    # Додаємо специфічний контент для сервісу
    specific_content = service_specific_content.get(service_slug, "")
    specific_content = specific_content.replace("{{ city_in }}", "")
    page_content = page_content.replace("{{ service_specific_content }}", specific_content)
    
    # Зберігаємо файл
    index_path = os.path.join(BASE_DIR, service_slug, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(page_content)
    
    print(f"Згенеровано індексну сторінку для сервісу: {service_name}")

def generate_geo_index_page(service_slug, service_name, geo_slug, geo_name):
    """Генерує індексну сторінку для гео"""
    service_name_lower = service_name.lower()
    service_name_lower_acc = service_accusative.get(service_name_lower, service_name_lower)
    
    # Шаблон для індексної сторінки гео
    template = """<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ service_name }} в {{ geo_name }} | Програміст Роман (RomanDev)</title>
    <meta name="description" content="Професійні послуги: {{ service_name_lower }} в {{ geo_name }}. {{ service_description }} Замовте {{ service_name_lower_acc }} у програміста Романа.">
    
    <!-- Canonical -->
    <link rel="canonical" href="https://programist.matviy.pp.ua/{{ service_slug }}/{{ geo_slug }}/">
    
    <!-- Favicon -->
    <link rel="icon" href="/img/favicon.ico" type="image/x-icon">
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    
    <!-- Styles -->
    <link rel="stylesheet" href="/css/style.css?ver=1">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{{ service_name }} в {{ geo_name }} | Програміст Роман (RomanDev)">
    <meta property="og:description" content="Професійні послуги: {{ service_name_lower }} в {{ geo_name }}. {{ service_description }} Замовте {{ service_name_lower_acc }} у програміста Романа.">
    <meta property="og:url" content="https://programist.matviy.pp.ua/{{ service_slug }}/{{ geo_slug }}/">
    <meta property="og:type" content="website">
    <meta property="og:image" content="/img/og-image.jpg">
</head>
<body>
    <!-- Header -->
    <header>
        <div class="container header-container">
            <a href="/" class="logo">RomanDev</a>
            <nav>
                <ul>
                    <li><a href="/#services">Послуги</a></li>
                    <li><a href="/#portfolio">Портфоліо</a></li>
                    <li><a href="/#about">Про мене</a></li>
                    <li><a href="/#contact">Контакти</a></li>
                </ul>
            </nav>
            <button class="mobile-menu-toggle">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>
    </header>

    <!-- Main Content -->
    <main>
        <div class="container">
            <!-- Breadcrumbs -->
            <div class="breadcrumbs" data-schema="BreadcrumbList">
                <a href="/">Головна</a> <span>></span> 
                <a href="/{{ service_slug }}">{{ service_name }}</a> <span>></span> 
                <span>{{ geo_name }}</span>
            </div>
            
            <!-- SEO Content -->
            <div class="seo-content">
                <h1>{{ service_name }} в {{ geo_name }} – професійно під ключ</h1>
                
                <div data-schema="LocalBusiness" 
                     data-name="Програміст Роман" 
                     data-description="Професійні послуги: {{ service_name_lower }} в {{ geo_name }}" 
                     data-city="{{ geo_name }}" 
                     data-region="{{ geo_name }}">
                </div>
                
                <div data-schema="Service" 
                     data-service-type="{{ service_name }}" 
                     data-city="{{ geo_name }}" 
                     data-description="Професійні послуги: {{ service_name_lower }} в {{ geo_name }}. {{ service_description }}">
                </div>
                
                <p>Потрібні професійні послуги: {{ service_name_lower }} в {{ geo_name }}? Програміст Роман пропонує повний спектр послуг для вашого бізнесу. {{ service_content }} Замовляючи {{ service_name_lower_acc }} в {{ geo_name }}, ви отримуєте ефективне рішення, яке приносить результат.</p>
                
                <h2>Послуги: {{ service_name_lower }} в {{ geo_name }}</h2>
                <p>Як професійний розробник в {{ geo_name }}, я пропоную широкий спектр послуг для бізнесу. Моя мета – створити не просто {{ service_name_lower_acc }}, а ефективний інструмент для залучення клієнтів та збільшення продажів. Кожен проект розробляється з урахуванням специфіки вашого бізнесу та потреб цільової аудиторії.</p>
                
                {{ service_specific_content }}
                
                <h2>Технології, які я використовую</h2>
                <p>У роботі в {{ geo_name }} я використовую сучасні технології та фреймворки:</p>
                <ul>
                    <li><strong>Laravel</strong> – потужний PHP-фреймворк для створення складних веб-додатків</li>
                    <li><strong>WordPress</strong> – найпопулярніша CMS для створення сайтів різної складності</li>
                    <li><strong>PrestaShop</strong> – спеціалізована платформа для створення інтернет-магазинів</li>
                    <li><strong>OpenCart</strong> – гнучка система для електронної комерції</li>
                    <li><strong>Vue.js</strong> – прогресивний JavaScript-фреймворк для створення інтерактивних інтерфейсів</li>
                </ul>
                
                <h2>Переваги замовлення послуг в {{ geo_name }}</h2>
                <p>Обираючи мої послуги в {{ geo_name }}, ви отримуєте ряд переваг:</p>
                <ul>
                    <li>Розуміння місцевого ринку та його особливостей</li>
                    <li>Оптимальне співвідношення ціни та якості</li>
                    <li>Дотримання термінів виконання</li>
                    <li>Підтримка після завершення проекту</li>
                    <li>Можливість подальшого розвитку проекту</li>
                </ul>
                
                <h2>Етапи роботи в {{ geo_name }}</h2>
                <p>Процес роботи включає наступні етапи:</p>
                <ol>
                    <li><strong>Аналіз вимог</strong> – визначення цілей, аудиторії та функціоналу</li>
                    <li><strong>Прототипування</strong> – створення структури та макетів</li>
                    <li><strong>Дизайн</strong> – розробка унікального візуального оформлення</li>
                    <li><strong>Розробка</strong> – реалізація функціоналу</li>
                    <li><strong>Тестування</strong> – перевірка працездатності</li>
                    <li><strong>Запуск</strong> – розміщення та налаштування</li>
                    <li><strong>Підтримка</strong> – подальший розвиток та обслуговування</li>
                </ol>
                
                <h2>SEO-оптимізація в {{ geo_name }}</h2>
                <p>Всі мої проекти створюються з урахуванням вимог пошукових систем. Це дозволяє досягти високих позицій у результатах пошуку за ключовими запитами, пов'язаними з вашим бізнесом в {{ geo_name }}. SEO-оптимізація включає:</p>
                <ul>
                    <li>Технічну оптимізацію</li>
                    <li>Створення SEO-friendly структури</li>
                    <li>Оптимізацію швидкості завантаження</li>
                    <li>Адаптивний дизайн для мобільних пристроїв</li>
                    <li>Налаштування мета-тегів та мікророзмітки</li>
                </ul>
                
                <h2>Вартість послуг в {{ geo_name }}</h2>
                <p>Ціна послуг залежить від складності проекту, необхідного функціоналу та термінів виконання. Для отримання точної вартості, зв'яжіться зі мною для безкоштовної консультації. Я пропоную конкурентні ціни на послуги в {{ geo_name }}, зберігаючи високу якість виконання.</p>
                
                <h2>{{ service_name }} у містах {{ geo_name }}</h2>
                <p>Я надаю послуги з {{ service_name_lower }} у всіх містах {{ geo_name }}. Ви можете замовити {{ service_name_lower_acc }} в таких містах:</p>
                <ul class="cities-list">
                    {{ cities_list }}
                </ul>
            </div>
        </div>
        
        <!-- CTA Section -->
        <section class="cta-section">
            <div class="container">
                <h2>Готові замовити {{ service_name_lower_acc }} в {{ geo_name }}?</h2>
                <p>Зв'яжіться зі мною для безкоштовної консультації та оцінки вашого проекту</p>
                <a href="/#contact" class="btn">Замовити консультацію</a>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer>
        <div class="container">
            <div class="footer-container">
                <div class="footer-col">
                    <h3>Послуги</h3>
                    <ul>
                        <li><a href="/rozrobka-saitiv/ukraine">Розробка сайтів</a></li>
                        <li><a href="/internet-magazin/ukraine">Інтернет-магазини</a></li>
                        <li><a href="/wordpress/ukraine">WordPress розробка</a></li>
                        <li><a href="/laravel/ukraine">Laravel розробка</a></li>
                        <li><a href="/crm-erp/ukraine">CRM/ERP системи</a></li>
                        <li><a href="/seo-optimizatsiya/ukraine">SEO-оптимізація</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h3>Міста</h3>
                    <ul>
                        <li><a href="/{{ service_slug }}/{{ geo_slug }}/kyiv">Київ</a></li>
                        <li><a href="/{{ service_slug }}/{{ geo_slug }}/lviv">Львів</a></li>
                        <li><a href="/{{ service_slug }}/{{ geo_slug }}/kharkiv">Харків</a></li>
                        <li><a href="/{{ service_slug }}/{{ geo_slug }}/odesa">Одеса</a></li>
                        <li><a href="/{{ service_slug }}/{{ geo_slug }}/dnipro">Дніпро</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h3>Контакти</h3>
                    <ul>
                        <li>Телефон: <a href="tel:+380938800822">+38 (093) 88-00-822</a></li>
                        <li>Email: <a href="mailto:info@matviy.pp.ua">info@matviy.pp.ua</a></li>
                    </ul>
                </div>
            </div>
            <div class="copyright">
                &copy; 2025 Програміст Роман. Всі права захищені.
            </div>
        </div>
    </footer>

    <!-- Scripts -->
    <script src="/js/main.js?ver=1"></script>
</body>
</html>
"""
    
    # Генеруємо список міст
    cities_list = ""
    for city_slug, city_data in cities.items():
        city_name = city_data["name"]
        cities_list += f'<li><a href="/{service_slug}/{geo_slug}/{city_slug}">{service_name} у {city_name}</a></li>\n'
    
    # Заповнюємо шаблон
    page_content = template
    page_content = page_content.replace("{{ service_slug }}", service_slug)
    page_content = page_content.replace("{{ geo_slug }}", geo_slug)
    page_content = page_content.replace("{{ service_name }}", service_name)
    page_content = page_content.replace("{{ service_name_lower }}", service_name_lower)
    page_content = page_content.replace("{{ service_name_lower_acc }}", service_name_lower_acc)
    page_content = page_content.replace("{{ geo_name }}", geo_name)
    page_content = page_content.replace("{{ service_description }}", service_descriptions[service_slug])
    page_content = page_content.replace("{{ service_content }}", service_contents[service_slug])
    page_content = page_content.replace("{{ cities_list }}", cities_list)
    
    # Додаємо специфічний контент для сервісу
    specific_content = service_specific_content.get(service_slug, "")
    specific_content = specific_content.replace("{{ city_in }}", f"в {geo_name}")
    page_content = page_content.replace("{{ service_specific_content }}", specific_content)
    
    # Зберігаємо файл
    index_path = os.path.join(BASE_DIR, service_slug, geo_slug, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(page_content)
    
    print(f"Згенеровано індексну сторінку для {service_name} в {geo_name}")

def generate_city_page(service_slug, service_name, geo_slug, geo_name, city_slug, city_data):
    """Генерує сторінку для міста"""
    service_name_lower = service_name.lower()
    service_name_lower_acc = service_accusative.get(service_name_lower, service_name_lower)
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
    
    # print(f"Згенеровано сторінку для {service_name} {city_in}")

if __name__ == "__main__":
    generate_all_static_pages()