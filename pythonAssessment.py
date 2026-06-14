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


def most_common_word(text: str) -> Tuple[str, int]:
    words = [w.lower() for w in tokenize_words(text)]
    if not words:
        return "", 0
    counter = Counter(words)
    word, count = counter.most_common(1)[0]
    return word, count


def average_word_length(text: str) -> float:
    words = tokenize_words(text)
    if not words:
        return 0.0
    lengths = [len(w) for w in words]
    return sum(lengths) / len(lengths)


def count_paragraphs(text: str) -> int:
    # paragraphs separated by one or more blank lines
    parts = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    return len(parts)


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
