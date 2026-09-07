from . import common
from . import pdf
from . import docx
from . import audio
from . import image

def clean_text(text,file_type):

    text = common.control_char(text)
    text = common.unicode_normalize(text)
    text = common.extra_space(text)
    text = common.extra_newline(text)
    text = common.trim_whitespace(text)

    if file_type == "pdf":
        text = pdf.page_num(text)
        text = pdf.header(text)
        text = pdf.footer(text)
        text = pdf.broke_line_wrapping(text)
        text = pdf.preserve_paragraphs(text)

    elif file_type == "docx":
        text = docx.broke_line_wrapping(text)
        text = docx.preserve_paragraphs(text)

    elif file_type == "image":
        text = image.OCR_garbage(text)
        text = image.OCR_mistakes(text)
        text = image.preserve_paragraphs(text)

    elif file_type == "audio":
        text = audio.timestamps(text)
        text = audio.preserve_paragraphs(text)
    
    return text


