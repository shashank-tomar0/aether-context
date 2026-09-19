with open('backend/static/cloned_cofounder.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Route Run a company / Launch Command Center buttons to /app
html = html.replace('href="https://app.cofounder.co"', 'href="/app"')
html = html.replace('href="/resources/introducing-cofounder-2"', 'href="/app"')
html = html.replace('Check out the launch', 'Explore Context Layer')

with open('backend/static/cloned_cofounder.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Updated CTA links to point to /app successfully!')
