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
    "seo-optimizatsiya": "SEO-оптимізація",
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
    <link rel="icon" href="/img/favicon.ico" type="image/x-icon">
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    
    <!-- Styles -->
    <link rel="stylesheet" href="/css/style.css">
    
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
                <a href="/{{ service_slug }}/{{ geo_slug }}">{{ geo_name }}</a> <span>></span> 
                <span>{{ city_name }}</span>
            </div>
            
            <!-- SEO Content -->
            <div class="seo-content">
                <h1>{{ service_name }} {{ city_in }} – професійно під ключ</h1>
                
                <div data-schema="LocalBusiness" 
                     data-name="Програміст Роман" 
                     data-description="Професійні послуги: {{ service_name_lower }} {{ city_in }}" 
                     data-city="{{ city_name }}" 
                     data-region="{{ city_name }}">
                </div>
                
                <div data-schema="Service" 
                     data-service-type="{{ service_name }}" 
                     data-city="{{ city_name }}" 
                     data-description="Професійні послуги: {{ service_name_lower }} {{ city_in }}. {{ service_description }}">
                </div>
                
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
                
                <h2>SEO-оптимізація {{ city_in }}</h2>
                <p>Всі мої проекти створюються з урахуванням вимог пошукових систем. Це дозволяє досягти високих позицій у результатах пошуку за ключовими запитами, пов'язаними з вашим бізнесом {{ city_in }}. SEO-оптимізація включає:</p>
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
    <script src="/js/main.js"></script>
</body>
</html>
"""

# Специфічний контент для кожного сервісу
service_specific_content = {
    "rozrobka-saitiv": """
<h2>Типи сайтів, які я розробляю {{ city_in }}</h2>
<p>Спеціалізуюсь на створенні різних типів веб-ресурсів для бізнесу {{ city_in }}:</p>
<ul>
    <li><strong>Корпоративні сайти</strong> – представництво вашої компанії в інтернеті з детальним описом послуг та продуктів</li>
    <li><strong>Інтернет-магазини</strong> – функціональні онлайн-платформи для продажу товарів з інтеграцією платіжних систем</li>
    <li><strong>Лендінги</strong> – висококонверсійні односторінкові сайти для просування конкретних товарів або послуг</li>
    <li><strong>Каталоги</strong> – зручні онлайн-каталоги продукції з можливістю фільтрації та пошуку</li>
    <li><strong>CRM/ERP системи</strong> – комплексні рішення для автоматизації бізнес-процесів</li>
</ul>
""",
    "internet-magazin": """
<h2>Функціонал інтернет-магазинів, які я розробляю {{ city_in }}</h2>
<p>Створюю інтернет-магазини з різним функціоналом для бізнесу {{ city_in }}:</p>
<ul>
    <li><strong>Каталог товарів</strong> – зручна структура з категоріями, підкатегоріями та фільтрами</li>
    <li><strong>Картки товарів</strong> – детальний опис, характеристики, фото та відгуки</li>
    <li><strong>Кошик та оформлення замовлення</strong> – зручний процес покупки з мінімальною кількістю кроків</li>
    <li><strong>Особистий кабінет</strong> – історія замовлень, збережені адреси, улюблені товари</li>
    <li><strong>Інтеграція з платіжними системами</strong> – LiqPay, WayForPay, Portmone, PayPal</li>
    <li><strong>Інтеграція з службами доставки</strong> – Нова Пошта, Укрпошта, Meest Express</li>
    <li><strong>Мультивалютність</strong> – можливість вибору валюти для відображення цін</li>
    <li><strong>Мультимовність</strong> – підтримка кількох мов інтерфейсу</li>
</ul>
""",
    "wordpress": """
<h2>WordPress послуги, які я надаю {{ city_in }}</h2>
<p>Пропоную широкий спектр послуг з WordPress {{ city_in }}:</p>
<ul>
    <li><strong>Створення сайтів на WordPress</strong> – від блогів до складних корпоративних сайтів</li>
    <li><strong>Розробка інтернет-магазинів на WooCommerce</strong> – повнофункціональні рішення для електронної комерції</li>
    <li><strong>Розробка тем</strong> – створення унікальних тем з нуля або на основі фреймворків</li>
    <li><strong>Розробка плагінів</strong> – створення кастомних плагінів для розширення функціоналу</li>
    <li><strong>Оптимізація швидкості</strong> – налаштування кешування, оптимізація бази даних, мінімізація ресурсів</li>
    <li><strong>Міграція сайтів</strong> – перенесення сайтів на WordPress з інших CMS</li>
    <li><strong>Оновлення та підтримка</strong> – регулярні оновлення, резервне копіювання, моніторинг безпеки</li>
</ul>
""",
    "prestashop": """
<h2>PrestaShop послуги, які я надаю {{ city_in }}</h2>
<p>Пропоную широкий спектр послуг з PrestaShop {{ city_in }}:</p>
<ul>
    <li><strong>Створення інтернет-магазинів на PrestaShop</strong> – повнофункціональні рішення для електронної комерції</li>
    <li><strong>Розробка тем</strong> – створення унікальних тем з нуля або на основі фреймворків</li>
    <li><strong>Розробка модулів</strong> – створення кастомних модулів для розширення функціоналу</li>
    <li><strong>Інтеграція з платіжними системами</strong> – LiqPay, WayForPay, Portmone, PayPal</li>
    <li><strong>Інтеграція з службами доставки</strong> – Нова Пошта, Укрпошта, Meest Express</li>
    <li><strong>Оптимізація швидкості</strong> – налаштування кешування, оптимізація бази даних, мінімізація ресурсів</li>
    <li><strong>Міграція магазинів</strong> – перенесення магазинів на PrestaShop з інших CMS</li>
    <li><strong>Оновлення та підтримка</strong> – регулярні оновлення, резервне копіювання, моніторинг безпеки</li>
</ul>
""",
    "opencart": """
<h2>OpenCart послуги, які я надаю {{ city_in }}</h2>
<p>Пропоную широкий спектр послуг з OpenCart {{ city_in }}:</p>
<ul>
    <li><strong>Створення інтернет-магазинів на OpenCart</strong> – повнофункціональні рішення для електронної комерції</li>
    <li><strong>Розробка тем</strong> – створення унікальних тем з нуля або на основі фреймворків</li>
    <li><strong>Розробка модулів</strong> – створення кастомних модулів для розширення функціоналу</li>
    <li><strong>Інтеграція з платіжними системами</strong> – LiqPay, WayForPay, Portmone, PayPal</li>
    <li><strong>Інтеграція з службами доставки</strong> – Нова Пошта, Укрпошта, Meest Express</li>
    <li><strong>Оптимізація швидкості</strong> – налаштування кешування, оптимізація бази даних, мінімізація ресурсів</li>
    <li><strong>Міграція магазинів</strong> – перенесення магазинів на OpenCart з інших CMS</li>
    <li><strong>Оновлення та підтримка</strong> – регулярні оновлення, резервне копіювання, моніторинг безпеки</li>
</ul>
""",
    "laravel": """
<h2>Laravel послуги, які я надаю {{ city_in }}</h2>
<p>Пропоную широкий спектр послуг з Laravel {{ city_in }}:</p>
<ul>
    <li><strong>Розробка веб-додатків</strong> – створення складних веб-додатків на Laravel</li>
    <li><strong>Розробка API</strong> – створення RESTful API для мобільних додатків та SPA</li>
    <li><strong>Інтеграція з зовнішніми сервісами</strong> – платіжні системи, CRM, ERP, соціальні мережі</li>
    <li><strong>Розробка CRM/ERP систем</strong> – створення кастомних систем для автоматизації бізнес-процесів</li>
    <li><strong>Оптимізація продуктивності</strong> – кешування, оптимізація запитів до бази даних, профілювання</li>
    <li><strong>Рефакторинг коду</strong> – покращення існуючого коду, впровадження кращих практик</li>
    <li><strong>Міграція на Laravel</strong> – перенесення проектів з інших фреймворків на Laravel</li>
    <li><strong>Підтримка та розвиток</strong> – супровід існуючих Laravel проектів</li>
</ul>
""",
    "vue": """
<h2>Vue.js послуги, які я надаю {{ city_in }}</h2>
<p>Пропоную широкий спектр послуг з Vue.js {{ city_in }}:</p>
<ul>
    <li><strong>Розробка SPA</strong> – створення односторінкових додатків на Vue.js</li>
    <li><strong>Розробка PWA</strong> – створення прогресивних веб-додатків з офлайн-функціональністю</li>
    <li><strong>Інтеграція з API</strong> – взаємодія з RESTful API та GraphQL</li>
    <li><strong>Розробка компонентів</strong> – створення перевикористовуваних компонентів</li>
    <li><strong>Міграція на Vue.js</strong> – перенесення проектів з інших фреймворків на Vue.js</li>
    <li><strong>Оптимізація продуктивності</strong> – lazy loading, code splitting, віртуальний скролінг</li>
    <li><strong>Тестування</strong> – написання модульних та інтеграційних тестів</li>
    <li><strong>Підтримка та розвиток</strong> – супровід існуючих Vue.js проектів</li>
</ul>
""",
    "seo-optimizatsiya": """
<h2>SEO-послуги, які я надаю {{ city_in }}</h2>
<p>Пропоную широкий спектр SEO-послуг {{ city_in }}:</p>
<ul>
    <li><strong>Аудит сайту</strong> – комплексний аналіз сайту з точки зору SEO</li>
    <li><strong>Технічна оптимізація</strong> – виправлення помилок, оптимізація швидкості, мобільна адаптивність</li>
    <li><strong>Внутрішня оптимізація</strong> – оптимізація мета-тегів, заголовків, контенту</li>
    <li><strong>Зовнішня оптимізація</strong> – нарощування якісної посилальної маси</li>
    <li><strong>Локальне SEO</strong> – оптимізація для місцевих пошукових запитів</li>
    <li><strong>Контент-маркетинг</strong> – створення оптимізованого контенту для сайту</li>
    <li><strong>Аналітика та звітність</strong> – відстеження результатів та надання регулярних звітів</li>
    <li><strong>Консультації</strong> – навчання команди клієнта основам SEO</li>
</ul>
""",
    "pidtrymka-saitiv": """
<h2>Послуги з підтримки сайтів, які я надаю {{ city_in }}</h2>
<p>Пропоную широкий спектр послуг з підтримки сайтів {{ city_in }}:</p>
<ul>
    <li><strong>Технічна підтримка</strong> – виправлення помилок, оновлення CMS, плагінів, модулів</li>
    <li><strong>Контент-підтримка</strong> – додавання та оновлення контенту на сайті</li>
    <li><strong>Моніторинг безпеки</strong> – регулярні перевірки на наявність вразливостей</li>
    <li><strong>Резервне копіювання</strong> – створення регулярних резервних копій сайту та бази даних</li>
    <li><strong>Оптимізація швидкості</strong> – покращення швидкості завантаження сайту</li>
    <li><strong>SEO-підтримка</strong> – підтримка та покращення позицій сайту в пошукових системах</li>
    <li><strong>Аналітика</strong> – аналіз відвідуваності та поведінки користувачів</li>
    <li><strong>Консультації</strong> – консультації з питань розвитку сайту</li>
</ul>
""",
    "crm-erp": """
<h2>CRM/ERP послуги, які я надаю {{ city_in }}</h2>
<p>Пропоную широкий спектр послуг з CRM/ERP систем {{ city_in }}:</p>
<ul>
    <li><strong>Розробка CRM систем</strong> – створення кастомних CRM систем для управління взаємовідносинами з клієнтами</li>
    <li><strong>Розробка ERP систем</strong> – створення кастомних ERP систем для управління ресурсами підприємства</li>
    <li><strong>Інтеграція з існуючими системами</strong> – інтеграція CRM/ERP з іншими системами компанії</li>
    <li><strong>Автоматизація бізнес-процесів</strong> – створення автоматизованих робочих процесів</li>
    <li><strong>Міграція даних</strong> – перенесення даних з існуючих систем</li>
    <li><strong>Навчання персоналу</strong> – навчання співробітників роботі з новою системою</li>
    <li><strong>Технічна підтримка</strong> – супровід та розвиток CRM/ERP систем</li>
    <li><strong>Консультації</strong> – консультації з питань автоматизації бізнес-процесів</li>
</ul>
"""
}

# Опис сервісів
service_descriptions = {
    "rozrobka-saitiv": "Створення сучасних, швидких та SEO-оптимізованих сайтів для бізнесу.",
    "internet-magazin": "Розробка функціональних інтернет-магазинів з інтеграцією платіжних систем та CRM.",
    "wordpress": "Створення та налаштування сайтів на WordPress, розробка тем та плагінів.",
    "prestashop": "Розробка інтернет-магазинів на PrestaShop з інтеграцією платіжних систем.",
    "opencart": "Створення та налаштування інтернет-магазинів на OpenCart.",
    "laravel": "Розробка складних веб-додатків та систем на фреймворку Laravel.",
    "vue": "Створення сучасних інтерактивних інтерфейсів з використанням Vue.js.",
    "seo-optimizatsiya": "Комплексна оптимізація сайтів для пошукових систем та підвищення конверсії.",
    "pidtrymka-saitiv": "Технічна підтримка, оновлення та розвиток існуючих веб-проектів.",
    "crm-erp": "Розробка та впровадження CRM та ERP систем для автоматизації бізнес-процесів."
}

# Контент для сервісів
service_contents = {
    "rozrobka-saitiv": "Працюю з Laravel, WordPress, PrestaShop, OpenCart, WooCommerce та Vue.js. Забезпечую SEO-оптимізацію, інтеграцію з платіжними системами та CRM.",
    "internet-magazin": "Створюю функціональні онлайн-магазини з інтеграцією платіжних систем, служб доставки та CRM. Працюю з PrestaShop, OpenCart, WooCommerce та кастомними рішеннями.",
    "wordpress": "Розробляю сайти на WordPress будь-якої складності: від блогів до інтернет-магазинів. Створюю унікальні теми та плагіни, оптимізую швидкість та безпеку.",
    "prestashop": "Створюю інтернет-магазини на PrestaShop з інтеграцією платіжних систем, служб доставки та CRM. Розробляю унікальні теми та модулі.",
    "opencart": "Розробляю інтернет-магазини на OpenCart з інтеграцією платіжних систем, служб доставки та CRM. Створюю унікальні теми та модулі.",
    "laravel": "Розробляю складні веб-додатки та системи на фреймворку Laravel. Створюю RESTful API, інтегрую з зовнішніми сервісами, оптимізую продуктивність.",
    "vue": "Створюю сучасні інтерактивні інтерфейси з використанням Vue.js. Розробляю SPA, PWA, інтегрую з API, оптимізую продуктивність.",
    "seo-optimizatsiya": "Проводжу комплексну оптимізацію сайтів для пошукових систем: технічний аудит, внутрішню та зовнішню оптимізацію, контент-маркетинг.",
    "pidtrymka-saitiv": "Забезпечую технічну підтримку, оновлення та розвиток існуючих веб-проектів. Моніторю безпеку, створюю резервні копії, оптимізую швидкість.",
    "crm-erp": "Розробляю та впроваджую CRM та ERP системи для автоматизації бізнес-процесів. Інтегрую з існуючими системами, навчаю персонал."
}

# Відмінки для сервісів (знахідний відмінок)
service_accusative = {
    "розробка сайтів": "розробку сайтів",
    "інтернет-магазин": "інтернет-магазин",
    "wordpress": "WordPress",
    "prestashop": "PrestaShop",
    "opencart": "OpenCart",
    "laravel": "Laravel",
    "vue.js": "Vue.js",
    "seo-оптимізація": "SEO-оптимізацію",
    "підтримка сайтів": "підтримку сайтів",
    "crm/erp системи": "CRM/ERP системи"
}

def generate_related_services(service_slug, geo_slug, city_slug):
    """Генерує HTML для пов'язаних послуг"""
    related_html = ""
    related_services = [s for s in services.keys() if s != service_slug][:3]
    
    for related in related_services:
        service_name = services[related]
        service_name_in_city = f"{service_name} {cities[city_slug]['in']}"
        img_src = f"/img/service-{related}.jpg"
        
        related_html += f"""
<div class="service-card">
    <img src="{img_src}" alt="{service_name_in_city}">
    <div class="service-content">
        <h3>{service_name_in_city}</h3>
        <p>{service_descriptions[related]}</p>
        <a href="/{related}/{geo_slug}/{city_slug}" class="btn">Детальніше</a>
    </div>
</div>
"""
    
    return related_html

def create_directory(path):
    """Створює директорію, якщо вона не існує"""
    if not os.path.exists(path):
        os.makedirs(path)

def generate_seo_pages():
    """Генерує SEO-сторінки для всіх комбінацій service/geo/city"""
    total_pages = 0
    
    for service_slug, service_name in services.items():
        service_name_lower = service_name.lower()
        service_name_lower_acc = service_accusative.get(service_name_lower, service_name_lower)
        
        for geo_slug, geo_name in geos.items():
            for city_slug, city_data in cities.items():
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
                
                # Виводимо прогрес
                if total_pages % 50 == 0:
                    print(f"Згенеровано {total_pages} сторінок...")
    
    print(f"Генерація завершена. Всього згенеровано {total_pages} SEO-сторінок.")

if __name__ == "__main__":
    generate_seo_pages()