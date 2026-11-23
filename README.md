# Skyscraper Race

A 2-player race to **150 meters**. Roll materials, place floors in your tower, stay stable, survive height challenges.

This repo is a **DSA project**. The graded work lives in `logic/`. The desktop UI in `game/` and this README were helped by AI.

---

## What you implement (3 + 3)

### Data structures

| # | Structure | File | Job in the game |
|---|-----------|------|-----------------|
| 1 | **Hash table** (dict) | `logic/data/materials.py` | Look up material stats from a roll |
| 2 | **List** (array) | `logic/algorithms/tower.py` | Store floors; index `0` = ground |
| 3 | **Min-heap** | `logic/algorithms/challenges.py` | Next challenge = smallest height |

### Algorithms

| # | Algorithm | File | Job in the game |
|---|-----------|------|-----------------|
| 1 | **Recursion** | `tower.load_above` | Sum the weight above one floor |
| 2 | **Heap peek / pop** | `challenges.run_challenges` | Fire events when height catches up |
| 3 | **Sequential search** | `tower.find_weakest_floor_index` | Find the floor closest to breaking |

Code is written in a plain, step-by-step style (explicit loops, clear names) so it is easy to read and explain — not packed “Pythonic” one-liners.

---

## Install

### 1. Get the code

```bash
git clone https://github.com/YousefAliAicha/Skyscraper-Race-DSA.git
cd Skyscraper-Race-DSA
```

### 2. Create a virtual environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (Command Prompt)**

```bat
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Python packages

```bash
pip install -r requirements.txt
```

### 4. Tk (only for the desktop GUI)

Check:

```bash
python3 -c "import tkinter; print('tk ok')"
```

If that fails:

| OS | Fix |
|----|-----|
| **macOS** | `brew install python` then recreate the venv. If still broken: `brew install python-tk` and recreate the venv again. |
| **Ubuntu / Debian** | `sudo apt install python3-tk` |
| **Windows** | Reinstall Python from [python.org](https://www.python.org/downloads/windows/) and enable **tcl/tk**. |

The **notebook** and `demo.py` / `test_core.py` do **not** need Tk.

---

## Run

Always from the **repo root** (the folder that contains `logic/` and `game/`):

```bash
python3 test_core.py      # unit tests
python3 demo.py           # console autoplay (no window)
python3 -m game.main      # fullscreen GUI
```

### Jupyter notebook (one file)

Open [`Skyscraper_Race_Play.ipynb`](Skyscraper_Race_Play.ipynb) in Jupyter, VS Code, or Colab → **Run all**.

```bash
pip install notebook
jupyter notebook Skyscraper_Race_Play.ipynb
```

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YousefAliAicha/Skyscraper-Race-DSA/blob/main/Skyscraper_Race_Play.ipynb)

---

## How to play (GUI)

| Control | Action |
|---------|--------|
| `R` or ROLL | Roll a floor |
| `↑` / `↓` | Move the place arrow |
| Enter / Space | Place at the arrow |
| Click your tower | Move the arrow |
| `S` or SCRAP | Discard the roll |
| Esc | Back to menu |

P1 builds on the **left**, P2 on the **right**. Three rolls per turn. Put strong materials at the bottom; junk on top or scrap it.

---

## Folder layout

```
logic/                     # graded DSA + rules
  data/
    constants.py           # balance numbers
    materials.py           # hash table
    floor.py               # one floor (data only)
  algorithms/
    tower.py               # list + recursion + sequential search
    challenges.py          # min-heap + peek/pop
    roll.py                # 5-digit roll decode
    player.py
    game.py                # turn flow (no GUI)

game/                      # UI only (AI-assisted)
  main.py
  match.py
  screens.py
  assets.py
  img/

test_core.py
demo.py
Skyscraper_Race_Play.ipynb
README.md
```

---

## Why these choices (short)

**Hash table** — “given a roll, get stats” is a lookup problem. Dict average **O(1)** beats a long `if/elif` or scanning a list.

**List** — you place by **slot index**. A list makes `insert(slot, floor)` natural. A linked list would add pointer complexity without helping placement.

**Min-heap** — next challenge is the **smallest** remaining height. Peek **O(1)**, pop **O(log n)**. Better than scanning an unsorted list every place.

**Recursion (`load_above`)** — load on floor *i* is defined as weight of *i+1* plus load on *i+1*. Base case: top floor → `0`. **O(n)** matches “must look at every floor above.”

**Heap peek/pop** — after each place, while tower height ≥ heap root, pop and apply the event. Standard priority-queue “next event” loop.

**Sequential search** — any floor can be weakest; there is no sorted key for binary search. Walk all floors, keep the worst ratio. Correct and easy to explain.

---

## AI note

AI helped with the **UI** (`game/`), **GitHub setup**, and **comments/docs**. The course focus is **`logic/`**: the three data structures and three algorithms above.
