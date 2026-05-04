"""INVEST criteria scoring for user stories."""

from dataclasses import dataclass, field

WEASEL_WORDS = frozenset(
    {
        "appropriate",
        "adequate",
        "easy",
        "fast",
        "user-friendly",
        "seamless",
        "intuitive",
        "simple",
        "efficient",
        "effective",
        "robust",
        "flexible",
        "scalable",
        "modern",
    }
)

UNMEASURABLE_PHRASES = [
    "as needed",
    "when required",
    "in a timely manner",
    "on a regular basis",
    "as appropriate",
    "when necessary",
    "as soon as possible",
]


@dataclass
class InvestScore:
    independent: float = 0.0
    negotiable: float = 0.0
    valuable: float = 0.0
    estimable: float = 0.0
    small: float = 0.0
    testable: float = 0.0

    @property
    def average(self) -> float:
        scores = [
            self.independent,
            self.negotiable,
            self.valuable,
            self.estimable,
            self.small,
            self.testable,
        ]
        return sum(scores) / len(scores)

    @property
    def passes(self) -> bool:
        return self.average >= 0.75


@dataclass
class AmbiguityReport:
    weasel_words: list[str] = field(default_factory=list)
    unmeasurable_phrases: list[str] = field(default_factory=list)
    passive_voice_count: int = 0

    @property
    def flag_count(self) -> int:
        return len(self.weasel_words) + len(self.unmeasurable_phrases) + self.passive_voice_count


def detect_ambiguity(text: str) -> AmbiguityReport:
    """Scan story text for ambiguity flags."""
    lower = text.lower()
    report = AmbiguityReport()

    for word in WEASEL_WORDS:
        if word in lower:
            report.weasel_words.append(word)

    for phrase in UNMEASURABLE_PHRASES:
        if phrase in lower:
            report.unmeasurable_phrases.append(phrase)

    return report


def score_story(
    story_text: str,
    acceptance_criteria: list[str],
    has_dependency: bool = False,
    estimated_days: float | None = None,
) -> tuple[InvestScore, AmbiguityReport]:
    """Score a user story against INVEST criteria."""
    invest = InvestScore()
    ambiguity = detect_ambiguity(story_text + " ".join(acceptance_criteria))

    invest.independent = 0.5 if has_dependency else 1.0

    solution_words = ["using", "via", "through", "with the", "by implementing"]
    invest.negotiable = 0.5 if any(w in story_text.lower() for w in solution_words) else 1.0

    value_words = ["so that", "in order to", "because", "to enable"]
    invest.valuable = 1.0 if any(w in story_text.lower() for w in value_words) else 0.4

    invest.estimable = 0.4 if ambiguity.flag_count > 2 else 1.0 if len(story_text) > 50 else 0.7

    if estimated_days is not None:
        invest.small = 1.0 if estimated_days <= 10 else 0.5 if estimated_days <= 20 else 0.2
    else:
        invest.small = 0.7

    invest.testable = 1.0 if len(acceptance_criteria) >= 2 else 0.4

    return invest, ambiguity
