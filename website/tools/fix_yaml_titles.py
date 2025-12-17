import os
import re

target_dir = r"c:\Users\aakan\Documents\Git\writeups\website\writeups\FinalTrace_2025"

def check_titles():
    files = [f for f in os.listdir(target_dir) if f.endswith('.md') and f != 'index.md']
    
    print(f"Checking {len(files)} markdown files.")

    for filename in files:
        filepath = os.path.join(target_dir, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract title line
        match = re.search(r'^title:\s*(.*)$', content, re.MULTILINE)
        if match:
            title_value = match.group(1).strip()
            
            # Check if title starts with - or contains : without quotes
            if title_value.startswith('-') or (':' in title_value and not (title_value.startswith('"') or title_value.startswith("'"))):
                print(f"Potential issue in {filename}: title: {title_value}")
                
                # Fix it by quoting
                # Also if it starts with - **Category**, maybe we can find a better title?
                # For now, let's just quote it to fix the build error.
                # But for 28--category-forensics.md, the title is garbage.
                
                if filename == '28--category-forensics.md':
                     new_title = '"Phantom User Forensics"'
                else:
                     # Escape quotes if needed
                     safe_title = title_value.replace('"', '\\"')
                     new_title = f'"{safe_title}"'
                
                new_content = content.replace(f'title: {title_value}', f'title: {new_title}')
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Fixed {filename} -> title: {new_title}")

if __name__ == "__main__":
    check_titles()
