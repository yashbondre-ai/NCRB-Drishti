import re

def broke_line_wrapping(text):
    lines = text.split("\n")
    result = []

    for line in lines:
        line = line.strip()

        if not line:
            result.append("")
        else:
            result.append(line)

    text = "\n".join(result)

    # Merge only single newlines
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)

    return text

def preserve_paragraphs(text):
    paragraphs = []

    for paragraph in text.split("\n\n"):

        paragraph = paragraph.strip()

        if paragraph:
            paragraphs.append(paragraph)

    return "\n\n".join(paragraphs)