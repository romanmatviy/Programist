#!/usr/bin/env python3
"""
Генерує сторінки /programist/ukraine/{city}/ для запитів "програміст [місто]"
"""
import os
import shutil
import datetime

BASE_URL = "https://programist.matviy.pp.ua"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

cities = {
    'kyiv':           {'name': 'Київ',           'in': 'у Києві',           'coords': (50.4501, 30.5234), 'desc': 'Київ — столиця України та найбільший IT-хаб країни. Конкуренція в інтернеті надвисока, тому ваш сайт має бути бездоганним технічно та SEO-оптимізованим.'},
    'lviv':           {'name': 'Львів',           'in': 'у Львові',           'coords': (49.8397, 24.0297), 'desc': 'Львів — культурна столиця та один із провідних IT-центрів України. Місцевий бізнес активно виходить в онлайн, і грамотно зроблений сайт стає ключовою конкурентною перевагою.'},
    'kharkiv':        {'name': 'Харків',          'in': 'у Харкові',          'coords': (49.9935, 36.2304), 'desc': 'Харків — велике індустріальне та наукове місто. Підприємці Харкова дедалі більше шукають надійного веб-розробника для виходу в онлайн.'},
    'odesa':          {'name': 'Одеса',           'in': 'в Одесі',            'coords': (46.4825, 30.7233), 'desc': 'Одеса — портове місто з розвиненою торгівлею. Інтернет-магазини та корпоративні сайти тут особливо затребувані.'},
    'dnipro':         {'name': 'Дніпро',          'in': 'у Дніпрі',           'coords': (48.4647, 35.0461), 'desc': 'Дніпро — великий промисловий центр із активно зростаючим IT-сектором. Тут зростає попит на якісні сайти для бізнесу.'},
    'zaporizhzhia':   {'name': 'Запоріжжя',       'in': 'у Запоріжжі',        'coords': (47.8388, 35.1395), 'desc': 'Запоріжжя — промислове місто, де бізнес все активніше переходить в онлайн і потребує якісних веб-рішень.'},
    'vinnytsia':      {'name': 'Вінниця',         'in': 'у Вінниці',          'coords': (49.2330, 28.4682), 'desc': 'Вінниця — динамічний обласний центр, де малий і середній бізнес шукає фахового програміста для розробки сайту.'},
    'poltava':        {'name': 'Полтава',         'in': 'у Полтаві',          'coords': (49.5882, 34.5514), 'desc': 'Полтава — місто з розвиненим підприємництвом. Якісний веб-сайт допомагає полтавським компаніям залучати клієнтів з усієї України.'},
    'chernivtsi':     {'name': 'Чернівці',        'in': 'у Чернівцях',        'coords': (48.2914, 25.9333), 'desc': 'Чернівці — університетське місто на заході України. Місцевий бізнес активно виходить в онлайн і потребує надійного програміста.'},
    'cherkasy':       {'name': 'Черкаси',         'in': 'у Черкасах',         'coords': (49.4444, 32.0597), 'desc': 'Черкаси — місто з розвиненою промисловістю та торгівлею. Підприємці шукають програміста для створення сучасного веб-сайту.'},
    'chernihiv':      {'name': 'Чернігів',        'in': 'у Чернігові',        'coords': (51.4982, 31.2893), 'desc': 'Чернігів — одне з найстаріших міст України з активно зростаючим малим бізнесом, що потребує цифрового присутності.'},
    'zhytomyr':       {'name': 'Житомир',         'in': 'у Житомирі',         'coords': (50.2546, 28.6586), 'desc': 'Житомир — обласний центр із розвиненою торгівлею та підприємництвом. Замовити сайт тут стає все більш нагальною потребою для бізнесу.'},
    'ivano-frankivsk':{'name': 'Івано-Франківськ','in': 'в Івано-Франківську', 'coords': (48.9226, 24.7111), 'desc': 'Івано-Франківськ — місто з сильним підприємницьким духом і розвиненим туризмом. Тут особливо важливо мати гарний сайт для залучення клієнтів.'},
    'khmelnytskyi':   {'name': 'Хмельницький',   'in': 'у Хмельницькому',    'coords': (49.4229, 26.9871), 'desc': 'Хмельницький — активно зростаючий обласний центр. Місцевий бізнес шукає кваліфікованого програміста для виходу в інтернет.'},
    'ternopil':       {'name': 'Тернопіль',       'in': 'у Тернополі',        'coords': (49.5535, 25.5947), 'desc': 'Тернопіль — місто з розвиненою освітою та підприємництвом. Програміст із Тернополя або для Тернополя допоможе вашому бізнесу вийти в онлайн.'},
    'rivne':          {'name': 'Рівне',           'in': 'у Рівному',          'coords': (50.6199, 26.2516), 'desc': 'Рівне — обласний центр на Волині з розвиненою торгівлею та ремесли. Хороший сайт відкриє нові можливості для рівненського бізнесу.'},
    'lutsk':          {'name': 'Луцьк',           'in': 'у Луцьку',           'coords': (50.7472, 25.3253), 'desc': 'Луцьк активно розвивається: з\'являються нові підприємства, малий бізнес виходить в онлайн. Тут особливо затребуваний фаховий програміст для розробки сайтів.'},
    'sumy':           {'name': 'Суми',            'in': 'у Сумах',            'coords': (50.9077, 34.7981), 'desc': 'Суми — промисловий та освітній центр на Сумщині. Підприємці шукають надійного програміста для створення сайту та просування бізнесу в мережі.'},
    'mykolaiv':       {'name': 'Миколаїв',        'in': 'у Миколаєві',        'coords': (46.9750, 31.9945), 'desc': 'Миколаїв — портове місто з розвиненою промисловістю та торгівлею. Якісний веб-сайт відкриє нові ринки для миколаївських підприємців.'},
    'kropyvnytskyi':  {'name': 'Кропивницький',  'in': 'у Кропивницькому',   'coords': (48.5079, 32.2623), 'desc': 'Кропивницький — центр Кіровоградщини. Місцеві підприємці все частіше звертаються до програмістів за розробкою сучасних сайтів.'},
    'uzhorod':        {'name': 'Ужгород',         'in': 'в Ужгороді',         'coords': (48.6208, 22.2878), 'desc': 'Ужгород — найзахідніше місто України з розвиненим туризмом та торгівлею. Гарний сайт допоможе ужгородському бізнесу залучати клієнтів з усього регіону.'},
    'kryvyi-rih':     {'name': 'Кривий Ріг',      'in': 'у Кривому Розі',     'coords': (47.9105, 33.3917), 'desc': 'Кривий Ріг — одне з найбільших міст України. Великий ринок потребує якісних веб-рішень для виходу бізнесу в онлайн.'},
    'mariupol':       {'name': 'Маріуполь',       'in': 'у Маріуполі',        'coords': (47.0971, 37.5433), 'desc': 'Маріуполь — портове місто з розвиненою промисловістю. Веб-присутність стає критично важливою для місцевого бізнесу.'},
}

CSS = """:root{--primary-color:#2563eb;--secondary-color:#1e40af;--text-color:#333;--light-bg:#f8fafc;--dark-bg:#1f2937;--font-main:'Roboto',sans-serif;--font-heading:'Montserrat',sans-serif;}*{margin:0;padding:0;box-sizing:border-box;}body{font-family:var(--font-main);color:var(--text-color);line-height:1.6;}.container{width:100%;max-width:1200px;margin:0 auto;padding:0 20px;}header{background-color:#fff;box-shadow:0 2px 10px rgba(0,0,0,0.1);position:sticky;top:0;z-index:100;}.header-container{display:flex;justify-content:space-between;align-items:center;padding:20px 15px;}.logo{font-size:24px;font-weight:700;color:var(--primary-color);text-decoration:none;}nav ul{display:flex;list-style:none;}nav ul li{margin-left:25px;}nav ul li a{text-decoration:none;color:var(--text-color);font-weight:500;transition:color 0.3s;}nav ul li a:hover{color:var(--primary-color);}.hero{padding:100px 0 60px;background:linear-gradient(135deg,#1e3a8a 0%,#2563eb 60%,#3b82f6 100%);color:#fff;text-align:center;}.hero h1{font-family:var(--font-heading);font-size:46px;margin-bottom:20px;line-height:1.2;}.hero p{font-size:20px;max-width:750px;margin:0 auto 30px;opacity:.92;}.hero-badges{display:flex;gap:15px;justify-content:center;flex-wrap:wrap;margin-bottom:35px;}.badge{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.3);padding:6px 16px;border-radius:20px;font-size:14px;font-weight:500;}.btn{display:inline-block;padding:14px 34px;background-color:#fff;color:var(--primary-color);text-decoration:none;border-radius:8px;font-weight:700;font-size:16px;transition:all 0.3s;box-shadow:0 4px 15px rgba(0,0,0,.15);}.btn:hover{transform:translateY(-2px);box-shadow:0 8px 25px rgba(0,0,0,.2);}.btn-outline{background:transparent;color:#fff;border:2px solid #fff;margin-left:15px;}.btn-outline:hover{background:#fff;color:var(--primary-color);}main{padding:60px 0;}.section-title{font-family:var(--font-heading);font-size:34px;margin-bottom:40px;text-align:center;color:var(--primary-color);}.breadcrumbs{margin-bottom:30px;font-size:14px;color:#666;}.breadcrumbs a{color:var(--primary-color);text-decoration:none;}.breadcrumbs a:hover{text-decoration:underline;}.seo-content{max-width:820px;margin:0 auto;}.seo-content h2{font-size:26px;margin:35px 0 15px;color:var(--primary-color);font-family:var(--font-heading);}.seo-content h3{font-size:20px;margin:25px 0 12px;color:var(--dark-bg);}.seo-content p{margin-bottom:18px;line-height:1.8;font-size:16px;}.seo-content ul,.seo-content ol{margin-bottom:18px;padding-left:24px;}.seo-content li{margin-bottom:10px;line-height:1.7;}.highlight-box{background:linear-gradient(135deg,#eff6ff,#dbeafe);border-left:4px solid var(--primary-color);padding:20px 24px;border-radius:0 8px 8px 0;margin:30px 0;}.highlight-box p{margin:0;font-size:16px;font-style:italic;color:#1e40af;}.services-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:24px;margin:40px 0;}.service-card{background:#fff;border-radius:12px;padding:24px;box-shadow:0 4px 20px rgba(0,0,0,.06);border:1px solid #e2e8f0;transition:all 0.3s;text-decoration:none;display:block;color:inherit;}.service-card:hover{transform:translateY(-4px);box-shadow:0 10px 30px rgba(37,99,235,.12);border-color:#93c5fd;}.service-card h3{font-size:18px;color:var(--primary-color);margin-bottom:8px;}.service-card p{font-size:14px;color:#666;margin:0;}.service-icon{font-size:28px;margin-bottom:12px;}.cta-section{background:linear-gradient(135deg,#1e3a8a,#2563eb);color:#fff;padding:70px 0;text-align:center;margin:60px 0;}.cta-section h2{font-size:34px;margin-bottom:15px;font-family:var(--font-heading);}.cta-section p{font-size:18px;max-width:650px;margin:0 auto 35px;opacity:.9;}.testimonials{padding:80px 0;background:#f8fbff;}.testimonials-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:30px;margin-top:40px;}.testimonial-card{background:#fff;padding:30px;border-radius:12px;box-shadow:0 10px 30px rgba(0,0,0,.05);}.testimonial-text{font-style:italic;color:#444;line-height:1.7;margin-bottom:20px;}.testimonial-author{display:flex;flex-direction:column;}.author-name{font-weight:600;color:var(--dark-bg);margin-bottom:4px;}.author-role{color:#7f8c8d;font-size:14px;}.stars{color:#f59e0b;margin-bottom:15px;font-size:18px;}.about-content{display:grid;grid-template-columns:1fr 380px;gap:60px;align-items:center;padding:20px 0;}.about-text p{font-size:16px;line-height:1.8;margin-bottom:18px;color:#444;}.about-skills{list-style:none;padding:0;margin-top:10px;}.about-skills li{font-size:15px;padding:8px 0;border-bottom:1px solid #f0f0f0;color:#333;}.about-photo img{width:100%;border-radius:16px;box-shadow:0 20px 60px rgba(37,99,235,.15);}@media(max-width:900px){.about-content{grid-template-columns:1fr;gap:40px;}}.faq-section{padding:80px 0;background:#fff;}.faq-col{max-width:800px;margin:0 auto;display:flex;flex-direction:column;gap:12px;}.faq-item{border:1px solid #e2e8f0;border-radius:10px;overflow:hidden;}.faq-q{width:100%;display:flex;justify-content:space-between;align-items:center;padding:20px 24px;background:none;border:none;font-size:17px;font-weight:600;color:var(--dark-bg);cursor:pointer;text-align:left;font-family:var(--font-main);transition:color 0.2s;}.faq-q:hover{color:var(--primary-color);}.faq-ic{font-size:22px;color:var(--primary-color);transition:transform 0.3s;flex-shrink:0;margin-left:16px;}.faq-item.open .faq-ic{transform:rotate(45deg);}.faq-a{max-height:0;overflow:hidden;transition:max-height 0.4s ease,padding 0.3s ease;padding:0 24px;}.faq-item.open .faq-a{max-height:300px;padding:0 24px 20px;}.faq-a p{color:#555;line-height:1.7;font-size:15px;}.contact-section{padding:80px 0;background:var(--light-bg);}.contact-wrap{display:flex;flex-direction:column;gap:40px;}@media(min-width:900px){.contact-wrap{flex-direction:row;gap:60px;}}.contact-left{flex:1;}.contact-right{flex:1;background:#fff;padding:40px;border-radius:12px;box-shadow:0 10px 40px rgba(0,0,0,.06);}.contact-left h2{font-family:var(--font-heading);font-size:38px;color:var(--dark-bg);margin-bottom:20px;}.contact-left p{color:#555;font-size:16px;margin-bottom:35px;line-height:1.7;}.c-info-grid{display:grid;grid-template-columns:1fr 1fr;gap:25px;}.c-info-item{display:flex;flex-direction:column;gap:6px;}.c-icon{font-size:22px;}.c-info-item h4{font-size:12px;text-transform:uppercase;color:#888;letter-spacing:1px;}.c-info-item a,.c-info-item span{color:var(--dark-bg);font-weight:500;text-decoration:none;font-size:15px;transition:color 0.2s;}.c-info-item a:hover{color:var(--primary-color);}.form-group{margin-bottom:18px;}.form-group label{display:block;font-weight:500;margin-bottom:8px;color:var(--dark-bg);}.form-group input,.form-group select,.form-group textarea{width:100%;border:1px solid #e2e8f0;border-radius:8px;padding:13px 15px;font-size:15px;outline:none;background:#f8fafc;transition:border-color 0.2s;box-sizing:border-box;}.form-group input:focus,.form-group select:focus,.form-group textarea:focus{border-color:var(--primary-color);background:#fff;}.submit-btn{width:100%;padding:15px;background:var(--primary-color);color:#fff;border:none;border-radius:8px;font-size:16px;font-weight:600;cursor:pointer;transition:background 0.2s;}.submit-btn:hover{background:var(--secondary-color);}footer{background:var(--dark-bg);color:#fff;padding:60px 0 30px;}.footer-container{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:40px;margin-bottom:40px;}.footer-col h3{font-size:18px;margin-bottom:18px;}.footer-col ul{list-style:none;}.footer-col ul li{margin-bottom:8px;}.footer-col ul li a{color:#ccc;text-decoration:none;transition:color 0.2s;font-size:14px;}.footer-col ul li a:hover{color:#fff;}.copyright{text-align:center;padding-top:25px;border-top:1px solid rgba(255,255,255,.1);font-size:13px;color:#9ca3af;}.mobile-menu-toggle{display:none;flex-direction:column;justify-content:space-around;width:28px;height:22px;background:transparent;border:none;cursor:pointer;}.mobile-menu-toggle span{width:28px;height:2px;background:var(--primary-color);border-radius:4px;transition:all 0.3s;}.mobile-menu-toggle.active span:first-child{transform:rotate(45deg);}.mobile-menu-toggle.active span:nth-child(2){opacity:0;}.mobile-menu-toggle.active span:nth-child(3){transform:rotate(-45deg);}@media(max-width:768px){.mobile-menu-toggle{display:flex;}nav ul{position:fixed;top:65px;left:0;width:100%;height:calc(100vh - 65px);background:#fff;flex-direction:column;align-items:center;padding-top:40px;transform:translateX(100%);transition:transform 0.3s ease;}nav ul.active{transform:translateX(0);}nav ul li{margin:12px 0;}nav ul li a{font-size:18px;}.hero h1{font-size:30px;}.hero p{font-size:16px;}.hero-badges{gap:10px;}.section-title{font-size:26px;}.services-grid{grid-template-columns:1fr;}.about-content{grid-template-columns:1fr;}.contact-wrap{flex-direction:column;}.c-info-grid{grid-template-columns:1fr;}}.lm-banner-wrap{background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #93c5fd;border-radius:16px;padding:40px;margin:60px 0;display:flex;align-items:center;gap:40px;box-shadow:0 10px 30px rgba(37,99,235,.1);}@media(max-width:900px){.lm-banner-wrap{flex-direction:column;padding:30px 20px;gap:20px;}}.lm-text h3{font-size:28px;color:#1e3a8a;margin-bottom:15px;font-family:var(--font-heading);}.lm-text p{color:#334155;font-size:16px;margin-bottom:0;line-height:1.6;}.lm-form-wrap{flex:1;min-width:320px;width:100%;}.lm-form{display:flex;flex-direction:column;gap:12px;}.lm-form input{padding:14px 16px;border:1px solid #cbd5e1;border-radius:8px;font-size:15px;outline:none;}.lm-form input:focus{border-color:var(--primary-color);}.lm-form button{background:var(--primary-color);color:#fff;border:none;padding:15px;border-radius:8px;font-size:16px;font-weight:600;cursor:pointer;transition:0.2s;}.lm-form button:hover{background:var(--secondary-color);}.lm-success{color:#047857;background:#d1fae5;padding:15px;border-radius:8px;text-align:center;font-weight:500;margin-top:10px;display:none;}.lm-modal{position:fixed;inset:0;background:rgba(15,23,42,.7);display:flex;justify-content:center;align-items:center;z-index:1000;opacity:0;visibility:hidden;transition:all 0.3s ease;backdrop-filter:blur(4px);}.lm-modal.show{opacity:1;visibility:visible;}.lm-modal-content{background:#fff;width:90%;max-width:450px;border-radius:16px;padding:35px 30px;position:relative;transform:translateY(20px);transition:transform 0.4s ease;box-shadow:0 25px 50px rgba(0,0,0,.25);}.lm-modal.show .lm-modal-content{transform:translateY(0);}.lm-close{position:absolute;top:15px;right:20px;background:none;border:none;font-size:28px;color:#64748b;cursor:pointer;line-height:1;}.lm-close:hover{color:#0f172a;}.lm-modal-content h3{font-size:24px;color:#1e3a8a;margin-bottom:15px;text-align:center;font-family:var(--font-heading);}.lm-modal-content p{text-align:center;color:#475569;margin-bottom:25px;font-size:15px;line-height:1.6;}"""

def generate_page(city_slug, city_data):
    name = city_data['name']
    city_in = city_data['in']
    lat, lon = city_data['coords']
    city_desc = city_data['desc']
    current_year = datetime.datetime.now().year

    # Пов'язані послуги
    related_services = [
        ('rozrobka-saitiv', 'Розробка сайтів', '🌐', 'Сучасний сайт під ключ з SEO-оптимізацією'),
        ('internet-magazin', 'Інтернет-магазин', '🛒', 'Повнофункціональний магазин з оплатою та CRM'),
        ('wordpress', 'WordPress', '📝', 'Сайти та блоги на найпопулярнішій CMS'),
        ('seo-optimizatsiya', 'SEO оптимізація', '📈', 'Просування в Google та підвищення трафіку'),
        ('laravel', 'Laravel', '⚡', 'Складні веб-додатки на потужному PHP-фреймворку'),
        ('crm-erp', 'CRM/ERP системи', '🏢', 'Автоматизація бізнес-процесів вашої компанії'),
    ]

    def service_card(slug, label, icon, desc):
        href = '/' + slug + '/ukraine/' + city_slug + '/'
        return (
            '            <a href="' + href + '" class="service-card">\n'
            '              <div class="service-icon">' + icon + '</div>\n'
            '              <h3>' + label + '</h3>\n'
            '              <p>' + desc + '</p>\n'
            '            </a>'
        )

    related_html = '\n'.join([service_card(s, label, icon, desc) for s, label, icon, desc in related_services])

    page = f'''<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Програміст {name} [{current_year}] 🚀 | Роман Матвій — від $300 ✓ 500+ проєктів</title>
    <meta name="description" content="Програміст {city_in}. Розробка сайтів, інтернет-магазинів, CRM від $300. 10+ років досвіду, 500+ проєктів. Безкоштовна консультація ✓">

    <!-- Canonical -->
    <link rel="canonical" href="{BASE_URL}/programist/ukraine/{city_slug}/">

    <!-- Favicon -->
    <link rel="icon" href="{BASE_URL}/img/favicon.ico" type="image/x-icon">

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Roboto:wght@300;400;500;700&display=swap" media="print" onload="this.media='all'">
    <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Roboto:wght@300;400;500;700&display=swap"></noscript>

    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="Програміст {name} [{current_year}] 🚀 | Роман Матвій">
    <meta property="og:description" content="Програміст {city_in} — Роман Матвій. Розробка сайтів від $300. Безкоштовна консультація.">
    <meta property="og:url" content="{BASE_URL}/programist/ukraine/{city_slug}/">
    <meta property="og:image" content="{BASE_URL}/img/og-image.jpg">
    <meta property="og:site_name" content="Програміст Роман">

    <!-- Twitter Cards -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Програміст {name} [{current_year}] 🚀 | Роман Матвій">
    <meta name="twitter:description" content="Програміст {city_in}. Розробка сайтів від $300. Безкоштовна консультація.">
    <meta name="twitter:image" content="{BASE_URL}/img/og-image.jpg">

    <!-- Schema.org JSON-LD -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@graph": [
        {{
          "@type": "Person",
          "@id": "{BASE_URL}/#person",
          "name": "Роман Матвій",
          "jobTitle": "Full Stack Senior Developer",
          "url": "{BASE_URL}",
          "sameAs": [
            "https://www.linkedin.com/in/romanmatviy/",
            "https://github.com/romanmatviy",
            "https://t.me/MatviyRoman"
          ]
        }},
        {{
          "@type": "BreadcrumbList",
          "@id": "{BASE_URL}/programist/ukraine/{city_slug}/#breadcrumb",
          "itemListElement": [
            {{
              "@type": "ListItem",
              "position": 1,
              "name": "Головна",
              "item": "{BASE_URL}/"
            }},
            {{
              "@type": "ListItem",
              "position": 2,
              "name": "Програміст",
              "item": "{BASE_URL}/programist/ukraine/"
            }},
            {{
              "@type": "ListItem",
              "position": 3,
              "name": "{name}",
              "item": "{BASE_URL}/programist/ukraine/{city_slug}/"
            }}
          ]
        }},
        {{
          "@type": "ProfessionalService",
          "name": "Програміст Роман Матвій — {name}",
          "description": "Розробка сайтів, інтернет-магазинів та CRM/ERP систем {city_in}. Програміст з 10+ роками досвіду.",
          "url": "{BASE_URL}/programist/ukraine/{city_slug}/",
          "telephone": "+380938800822",
          "email": "info@matviy.pp.ua",
          "address": {{
            "@type": "PostalAddress",
            "addressLocality": "{name}",
            "addressCountry": "UA"
          }},
          "geo": {{
            "@type": "GeoCoordinates",
            "latitude": {lat},
            "longitude": {lon}
          }},
          "areaServed": {{"@type": "City", "name": "{name}"}},
          "priceRange": "$$",
          "openingHours": "Mo-Fr 09:00-18:00",
          "image": "{BASE_URL}/img/programist-fullstack-Roman-Senior-Developer.png",
          "offers": {{
            "@type": "Offer",
            "price": "300",
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock"
          }},
          "aggregateRating": {{
            "@type": "AggregateRating",
            "ratingValue": "5",
            "reviewCount": "24"
          }},
          "founder": {{"@id": "{BASE_URL}/#person"}}
        }},
        {{
          "@type": "FAQPage",
          "mainEntity": [
            {{
              "@type": "Question",
              "name": "Скільки коштує сайт {city_in}?",
              "acceptedAnswer": {{
                "@type": "Answer",
                "text": "Сайт-візитка — від $300, інтернет-магазин — від $800, веб-додаток (CRM/ERP) — від $1500. Безкоштовна оцінка протягом 24 годин."
              }}
            }},
            {{
              "@type": "Question",
              "name": "Які терміни розробки сайту?",
              "acceptedAnswer": {{
                "@type": "Answer",
                "text": "Landing Page: 5–10 днів. Корпоративний сайт: 2–4 тижні. Інтернет-магазин: 4–8 тижнів."
              }}
            }},
            {{
              "@type": "Question",
              "name": "Чи надаєте підтримку після запуску?",
              "acceptedAnswer": {{
                "@type": "Answer",
                "text": "Так. Безкоштовна 30-денна гарантія на кожен проєкт. Надалі — погодинна або абонентська підтримка."
              }}
            }}
          ]
        }}
      ]
    }}
    </script>

    <style>{CSS}</style>
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
                    <li><a href="/blog/">Блог</a></li>
                    <li><a href="/faq.html">FAQ</a></li>
                    <li><a href="/#contact">Контакти</a></li>
                </ul>
            </nav>
            <button class="mobile-menu-toggle" aria-label="Меню">
                <span></span><span></span><span></span>
            </button>
        </div>
    </header>

    <!-- Hero -->
    <section class="hero">
        <div class="container">
            <div class="hero-badges">
                <span class="badge">⭐ 5/5 — 24 відгуки</span>
                <span class="badge">✅ 500+ проєктів</span>
                <span class="badge">🕐 10+ років досвіду</span>
            </div>
            <h1>Програміст {name}<br>Роман Матвій</h1>
            <p>Розробка сайтів, інтернет-магазинів та CRM-систем {city_in}. Від $300. Безкоштовна консультація.</p>
            <a href="#contact" class="btn">Замовити консультацію</a>
            <a href="tel:+380938800822" class="btn btn-outline">📞 Подзвонити</a>
        </div>
    </section>

    <!-- Main -->
    <main>
        <div class="container">
            <!-- Breadcrumbs -->
            <nav class="breadcrumbs" aria-label="Breadcrumb">
                <ol itemscope itemtype="https://schema.org/BreadcrumbList" style="list-style:none;padding:0;display:flex;flex-wrap:wrap;gap:5px;">
                    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
                        <a itemprop="item" href="/"><span itemprop="name">Головна</span></a>
                        <meta itemprop="position" content="1">
                    </li>
                    <span>›</span>
                    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
                        <a itemprop="item" href="/programist/ukraine/"><span itemprop="name">Програміст Україна</span></a>
                        <meta itemprop="position" content="2">
                    </li>
                    <span>›</span>
                    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
                        <span itemprop="name">{name}</span>
                        <meta itemprop="position" content="3">
                    </li>
                </ol>
            </nav>

            <!-- SEO Content -->
            <div class="seo-content">
                <h2>Програміст {city_in} — чим я можу вам допомогти?</h2>
                <p>{city_desc}</p>
                <p>Я Роман Матвій — фрілансер-програміст із понад <strong>10-річним досвідом</strong>. Я розробляю <strong>сайти, інтернет-магазини та CRM/ERP-системи</strong> для клієнтів по всій Україні. Прямий контакт із виконавцем, без посередників та прихованих платежів.</p>

                <div class="highlight-box">
                    <p>«Сайт від $300 — це реальна ціна. Я не беру гроші за офіс у центрі міста та штат менеджерів. Ви платите лише за роботу програміста.»</p>
                </div>

                <h2>Що я розробляю {city_in}</h2>
                <ul>
                    <li><strong>Сайти-візитки та лендінги</strong> — від $300, термін 5–10 днів</li>
                    <li><strong>Корпоративні сайти</strong> — від $600, термін 2–4 тижні</li>
                    <li><strong>Інтернет-магазини</strong> — від $800 (WooCommerce, PrestaShop, OpenCart)</li>
                    <li><strong>WordPress сайти</strong> — розробка, налаштування, плагіни</li>
                    <li><strong>Laravel веб-додатки</strong> — CRM, ERP, портали, API</li>
                    <li><strong>SEO-оптимізація</strong> — технічна, on-page, локальне SEO для {name}</li>
                </ul>

                <h2>Чому обирають мене, а не агенцію?</h2>
                <ul>
                    <li>🎯 <strong>Ви спілкуєтесь напряму з програмістом</strong> — без менеджерів та зіпсованого телефону</li>
                    <li>💰 <strong>Ціна нижча на 30–50%</strong> порівняно з веб-студіями — за рахунок відсутності офісу</li>
                    <li>⚡ <strong>Швидше та гнучкіше</strong> — легко вносити зміни без бюрократії</li>
                    <li>🔒 <strong>30-денна безкоштовна гарантія</strong> після здачі проєкту</li>
                    <li>📍 <strong>Дистанційно по всій Україні</strong> — для {name} та будь-якого міста</li>
                </ul>

                <h2>Стек технологій</h2>
                <ul>
                    <li><strong>Frontend:</strong> HTML5, CSS3, JavaScript, Vue.js, React, Next.js</li>
                    <li><strong>Backend:</strong> PHP 8+ (Laravel), Node.js</li>
                    <li><strong>CMS:</strong> WordPress, PrestaShop, OpenCart</li>
                    <li><strong>Бази даних:</strong> MySQL, PostgreSQL</li>
                    <li><strong>Інструменти:</strong> Docker, Git, REST API</li>
                </ul>
            </div>
        </div>

        <!-- Services Grid -->
        <section style="padding:60px 0;background:var(--light-bg);">
            <div class="container">
                <h2 class="section-title">Послуги {city_in}</h2>
                <div class="services-grid">
{related_html}
                </div>
            </div>
        </section>

        <!-- CTA -->
        <section class="cta-section">
            <div class="container">
                <h2>Готові замовити розробку {city_in}?</h2>
                <p>Опишіть свій проєкт — я надішлю безкоштовну оцінку вартості протягом 24 годин</p>
                <a href="#contact" class="btn">Замовити консультацію</a>
                <a href="tel:+380938800822" class="btn btn-outline" style="margin-left:15px;">📞 +38 (093) 88-00-822</a>
            </div>
        </section>

        <!-- Testimonials -->
        <section class="testimonials">
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
                        <p class="testimonial-text">Замовляли SEO-оптимізацію та редизайн сайту на WordPress. Позиції в Google значно виросли вже за перший місяць після запуску нової версії.</p>
                        <div class="testimonial-author">
                            <span class="author-name">Сергій Притула</span>
                            <span class="author-role">Співзасновник Creative Agency</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- About -->
        <section style="padding:80px 0;background:#fff;">
            <div class="container">
                <h2 class="section-title">Про мене</h2>
                <div class="about-content">
                    <div class="about-text">
                        <p>Я Роман Матвій, програміст із понад 10-річним досвідом розробки сайтів та веб-додатків. Працюю з клієнтами {city_in} та по всій Україні дистанційно.</p>
                        <p>Спеціалізуюсь на Laravel, WordPress, PrestaShop, Vue.js, Next.js та Node.js. Моя мета — не просто написати код, а створити інструмент, який реально приносить клієнтів та прибуток.</p>
                        <ul class="about-skills">
                            <li>✅ 10+ років досвіду у веб-розробці</li>
                            <li>✅ 500+ успішних проєктів</li>
                            <li>✅ SEO-оптимізація вбудована в кожен проєкт</li>
                            <li>✅ 30-денна безкоштовна гарантія</li>
                            <li>✅ Пряма комунікація, без менеджерів</li>
                        </ul>
                    </div>
                    <div class="about-photo">
                        <img src="/img/programist-fullstack-Roman-Senior-Developer.png" alt="Програміст Роман Матвій — Full Stack Senior Developer" width="380" height="380" loading="lazy">
                    </div>
                </div>
            </div>
        </section>

        <!-- FAQ -->
        <section class="faq-section">
            <div class="container">
                <h2 class="section-title">Часті запитання</h2>
                <div class="faq-col">
                    <div class="faq-item">
                        <button class="faq-q" aria-expanded="false">Скільки коштує сайт {city_in}?<span class="faq-ic">+</span></button>
                        <div class="faq-a"><p>Сайт-візитка — від $300, корпоративний сайт — від $600, інтернет-магазин — від $800, веб-додаток (CRM/ERP) — від $1500. Безкоштовна оцінка протягом 24 годин після брифу.</p></div>
                    </div>
                    <div class="faq-item">
                        <button class="faq-q" aria-expanded="false">Які терміни розробки?<span class="faq-ic">+</span></button>
                        <div class="faq-a"><p>Landing Page: 5–10 робочих днів. Корпоративний сайт: 2–4 тижні. Інтернет-магазин: 4–8 тижнів. Складний веб-додаток: від 8 тижнів. Терміни фіксуються у договорі.</p></div>
                    </div>
                    <div class="faq-item">
                        <button class="faq-q" aria-expanded="false">Чи потрібен офіс або зустріч {city_in}?<span class="faq-ic">+</span></button>
                        <div class="faq-a"><p>Ні. Я працюю повністю дистанційно через Telegram, Zoom або email. Це зручно та дозволяє заощадити час для обох сторін.</p></div>
                    </div>
                    <div class="faq-item">
                        <button class="faq-q" aria-expanded="false">Чи надаєте підтримку після запуску?<span class="faq-ic">+</span></button>
                        <div class="faq-a"><p>Так. Безкоштовна 30-денна гарантія на кожен проєкт. Після цього — погодинна підтримка або щомісячна підписка за домовленістю.</p></div>
                    </div>
                    <div class="faq-item">
                        <button class="faq-q" aria-expanded="false">Як відбувається оплата?<span class="faq-ic">+</span></button>
                        <div class="faq-a"><p>Передоплата 30–50%, решта — після здачі проєкту. Для великих проєктів — поетапна оплата. Способи: банківський переказ, Wise, PayPal.</p></div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Lead Magnet Banner -->
        <section class="container">
            <div class="lm-banner-wrap">
                <div class="lm-text">
                    <h3>Отримайте безкоштовний SEO-аудит вашого сайту</h3>
                    <p>Дізнайтесь, чому ваш сайт втрачає клієнтів у Google та як це виправити. Залиште email та адресу сайту, і я надішлю вам детальний звіт.</p>
                </div>
                <div class="lm-form-wrap">
                    <form class="lm-form" action="/contact.php" method="POST">
                        <input type="hidden" name="source" value="SEO Audit Banner - {name}">
                        <input type="hidden" name="message" class="hidden-message" value="">
                        <input type="text" name="name" placeholder="Ваше ім'я" required>
                        <input type="email" name="email" placeholder="Ваш Email" required>
                        <input type="url" name="website" placeholder="Посилання на сайт (напр. https://...)" required>
                        <button type="submit">Отримати аудит 🚀</button>
                    </form>
                    <div class="lm-success">Дякуємо! Ваша заявка прийнята. Я надішлю аудит найближчим часом.</div>
                </div>
            </div>
        </section>

        <!-- Contact -->
        <section class="contact-section" id="contact">
            <div class="container">
                <div class="contact-wrap">
                    <div class="contact-left">
                        <h2>Замовте сайт {city_in}</h2>
                        <p>Опишіть ваш проєкт — я зв'яжуся протягом 24 годин з безкоштовною оцінкою вартості.</p>
                        <div class="c-info-grid">
                            <div class="c-info-item"><div class="c-icon">📧</div><h4>Email</h4><a href="mailto:info@matviy.pp.ua">info@matviy.pp.ua</a></div>
                            <div class="c-info-item"><div class="c-icon">📱</div><h4>Телефон / WhatsApp</h4><a href="tel:+380938800822">+38 (093) 88-00-822</a></div>
                            <div class="c-info-item"><div class="c-icon">✈️</div><h4>Telegram</h4><a href="https://t.me/MatviyRoman" target="_blank" rel="noopener">@MatviyRoman</a></div>
                            <div class="c-info-item"><div class="c-icon">🕐</div><h4>Робочі години</h4><span>Пн–Пт: 9:00–18:00</span></div>
                        </div>
                    </div>
                    <div class="contact-right">
                        <form class="contact-form-new" action="/contact.php" method="POST">
                            <input type="hidden" name="source" value="programist-{city_slug}">
                            <div class="form-group"><label for="name_{city_slug}">Ваше ім'я *</label><input type="text" id="name_{city_slug}" name="name" placeholder="Як до вас звертатися?" required></div>
                            <div class="form-group"><label for="email_{city_slug}">Email *</label><input type="email" id="email_{city_slug}" name="email" placeholder="ivan@firma.ua" required></div>
                            <div class="form-group"><label for="service_{city_slug}">Що потрібно?</label>
                                <select id="service_{city_slug}" name="service">
                                    <option value="" disabled selected>— Виберіть —</option>
                                    <option>Розробка сайту</option>
                                    <option>Інтернет-магазин</option>
                                    <option>CRM / ERP система</option>
                                    <option>SEO оптимізація</option>
                                    <option>Інше</option>
                                </select>
                            </div>
                            <div class="form-group"><label for="message_{city_slug}">Опис проєкту *</label><textarea id="message_{city_slug}" name="message" rows="4" placeholder="Опишіть що потрібно..." required></textarea></div>
                            <button type="submit" class="submit-btn">Надіслати запит ✉️</button>
                        </form>
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
                        <li><a href="/rozrobka-saitiv/ukraine/{city_slug}/">Розробка сайтів</a></li>
                        <li><a href="/internet-magazin/ukraine/{city_slug}/">Інтернет-магазини</a></li>
                        <li><a href="/wordpress/ukraine/{city_slug}/">WordPress</a></li>
                        <li><a href="/laravel/ukraine/{city_slug}/">Laravel</a></li>
                        <li><a href="/seo-optimizatsiya/ukraine/{city_slug}/">SEO оптимізація</a></li>
                        <li><a href="/crm-erp/ukraine/{city_slug}/">CRM/ERP системи</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h3>Міста</h3>
                    <ul>
                        <li><a href="/programist/ukraine/kyiv/">Київ</a></li>
                        <li><a href="/programist/ukraine/lviv/">Львів</a></li>
                        <li><a href="/programist/ukraine/kharkiv/">Харків</a></li>
                        <li><a href="/programist/ukraine/dnipro/">Дніпро</a></li>
                        <li><a href="/programist/ukraine/lutsk/">Луцьк</a></li>
                        <li><a href="/programist/ukraine/ivano-frankivsk/">Івано-Франківськ</a></li>
                        <li><a href="/programist/ukraine/ternopil/">Тернопіль</a></li>
                        <li><a href="/programist/ukraine/chernivtsi/">Чернівці</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h3>Контакти</h3>
                    <ul>
                        <li>📞 <a href="tel:+380938800822">+38 (093) 88-00-822</a></li>
                        <li>📧 <a href="mailto:info@matviy.pp.ua">info@matviy.pp.ua</a></li>
                        <li>✈️ <a href="https://t.me/MatviyRoman" target="_blank" rel="noopener">Telegram: @MatviyRoman</a></li>
                    </ul>
                </div>
            </div>
            <div class="copyright">© 2026 Програміст Роман Матвій. Всі права захищені.</div>
        </div>
    </footer>

    <script>
    // Mobile menu
    const toggle = document.querySelector('.mobile-menu-toggle');
    const navList = document.querySelector('nav ul');
    if (toggle) {{
        toggle.addEventListener('click', () => {{
            toggle.classList.toggle('active');
            navList.classList.toggle('active');
        }});
    }}
    // FAQ accordion
    document.querySelectorAll('.faq-q').forEach(btn => {{
        btn.addEventListener('click', () => {{
            const item = btn.closest('.faq-item');
            const isOpen = item.classList.contains('open');
            document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
            if (!isOpen) item.classList.add('open');
            btn.setAttribute('aria-expanded', !isOpen);
        }});
    }});
    // Smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(a => {{
        a.addEventListener('click', e => {{
            e.preventDefault();
            const target = document.querySelector(a.getAttribute('href'));
            if (target) target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
        }});
    }});
    </script>
</body>
</html>'''
    return page


def generate_index_page():
    """Генерує /programist/ukraine/index.html"""
    city_links = '\n'.join([
        f'                    <li><a href="/programist/ukraine/{slug}/">Програміст {data["name"]}</a></li>'
        for slug, data in sorted(cities.items(), key=lambda x: x[1]['name'])
    ])

    current_year = datetime.datetime.now().year
    return f'''<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Програміст Україна [{current_year}] 🚀 | Роман Матвій — Розробка сайтів по містах</title>
    <meta name="description" content="Програміст-фрілансер Роман Матвій. Розробка сайтів по всій Україні від $300. Виберіть своє місто та замовте безкоштовну консультацію.">
    
    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="Програміст Україна [{current_year}] 🚀 | Роман Матвій">
    <meta property="og:description" content="Програміст-фрілансер Роман Матвій. Розробка сайтів по всій Україні від $300.">
    <meta property="og:url" content="{BASE_URL}/programist/ukraine/">
    <meta property="og:image" content="{BASE_URL}/img/og-image.jpg">
    <meta property="og:site_name" content="Програміст Роман">

    <!-- Twitter Cards -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Програміст Україна [{current_year}] 🚀 | Роман Матвій">
    <meta name="twitter:description" content="Програміст-фрілансер Роман Матвій. Розробка сайтів по всій Україні від $300.">
    <meta name="twitter:image" content="{BASE_URL}/img/og-image.jpg">
    <link rel="canonical" href="{BASE_URL}/programist/ukraine/">
    <link rel="icon" href="{BASE_URL}/img/favicon.ico" type="image/x-icon">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Roboto:wght@300;400;500;700&display=swap" media="print" onload="this.media='all'">
    <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Roboto:wght@300;400;500;700&display=swap"></noscript>
    <style>{CSS}
    .cities-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:15px;margin-top:30px;}}
    .city-link{{display:block;padding:14px 20px;background:#fff;border:1px solid #e2e8f0;border-radius:8px;text-decoration:none;color:var(--primary-color);font-weight:500;transition:all 0.2s;}}
    .city-link:hover{{background:var(--primary-color);color:#fff;transform:translateY(-2px);box-shadow:0 5px 15px rgba(37,99,235,.2);}}
    </style>
</head>
<body>
    <header>
        <div class="container header-container">
            <a href="/" class="logo">RomanDev</a>
            <nav><ul>
                <li><a href="/#services">Послуги</a></li>
                <li><a href="/#portfolio">Портфоліо</a></li>
                <li><a href="/#about">Про мене</a></li>
                <li><a href="/blog/">Блог</a></li>
                <li><a href="/faq.html">FAQ</a></li>
                <li><a href="/#contact">Контакти</a></li>
            </ul></nav>
            <button class="mobile-menu-toggle" aria-label="Меню"><span></span><span></span><span></span></button>
        </div>
    </header>

    <section class="hero">
        <div class="container">
            <div class="hero-badges">
                <span class="badge">⭐ 5/5 — 24 відгуки</span>
                <span class="badge">✅ 500+ проєктів</span>
                <span class="badge">🕐 10+ років досвіду</span>
            </div>
            <h1>Програміст по всій Україні</h1>
            <p>Роман Матвій — розробка сайтів, інтернет-магазинів та CRM для бізнесу в будь-якому місті України. Від $300.</p>
            <a href="/#contact" class="btn">Замовити консультацію</a>
        </div>
    </section>

    <main>
        <div class="container" style="padding:60px 20px;">
            <h2 class="section-title">Виберіть ваше місто</h2>
            <div class="cities-grid">
{chr(10).join([f'                <a href="/programist/ukraine/{slug}/" class="city-link">📍 Програміст {data["name"]}</a>' for slug, data in sorted(cities.items(), key=lambda x: x[1]["name"])])}
            </div>
        </div>
    </main>

    <footer>
        <div class="container">
            <div class="footer-container">
                <div class="footer-col"><h3>Послуги</h3><ul>
                    <li><a href="/rozrobka-saitiv/ukraine/">Розробка сайтів</a></li>
                    <li><a href="/internet-magazin/ukraine/">Інтернет-магазини</a></li>
                    <li><a href="/wordpress/ukraine/">WordPress</a></li>
                    <li><a href="/seo-optimizatsiya/ukraine/">SEO оптимізація</a></li>
                </ul></div>
                <div class="footer-col"><h3>Контакти</h3><ul>
                    <li>📞 <a href="tel:+380938800822">+38 (093) 88-00-822</a></li>
                    <li>📧 <a href="mailto:info@matviy.pp.ua">info@matviy.pp.ua</a></li>
                </ul></div>
            </div>
            <div class="copyright">© 2026 Програміст Роман Матвій. Всі права захищені.</div>
        </div>
    </footer>
    <script>
    const toggle = document.querySelector('.mobile-menu-toggle');
    const navList = document.querySelector('nav ul');
    if (toggle) {{ toggle.addEventListener('click', () => {{ toggle.classList.toggle('active'); navList.classList.toggle('active'); }}); }}
    
    // Lead Magnet Modal — open after delay
    setTimeout(() => {{
        const modal = document.getElementById('leadMagnetModal');
        if (modal && !localStorage.getItem('lm_closed')) {{
            modal.classList.add('show');
        }}
    }}, 15000);

    document.addEventListener('click', (e) => {{
        if (e.target.closest('.lm-close') || e.target.classList.contains('lm-modal')) {{
            const modal = document.getElementById('leadMagnetModal');
            if (modal) {{
                modal.classList.remove('show');
                localStorage.setItem('lm_closed', 'true');
            }}
        }}
    }});
    </script>
    
    <!-- Lead Magnet Modal -->
    <div id="leadMagnetModal" class="lm-modal">
        <div class="lm-modal-content">
            <button class="lm-close">&times;</button>
            <h3>🎁 Безкоштовний SEO-аудит</h3>
            <p>Дізнайтесь, чому ваш сайт втрачає клієнтів у Google. Залиште email та адресу сайту, і я надішлю вам детальний звіт.</p>
            <form class="lm-form" action="/contact.php" method="POST">
                <input type="hidden" name="source" value="SEO Audit Modal - Cities Index">
                <input type="hidden" name="message" class="hidden-message" value="">
                <input type="text" name="name" placeholder="Ваше ім'я" required>
                <input type="email" name="email" placeholder="Ваш Email" required>
                <input type="url" name="website" placeholder="Посилання на сайт (напр. https://...)" required>
                <button type="submit">Отримати аудит 🚀</button>
            </form>
            <div class="lm-success">Дякуємо! Ваша заявка прийнята. Я надішлю аудит найближчим часом.</div>
        </div>
    </div>
</body>
</html>'''


def main():
    # Створюємо /programist/ukraine/index.html
    index_dir = os.path.join(BASE_DIR, 'programist', 'ukraine')
    os.makedirs(index_dir, exist_ok=True)
    with open(os.path.join(index_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(generate_index_page())
    print(f"Created: programist/ukraine/index.html")

    # Створюємо сторінку для кожного міста
    count = 0
    for city_slug, city_data in cities.items():
        city_dir = os.path.join(BASE_DIR, 'programist', 'ukraine', city_slug)
        os.makedirs(city_dir, exist_ok=True)
        page = generate_page(city_slug, city_data)
        filepath = os.path.join(city_dir, 'index.html')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(page)
        count += 1
        print(f"Created: programist/ukraine/{city_slug}/index.html")

    print(f"\nGotovo! Zghenerovano {count} mist + 1 indeks-storinka")
    print(f"Papka: {os.path.join(BASE_DIR, 'programist')}")


if __name__ == '__main__':
    main()
