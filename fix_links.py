import re

def fix_links():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    replacements = {
        # Services
        r'<h3>Розробка сайтів</h3>\s*<p>.*?</p>\s*<a href="/rozrobka-saitiv/ukraine/" class="btn">Детальніше</a>': 
        r'<h3>Розробка сайтів</h3>\n                        <p>Створення сучасних, швидких та SEO-оптимізованих сайтів для бізнесу будь-якого масштабу.</p>\n                        <a href="/rozrobka-saitiv/ukraine/" class="btn">Детальніше про розробку</a>',
        
        r'<h3>Інтернет-магазини</h3>\s*<p>.*?</p>\s*<a href="/internet-magazin/ukraine/" class="btn">Детальніше</a>': 
        r'<h3>Інтернет-магазини</h3>\n                        <p>Розробка функціональних інтернет-магазинів з інтеграцією платіжних систем та CRM.</p>\n                        <a href="/internet-magazin/ukraine/" class="btn">Детальніше про магазини</a>',
        
        r'<h3>WordPress розробка</h3>\s*<p>.*?</p>\s*<a href="/wordpress/ukraine/" class="btn">Детальніше</a>': 
        r'<h3>WordPress розробка</h3>\n                        <p>Створення та налаштування сайтів на WordPress, розробка тем та плагінів.</p>\n                        <a href="/wordpress/ukraine/" class="btn">Сайти на WordPress</a>',
        
        r'<h3>Laravel розробка</h3>\s*<p>.*?</p>\s*<a href="/laravel/ukraine/" class="btn">Детальніше</a>': 
        r'<h3>Laravel розробка</h3>\n                        <p>Розробка складних веб-додатків та систем на фреймворку Laravel.</p>\n                        <a href="/laravel/ukraine/" class="btn">Розробка на Laravel</a>',
        
        r'<h3>CRM/ERP системи</h3>\s*<p>.*?</p>\s*<a href="/crm-erp/ukraine/" class="btn">Детальніше</a>': 
        r'<h3>CRM/ERP системи</h3>\n                        <p>Розробка та впровадження CRM та ERP систем для автоматизації бізнес-процесів.</p>\n                        <a href="/crm-erp/ukraine/" class="btn">Замовити CRM/ERP</a>',
        
        r'<h3>SEO оптимізація</h3>\s*<p>.*?</p>\s*<a href="/seo-optimizatsiya/ukraine/" class="btn">Детальніше</a>': 
        r'<h3>SEO оптимізація</h3>\n                        <p>Комплексна оптимізація сайтів для пошукових систем та підвищення конверсії.</p>\n                        <a href="/seo-optimizatsiya/ukraine/" class="btn">Детальніше про SEO</a>',
        
        r'<h3>Next.js розробка</h3>\s*<p>.*?</p>\s*<a href="/nextjs/ukraine/" class="btn">Детальніше</a>': 
        r'<h3>Next.js розробка</h3>\n                        <p>Створення сучасних, швидких та масштабованих веб-додатків на базі Next.js.</p>\n                        <a href="/nextjs/ukraine/" class="btn">Розробка на Next.js</a>',
        
        r'<h3>Node.js розробка</h3>\s*<p>.*?</p>\s*<a href="/nodejs/ukraine/" class="btn">Детальніше</a>': 
        r'<h3>Node.js розробка</h3>\n                        <p>Створення високопродуктивних серверних рішень та API на платформі Node.js.</p>\n                        <a href="/nodejs/ukraine/" class="btn">Розробка на Node.js</a>',
        
        r'<h3>UX/UI Дизайн</h3>\s*<p>.*?</p>\s*<a href="/ux-ui-design/ukraine/" class="btn">Детальніше</a>': 
        r'<h3>UX/UI Дизайн</h3>\n                        <p>Проектування зручних, інтуїтивно зрозумілих та естетично привабливих інтерфейсів для користувачів.</p>\n                        <a href="/ux-ui-design/ukraine/" class="btn">Замовити UX/UI Дизайн</a>',

        # Portfolio
        r'<h3>Інтернет-магазин</h3>\s*<p>.*?</p>\s*<a href="/internet-magazin/ukraine" class="btn">Детальніше</a>': 
        r'<h3>Інтернет-магазин</h3>\n                        <p>Каталог, кошик, оплати, інтеграції з CRM та службами доставки.</p>\n                        <a href="/internet-magazin/ukraine" class="btn">Дивитись кейс магазину</a>',
        
        r'<h3>WordPress проєкт</h3>\s*<p>.*?</p>\s*<a href="/wordpress/ukraine" class="btn">Детальніше</a>': 
        r'<h3>WordPress проєкт</h3>\n                        <p>Кастомна тема/плагін, зручна адмінка та високі показники Core Web Vitals.</p>\n                        <a href="/wordpress/ukraine" class="btn">Дивитись WordPress кейс</a>',
        
        r'<h3>PrestaShop магазин</h3>\s*<p>.*?</p>\s*<a href="/internet-magazin/ukraine" class="btn">Детальніше</a>': 
        r'<h3>PrestaShop магазин</h3>\n                        <p>Повний цикл: налаштування, імпорт товарів, платіжні системи, аналітика.</p>\n                        <a href="/internet-magazin/ukraine" class="btn">Кейс PrestaShop</a>',
        
        r'<h3>Підтримка PrestaShop</h3>\s*<p>.*?</p>\s*<a href="/internet-magazin/ukraine" class="btn">Детальніше</a>': 
        r'<h3>Підтримка PrestaShop</h3>\n                        <p>Оновлення, виправлення, оптимізація швидкості та інтеграції для PrestaShop.</p>\n                        <a href="/internet-magazin/ukraine" class="btn">Деталі підтримки</a>',
    }

    for pattern, rep in replacements.items():
        html = re.sub(pattern, rep, html)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Links updated successfully!")

if __name__ == '__main__':
    fix_links()
