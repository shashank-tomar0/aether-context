import re

with open('cloned_raw.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Make all asset URLs absolute to cofounder.co
text = text.replace('href="/_next/', 'href="https://cofounder.co/_next/')
text = text.replace('src="/_next/', 'src="https://cofounder.co/_next/')
text = text.replace('srcSet="/_next/', 'srcSet="https://cofounder.co/_next/')
text = text.replace('src="/logos/', 'src="https://cofounder.co/logos/')
text = text.replace('src="/hero/', 'src="https://cofounder.co/hero/')
text = text.replace('poster="/hero/', 'poster="https://cofounder.co/hero/')
text = text.replace('href="/favicon', 'href="https://cofounder.co/favicon')
text = text.replace('href="/apple-icon', 'href="https://cofounder.co/apple-icon')
text = text.replace('href="/icon.png', 'href="https://cofounder.co/icon.png')
text = text.replace('url(\\"/decor/', 'url(\\"https://cofounder.co/decor/')
text = text.replace('src=\\"/books-covers/', 'src=\\"https://cofounder.co/books-covers/')

# Transform Headlines and Copy to AETHER Context Layer (the winning product!)
text = text.replace(
    "Cofounder lets you run an entire company with AI",
    "AETHER gives your platform an autonomous cognitive context layer"
)

text = text.replace(
    "Start with an AI roadmap, then hand off engineering, sales, marketing, design, finance, and ops to agents.",
    "Continuously synthesize raw platform logs into living 4D profiles. Run existence checks, conversational synthesis, and graph matchmaking."
)

text = text.replace(
    "Run a company",
    "Launch Command Center"
)

text = text.replace(
    "Cofounder is an agent orchestration platform",
    "AETHER is a universal cognitive context layer"
)

text = text.replace(
    "designed to help you run an entire business",
    "built above your database to understand who your users actually are"
)

text = text.replace(
    "over 10,650 companies",
    "over 10,650 builders indexed"
)

text = text.replace(
    "are running on Cofounder",
    "are powered by AETHER Context Layer"
)

with open('backend/static/cloned_cofounder.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Transformed cloned cofounder page successfully! Size:", len(text))
