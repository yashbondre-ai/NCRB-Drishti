import re


def preserve_paragraphs(text):
    """
    Normalize paragraph spacing while preserving paragraphs.
    """

    paragraphs = []

    for paragraph in text.split("\n\n"):
        paragraph = paragraph.strip()

        if paragraph:
            paragraphs.append(paragraph)

    return "\n\n".join(paragraphs)


def timestamps(text):
    """
    Remove common timestamp formats.

    Examples:
    [00:01]
    00:01
    00:01:25
    01:02:03
    [01:02:03]
    """

    pattern = (
        r"\[?\d{1,2}:\d{2}(?::\d{2})?\]?"
    )

    return re.sub(pattern, "", text)

