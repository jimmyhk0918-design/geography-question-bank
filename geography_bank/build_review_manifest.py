#!/usr/bin/env python3
"""Build the image-question review manifest used by cleaning.html."""

from __future__ import annotations

import ast
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent.parent
BANK_INDEX = ROOT / "geography_bank" / "question_banks.json"
OUT_FILE = ROOT / "geography_bank" / "review_manifest.json"
OUT_SCRIPT_FILE = ROOT / "geography_bank" / "review_manifest.js"


def load_literal_assignment(path: Path, variable: str):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(target, ast.Name) and target.id == variable for target in targets):
                return ast.literal_eval(node.value)
    return []


def web_path(path: Path) -> str:
    return "./" + path.relative_to(ROOT).as_posix()


def find_page(base_dir: Path, page_number: int) -> Path | None:
    page_dir = base_dir / "pages"
    matches = sorted(page_dir.glob(f"page-{page_number:02d}.*"))
    return matches[0] if matches else None


def review_box(page_size: tuple[int, int], figure_box: tuple[int, int, int, int]) -> list[int]:
    width, height = page_size
    _, top, _, bottom = figure_box
    above = max(260, round(height * 0.22))
    below = max(340, round(height * 0.24))
    crop_top = max(0, top - above)
    crop_bottom = min(height, bottom + below)
    return [0, crop_top, width, max(1, crop_bottom - crop_top)]


def main() -> None:
    bank_index = json.loads(BANK_INDEX.read_text(encoding="utf-8"))
    manifest_banks = []
    total_questions = 0

    for bank in bank_index:
        base_dir = ROOT / bank["basePath"].removeprefix("./")
        question_file = ROOT / bank["url"].removeprefix("./")
        builder_file = base_dir / "build_question_bank.py"
        if not question_file.exists() or not builder_file.exists():
            continue

        payload = json.loads(question_file.read_text(encoding="utf-8"))
        figures = load_literal_assignment(builder_file, "FIGURES")
        figure_map = {}

        for name, page_number, box, caption, linked_questions in figures:
            page_file = find_page(base_dir, int(page_number))
            if not page_file:
                continue
            with Image.open(page_file) as image:
                page_size = image.size
            figure_map[name] = {
                "figure": name,
                "caption": caption,
                "page": int(page_number),
                "pageImage": web_path(page_file),
                "pageWidth": page_size[0],
                "pageHeight": page_size[1],
                "box": review_box(page_size, tuple(box)),
                "figureBox": list(box),
                "linkedQuestions": list(linked_questions),
            }

        review_questions = []
        for question in payload.get("questions", []):
            images = question.get("images") or []
            if not images:
                continue

            reviews = []
            resolved_images = []
            for image_path in images:
                resolved_images.append(web_path(base_dir / image_path))
                figure = figure_map.get(Path(image_path).stem)
                if figure:
                    reviews.append(figure)

            if not reviews:
                page_file = find_page(base_dir, int(question.get("source_page", 1)))
                if page_file:
                    with Image.open(page_file) as image:
                        width, height = image.size
                    reviews.append(
                        {
                            "figure": "",
                            "caption": "原卷整页",
                            "page": int(question.get("source_page", 1)),
                            "pageImage": web_path(page_file),
                            "pageWidth": width,
                            "pageHeight": height,
                            "box": [0, 0, width, height],
                            "figureBox": [0, 0, width, height],
                            "linkedQuestions": [question.get("number")],
                        }
                    )

            review_questions.append(
                {
                    "id": question.get("id"),
                    "number": question.get("number"),
                    "type": question.get("type"),
                    "score": question.get("score"),
                    "sourcePage": question.get("source_page"),
                    "groupPrompt": question.get("group_prompt", ""),
                    "stem": question.get("stem", ""),
                    "options": question.get("options", {}),
                    "answer": question.get("answer", ""),
                    "images": resolved_images,
                    "reviews": reviews,
                }
            )

        total_questions += len(review_questions)
        manifest_banks.append(
            {
                "id": bank["id"],
                "title": bank["title"],
                "basePath": bank["basePath"],
                "questions": review_questions,
            }
        )

    output = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "bankCount": len(manifest_banks),
        "questionCount": total_questions,
        "banks": manifest_banks,
    }
    OUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_SCRIPT_FILE.write_text(
        "window.GEOGRAPHY_REVIEW_MANIFEST = "
        + json.dumps(output, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUT_FILE}")
    print(f"Wrote {OUT_SCRIPT_FILE}")
    print(f"Banks: {len(manifest_banks)}, image questions: {total_questions}")


if __name__ == "__main__":
    main()
