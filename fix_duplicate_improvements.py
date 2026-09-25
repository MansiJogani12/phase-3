import codecs

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'r', 'utf-8') as f:
    lines = f.readlines()

# Look for the line starting with '%</p>' or orphan static improvements block around line 930
new_lines = []
skip = False
for l in lines:
    if '%</p>' in l:
        skip = True
    if skip and '</div>\n' in l and '}\n' in lines[lines.index(l)+1] if lines.index(l)+1 < len(lines) else False:
        # Check if we reached the end of duplicate improvements block
        pass
    
    # Simple strategy: find exact line indices
    new_lines.append(l)

# Let's cleanly strip from line '%</p>' to the second ')}' before line '/* Right Side Column'
content = "".join(lines)

# Remove the leftover snippet between })()} and {/* Right Side Column */}
import re

# Match from '%</p>' up to ')}' right before '</div>'
content = re.sub(
    r'%</p>[\s\S]*?\}\)\}\s*(?=\s*</div>\s*</div>\s*</div>\s*\{/\* Right Side Column)',
    '',
    content
)

with codecs.open(r'd:\GITHUB\gitforme\gitforme\src\components\RepoDetailView.jsx', 'w', 'utf-8') as f:
    f.write(content)

print('Cleaned up orphan static improvements block!')
