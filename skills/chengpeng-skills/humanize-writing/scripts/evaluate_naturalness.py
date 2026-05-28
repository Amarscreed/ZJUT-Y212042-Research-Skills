#!/usr/bin/env python3
"""
Evaluate writing naturalness of academic text.
Measures AI-ism density, readability, sentence variety, and passive voice.

Usage: python evaluate_naturalness.py <input.txt>
       python evaluate_naturalness.py <input.txt> --before <before.txt>
"""

import re
import sys
import argparse
import statistics as stats


# Patterns
HEDGE_WORDS = [
    "notably", "importantly", "interestingly", "remarkably",
    "significantly", "particularly", "noteworthy", "of note",
    "it is worth", "it should be noted", "it is important to",
    "it is interesting to", "we observe that", "as can be seen",
    "as shown in", "as illustrated by", "as demonstrated by",
]

EMPTY_TRANSITIONS = [
    "furthermore", "moreover", "in addition", "additionally",
    "nevertheless", "nonetheless", "however", "therefore",
    "thus", "hence", "consequently", "as a result",
]

FORMULAIC_OPENINGS = [
    "in recent years", "in the past decade", "recently",
    "with the rapid development", "with the advent",
    "there has been growing interest", "it is widely recognized",
]


def count_passive(text):
    """Count passive voice constructions."""
    # Patterns: "was/were/been/being + past participle"
    passive_pattern = r"\b(was|were|been|being|is|are|be|has been|have been|had been)\s+\w+ed\b"
    return len(re.findall(passive_pattern, text, re.IGNORECASE))


def avg_sentence_length(text):
    """Calculate average sentence length in words."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
    if not sentences:
        return 0, 0, 0
    lengths = [len(s.split()) for s in sentences]
    return stats.mean(lengths), stats.stdev(lengths) if len(lengths) > 1 else 0, len(sentences)


def count_hedges(text):
    """Count hedge word occurrences."""
    total = 0
    for w in HEDGE_WORDS:
        total += len(re.findall(r'\b' + re.escape(w) + r'\b', text, re.IGNORECASE))
    return total


def count_transitions(text):
    """Count empty transition words."""
    total = 0
    for w in EMPTY_TRANSITIONS:
        total += len(re.findall(r'\b' + re.escape(w) + r'\b', text, re.IGNORECASE))
    return total


def count_formulaic(text):
    """Count formulaic openings."""
    total = 0
    for p in FORMULAIC_OPENINGS:
        total += len(re.findall(re.escape(p), text, re.IGNORECASE))
    return total


def flesch_reading_ease(text):
    """Flesch Reading Ease score."""
    sentences = len(re.split(r'[.!?]+', text)) - 1
    words = len(re.findall(r'\b\w+\b', text))
    syllables = sum([_count_syllables(w) for w in re.findall(r'\b\w+\b', text)])
    if sentences == 0 or words == 0:
        return 0
    return 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)


def flesch_kincaid(text):
    """Flesch-Kincaid Grade Level."""
    sentences = max(len(re.split(r'[.!?]+', text)) - 1, 1)
    words = max(len(re.findall(r'\b\w+\b', text)), 1)
    syllables = sum([_count_syllables(w) for w in re.findall(r'\b\w+\b', text)])
    return 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59


def _count_syllables(word):
    """Simple syllable counter."""
    word = word.lower().strip(".,!?;:\"'-")
    if len(word) <= 3:
        return 1
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for ch in word:
        is_vowel = ch in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    if count == 0:
        count = 1
    return count


def evaluate(text, label="Current"):
    """Full evaluation report."""
    words = re.findall(r'\b\w+\b', text)
    word_count = len(words)
    
    avg_len, std_len, num_sents = avg_sentence_length(text)
    hedges = count_hedges(text)
    transitions = count_transitions(text)
    formulaic = count_formulaic(text)
    passive_count = count_passive(text)
    hedge_density = hedges / word_count * 100 if word_count > 0 else 0
    
    fre = flesch_reading_ease(text)
    fkg = flesch_kincaid(text)
    
    ai_ism_total = hedges + transitions + formulaic
    ai_ism_density = ai_ism_total / word_count * 100 if word_count > 0 else 0
    
    print(f"\n{'='*50}")
    print(f"Writing Quality Report: {label}")
    print(f"{'='*50}")
    print(f"Word count:            {word_count}")
    print(f"Sentences:             {num_sents}")
    print(f"Avg sentence length:   {avg_len:.1f} words (σ={std_len:.1f})")
    print(f"Flesch Reading Ease:   {fre:.1f}")
    print(f"Flesch-Kincaid Grade:  {fkg:.1f}")
    print(f"Passive count:         {passive_count} ({passive_count/max(num_sents,1)*100:.0f}% of sents)")
    print(f"")
    print(f"--- AI-ism Analysis ---")
    print(f"Hedge words:           {hedges} ({hedge_density:.1f}/100 words)")
    print(f"Empty transitions:     {transitions}")
    print(f"Formulaic openings:    {formulaic}")
    print(f"Total AI-isms:         {ai_ism_total} ({ai_ism_density:.1f}/100 words)")
    print(f"{'='*50}")
    
    return {
        "words": word_count,
        "sentences": num_sents,
        "avg_sent_len": avg_len,
        "std_sent_len": std_len,
        "fre": fre,
        "fkg": fkg,
        "passive": passive_count,
        "hedges": hedges,
        "transitions": transitions,
        "formulaic": formulaic,
        "ai_ism_density": ai_ism_density,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate writing naturalness")
    parser.add_argument("input", help="Input text file")
    parser.add_argument("--before", "-b", default="", help="Before-edits text file for comparison")
    args = parser.parse_args()
    
    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()
    
    result = evaluate(text, "After")
    
    if args.before:
        with open(args.before, "r", encoding="utf-8") as f:
            before_text = f.read()
        before_result = evaluate(before_text, "Before")
        
        print(f"\n{'='*50}")
        print(f"COMPARISON: Before → After")
        print(f"{'='*50}")
        print(f"AI-ism density:      {before_result['ai_ism_density']:.1f} → {result['ai_ism_density']:.1f} /100 words")
        print(f"Flesch Reading Ease: {before_result['fre']:.1f} → {result['fre']:.1f}")
        print(f"Avg sentence length: {before_result['avg_sent_len']:.1f} → {result['avg_sent_len']:.1f}")
        print(f"Word count:          {before_result['words']} → {result['words']}")
        print(f"{'='*50}")
