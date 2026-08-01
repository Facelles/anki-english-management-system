"""
generate_handwriting_pdf.py — printable handwriting-practice PDF from today's due cards.

Queries AnkiConnect for the cards a deck's reviewer would show today (`is:due`),
takes the English `Back` field, and renders it repeated a few times per card in a
dotted tracing font (kg_primary_dots/) so it can be printed and traced by hand.
Read-only: never writes anything back to Anki or to cards.yaml.

Usage:
  python scripts/generate_handwriting_pdf.py --deck interview
  python scripts/generate_handwriting_pdf.py --deck l2-vocab --repeat 3 --font lined-alt
  python scripts/generate_handwriting_pdf.py --deck interview --limit 5

Exit codes:
  0 — ok (including "no due cards")
  1 — bad args, Anki not running, or deck not found
"""

import argparse
import sys
from datetime import date
from pathlib import Path

import requests
import yaml
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ANKI_URL = "http://localhost:8765"
DECKS_DIR = Path("decks")
FONTS_DIR = Path("kg_primary_dots")
OUTPUT_DIR = Path("handwriting_practice")

FONT_NAME = "Handwriting"
FONT_FILES = {
    "dotted": "KGPrimaryDots.ttf",
    "lined": "KGPrimaryDotsLined.ttf",
    "lined-alt": "KGPrimaryDotsLinedAlt.ttf",
    "lined-nospace": "KGPrimaryDotsLinedNOSPACE.ttf",
}

MARGIN_X = 40
MARGIN_TOP = 50
MARGIN_BOTTOM = 40
CARD_GAP = 1  # extra space between cards, on top of line_height


def anki(action, **params):
    """Single AnkiConnect call. Raises on error."""
    response = requests.post(
        ANKI_URL,
        json={"action": action, "version": 6, "params": params},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    if data.get("error"):
        raise RuntimeError(f"AnkiConnect error on {action}: {data['error']}")
    return data["result"]


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def clean_text(html_text):
    """Strip HTML/hint markup, collapse whitespace, return plain text."""
    text = BeautifulSoup(html_text or "", "html.parser").get_text()
    return " ".join(text.split())


def fetch_due_sentences(deck_name):
    card_ids = anki("findCards", query=f'deck:"{deck_name}" is:due')
    if not card_ids:
        return []
    cards_info = anki("cardsInfo", cards=card_ids)
    sentences = []
    for card in cards_info:
        back = card.get("fields", {}).get("Back", {}).get("value", "")
        text = clean_text(back)
        if text:
            sentences.append(text)
    return sentences


def wrap_text(text, font_name, font_size, max_width):
    """Greedy word-wrap so lines fit within max_width at the given font/size."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if pdfmetrics.stringWidth(candidate, font_name, font_size) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def build_pdf(sentences, output_path, font_path, font_size, repeat, intensity=1.0):
    """intensity: 0.0 (white, invisible) .. 1.0 (full black). Lower values print
    a fainter guide that's easier to trace over without the pen just following ink."""
    pdfmetrics.registerFont(TTFont(FONT_NAME, str(font_path)))

    width, height = A4
    line_height = font_size * .90
    max_width = width - 2 * MARGIN_X
    x = MARGIN_X
    gray = 1.0 - intensity

    c = canvas.Canvas(str(output_path), pagesize=A4)
    c.setFont(FONT_NAME, font_size)
    c.setFillGray(gray)
    y = height - MARGIN_TOP

    pages = 1
    for sentence in sentences:
        wrapped_lines = wrap_text(sentence, FONT_NAME, font_size, max_width)
        block_height = line_height * len(wrapped_lines) * repeat
        if y - block_height < MARGIN_BOTTOM:
            c.showPage()
            c.setFont(FONT_NAME, font_size)
            c.setFillGray(gray)
            y = height - MARGIN_TOP
            pages += 1

        for _ in range(repeat):
            for line in wrapped_lines:
                c.drawString(x, y, line)
                y -= line_height
        y -= CARD_GAP

    c.save()
    return pages


def main():
    ap = argparse.ArgumentParser(
        description="Generate a printable handwriting-practice PDF from today's due Anki cards"
    )
    ap.add_argument("--deck", required=True, help="Deck directory name under decks/ (e.g. interview)")
    ap.add_argument("--repeat", type=int, default=2, help="Times to repeat each sentence (default: 2)")
    ap.add_argument(
        "--font",
        choices=sorted(FONT_FILES),
        default="lined",
        help="kg_primary_dots font variant (default: lined)",
    )
    ap.add_argument("--font-size", type=float, default=26, help="Font size in pt (default: 26)")
    ap.add_argument(
        "--intensity",
        type=float,
        default=1.0,
        help="Text darkness: 0.0 (white) .. 1.0 (full black, default). Lower = fainter guide to trace over.",
    )
    ap.add_argument("--limit", type=int, default=None, help="Cap number of cards (for quick layout tests)")
    ap.add_argument("--output", default=None, help="Output PDF path (default: handwriting_practice/<deck>_<date>.pdf)")
    args = ap.parse_args()

    deck_dir = DECKS_DIR / args.deck
    meta_path = deck_dir / "_meta.yaml"
    if not meta_path.exists():
        print(f"✗ No _meta.yaml found in {deck_dir}")
        sys.exit(1)
    deck_name = load_yaml(meta_path)["deckName"]

    if not 0.0 <= args.intensity <= 1.0:
        print("✗ --intensity must be between 0.0 and 1.0")
        sys.exit(1)

    try:
        anki("version")
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to AnkiConnect. Is Anki running?")
        sys.exit(1)

    sentences = fetch_due_sentences(deck_name)
    if not sentences:
        print(f"✓ No due cards in '{deck_name}' today. Nothing to print.")
        return

    if args.limit:
        sentences = sentences[: args.limit]

    font_path = FONTS_DIR / FONT_FILES[args.font]
    if not font_path.exists():
        print(f"✗ Font file not found: {font_path}")
        sys.exit(1)

    output_path = Path(args.output) if args.output else OUTPUT_DIR / f"{args.deck}_{date.today().isoformat()}.pdf"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pages = build_pdf(sentences, output_path, font_path, args.font_size, args.repeat, args.intensity)

    print(f"✓ Deck: {deck_name}")
    print(f"  Cards: {len(sentences)}  |  Repeat: {args.repeat}  |  Pages: {pages}")
    print(f"  → {output_path}")


if __name__ == "__main__":
    main()
