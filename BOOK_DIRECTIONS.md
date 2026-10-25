# Book directions — Water Bucket Puzzle

**Catalog #523** · Al Sweigart, *The Big Book of Small Python Projects*, **Project #81**

- Online chapter: [inventwithpython.com/bigbookpython/project81.html](https://inventwithpython.com/bigbookpython/project81.html)
- Upstream: [waterbucket.py](https://github.com/asweigart/the-big-book-of-small-python-projects/blob/main/waterbucket.py)
- Local reference: [`reference/waterbucket.py`](./reference/waterbucket.py)
- Shared logic: [`water_bucket_core.py`](./water_bucket_core.py)

## What the book asks you to build

A **water-pouring puzzle**: three buckets (**8 L**, **5 L**, **3 L**) start empty. Get exactly **4 L** in any one bucket using only:

- **Fill** — fill a bucket to its capacity
- **Empty** — drain a bucket
- **Pour** — transfer from one bucket into another until the source is empty or the destination is full

The terminal game counts **steps** and exits when any bucket holds **4 L**.

## Core state

| Key | Role |
|-----|------|
| `waterInBucket['8' \| '5' \| '3']` | Liters currently in each bucket |
| `GOAL = 4` | Win condition |
| `steps` | Moves taken |

## Step order (terminal program)

1. Print ASCII art of bucket levels (`WWWWWW` vs spaces).
2. If any bucket equals `GOAL`, print success and exit.
3. Prompt for **F** / **E** / **P** / **Q**.
4. Prompt for source bucket **8**, **5**, or **3** (or quit).
5. For **P**, prompt for destination bucket; pour `min(empty space in dest, water in source)`.
6. Increment `steps` and loop.

## Web version (`web/` — FastAPI, port **3007**)

| Book step | Web equivalent |
|-----------|----------------|
| Display buckets | Visual tanks + liter labels |
| F / E / P | **Fill**, **Empty**, **Pour** controls + bucket selection |
| Step counter | Shown after each `POST /api/move` |
| Win at 4 L | Banner when `won` is true |
| Reset | **New game** → `POST /api/reset` |
| Pour math | [`water_bucket_core.py`](./water_bucket_core.py) |
