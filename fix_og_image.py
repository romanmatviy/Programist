import os

def fix_og_image():
    updated = 0
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                changed = False
                if 'content="/img/og-image.jpg"' in content:
                    content = content.replace('content="/img/og-image.jpg"', 'content="https://programist.matviy.pp.ua/img/og-image.jpg"')
                    changed = True
                if 'content="img/og-image.jpg"' in content:
                    content = content.replace('content="img/og-image.jpg"', 'content="https://programist.matviy.pp.ua/img/og-image.jpg"')
                    changed = True
                    
                if changed:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    updated += 1
    print(f"Fixed {updated} files.")

if __name__ == '__main__':
    fix_og_image()
