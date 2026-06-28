from services.file_processors.text_cleaner import TextCleaner


def test_clean_multiple_spaces():
    text = "Hello     World"

    cleaned = TextCleaner.clean(text)

    assert cleaned == "Hello World"


def test_clean_multiple_newlines():
    text = "Hello\n\n\nWorld"

    cleaned = TextCleaner.clean(text)

    assert cleaned == "Hello World"


def test_clean_tabs():
    text = "Hello\t\tWorld"

    cleaned = TextCleaner.clean(text)

    assert cleaned == "Hello World"


def test_clean_mixed_whitespace():
    text = "Hello \n\t  World"

    cleaned = TextCleaner.clean(text)

    assert cleaned == "Hello World"


def test_clean_empty_text():
    assert TextCleaner.clean("") == ""