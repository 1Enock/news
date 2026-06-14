"""pythonAssessment.py

Utilities for simple text analysis on news articles.

Functions:
- count_word(text, word, case_sensitive=False)
- most_common_word(text)
- average_word_length(text)
- count_paragraphs(text)
- count_sentences(text)

Includes a minimal CLI to run against a text file.
"""
from collections import Counter
import re
import sys
from typing import List, Tuple


def tokenize_words(text: str) -> List[str]:
    # split on non-word characters, keep words with letters/numbers
    words = re.findall(r"\b[\w']+\b", text)
    return words


def count_word(text: str, word: str, case_sensitive: bool = False) -> int:
    if not case_sensitive:
        text = text.lower()
        word = word.lower()
    words = tokenize_words(text)
    return sum(1 for w in words if w == word)


# Backwards-compatible wrapper for assignment tests
def count_specific_word(text: str, word: str) -> int:
    """Count occurrences of `word` in `text` using loops and conditionals.

    This function matches the expected test name `count_specific_word`.
    """
    if text is None or word is None:
        return 0
    words = tokenize_words(text.lower())
    target = word.lower()
    count = 0
    i = 0
    while i < len(words):
        if words[i] == target:
            count += 1
        i += 1
    return count


def most_common_word(text: str) -> Tuple[str, int]:
    words = [w.lower() for w in tokenize_words(text)]
    if not words:
        return "", 0
    counter = Counter(words)
    word, count = counter.most_common(1)[0]
    return word, count


def identify_most_common_word(text: str) -> str:
    """Return the most common word in `text` (lowercased). Returns empty string on empty input.

    Implements counting using a `for` loop and selects the max with a conditional.
    """
    words = [w.lower() for w in tokenize_words(text)]
    if not words:
        return ""
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    max_word = ""
    max_count = 0
    for k, v in freq.items():
        if v > max_count:
            max_word = k
            max_count = v
    return max_word


def average_word_length(text: str) -> float:
    words = tokenize_words(text)
    if not words:
        return 0.0
    lengths = [len(w) for w in words]
    return sum(lengths) / len(lengths)


def calculate_average_word_length(text: str) -> float:
    """Calculate and return average word length using a for loop."""
    words = tokenize_words(text)
    if not words:
        return 0.0
    total = 0
    count = 0
    for w in words:
        total += len(w)
        count += 1
    return total / count


def count_paragraphs(text: str) -> int:
    # Count paragraphs by iterating lines and detecting non-blank blocks.
    if text is None:
        return 0
    lines = text.splitlines()
    paragraph_count = 0
    in_paragraph = False
    for line in lines:
        if line.strip():
            if not in_paragraph:
                paragraph_count += 1
                in_paragraph = True
        else:
            in_paragraph = False
    return paragraph_count


def count_sentences(text: str) -> int:
    # naive sentence splitter using punctuation
    # collapse ellipses and split at . ! ? followed by space or line end
    cleaned = re.sub(r"\.\.\.+", ".", text)
    sentences = re.split(r"(?<=[.!?])\s+", cleaned.strip())
    sentences = [s for s in sentences if s and re.search(r"[a-zA-Z0-9]", s)]
    return len(sentences)


def analyze(text: str, word: str = None) -> dict:
    result = {
        "most_common_word": most_common_word(text),
        "average_word_length": average_word_length(text),
        "paragraph_count": count_paragraphs(text),
        "sentence_count": count_sentences(text),
    }
    if word is not None:
        result["count_of_word"] = count_word(text, word)
    return result


def _read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _print_report(report: dict, word: str = None) -> None:
    mcw, mcw_count = report["most_common_word"]
    print(f"Most common word: {mcw!r} ({mcw_count} occurrences)")
    print(f"Average word length: {report['average_word_length']:.2f}")
    print(f"Paragraphs: {report['paragraph_count']}")
    print(f"Sentences: {report['sentence_count']}")
    if word is not None:
        print(f"Count of '{word}': {report.get('count_of_word', 0)}")


def main(argv: List[str]):
    if len(argv) < 2:
        print("Usage: python pythonAssessment.py <text-file> [word-to-count]")
        return 2
    path = argv[1]
    word = argv[2] if len(argv) >= 3 else None
    text = _read_file(path)
    report = analyze(text, word)
    _print_report(report, word)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
