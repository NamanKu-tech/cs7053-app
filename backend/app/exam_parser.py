"""
Parse exam and solution txt files into structured question dicts.

Returns list of:
  {year, exam_slot (e.g. "Q1a"), marks, question_text, sample_answer}
"""

import os
import re

DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "exams")

YEARS = [2015, 2016, 2017, 2018, 2019, 2020, 2022, 2023, 2024, 2025]

# Map Q number -> path slug
Q_TO_SLUG = {
    1: "q1-risk-analysis",
    2: "q2-tls-protocols",
    3: "q3-system-design",
    4: "q4-dns-dnssec",
}


def _read(year: int, kind: str) -> str:
    path = os.path.join(DATA_DIR, f"exam_{year}_{kind}.txt")
    if not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def _split_questions(text: str) -> dict[int, str]:
    """Split full exam text into {question_number: text_block}."""
    # Match "Question N" or "Question N." at start of line (case-insensitive)
    pattern = re.compile(r"^\s*Question\s+(\d+)[\.\s]", re.MULTILINE | re.IGNORECASE)
    parts = {}
    matches = list(pattern.finditer(text))
    for i, m in enumerate(matches):
        qnum = int(m.group(1))
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        parts[qnum] = text[start:end].strip()
    return parts


def _clean(text: str) -> str:
    """Strip page footers, total-marks headers, and excessive whitespace."""
    text = re.sub(r"Page \d+ of \d+\s*\n?", "", text)
    text = re.sub(r"© Trinity College Dublin.*?(\n|$)", "", text)
    text = re.sub(r"Paper Code\s*", "", text)
    # Strip total question marks like "(33 marks)" or "(40 marks)" at start of block
    text = re.sub(r"^\s*\(\d{2,3}\s+marks?\)\s*\n", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{3,}", " ", text)
    return text.strip()


def _split_subparts(qtext: str) -> dict[str, tuple[str, int]]:
    """
    Split a question block into sub-parts.
    Returns {letter: (text, marks)}.
    Sub-parts must start at beginning of line (with optional whitespace).
    """
    # Match (a)/(b)/(c) OR a)/b)/c) at the START of a line only
    pattern = re.compile(r"^[ \t]*\(?([a-e])\)[ \t]+", re.MULTILINE)
    # [15 marks] format
    marks_pat_bracket = re.compile(r"\[(\d+)\s+marks?\]", re.IGNORECASE)
    # (15 marks) format — 2015 round-bracket style
    marks_pat_paren_word = re.compile(r"\((\d+)\s+marks?\)", re.IGNORECASE)
    # Inline bare (10) at end of line — 2015 style
    marks_pat_inline = re.compile(r"\((\d{1,2})\)\s*$", re.MULTILINE)

    parts = {}
    matches = list(pattern.finditer(qtext))

    for i, m in enumerate(matches):
        letter = m.group(1)
        # First occurrence wins — skip duplicate letters (e.g. "from part (a)" mid-text)
        if letter in parts:
            continue
        start = m.start()
        # Find end: next match that hasn't been seen as a first occurrence yet
        end = len(qtext)
        for j in range(i + 1, len(matches)):
            if matches[j].group(1) not in parts and matches[j].group(1) != letter:
                end = matches[j].start()
                break
        chunk = qtext[start:end].strip()
        chunk = _clean(chunk)

        # Extract mark allocation — try each format in order
        marks = 0
        mark_match = marks_pat_bracket.search(chunk)
        if mark_match:
            marks = int(mark_match.group(1))
            chunk = marks_pat_bracket.sub("", chunk).strip()
        else:
            mark_match = marks_pat_paren_word.search(chunk)
            if mark_match:
                marks = int(mark_match.group(1))
                chunk = marks_pat_paren_word.sub("", chunk, count=1).strip()
            else:
                mark_match = marks_pat_inline.search(chunk)
                if mark_match:
                    marks = int(mark_match.group(1))
                    chunk = marks_pat_inline.sub("", chunk, count=1).strip()

        # Remove leading "(x)" from chunk
        chunk = re.sub(r"^[ \t]*\([a-e]\)[ \t]*", "", chunk).strip()

        parts[letter] = (chunk, marks)

    return parts


def _extract_scenario(qtext: str) -> str:
    """Extract the scenario/preamble before the first (a) sub-part."""
    pattern = re.compile(r"^[ \t]*\(?([a-e])\)[ \t]+", re.MULTILINE)
    m = pattern.search(qtext)
    if m:
        scenario = qtext[: m.start()].strip()
        scenario = _clean(scenario)
        # Remove "Question N" header line and total-marks indicators
        scenario = re.sub(r"^Question\s+\d+\.?\s*", "", scenario, flags=re.IGNORECASE)
        scenario = re.sub(r"\(\d{2,3}\s+marks?\)\s*", "", scenario, flags=re.IGNORECASE)
        return scenario.strip()
    return ""


def _split_solution_parts(sol_qtext: str) -> dict[str, str]:
    """
    From a solution question block, extract solution text per sub-part.
    Solution files interleave question text with solution notes.
    We grab text between sub-part markers.
    """
    pattern = re.compile(r"^[ \t]*\(([a-e])\)[ \t]+", re.MULTILINE)
    parts = {}
    matches = list(pattern.finditer(sol_qtext))

    for i, m in enumerate(matches):
        letter = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(sol_qtext)
        chunk = sol_qtext[start:end].strip()

        # Heuristic: solution notes tend to come after the mark allocation line
        # Try to strip the question text and keep solution notes
        marks_pat = re.compile(r"\[(\d+)\s+marks?\]", re.IGNORECASE)
        mark_match = marks_pat.search(chunk)
        if mark_match:
            # Take everything after the marks indicator as solution text
            sol_text = chunk[mark_match.end():].strip()
        else:
            sol_text = chunk

        # Clean up
        sol_text = _clean(sol_text)
        sol_text = sol_text[:2000]  # cap length

        parts[letter] = sol_text

    return parts


def parse_year(year: int) -> list[dict]:
    """Return all exam questions for a given year as structured dicts."""
    exam_text = _read(year, "exam")
    sol_text = _read(year, "solutions")

    if not exam_text:
        return []

    exam_questions = _split_questions(exam_text)
    sol_questions = _split_questions(sol_text) if sol_text else {}

    results = []
    for qnum in sorted(exam_questions.keys()):
        if qnum not in (1, 2, 3, 4):
            continue

        qtext = exam_questions[qnum]
        scenario = _extract_scenario(qtext)
        subparts = _split_subparts(qtext)

        sol_subparts = {}
        if qnum in sol_questions:
            sol_subparts = _split_solution_parts(sol_questions[qnum])

        for letter, (question_text, marks) in subparts.items():
            full_question = (
                f"{scenario}\n\n({letter}) {question_text}".strip()
                if scenario
                else question_text
            )
            sample_answer = sol_subparts.get(letter, "")

            results.append(
                {
                    "year": year,
                    "exam_slot": f"Q{qnum}{letter}",
                    "marks": marks,
                    "question_text": full_question.strip(),
                    "sample_answer": sample_answer.strip(),
                    "path_slug": Q_TO_SLUG[qnum],
                }
            )

    return results


def parse_all() -> list[dict]:
    """Return all exam questions across all years."""
    all_questions = []
    for year in YEARS:
        all_questions.extend(parse_year(year))
    return all_questions


if __name__ == "__main__":
    qs = parse_all()
    print(f"Total questions parsed: {len(qs)}")
    for q in qs[:5]:
        print(f"\n--- {q['year']} {q['exam_slot']} ({q['marks']}m) ---")
        print(q["question_text"][:200])
        print("ANSWER:", q["sample_answer"][:150])
