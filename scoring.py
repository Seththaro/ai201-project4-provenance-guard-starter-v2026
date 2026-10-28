"""
Turning signals into one number, and one number into something a person can read.

`combine_signals` is where the false-positive decision actually gets made.
`score_to_label` is where the number becomes words a writer will read.

README pointer: the combining rule lives at `scoring.py::combine_signals`.
"""

import config


def combine_signals(
    model_score: float,
    style_score: float,
    phrase_score: float | None = None,
) -> float:
    """
    Combine the signals into one 0–1 score. Higher = more likely AI.

    The rule, written before the code:

      1. Weighted average. Weights are in config.py (model 0.45, style 0.35,
         phrase 0.20). If the phrase signal is absent the other two are
         renormalised, so the rule still works with two signals.
      2. Disagreement rule. If the highest and lowest signal are more than
         config.DISAGREE_GAP (0.35) apart, the average is pulled
         config.DISAGREE_SHRINK (50%) of the way back toward 0.5. Two methods
         that split are telling us we don't know, and "unsure" is the honest
         answer. It also stops one over-confident signal from accusing alone,
         which is the false-positive protection the whole project is about.
    """
    parts = [
        (config.WEIGHT_MODEL_SIGNAL, model_score),
        (config.WEIGHT_STYLE_SIGNAL, style_score),
    ]
    if phrase_score is not None:
        parts.append((config.WEIGHT_PHRASE_SIGNAL, phrase_score))

    total_weight = sum(w for w, _ in parts)
    average = sum(w * v for w, v in parts) / total_weight

    values = [v for _, v in parts]
    if max(values) - min(values) > config.DISAGREE_GAP:
        average = 0.5 + (average - 0.5) * (1 - config.DISAGREE_SHRINK)

    return round(min(max(average, 0.0), 1.0), 4)


def confidence_of(score: float) -> float:
    """How sure the system is of its leaning: 0.5 (coin flip) to 1.0 (certain)."""
    return round(max(score, 1 - score), 4)


LABELS = {
    "human": (
        "We think this was probably written by a person. Our checks found "
        "nothing that points to an AI tool."
    ),
    "unsure": (
        "We can't tell for certain whether this was written by a person or "
        "with an AI tool. Our automated checks aren't reliable enough to say, "
        "so no conclusion has been drawn about this piece. If you wrote it "
        "yourself, nothing is needed from you."
    ),
    "ai": (
        "Our checks suggest this may have been written with an AI tool. "
        "Automated checks can be wrong, especially for plain or "
        "second-language writing. If you wrote it yourself, you can appeal "
        "and a person will review it."
    ),
}


def score_to_label(score: float) -> tuple[str, str]:
    """
    Turn a score into a guess and the text a reader actually sees.

    Returns (guess, label_text). Every score in 0–1 maps to exactly one of the
    three: <= HUMAN_THRESHOLD human, >= AI_THRESHOLD ai, otherwise unsure.
    """
    if score >= config.AI_THRESHOLD:
        return "ai", LABELS["ai"]
    if score <= config.HUMAN_THRESHOLD:
        return "human", LABELS["human"]
    return "unsure", LABELS["unsure"]


def label_ranges() -> list[tuple[str, str]]:
    """The score range each label covers, straight from config.py."""
    return [
        ("high-confidence human", f"0.00 – {config.HUMAN_THRESHOLD:.2f}"),
        ("unsure", f"{config.HUMAN_THRESHOLD:.2f} – {config.AI_THRESHOLD:.2f}"),
        ("high-confidence AI", f"{config.AI_THRESHOLD:.2f} – 1.00"),
    ]


if __name__ == "__main__":
    for name, rng in label_ranges():
        print(f"{name:24} {rng}")
