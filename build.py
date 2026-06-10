import re
import os

def minify_css(css_content):
    # Remove comments
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    # Remove newlines and extra spaces
    css_content = re.sub(r'\s+', ' ', css_content)
    # Remove spaces around specific characters
    css_content = re.sub(r'\s*([\{\}\:\;\,\>])\s*', r'\1', css_content)
    return css_content.strip()

def build():
    css_path = 'css/style.css'
    index_path = 'index.html'
    
    if not os.path.exists(css_path):
        print(f"Error: {css_path} not found.")
        return
        
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()
    
    minified_css = minify_css(css)
    
    if not os.path.exists(index_path):
        print(f"Error: {index_path} not found.")
        return
        
    with open(index_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Replace the styles block
    pattern = r'<!-- CSS INJECT START -->.*?<!-- CSS INJECT END -->'
    replacement = f'<!-- CSS INJECT START -->\n    <style>{minified_css}</style>\n    <!-- CSS INJECT END -->'
    
    if '<!-- CSS INJECT START -->' not in html:
        print("Error: Please add <!-- CSS INJECT START --> and <!-- CSS INJECT END --> markers to index.html.")
        return
        
    new_html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
        
    print(f"Success! CSS minified ({len(css)} bytes -> {len(minified_css)} bytes) and injected into index.html!")

if __name__ == '__main__':
    build()
