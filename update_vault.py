#!/usr/bin/env python3
"""
Two-in-one cleanup, run ONCE from the repo root (the folder containing
problems/ and roadmaps/):

1. Simplifies every problems/<slug>/problem.md down to frontmatter +
   a single "## Crux" section (drops "Thought process" / "Things to
   remember" — your thought process already lives in code comments,
   and "things to remember" IS the crux). Preserves title/topic/all
   frontmatter fields exactly. If you'd already typed anything real
   under Crux, it's preserved; blank placeholders collapse to ">".

2. Creates 1-brute-force.cpp, 2-better.cpp, 3-optimal.cpp inside every
   problems/<slug>/solutions/ folder that doesn't already have them.
   Delete whichever ones you don't end up needing per problem — that's
   less friction than creating files from scratch each time.

Safe to re-run: never overwrites a solution file that already exists,
and re-running the problem.md simplification on an already-simplified
file is a no-op.

Usage:
    python update_vault.py
"""

import os

STUBS = [
    ("1-brute-force.cpp", "Brute Force"),
    ("2-better.cpp", "Better"),
    ("3-optimal.cpp", "Optimal"),
]

STUB_TEMPLATE = """// {title} — {label}
// TODO: paste your best submission for this approach.
// Delete this file if you don't have a separate {label_lower} solution.

"""


def get_title(problem_md_path):
    if not os.path.exists(problem_md_path):
        return None
    with open(problem_md_path, encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("title:"):
                return line.split(":", 1)[1].strip()
    return None


def simplify_problem_md(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()

    parts = content.split("---", 2)
    if len(parts) < 3:
        return False  # not frontmatter-shaped, leave it alone

    frontmatter = parts[1]
    body = parts[2]

    crux_text = ""
    if "## Crux" in body:
        after = body.split("## Crux", 1)[1]
        crux_text = after.split("\n## ", 1)[0].strip("\n")

    crux_final = crux_text.strip() if crux_text.strip() not in ("", ">") else ">"
    new_content = f"---{frontmatter}---\n\n## Crux\n{crux_final}\n"

    if new_content == content:
        return False  # already simplified, nothing to do

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True


def main():
    if not os.path.isdir("problems"):
        print("Run this from the repo root (the folder containing problems/).")
        return

    simplified = 0
    stubs_created = 0

    for slug in sorted(os.listdir("problems")):
        folder = os.path.join("problems", slug)
        if not os.path.isdir(folder):
            continue

        problem_md = os.path.join(folder, "problem.md")
        if os.path.exists(problem_md) and simplify_problem_md(problem_md):
            simplified += 1

        sol_folder = os.path.join(folder, "solutions")
        if not os.path.isdir(sol_folder):
            continue

        title = get_title(problem_md) or slug
        for fname, label in STUBS:
            fpath = os.path.join(sol_folder, fname)
            if os.path.exists(fpath):
                continue
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(STUB_TEMPLATE.format(title=title, label=label, label_lower=label.lower()))
            stubs_created += 1

    print(f"Simplified {simplified} problem.md file(s).")
    print(f"Created {stubs_created} solution stub file(s).")


if __name__ == "__main__":
    main()
