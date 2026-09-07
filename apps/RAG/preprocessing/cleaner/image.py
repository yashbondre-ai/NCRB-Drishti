import re


def preserve_paragraphs(text):
    """
    Preserve paragraph breaks while removing unnecessary spaces.
    """

    paragraphs = []

    for paragraph in text.split("\n\n"):
        paragraph = paragraph.strip()

        if paragraph:
            paragraphs.append(paragraph)

    return "\n\n".join(paragraphs)


def OCR_garbage(text):
    """
    Remove obvious OCR garbage such as lines containing
    only symbols or repeated random characters.
    """

    cleaned = []

    for line in text.splitlines():

        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Remove lines made only of symbols
        if re.fullmatch(r"[\W_]+", line):
            continue

        # Remove repeated single-character garbage
        if re.fullmatch(r"(.)\1{5,}", line):
            continue

        cleaned.append(line)

    return "\n".join(cleaned)


def OCR_mistakes(text):
    """
    Fix some common OCR mistakes.
    """

    replacements = {
        "ﬁ": "fi",
        "ﬂ": "fl",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "–": "-",
        "—": "-",
    }

    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)

    return text