"""Build the anonymized LREC review-mode LaTeX source from the Markdown manuscript."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).parent
SOURCE = ROOT / "final_research_paper.md"
OUTPUT = ROOT / "lrec_submission.tex"


def escape(text: str) -> str:
    for old, new in [
        ("&", r"\&"),
        ("%", r"\%"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
    ]:
        text = text.replace(old, new)
    return text.strip()


def text_with_urls(text: str) -> str:
    parts = re.split(r"(https?://[^\s]+)", text)
    result = []
    for part in parts:
        if part.startswith(("http://", "https://")):
            suffix = "." if part.endswith(".") else ""
            result.append(r"\url{" + part.rstrip(".") + "}" + suffix)
        else:
            result.append(escape(part))
    return "".join(result)


def reference_label(text: str) -> str:
    match = re.match(r"([^,]+).*?\((\d{4})\)", text)
    if not match:
        return "Reference"
    author = match.group(1).strip()
    return author.split(",")[0] + (" et al." if " and " not in text.split("(")[0] else "")


def build() -> None:
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    title = lines[0].strip()
    abstract_start = lines.index("## Abstract") + 1
    abstract_end = next(
        index for index in range(abstract_start, len(lines))
        if lines[index].startswith("## ")
    )
    abstract = " ".join(line.strip() for line in lines[abstract_start:abstract_end] if line.strip())
    abstract, keywords = abstract.split("Keywords:", 1)

    output = [
        r"\documentclass[10pt,a4paper]{article}",
        r"\usepackage[review]{lrec2026}",
        r"\usepackage{tabularx,booktabs,graphicx,url}",
        rf"\title{{{escape(title)}}}",
        r"\name{Anonymous submission}",
        r"\address{Author information omitted for double-blind review}",
        rf"\abstract{{{text_with_urls(abstract)} \\ \newline \Keywords{{{escape(keywords.strip())}}}}}",
        r"\begin{document}",
        r"\maketitleabstract",
    ]

    index = abstract_end
    table_number = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line == "## References":
            output.append(r"\begin{thebibliography}{99}")
            for reference in lines[index + 1:]:
                reference = reference.strip()
                if not reference or reference.startswith("### "):
                    continue
                year = re.search(r"\((\d{4})\)", reference)
                year_text = year.group(1) if year else "n.d."
                output.append(
                    rf"\bibitem[{escape(reference_label(reference))} ({year_text})]{{ref{year_text}}} "
                    + text_with_urls(reference)
                )
            output.append(r"\end{thebibliography}")
            break
        if line.startswith("## "):
            output.append(r"\section{" + escape(line[3:]) + "}")
            index += 1
            continue
        if line.startswith("### "):
            output.append(r"\subsection{" + escape(line[4:]) + "}")
            index += 1
            continue
        if line.startswith("| "):
            table_number += 1
            rows = []
            while index < len(lines) and lines[index].strip().startswith("| "):
                cells = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
                if not all(set(cell) <= set("- ") for cell in cells):
                    rows.append(cells)
                index += 1
            columns = len(rows[0])
            caption = {
                1: "Benchmark label distribution by topic.",
                2: "Absolute-term wording distribution by gold label.",
                3: "Pilot accuracy, macro-F1, and invalid outputs by condition and form.",
                4: "Zero-shot per-class recall by form.",
            }.get(table_number, "Summary table.")
            output.extend([
                r"\begin{table}[t]",
                r"\centering",
                r"\scriptsize",
                r"\begin{tabular}{" + "l" * columns + "}",
                r"\toprule",
            ])
            for row_index, row in enumerate(rows):
                output.append(" & ".join(escape(cell) for cell in row) + r" \\")
                if row_index == 0:
                    output.append(r"\midrule")
            output.extend([r"\bottomrule", r"\end{tabular}", r"\caption{" + caption + "}", r"\end{table}"])
            continue

        paragraph = [line]
        index += 1
        while (
            index < len(lines)
            and lines[index].strip()
            and not lines[index].startswith(("## ", "### ", "| "))
        ):
            paragraph.append(lines[index].strip())
            index += 1
        output.extend([text_with_urls(" ".join(paragraph)), ""])

    output.append(r"\end{document}")
    OUTPUT.write_text("\n".join(output) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
