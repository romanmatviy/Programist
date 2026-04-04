#!/usr/bin/env python3
"""
Скрипт для генерації SEO-сторінок за схемою /service/geo/city
"""

import os
import shutil
import re

# Базова директорія проекту
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Список сервісів з українськими назвами
services = {
    "rozrobka-saitiv": "Розробка сайтів",
    "internet-magazin": "Інтернет-магазин",
    "wordpress": "WordPress",
    "prestashop": "PrestaShop",
    "opencart": "OpenCart",
    "laravel": "Laravel",
    "vue": "Vue.js",
    "seo-optimizatsiya": "SEO оптимізація",
    "pidtrymka-saitiv": "Підтримка сайтів",
    "crm-erp": "CRM/ERP системи"
}

# Список гео (поки тільки Україна)
geos = {
    "ukraine": "Україна"
}

# Список міст з відмінками (називний - "у/в місті")
cities = {
    "kyiv": {"name": "Київ", "in": "у Києві"},
    "lviv": {"name": "Львів", "in": "у Львові"},
    "kharkiv": {"name": "Харків", "in": "у Харкові"},
    "odesa": {"name": "Одеса", "in": "в Одесі"},
    "dnipro": {"name": "Дніпро", "in": "у Дніпрі"},
    "zaporizhzhia": {"name": "Запоріжжя", "in": "у Запоріжжі"},
    "vinnytsia": {"name": "Вінниця", "in": "у Вінниці"},
    "poltava": {"name": "Полтава", "in": "у Полтаві"},
    "chernivtsi": {"name": "Чернівці", "in": "у Чернівцях"},
    "cherkasy": {"name": "Черкаси", "in": "у Черкасах"},
    "chernihiv": {"name": "Чернігів", "in": "у Чернігові"},
    "zhytomyr": {"name": "Житомир", "in": "у Житомирі"},
    "ivano-frankivsk": {"name": "Івано-Франківськ", "in": "в Івано-Франківську"},
    "rivne": {"name": "Рівне", "in": "у Рівному"},
    "lutsk": {"name": "Луцьк", "in": "у Луцьку"},
    "ternopil": {"name": "Тернопіль", "in": "у Тернополі"},
    "mykolaiv": {"name": "Миколаїв", "in": "у Миколаєві"},
    "khmelnytskyi": {"name": "Хмельницький", "in": "у Хмельницькому"},
    "sumy": {"name": "Суми", "in": "у Сумах"},
    "kropyvnytskyi": {"name": "Кропивницький", "in": "у Кропивницькому"},
    "uzhorod": {"name": "Ужгород", "in": "в Ужгороді"},
    "kryvyi-rih": {"name": "Кривий Ріг", "in": "у Кривому Розі"},
    "mariupol": {"name": "Маріуполь", "in": "у Маріуполі"}
}

# Шаблон HTML-сторінки
PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ service_name }} {{ city_in }} | Програміст Роман (RomanDev)</title>
    <meta name="description" content="Професійні послуги: {{ service_name_lower }} {{ city_in }}. {{ service_description }} Замовте {{ service_name_lower_acc }} у програміста Романа.">
    
    <!-- Canonical -->
    <link rel="canonical" href="https://programist.matviy.pp.ua/{{ service_slug }}/{{ geo_slug }}/{{ city_slug }}/">
    
    <!-- Favicon -->
    <link rel="icon" href="https://programist.matviy.pp.ua/img/favicon.ico" type="image/x-icon">
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    
    <!-- Styles -->
    <link rel="stylesheet" href="/css/style.css?ver=1">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{{ service_name }} {{ city_in }} | Програміст Роман (RomanDev)">
    <meta property="og:description" content="Професійні послуги: {{ service_name_lower }} {{ city_in }}. {{ service_description }} Замовте {{ service_name_lower_acc }} у програміста Романа.">
    <meta property="og:url" content="https://programist.matviy.pp.ua/{{ service_slug }}/{{ geo_slug }}/{{ city_slug }}/">
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
        <meta itemprop="name" content="Програміст Роман - {{ service_name }} {{ city_in }}">
        <meta itemprop="description" content="Професійні послуги: {{ service_name_lower }} {{ city_in }}. {{ service_description }}">
        <link itemprop="url" href="https://programist.matviy.pp.ua/{{ service_slug }}/{{ geo_slug }}/{{ city_slug }}/">
        <link itemprop="image" href="https://programist.matviy.pp.ua/img/og-image.jpg">
        <meta itemprop="telephone" content="+380938800822">
        <div itemprop="address" itemscope itemtype="https://schema.org/PostalAddress">
            <meta itemprop="addressLocality" content="{{ city_name }}">
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
                            <a itemprop="item" href="/{{ service_slug }}/{{ geo_slug }}">
                                <span itemprop="name">{{ geo_name }}</span>
                            </a>
                            <meta itemprop="position" content="3">
                        </li>
                        <span>></span>
                        <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
                            <span itemprop="name">{{ city_name }}</span>
                            <meta itemprop="position" content="4">
                        </li>
                    </ol>
                </nav>
            </div>
            
            <!-- SEO Content -->
            <div class="seo-content">
                <h1>{{ service_name }} {{ city_in }} – професійно під ключ</h1>
                
                <p>Потрібні послуги: {{ service_name_lower }} {{ city_in }}? Програміст Роман пропонує професійні рішення для вашого бізнесу. {{ service_content }} Замовляючи {{ service_name_lower_acc }} {{ city_in }}, ви отримуєте сучасне рішення, яке приносить результат.</p>
                
                <h2>Послуги: {{ service_name_lower }} {{ city_in }}</h2>
                <p>Як професійний розробник {{ city_in }}, я пропоную повний спектр послуг для вашого бізнесу. Моя мета – створити не просто {{ service_name_lower_acc }}, а ефективний інструмент для залучення клієнтів та збільшення продажів. Кожен проект розробляється з урахуванням специфіки вашого бізнесу та потреб цільової аудиторії.</p>
                
                {{ service_specific_content }}
                
                <h2>Технології, які я використовую</h2>
                <p>У роботі {{ city_in }} я використовую сучасні технології та фреймворки:</p>
                <ul>
                    <li><strong>Laravel</strong> – потужний PHP-фреймворк для створення складних веб-додатків</li>
                    <li><strong>WordPress</strong> – найпопулярніша CMS для створення сайтів різної складності</li>
                    <li><strong>PrestaShop</strong> – спеціалізована платформа для створення інтернет-магазинів</li>
                    <li><strong>OpenCart</strong> – гнучка система для електронної комерції</li>
                    <li><strong>Vue.js</strong> – прогресивний JavaScript-фреймворк для створення інтерактивних інтерфейсів</li>
                </ul>
                
                <h2>Переваги замовлення послуг {{ city_in }}</h2>
                <p>Обираючи мої послуги {{ city_in }}, ви отримуєте ряд переваг:</p>
                <ul>
                    <li>Особисті зустрічі для обговорення проекту</li>
                    <li>Розуміння локального ринку та конкуренції</li>
                    <li>Швидка комунікація та оперативне вирішення питань</li>
                    <li>Підтримка після завершення проекту</li>
                    <li>Індивідуальний підхід до кожного клієнта</li>
                </ul>
                
                <h2>Етапи роботи {{ city_in }}</h2>
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
                
                <h2>SEO оптимізація {{ city_in }}</h2>
                <p>Всі мої проекти створюються з урахуванням вимог пошукових систем. Це дозволяє досягти високих позицій у результатах пошуку за ключовими запитами, пов'язаними з вашим бізнесом {{ city_in }}. SEO оптимізація включає:</p>
                <ul>
                    <li>Технічну оптимізацію</li>
                    <li>Створення SEO-friendly структури</li>
                    <li>Оптимізацію швидкості завантаження</li>
                    <li>Адаптивний дизайн для мобільних пристроїв</li>
                    <li>Налаштування мета-тегів та мікророзмітки</li>
                </ul>
                
                <h2>Вартість послуг {{ city_in }}</h2>
                <p>Ціна послуг залежить від складності проекту, необхідного функціоналу та термінів виконання. Для отримання точної вартості, зв'яжіться зі мною для безкоштовної консультації. Я пропоную конкурентні ціни на послуги {{ city_in }}, зберігаючи високу якість виконання.</p>
            </div>
        </div>
        
        <!-- CTA Section -->
        <section class="cta-section">
            <div class="container">
                <h2>Готові замовити {{ service_name_lower_acc }} {{ city_in }}?</h2>
                <p>Зв'яжіться зі мною для безкоштовної консультації та оцінки вашого проекту</p>
                <a href="/#contact" class="btn">Замовити консультацію</a>
            </div>
        </section>
        
        <!-- Related Services -->
        <div class="container">
            <h2 class="section-title">Інші послуги {{ city_in }}</h2>
            <div class="services">
                {{ related_services }}
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
                    </ul>
                </div>
                <div class="footer-col">
                    <h3>Міста</h3>
                    <ul>
                        <li><a href="/{{ service_slug }}/{{ geo_slug }}/kyiv/">Київ</a></li>
                        <li><a href="/{{ service_slug }}/{{ geo_slug }}/lviv/">Львів</a></li>
                        <li><a href="/{{ service_slug }}/{{ geo_slug }}/kharkiv/">Харків</a></li>
                        <li><a href="/{{ service_slug }}/{{ geo_slug }}/odesa/">Одеса</a></li>
                        <li><a href="/{{ service_slug }}/{{ geo_slug }}/dnipro/">Дніпро</a></li>
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

# Описи для різних сервісів
service_descriptions = {
    "rozrobka-saitiv": "Створення сучасних та швидких сайтів для бізнесу.",
    "internet-magazin": "Розробка функціональних інтернет-магазинів з високою конверсією.",
    "wordpress": "Створення та підтримка сайтів на CMS WordPress будь-якої складності.",
    "prestashop": "Розробка професійних інтернет-магазинів на платформі PrestaShop.",
    "opencart": "Створення магазинів на OpenCart з оптимальною структурою.",
    "laravel": "Розробка складних веб-додатків та систем на фреймворку Laravel.",
    "vue": "Створення інтерактивних інтерфейсів та SPA на Vue.js.",
    "seo-optimizatsiya": "Внутрішня та зовнішня SEO оптимізація для виводу в ТОП Google.",
    "pidtrymka-saitiv": "Технічна підтримка, оновлення та наповнення ваших проектів.",
    "crm-erp": "Розробка індивідуальних CRM та ERP систем для автоматизації бізнесу."
}

# Текстовий контент для різних сервісів
service_contents = {
    "rozrobka-saitiv": "Розробка сайту - це перший крок до успіху вашого бізнесу в інтернеті. Я створюю адаптивні, швидкі та SEO-оптимізовані сайти, які допомагають залучати нових клієнтів.",
    "internet-magazin": "Інтернет-магазин дозволяє продавати товари 24/7. Моя розробка включає налаштування кошика, оплати, доставки та інтеграцію з платіжними системами.",
    "wordpress": "WordPress - це гнучкість та зручність. Я розробляю унікальні теми, налаштовую плагіни та забезпечую швидку роботу сайту на цій CMS.",
    "prestashop": "PrestaShop ідеально підходить для великих магазинів. Я пропоную повний цикл розробки: від дизайну до налаштування складних модулів.",
    "opencart": "OpenCart - популярний вибір для e-commerce. Я створюю швидкі магазини з зручною панеллю керування та необхідним функціоналом.",
    "laravel": "Laravel дозволяє реалізувати будь-які бізнес-вимоги. Я створюю масштабовані та безпечні рішення для вашого проекту.",
    "vue": "Vue.js забезпечує плавність роботи інтерфейсу. Я використовую його для створення динамічних елементів та повноцінних SPA додатків.",
    "seo-optimizatsiya": "SEO допомагає вашому сайту бути помітним. Я проводжу технічний аудит, збираю семантичне ядро та оптимізую кожну сторінку для пошукових систем.",
    "pidtrymka-saitiv": "Ваш сайт потребує постійного догляду. Я забезпечую стабільну роботу, виправлення помилок та впровадження нових фішок.",
    "crm-erp": "Автоматизація процесів економить час та гроші. Я створюю індивідуальні системи, які ідеально підходять під ваші бізнес-процеси."
}

# Назви сервісів у знахідному відмінку (для текстів "Замовити що?")
service_accusative = {
    "розробка сайтів": "розробку сайтів",
    "інтернет-магазин": "інтернет-магазин",
    "wordpress": "розробку на WordPress",
    "prestashop": "розробку на PrestaShop",
    "opencart": "розробку на OpenCart",
    "laravel": "розробку на Laravel",
    "vue.js": "розробку на Vue.js",
    "seo оптимізація": "SEO оптимізацію",
    "підтримка сайтів": "підтримку сайтів",
    "crm/erp системи": "CRM/ERP систему"
}

# Специфічний контент для сервісів (списки функцій тощо)
service_specific_content = {
    "rozrobka-saitiv": "<h3>Типи сайтів, які я розробляю:</h3><ul><li>Лендінги (Landing Page)</li><li>Корпоративні сайти</li><li>Сайти-візитки</li><li>Портали та новинні ресурси</li></ul>",
    "internet-magazin": "<h3>Функціонал магазину:</h3><ul><li>Фільтрація та пошук товарів</li><li>Особистий кабінет покупця</li><li>Синхронізація з 1С/CRM</li><li>Різні методи оплати (LiqPay, WayForPay)</li></ul>",
    "wordpress": "<h3>Послуги WordPress:</h3><ul><li>Розробка унікальних тем</li><li>Налаштування WooCommerce</li><li>Оптимізація швидкості</li><li>Виправлення помилок та вірусів</li></ul>",
    "laravel": "<h3>Розробка на Laravel:</h3><ul><li>Backend API для мобільних додатків</li><li>Складні адмін-панелі</li><li>Системи бронювання та обліку</li><li>Інтеграція зовнішніх сервісів</li></ul>"
}

def create_directory(path):
    """Створює директорію, якщо вона не існує"""
    if not os.path.exists(path):
        os.makedirs(path)

def generate_related_services(current_service_slug, city_in):
    """Генерує блоки інших послуг"""
    html = ""
    for slug, name in services.items():
        if slug != current_service_slug:
            html += f'<div class="service-card"><a href="/{slug}/ukraine/"><h3>{name} {city_in}</h3></a></div>'
    return html

def generate_seo_page(service_slug, service_name, geo_slug, geo_name, city_slug, city_data):
    """Генерує одну SEO-сторінку"""
    city_name = city_data["name"]
    city_in = city_data["in"]
    service_name_lower = service_name.lower()
    service_name_lower_acc = service_accusative.get(service_name_lower, service_name_lower)
    
    # Створюємо шлях до директорії
    dir_path = os.path.join(BASE_DIR, service_slug, geo_slug, city_slug)
    create_directory(dir_path)
    
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
    related_services = generate_related_services(service_slug, city_in)
    page_content = page_content.replace("{{ related_services }}", related_services)
    
    # Зберігаємо файл
    file_path = os.path.join(dir_path, "index.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(page_content)

def generate_all_pages():
    """Генерує всі можливі сторінки"""
    total_pages = 0
    for service_slug, service_name in services.items():
        for geo_slug, geo_name in geos.items():
            for city_slug, city_data in cities.items():
                generate_seo_page(service_slug, service_name, geo_slug, geo_name, city_slug, city_data)
                total_pages += 1
                if total_pages % 50 == 0:
                    print(f"Згенеровано {total_pages} сторінок...")
    
    print(f"Генерація завершена. Всього згенеровано {total_pages} SEO-сторінок.")

if __name__ == "__main__":
    generate_all_pages()