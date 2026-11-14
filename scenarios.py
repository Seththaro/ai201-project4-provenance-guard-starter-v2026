"""
What my test runs. <- UNIT 8, MILESTONE 3

Each of my five criteria (criteria_unit7.md) needs something run against it.
`run_eval.py` runs every scenario here three times and saves the raw output to
results/. `check_criteria.py` reads the same lists and turns them into the pass /
fail numbers for the run log, and it also does the two things run_eval.py cannot:
criterion 4 (an appeal needs a content_id from an earlier submission) and the
label sweep half of criterion 3.

Where the texts come from, stated plainly:

  - HUMAN_CLASSIC: five well-known public-domain passages. A person wrote them,
    but they are formal, literary prose, which is easy for a detector to call
    human and is NOT the hard case.
  - HUMAN_PLAIN: five short paragraphs in the plain voice of a younger or
    second-language writer. Criterion 1 asks for these, because plain writing is
    where signal one is most likely to accuse the wrong person. I wrote these
    five as stand-ins in that style; they are not samples from a real student.
    Swapping in real plain writing is the single change that would make
    criterion 1 a stronger test.
  - AI_TEXTS: five paragraphs in the usual assistant register, written for this
    test.
  - BORDERLINE: five pieces I would not call either way (an email, a news
    paragraph, two lightly edited AI-style paragraphs, a casual review).
"""

HUMAN_CLASSIC = [
    "Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal. Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived and so dedicated, can long endure. We are met on a great battle-field of that war. We have come to dedicate a portion of that field, as a final resting place for those who here gave their lives that that nation might live.",
    "I went to the woods because I wished to live deliberately, to front only the essential facts of life, and see if I could not learn what it had to teach, and not, when I came to die, discover that I had not lived. I did not wish to live what was not life, living is so dear; nor did I wish to practise resignation, unless it was quite necessary.",
    "Call me Ishmael. Some years ago, never mind how long precisely, having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world. It is a way I have of driving off the spleen and regulating the circulation.",
    "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife. However little known the feelings or views of such a man may be on his first entering a neighbourhood, this truth is so well fixed in the minds of the surrounding families, that he is considered the rightful property of some one or other of their daughters.",
    "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair, we had everything before us, we had nothing before us.",
]

HUMAN_PLAIN = [
    "My name is Sam and I am eleven. I have a dog named Max. Max is brown and he likes to run. Every day after school I take him to the park. We play with a ball. He always brings it back. I like my dog a lot and he is my best friend.",
    "In my country we eat rice every day. My mother cooks it with vegetables and sometimes with fish. When I came here I missed this food very much. Now I cook it by myself on Sunday. I invite my friends and they like it. It makes me feel like I am home.",
    "Last summer I went to my uncle's farm. We woke up early and fed the cows. Then we ate eggs for breakfast. The work was hard but I was happy. My uncle said I am a good helper. I want to go back next year.",
    "The best day of my year was my birthday. My mom made a big chocolate cake. Six friends came to my house. We played games in the yard and ate pizza. I got a new bike from my dad. I rode it until it got dark.",
    "I think school should start later in the morning. Many students are tired when they get to class. Tired students can not learn well. If school started at nine we could sleep more. Then we would pay attention better. I hope the school will think about this.",
]

AI_TEXTS = [
    "In today's rapidly evolving digital landscape, it is important to note that effective communication plays a crucial role in the success of any organization. Furthermore, leveraging the right tools can significantly enhance collaboration and productivity. By fostering a culture of transparency and continuous improvement, teams can navigate challenges more effectively. In conclusion, prioritizing clear communication is essential for achieving long-term growth and sustainable success.",
    "Renewable energy has emerged as a pivotal solution to the growing challenges of climate change. Moreover, advancements in solar and wind technology have made clean power more accessible and affordable than ever before. It is worth noting that transitioning to sustainable energy sources not only reduces carbon emissions but also creates new economic opportunities. Ultimately, a collaborative approach among governments, businesses, and communities is essential to ensure a greener future.",
    "Time management is a fundamental skill that can greatly improve both personal and professional life. First, it is essential to prioritize tasks based on their importance and urgency. Additionally, setting clear goals helps individuals stay focused and motivated. Furthermore, taking regular breaks can enhance overall productivity and well-being. By implementing these strategies consistently, anyone can achieve a healthier work-life balance and reach their full potential.",
    "Artificial intelligence is transforming the landscape of modern education in numerous ways. For instance, personalized learning platforms can adapt to the unique needs of each student, delivering tailored content at an optimal pace. Moreover, intelligent tutoring systems provide instant feedback, fostering deeper understanding. However, it is crucial to address concerns surrounding data privacy and equitable access. Overall, thoughtfully integrating AI can empower both educators and learners.",
    "Exploring a new city offers a unique opportunity to immerse oneself in diverse cultures and experiences. To begin with, visiting local landmarks provides valuable insight into the history and heritage of the region. Additionally, sampling traditional cuisine allows travelers to connect with the community on a deeper level. It is important to plan ahead while remaining flexible, as unexpected discoveries often become the most memorable moments of any journey.",
]

BORDERLINE = [
    "Thanks for sending over the draft. I read through it twice and left comments in the margins, mostly small things. The introduction takes too long to get to the point, and the third section repeats what we already said earlier. If you can tighten those two parts we should be ready to send it to the committee by Friday.",
    "Honestly, remote work has changed how I think about my day. It gives people flexibility, sure, but it also blurs the line between home and office. I have learned that setting a firm schedule matters more than any app. Some days it works great and other days I am still answering email at ten at night, which defeats the whole point.",
    "Social media has changed the way we comunicate in many ways. It lets us stay in touch with freinds far away and share moments instantly. At the same time, it can make people feel anxious or left out. Learning to use it in moderation, and to take breaks when needed, is probably the healthiest approach for most people.",
    "The city council voted on Tuesday to approve a new bike lane along Main Street, ending months of debate between local business owners and cycling advocates. The project will remove about forty parking spaces and is expected to cost two million dollars. Construction is scheduled to begin in the spring, pending a final review of the traffic study.",
    "So we finally tried that new ramen place downtown last night. The broth was great, really rich, but the wait was almost an hour and my feet were killing me by the end. I would go back, just not on a weekend. My brother ordered the spicy one and could not stop sweating, which was honestly the best part of the evening.",
]

# Criterion 1: 10 human pieces, 5 of them plain. (criteria_unit7.md asks for at least 4.)
CRITERION_1_TEXTS = HUMAN_PLAIN + HUMAN_CLASSIC

# Criterion 3(b): 20 real submissions across the range.
CRITERION_3_TEXTS = HUMAN_PLAIN + HUMAN_CLASSIC + AI_TEXTS + BORDERLINE

# Criterion 5: the malformed bodies, sent exactly as written. The eighth (a JSON
# list body) cannot be a dict, so check_criteria.py sends it separately.
BAD_BODIES = [
    {"creator_id": "eval_bad_notext"},                                   # no text field
    {"text": "", "creator_id": "eval_bad_empty"},                        # empty text
    {"text": "   \n\t  ", "creator_id": "eval_bad_blank"},               # whitespace only
    {"text": 42, "creator_id": "eval_bad_number"},                       # text is a number
    {"text": "one two three four five six seven eight nine ten eleven twelve thirteen fourteen",
     "creator_id": "eval_bad_14words"},                                  # 14 words
    {"text": "a" * 25000, "creator_id": "eval_bad_25000chars"},          # 25,000 characters
    {"text": "This text is long enough to pass the minimum word check easily because it keeps going for a while.",
     },                                                                  # no creator_id
]

SCENARIOS = [
    {"name": "false positives", "criterion": 1, "texts": CRITERION_1_TEXTS},
    {"name": "score spread", "criterion": 2, "texts": AI_TEXTS + HUMAN_CLASSIC},
    {"name": "label coverage", "criterion": 3, "texts": CRITERION_3_TEXTS},
    # Criterion 4 (appeals) needs a content_id from an earlier submission, so
    # run_eval.py cannot do it. check_criteria.py does it, and says so.
    {"name": "bad input", "criterion": 5, "bodies": BAD_BODIES},
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check - an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies - pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict - bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty - if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
