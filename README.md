# AI Copywriting course quizzes

Every quiz page for the AI Copywriting beginner course lives here and is served
from GitHub Pages at https://sethczerepak.github.io/aic-course/lesson-N-quiz.html

## Before you ship a quiz, run this

    python3 check.py

It reads **Lessons 1, 2 and 3** and holds every other quiz to what they do:
the title, the heading, the unlock button, the copy button, both miss headings,
the rewatch link, the footer, the reveal heading, the question count and the
resize script.

It does not describe the pattern from memory or from a document. It reads the
published work, so it cannot drift away from it. If Lessons 1-3 ever disagree
with each other, it stops and says so instead of guessing.

Exit code 1 means something deviates. Fix it before shipping.

## Building a new quiz

Copy the nearest existing quiz, swap the content, then run `check.py` until it
passes. Do not invent new wording for buttons or headings. If you think the
pattern itself should change, change Lessons 1-3 first and deliberately, so the
reference moves on purpose rather than by accident.

## Why this file exists

Lesson 4 renamed its quiz from "The Lesson 4 Quiz" to "The Concrete & Specific
Quiz". Lessons 5, 6 and 7 were each built by copying the one before, so they
inherited it. Lesson 7 also renamed its unlock button and dropped the VQ logo
from its footer. None of it was caught until Seth spotted it himself, weeks
later. That is what this check is for.
