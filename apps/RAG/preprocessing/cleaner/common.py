import re
import unicodedata

def control_char(text):
    return "".join(
        ch for ch in text
        if ch == "\n" or ch == "\t" or unicodedata.category(ch)[0] != "C"
    )


def unicode_normalize(text):
    return unicodedata.normalize("NFKC", text)


def extra_space(text):
    text = re.sub(r"[ \t]+", " ", text)
    return text


def extra_newline(text):
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def trim_whitespace(text):
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(lines).strip()