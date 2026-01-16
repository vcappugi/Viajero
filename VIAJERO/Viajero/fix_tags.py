import os
import re

def fix_multiline_tags(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                with open(path, 'r') as f:
                    content = f.read()
                
                # Fix {{ ... }} tags
                # This regex looks for {{ followed by anything (including newlines) until it finds }}
                # We replace it by joining the lines and removing extra spaces
                def join_var_tag(match):
                    tag_content = match.group(1).replace('\n', ' ')
                    tag_content = re.sub(r'\s+', ' ', tag_content).strip()
                    return f'{{{{ {tag_content} }}}}'
                
                new_content = re.sub(r'\{\{(.*?)\}\}', join_var_tag, content, flags=re.DOTALL)
                
                # Fix {% ... %} tags
                def join_block_tag(match):
                    tag_content = match.group(1).replace('\n', ' ')
                    tag_content = re.sub(r'\s+', ' ', tag_content).strip()
                    return f'{{% {tag_content} %}}'
                
                new_content = re.sub(r'\{%(.*?)%\}', join_block_tag, new_content, flags=re.DOTALL)
                
                if new_content != content:
                    print(f"Fixed {path}")
                    with open(path, 'w') as f:
                        f.write(new_content)

if __name__ == "__main__":
    fix_multiline_tags('/Users/vcappugi/sources/proyectos Python/VIAJERO/VIAJERO/Viajero/templates/viaticos')
