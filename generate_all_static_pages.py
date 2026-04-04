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
    
    # Шаблон для індексної сторінки сервісу (Microdata)
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
    <link rel="icon" href="https://programist.matviy.pp.ua/img/favicon.ico" type="image/x-icon">
    
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
                    <li><a href="/faq.html">FAQ</a></li>
                    <li><a href="/#contact">Контакти</a></li>
                </ul>
            </nav>
            <button class="mobile-menu-toggle" aria-label="Меню">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>
    </header>

    <!-- Main Content -->
    <main itemscope itemtype="https://schema.org/ProfessionalService">
        <meta itemprop="name" content="Програміст Роман - {{ service_name }}">
        <meta itemprop="description" content="Професійні послуги: {{ service_name_lower }}. {{ service_description }}">
        <link itemprop="url" href="https://programist.matviy.pp.ua/{{ service_slug }}/">
        <link itemprop="image" href="https://programist.matviy.pp.ua/img/og-image.jpg">
        <meta itemprop="telephone" content="+380938800822">
        <div itemprop="address" itemscope itemtype="https://schema.org/PostalAddress">
            <meta itemprop="addressLocality" content="Україна">
            <meta itemprop="addressCountry" content="UA">
        </div>
        <div itemprop="aggregateRating" itemscope itemtype="https://schema.org/AggregateRating">
            <meta itemprop="ratingValue" content="5">
            <meta itemprop="reviewCount" content="24">
        </div>

        <div class="container">
            <!-- Breadcrumbs -->
            <div class="breadcrumbs">
                <nav aria-label="Breadcrumb">
                    <ol itemscope itemtype="https://schema.org/BreadcrumbList" style="list-style: none; padding: 0; display: flex; gap: 5px;">
                        <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
                            <a itemprop="item" href="/">
                                <span itemprop="name">Головна</span>
                            </a>
                            <meta itemprop="position" content="1">
                        </li>
                        <span>></span>
                        <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
                            <span itemprop="name">{{ service_name }}</span>
                            <meta itemprop="position" content="2">
                        </li>
                    </ol>
                </nav>
            </div>
            
            <!-- SEO Content -->
            <div class="seo-content">
                <h1>{{ service_name }} – професійно під ключ</h1>
                
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
                    <li><strong>Next.js</strong> – потужний React-фреймворк для швидких та SEO-оптимізованих сайтів</li>
                    <li><strong>Node.js</strong> – високопродуктивна платформа для серверних рішень та API</li>
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
                
                <h2>SEO оптимізація</h2>
                <p>Всі мої проекти створюються з урахуванням вимог пошукових систем. Це дозволяє досягти високих позицій у результатах пошуку за ключовими запитами, пов'язаними з вашим бізнесом. SEO оптимізація включає:</p>
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
                    <li><a href="/{{ service_slug }}/ukraine/">{{ service_name }} в Україні</a></li>
                </ul>
            </div>
        </div>

        <!-- Testimonials Section -->
        <section id="testimonials" class="testimonials">
            <div class="container">
                <h2 class="section-title">Відгуки клієнтів</h2>
                <div class="testimonials-grid">
                    <div class="testimonial-card">
                        <div class="stars">★★★★★</div>
                        <p class="testimonial-text">Роман розробив для нас інтернет-магазин на PrestaShop. Все було зроблено професійно та в термін. Особливо вражений увагою до SEO-деталей та швидкістю роботи сайту.</p>
                        <div class="testimonial-author">
                            <span class="author-name">Олександр Ковальчук</span>
                            <span class="author-role">Власник магазину TechShop</span>
                        </div>
                    </div>
                    <div class="testimonial-card">
                        <div class="stars">★★★★★</div>
                        <p class="testimonial-text">Працюємо з Романом над підтримкою нашого корпоративного сайту на Laravel. Дуже задоволені оперативністю та якістю коду. Рекомендую як надійного розробника.</p>
                        <div class="testimonial-author">
                            <span class="author-name">Марина Мельник</span>
                            <span class="author-role">Маркетинг-директор AgroGroup</span>
                        </div>
                    </div>
                    <div class="testimonial-card">
                        <div class="stars">★★★★★</div>
                        <p class="testimonial-text">Замовляли SEO-оптимізацію та редизайн сайту на WordPress. Позиції в Google значно виросли вже за перший місяць після запуску нової версії. Дякуємо за роботу!</p>
                        <div class="testimonial-author">
                            <span class="author-name">Сергій Притула</span>
                            <span class="author-role">Співзасновник Creative Agency</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- CTA Section -->
        <section class="cta-section">
            <div class="container">
                <h2>Готові замовити {{ service_name_lower_acc }}?</h2>
                <p>Зв'яжіться зі мною для безкоштовної консультації та оцінки вашого проекту</p>
                <a href="/#contact" class="btn">Замовити консультацію</a>
            </div>
        </section>

        <!-- Other Projects Section -->
        <section class="other-projects">
            <div class="container">
                <h2 class="section-title">Корисні сервіси та мої проєкти</h2>
                <div class="projects-grid">
                    <div class="project-item">
                        <a href="https://monitortest.pp.ua" target="_blank" rel="noopener">Monitor Test — Тестування монітора</a>
                    </div>
                    <div class="project-item">
                        <a href="https://keytest.pp.ua" target="_blank" rel="noopener">Key Test — Тестування клавіатури</a>
                    </div>
                    <div class="project-item">
                        <a href="https://php.apartner.pro" target="_blank" rel="noopener">PHP Course — Курс програмування</a>
                    </div>
                    <div class="project-item">
                        <a href="https://hostpro.apartner.pro/" target="_blank" rel="noopener">HostPro — Надійний хостинг</a>
                    </div>
                    <div class="project-item">
                        <a href="https://programist.pp.ua" target="_blank" rel="noopener">Programist.pp.ua — Послуги програміста</a>
                    </div>
                    <div class="project-item">
                        <a href="https://hire-web-developer.com" target="_blank" rel="noopener">Hire Web Developer — Веб-розробка</a>
                    </div>
                    <div class="project-item">
                        <a href="https://hirewebdeveloper.pp.ua" target="_blank" rel="noopener">HireWebDeveloper.pp.ua — Веб-розробка</a>
                    </div>
                </div>
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
                        <li><a href="/rozrobka-saitiv/ukraine/">Розробка сайтів</a></li>
                        <li><a href="/internet-magazin/ukraine/">Інтернет-магазини</a></li>
                        <li><a href="/wordpress/ukraine/">WordPress розробка</a></li>
                        <li><a href="/laravel/ukraine/">Laravel розробка</a></li>
                        <li><a href="/crm-erp/ukraine/">CRM/ERP системи</a></li>
                        <li><a href="/seo-optimizatsiya/ukraine/">SEO оптимізація</a></li>
                        <li><a href="/nextjs/ukraine/">Next.js розробка</a></li>
                        <li><a href="/nodejs/ukraine/">Node.js розробка</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h3>Міста</h3>
                    <ul>
                        <li><a href="/{{ service_slug }}/ukraine/kyiv/">Київ</a></li>
                        <li><a href="/{{ service_slug }}/ukraine/lviv/">Львів</a></li>
                        <li><a href="/{{ service_slug }}/ukraine/kharkiv/">Харків</a></li>
                        <li><a href="/{{ service_slug }}/ukraine/odesa/">Одеса</a></li>
                        <li><a href="/{{ service_slug }}/ukraine/dnipro/">Дніпро</a></li>
                        <li><a href="/{{ service_slug }}/ukraine/zaporizhzhia/">Запоріжжя</a></li>
                        <li><a href="/{{ service_slug }}/ukraine/vinnytsia/">Вінниця</a></li>
                        <li><a href="/{{ service_slug }}/ukraine/kryvyi-rih/">Кривий Ріг</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h3>Контакти</h3>
                    <ul>
                        <li>Телефон: <a href="tel:+380938800822">+38 (093) 88-00-822</a></li>
                        <li>Email: <a href="mailto:info@matviy.pp.ua">info@matviy.pp.ua</a></li>
                        <li>LinkedIn: <a href="https://www.linkedin.com/in/romanmatviy/" target="_blank">romanmatviy</a></li>
                        <li>GitHub: <a href="https://github.com/romanmatviy" target="_blank">romanmatviy</a></li>
                    </ul>
                </div>
            </div>
            <div class="copyright">
                &copy; 2025 Програміст Роман. Всі права захищені.
            </div>
        </div>
    </footer>

    <!-- Scripts -->
    <script src="/js/main.js?ver=2"></script>
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
    
    # Шаблон для індексної сторінки гео (Microdata)
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
    <link rel="icon" href="https://programist.matviy.pp.ua/img/favicon.ico" type="image/x-icon">
    
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
                    <li><a href="/faq.html">FAQ</a></li>
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
    <main itemscope itemtype="https://schema.org/ProfessionalService">
        <meta itemprop="name" content="Програміст Роман - {{ service_name }} в {{ geo_name }}">
        <meta itemprop="description" content="Професійні послуги: {{ service_name_lower }} в {{ geo_name }}. {{ service_description }}">
        <link itemprop="url" href="https://programist.matviy.pp.ua/{{ service_slug }}/{{ geo_slug }}/">
        <link itemprop="image" href="https://programist.matviy.pp.ua/img/og-image.jpg">
        <meta itemprop="telephone" content="+380938800822">
        <div itemprop="address" itemscope itemtype="https://schema.org/PostalAddress">
            <meta itemprop="addressLocality" content="{{ geo_name }}">
            <meta itemprop="addressCountry" content="UA">
        </div>
        <div itemprop="aggregateRating" itemscope itemtype="https://schema.org/AggregateRating">
            <meta itemprop="ratingValue" content="5">
            <meta itemprop="reviewCount" content="24">
        </div>

        <div class="container">
            <!-- Breadcrumbs -->
            <div class="breadcrumbs">
                <nav aria-label="Breadcrumb">
                    <ol itemscope itemtype="https://schema.org/BreadcrumbList" style="list-style: none; padding: 0; display: flex; gap: 5px;">
                        <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
                            <a itemprop="item" href="/">
                                <span itemprop="name">Головна</span>
                            </a>
                            <meta itemprop="position" content="1">
                        </li>
                        <span>></span>
                        <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
                            <a itemprop="item" href="/{{ service_slug }}">
                                <span itemprop="name">{{ service_name }}</span>
                            </a>
                            <meta itemprop="position" content="2">
                        </li>
                        <span>></span>
                        <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
                            <span itemprop="name">{{ geo_name }}</span>
                            <meta itemprop="position" content="3">
                        </li>
                    </ol>
                </nav>
            </div>
            
            <!-- SEO Content -->
            <div class="seo-content">
                <h1>{{ service_name }} в {{ geo_name }} – професійно під ключ</h1>
                
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
                    <li><strong>Next.js</strong> – потужний React-фреймворк для швидких та SEO-оптимізованих сайтів</li>
                    <li><strong>Node.js</strong> – високопродуктивна платформа для серверних рішень та API</li>
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
                
                <h2>SEO оптимізація в {{ geo_name }}</h2>
                <p>Всі мої проекти створюються з урахуванням вимог пошукових систем. Це дозволяє досягти високих позицій у результатах пошуку за ключовими запитами, пов'язаними з вашим бізнесом в {{ geo_name }}. SEO оптимізація включає:</p>
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

        <!-- Testimonials Section -->
        <section id="testimonials" class="testimonials">
            <div class="container">
                <h2 class="section-title">Відгуки клієнтів</h2>
                <div class="testimonials-grid">
                    <div class="testimonial-card">
                        <div class="stars">★★★★★</div>
                        <p class="testimonial-text">Роман розробив для нас інтернет-магазин на PrestaShop. Все було зроблено професійно та в термін. Особливо вражений увагою до SEO-деталей та швидкістю роботи сайту.</p>
                        <div class="testimonial-author">
                            <span class="author-name">Олександр Ковальчук</span>
                            <span class="author-role">Власник магазину TechShop</span>
                        </div>
                    </div>
                    <div class="testimonial-card">
                        <div class="stars">★★★★★</div>
                        <p class="testimonial-text">Працюємо з Романом над підтримкою нашого корпоративного сайту на Laravel. Дуже задоволені оперативністю та якістю коду. Рекомендую як надійного розробника.</p>
                        <div class="testimonial-author">
                            <span class="author-name">Марина Мельник</span>
                            <span class="author-role">Маркетинг-директор AgroGroup</span>
                        </div>
                    </div>
                    <div class="testimonial-card">
                        <div class="stars">★★★★★</div>
                        <p class="testimonial-text">Замовляли SEO-оптимізацію та редизайн сайту на WordPress. Позиції в Google значно виросли вже за перший місяць після запуску нової версії. Дякуємо за роботу!</p>
                        <div class="testimonial-author">
                            <span class="author-name">Сергій Притула</span>
                            <span class="author-role">Співзасновник Creative Agency</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <!-- CTA Section -->
        <section class="cta-section">
            <div class="container">
                <h2>Готові замовити {{ service_name_lower_acc }} в {{ geo_name }}?</h2>
                <p>Зв'яжіться зі мною для безкоштовної консультації та оцінки вашого проекту</p>
                <a href="/#contact" class="btn">Замовити консультацію</a>
            </div>
        </section>

        <!-- Other Projects Section -->
        <section class="other-projects">
            <div class="container">
                <h2 class="section-title">Корисні сервіси та мої проєкти</h2>
                <div class="projects-grid">
                    <div class="project-item">
                        <a href="https://monitortest.pp.ua" target="_blank" rel="noopener">Monitor Test — Тестування монітора</a>
                    </div>
                    <div class="project-item">
                        <a href="https://keytest.pp.ua" target="_blank" rel="noopener">Key Test — Тестування клавіатури</a>
                    </div>
                    <div class="project-item">
                        <a href="https://php.apartner.pro" target="_blank" rel="noopener">PHP Course — Курс програмування</a>
                    </div>
                    <div class="project-item">
                        <a href="https://hostpro.apartner.pro/" target="_blank" rel="noopener">HostPro — Надійний хостинг</a>
                    </div>
                    <div class="project-item">
                        <a href="https://programist.pp.ua" target="_blank" rel="noopener">Programist.pp.ua — Послуги програміста</a>
                    </div>
                    <div class="project-item">
                        <a href="https://hire-web-developer.com" target="_blank" rel="noopener">Hire Web Developer — Веб-розробка</a>
                    </div>
                    <div class="project-item">
                        <a href="https://hirewebdeveloper.pp.ua" target="_blank" rel="noopener">HireWebDeveloper.pp.ua — Веб-розробка</a>
                    </div>
                </div>
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
                        <li><a href="/rozrobka-saitiv/ukraine/">Розробка сайтів</a></li>
                        <li><a href="/internet-magazin/ukraine/">Інтернет-магазини</a></li>
                        <li><a href="/wordpress/ukraine/">WordPress розробка</a></li>
                        <li><a href="/laravel/ukraine/">Laravel розробка</a></li>
                        <li><a href="/crm-erp/ukraine/">CRM/ERP системи</a></li>
                        <li><a href="/seo-optimizatsiya/ukraine/">SEO оптимізація</a></li>
                        <li><a href="/nextjs/ukraine/">Next.js розробка</a></li>
                        <li><a href="/nodejs/ukraine/">Node.js розробка</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h3>Міста</h3>
                    <ul>
                        <li><a href="/{{ service_slug }}/ukraine/kyiv/">Київ</a></li>
                        <li><a href="/{{ service_slug }}/ukraine/lviv/">Львів</a></li>
                        <li><a href="/{{ service_slug }}/ukraine/kharkiv/">Харків</a></li>
                        <li><a href="/{{ service_slug }}/ukraine/odesa/">Одеса</a></li>
                        <li><a href="/{{ service_slug }}/ukraine/dnipro/">Дніпро</a></li>
                        <li><a href="/{{ service_slug }}/ukraine/zaporizhzhia/">Запоріжжя</a></li>
                        <li><a href="/{{ service_slug }}/ukraine/vinnytsia/">Вінниця</a></li>
                        <li><a href="/{{ service_slug }}/ukraine/kryvyi-rih/">Кривий Ріг</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h3>Контакти</h3>
                    <ul>
                        <li>Телефон: <a href="tel:+380938800822">+38 (093) 88-00-822</a></li>
                        <li>Email: <a href="mailto:info@matviy.pp.ua">info@matviy.pp.ua</a></li>
                        <li>LinkedIn: <a href="https://www.linkedin.com/in/romanmatviy/" target="_blank">romanmatviy</a></li>
                        <li>GitHub: <a href="https://github.com/romanmatviy" target="_blank">romanmatviy</a></li>
                    </ul>
                </div>
            </div>
            <div class="copyright">
                &copy; 2025 Програміст Роман. Всі права захищені.
            </div>
        </div>
    </footer>

    <!-- Scripts -->
    <script src="/js/main.js?ver=2"></script>
</body>
</html>
"""
    
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
    
    # Додаємо список міст
    cities_list_html = ""
    for city_slug, city_data in cities.items():
        cities_list_html += f'<li><a href="/{service_slug}/{geo_slug}/{city_slug}/">{service_name} {city_data["in"]}</a></li>\n'
    page_content = page_content.replace("{{ cities_list }}", cities_list_html)
    
    # Додаємо специфічний контент для сервісу
    specific_content = service_specific_content.get(service_slug, "")
    specific_content = specific_content.replace("{{ city_in }}", f"в {geo_name}")
    page_content = page_content.replace("{{ service_specific_content }}", specific_content)
    
    page_content = page_content.replace("{{ geo_slug }}", geo_slug)
    page_content = page_content.replace("{{ geo_name }}", geo_name)
    
    # Зберігаємо файл
    index_path = os.path.join(BASE_DIR, service_slug, geo_slug, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(page_content)
    
    print(f"Згенеровано індексну сторінку для гео: {service_name} / {geo_name}")

def generate_city_page(service_slug, service_name, geo_slug, geo_name, city_slug, city_data):
    """Генерує сторінку для конкретного міста (викликає функцію з іншого файлу для уникнення дублювання логіки)"""
    from generate_seo_pages import generate_seo_page
    generate_seo_page(service_slug, service_name, geo_slug, geo_name, city_slug, city_data)

if __name__ == "__main__":
    generate_all_static_pages()