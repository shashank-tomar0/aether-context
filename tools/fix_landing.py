import re

with open('backend/static/cloned_cofounder.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. CSS Injection at top of <style>
css_fix = """
html, body {
  overflow-x: hidden !important;
  max-width: 100vw !important;
  margin: 0 !important;
  padding: 0 !important;
  position: relative !important;
}
#site-hero {
  max-width: 100vw !important;
  overflow: hidden !important;
  position: relative !important;
}
#site-hero video {
  width: 100% !important;
  max-width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
  transform: none !important;
  left: 0 !important;
  right: 0 !important;
}
.orch-frame {
  max-width: 100% !important;
  width: 100% !important;
}
.hero-stagger h1 {
  word-wrap: break-word !important;
  overflow-wrap: break-word !important;
  max-width: 100% !important;
}
"""

content = content.replace('<style>', '<style>' + css_fix, 1)

# 2. Text Replacements for all Cofounder instances
replacements = [
    ('Keep building the product.Put Cofounder to work on the company.', 'Stop guessing builder capabilities. Put AETHER to work on your context layer.'),
    ('Keep building the product. Put Cofounder to work on the company.', 'Stop guessing builder capabilities. Put AETHER to work on your context layer.'),
    ('Cofounder launches a companywith you', 'AETHER synthesizes 4D cognitive profiles continuously'),
    ('Cofounder launches a company with you', 'AETHER synthesizes 4D cognitive profiles continuously'),
    ('Cofounder finds the right customersand gives them a reason to care', 'AETHER computes orthogonal complementary squads with mathematical synergy'),
    ('Cofounder finds the right customers and gives them a reason to care', 'AETHER computes orthogonal complementary squads with mathematical synergy'),
    ('Cofounder keeps the business movingafter launch', 'AETHER auto-allocates downstream grants and bounties to verified builders'),
    ('Cofounder keeps the business moving after launch', 'AETHER auto-allocates downstream grants and bounties to verified builders'),
    ('All the tools and systemsyour company needs', 'All the context pipelines your developer ecosystem needs'),
    ('All the tools and systems your company needs', 'All the context pipelines your developer ecosystem needs'),
    ('Run an entire companywith AI agents', 'Power your entire developer platform with cognitive context intelligence'),
    ('Run an entire company with AI agents', 'Power your entire developer platform with cognitive context intelligence'),
    ('View Cofounder case studies', 'View AETHER Platform Architecture'),
    ('name="application-name" content="Cofounder"', 'name="application-name" content="AETHER Context Layer"'),
    ('property="og:site_name" content="Cofounder"', 'property="og:site_name" content="AETHER Context Layer"'),
    ('"name":"Cofounder"', '"name":"AETHER Context Layer"'),
    ('Cofounder is an agent-native company operating system', 'AETHER is a universal cognitive context layer and autonomous graph matchmaker'),
    ('Cofounder', 'AETHER'),
    ('cofounder.co', 'aether-context.dev'),
    ('cofounder', 'aether')
]

for old, new in replacements:
    content = content.replace(old, new)

with open('backend/static/cloned_cofounder.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated cloned_cofounder.html successfully')
