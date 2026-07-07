from pathlib import Path
import re

source = Path(".")

for md in source.glob("*.md"):
    text = md.read_text(encoding="utf-8", errors="ignore")

    # Remove horizontal rules
    text = re.sub(r'^\s*---+\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\*\*\*+\s*$', '', text, flags=re.MULTILINE)

    # Remove broken media image links
    text = re.sub(r'!\[.*?\]\(.*?media.*?\)', '', text)

    # Remove numbered headings like:
    # 12. # Heading
    text = re.sub(r'^\d+\.\s*#\s*', '# ', text, flags=re.MULTILINE)

    # Convert:
    # 12. **Heading**
    # into
    # # Heading
    text = re.sub(
        r'^\d+\.\s*\*\*(.*?)\*\*',
        lambda m: '# ' + m.group(1),
        text,
        flags=re.MULTILINE
    )

    # If first heading is ##, change only the first one to #
    text = re.sub(r'^##\s+', '# ', text, count=1, flags=re.MULTILINE)

    # Fix heading jumps
    text = re.sub(r'^#### ', '### ', text, flags=re.MULTILINE)
    text = re.sub(r'^##### ', '#### ', text, flags=re.MULTILINE)

    # Remove multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)

    md.write_text(text, encoding="utf-8")

print("Done! All Markdown files fixed.")