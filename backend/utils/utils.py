
def short_text(text, word_limit=15):
    words = text.split()
    shortened = " ".join(words[:word_limit])
    return shortened