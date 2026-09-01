#!/usr/bin/env python3
"""Quiz conformance checker for the AI Copywriting course.

It does NOT describe what a quiz should look like. It READS Lessons 1-3,
which are the pattern Seth set, and holds every other quiz to what they do.
That is the point: a document can drift from the work. This cannot, because
the work is the reference.

    python3 check.py            check every quiz
    python3 check.py 8          check one

Exit code 1 if anything deviates. Run it before you ship a quiz.
"""
import re, sys, glob, os

HERE = os.path.dirname(os.path.abspath(__file__))
REFERENCE = [1, 2, 3]            # the lessons that define the pattern

def load(n):
    p = os.path.join(HERE, f"lesson-{n}-quiz.html")
    return open(p, encoding="utf-8").read() if os.path.exists(p) else None

def grab(h, pat, all=False):
    m = re.findall(pat, h, re.S) if all else re.search(pat, h, re.S)
    if all: return m
    return m.group(1).strip() if m else None

# --- the fields we hold constant, and how to read each one ----------------
FIELDS = {
 "title":        lambda h: grab(h, r"<title>([^<]*)</title>"),
 "h1":           lambda h: grab(h, r"<h1>([^<]*)</h1>"),
 "unlock_label": lambda h: grab(h, r'id="unlock"[^>]*>([^<]*)<'),
 "unlock_attrs": lambda h: grab(h, r"<button ([^>]*id=\"unlock\"[^>]*)>"),
 "copy_label":   lambda h: grab(h, r'id="copy"[^>]*>([^<]*)<'),
 "hold_head":    lambda h: (grab(h, r"<h3>([^<]*)</h3>", all=True) or [None])[0],
 "miss_head":    lambda h: (grab(h, r"<h3>([^<]*)</h3>", all=True) or [None,None])[-1],
 "rewatch":      lambda h: grab(h, r'class="rewatch"[^>]*>([^<]*)<'),
 "footer":       lambda h: grab(h, r'(<div class="foot">.*?</div></div>)'),
 "ok_head":      lambda h: grab(h, r"<h2>([^<]*)</h2>"),
 "questions":    lambda h: str(len(re.findall(r'class="q" data-correct', h))),
 "resize":       lambda h: "yes" if "aicQuizHeight" in h else "no",
}
# fields whose value legitimately carries the lesson number
NUMBERED = {"title", "h1", "rewatch", "ok_head"}

def normalise(v, n):
    """Blank out the lesson number so patterns compare across lessons."""
    if v is None: return None
    return re.sub(rf"\b{n}\b", "N", v)

def build_pattern():
    pat, src = {}, {}
    for n in REFERENCE:
        h = load(n)
        if h is None: sys.exit(f"reference lesson {n} is missing - cannot check anything")
        for f, fn in FIELDS.items():
            v = normalise(fn(h), n) if f in NUMBERED else fn(h)
            if f in pat and pat[f] != v:
                sys.exit(f"Lessons {REFERENCE} disagree on '{f}'. Settle that first:\n"
                         f"  lesson {src[f]}: {pat[f]!r}\n  lesson {n}: {v!r}")
            pat[f], src[f] = v, n
    return pat

def check(n, pat):
    h = load(n)
    if h is None: return [f"lesson-{n}-quiz.html does not exist"]
    bad = []
    two_rewards = len(re.findall(r'class="copy"', h)) == 2
    for f, fn in FIELDS.items():
        got = normalise(fn(h), n) if f in NUMBERED else fn(h)
        want = pat[f]
        # a quiz that hands over a rule AND a practice prompt says so; that is
        # a real difference in what the student receives, not a style drift.
        if f == "ok_head" and two_rewards:
            if got and got.startswith("Unlocked: Your Lesson N"): continue
        if got != want:
            bad.append(f"{f}\n      is:     {got!r}\n      should: {want!r}")
    return bad

def main():
    pat = build_pattern()
    only = [int(sys.argv[1])] if len(sys.argv) > 1 else sorted(
        int(re.search(r"lesson-(\d+)-quiz", p).group(1))
        for p in glob.glob(os.path.join(HERE, "lesson-*-quiz.html")))
    print(f"pattern taken from lessons {REFERENCE}\n")
    fails = 0
    for n in only:
        bad = check(n, pat)
        if bad:
            fails += 1
            print(f"  FAIL  lesson {n}")
            for b in bad: print(f"      {b}")
        else:
            print(f"  ok    lesson {n}")
    print()
    if fails:
        print(f"{fails} quiz(zes) do not match Lessons {REFERENCE}. Fix before shipping.")
        sys.exit(1)
    print("All quizzes match the pattern.")

if __name__ == "__main__":
    main()
