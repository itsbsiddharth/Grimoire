#!/usr/bin/env python3
"""
Scaffolds the DSA vault: creates a problems/<slug>/ folder for each
solved TUF+ problem, pre-filled with problem.md (frontmatter + notes
sections) and an empty solutions/ folder — then writes the TUF+ SDE
Sheet roadmap in solve order.

Run this from the ROOT of your Grimoire repo (the folder that
directly contains problems/ and roadmaps/).

Usage:
    python scaffold.py

Safe to re-run: it skips any problem folder that already exists,
so if you add more solved problems later, add them to the PROBLEMS
list below and run it again — it won't touch what's already there.
"""

import os

# (title, topic, slug) in TUF+ SDE Sheet order
PROBLEMS = [
    ("Kadane's Algorithm", "arrays", "kadanes-algorithm"),
    ("Lower Bound", "binary-search", "lower-bound"),
    ("Upper Bound", "binary-search", "upper-bound"),
    ("Search in Rotated Sorted Array II", "binary-search", "search-in-rotated-sorted-array-ii"),
    ("Find Minimum in Rotated Sorted Array", "binary-search", "find-minimum-in-rotated-sorted-array"),
    ("Koko Eating Bananas", "binary-search", "koko-eating-bananas"),
    ("Aggressive Cows", "binary-search", "aggressive-cows"),
    ("Median of Two Sorted Arrays", "binary-search", "median-of-two-sorted-arrays"),
    ("Matrix Median", "binary-search", "matrix-median"),
    ("Power Set", "recursion", "power-set"),
    ("Check if There Exists a Subsequence With Sum K", "recursion", "subsequence-with-sum-k"),
    ("Rat in a Maze", "recursion", "rat-in-a-maze"),
    ("N Meetings in One Room", "greedy", "n-meetings-in-one-room"),
    ("Non-overlapping Intervals", "greedy", "non-overlapping-intervals"),
    ("Minimum Number of Platforms Required", "greedy", "minimum-platforms"),
    ("Valid Parenthesis Checker", "greedy", "valid-parenthesis-checker"),
    ("Candy", "greedy", "candy"),
    ("Preorder Traversal", "trees", "preorder-traversal"),
    ("Inorder Traversal", "trees", "inorder-traversal"),
    ("Postorder Traversal", "trees", "postorder-traversal"),
    ("Level Order Traversal", "trees", "level-order-traversal"),
    ("Maximum Depth of Binary Tree", "trees", "maximum-depth-of-binary-tree"),
    ("Diameter of Binary Tree", "trees", "diameter-of-binary-tree"),
    ("Binary Tree Maximum Path Sum", "trees", "binary-tree-maximum-path-sum"),
    ("Symmetric Binary Tree", "trees", "symmetric-binary-tree"),
    ("Boundary Traversal of Binary Tree", "trees", "boundary-traversal-of-binary-tree"),
    ("Vertical Order Traversal", "trees", "vertical-order-traversal"),
    ("Top View of Binary Tree", "trees", "top-view-of-binary-tree"),
    ("Graph Traversal Techniques", "graphs", "graph-traversal-techniques"),
    ("Number of Islands", "graphs", "number-of-islands"),
    ("Flood Fill Algorithm", "graphs", "flood-fill"),
    ("Rotten Oranges", "graphs", "rotten-oranges"),
    ("Surrounded Regions", "graphs", "surrounded-regions"),
    ("Number of Distinct Islands", "graphs", "number-of-distinct-islands"),
    ("Bipartite Graph", "graphs", "bipartite-graph"),
    ("Climbing Stairs", "dp", "climbing-stairs"),
    ("Maximum Sum of Non-Adjacent Elements", "dp", "maximum-sum-of-non-adjacent-elements"),
    ("House Robber", "dp", "house-robber"),
]

PROBLEM_MD_TEMPLATE = """---
title: {title}
topic: {topic}
subtopics: []
platforms: [tuf-plus]
type: practice
company: []
difficulty:
canonical_link:
aliases: []
---

## Crux
>

## Thought process
-

## Things to remember
-
"""


def main():
    if not os.path.isdir("problems") or not os.path.isdir("roadmaps"):
        print("Run this from the repo root (the folder containing problems/ and roadmaps/).")
        return

    created, skipped = 0, 0

    for title, topic, slug in PROBLEMS:
        folder = os.path.join("problems", slug)
        if os.path.exists(folder):
            skipped += 1
            continue
        os.makedirs(os.path.join(folder, "solutions"))
        with open(os.path.join(folder, "problem.md"), "w", encoding="utf-8") as f:
            f.write(PROBLEM_MD_TEMPLATE.format(title=title, topic=topic))
        # keeps the empty solutions/ folder visible in git until a real file lands in it
        open(os.path.join(folder, "solutions", ".gitkeep"), "w").close()
        created += 1

    # the roadmap list order IS the revision order — no duplicate 'order' field needed anywhere else
    roadmap_path = os.path.join("roadmaps", "tuf-plus-sde-sheet.yaml")
    with open(roadmap_path, "w", encoding="utf-8") as f:
        f.write("name: TUF+ SDE Sheet\nproblems:\n")
        for _, _, slug in PROBLEMS:
            f.write(f"  - {slug}\n")

    print(f"Created {created} problem folders, skipped {skipped} that already existed.")
    print(f"Wrote {roadmap_path} with {len(PROBLEMS)} entries.")


if __name__ == "__main__":
    main()
