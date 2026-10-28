"""
Signal three (stretch): the phrase habit signal.

Counts two habits that differ between assistants and most people:

    stock phrases   "furthermore", "it is important to note", "delve" ... -
                    the connective tissue models reach for again and again
    contractions    "don't", "it's" ... - models writing formally avoid them,
                    people writing to people mostly don't

The score is 0–1, **higher = more likely AI**, same direction as the other two.

Blind spot: it is a word list. It cannot tell a model from a student who was
taught to write "furthermore", and it is defeated by deleting nine words. It is
also silent on short text, so it is weighted lowest of the three.
"""

import re

import stylometry

STOCK_PHRASES = [
    "furthermore", "moreover", "additionally", "in conclusion", "in summary",
    "it is important to note", "it is worth noting", "delve", "tapestry",
    "multifaceted", "crucial", "plays a vital role", "a wide range of",
    "in today's", "navigate", "landscape", "underscores", "leverage",
    "ensure that", "overall,", "comprehensive", "seamless", "foster",
    "key factors", "various factors", "a variety of", "it is essential",
]

CONTRACTION = re.compile(r"\b\w+['’](?:t|s|re|ve|ll|d|m)\b", re.IGNORECASE)


def phrase_signal(text: str) -> float:
    n_words = len(stylometry.words(text))
    if n_words < 15:
        return 0.5
    lowered = text.lower()
    stock_per_100 = 100 * sum(lowered.count(p) for p in STOCK_PHRASES) / n_words
    contractions_per_100 = 100 * len(CONTRACTION.findall(text)) / n_words

    stock_part = min(stock_per_100 / 3.0, 1.0)  # 3 per 100 words = maximum
    contraction_part = 1.0 - min(contractions_per_100 / 2.0, 1.0)  # 2 per 100 = fully human

    return round(0.6 * stock_part + 0.4 * contraction_part, 4)


if __name__ == "__main__":
    import sys

    t = " ".join(sys.argv[1:]) or (
        "Furthermore, it is important to note that the system is comprehensive "
        "and ensures that a wide range of users can navigate it with ease."
    )
    print(f"phrase_signal   {phrase_signal(t)}   (higher = more likely AI)")
