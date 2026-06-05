# SUPERtree BEVerages! (Superbev)
Watch gameplay: https://youtu.be/kQygGFkp2wU
![Game Screenshot](superbev_screenshot.png)

---

## How to Play

1. **Welcome Screen:** Click **PLAY** to begin your shift at the Gardens.
2. **Review Instructions:** Learn your targets! You must answer the Python fundamentals questions correctly to secure your sales.
3. **Run the Shop:** Different customers will request random drinks. Select option **A** or **B** to solve the Python concept.
   * **Correct Answer:** The drink is sold! You earn the cash value towards your target.
   * **Incorrect Answer:** The customer leaves, and you miss out on the sale.
4. **The Ultimate Goal:** Get a flawless streak, earn **$45 or more**, and sit back to watch the dynamic Supertree Light Show celebrate your victory!

---

## Installation & Running the Game

### Windows

> **Prerequisites:** Make sure you have [Python 3](https://www.python.org/downloads/) installed.

1. Click the green **Code** button on the top right corner
2. Click **Download ZIP** and choose **Extract All**
3. Open the extracted folder
4. Double-click **run_game.bat** to play

That's it — no additional setup needed!

---

### macOS

> **Prerequisites:** Make sure you have [Python 3](https://www.python.org/downloads/) installed.

**Step 1 — Install required libraries**

Open **Terminal** (search for it in Spotlight with ⌘ + Space) and run:

```bash
pip3 install pygame pillow
```

**Step 2 — Download the game**

1. Click the green **Code** button on the top right corner
2. Click **Download ZIP** and choose to extract it
3. Note where the extracted **superbev** folder is saved (e.g. your Downloads folder)

**Step 3 — Run the game**

In Terminal, navigate to the folder and run:

```bash
cd ~/Downloads/superbev-main
python3 main.py
```

> **Tip:** If you're unsure of the path, open the extracted superbev folder in Finder, then drag the folder icon into your Terminal window after typing `cd ` — it will fill in the path automatically. Then press Enter.

---

## The Concept & Creation Story

As a Singaporean student in the CIP 2026 course, I wanted to build a graphics-based game that uniquely represents home.

### The Inspiration

Gardens by the Bay frequently hosts vibrant pop-up stalls under its towering Supertrees. This inspired the core mechanics of the game: selling beloved local drinks (**Milo Dinosaur, Bandung, and Sugarcane**) packed in unique bottles shaped exactly like the Supertrees themselves!

### Development & Design Choices

* **Color Palette Accuracies:** The visual colors used throughout the user interface, tables, backgrounds, and tree models were carefully selected to match the real-life aesthetic of the **Supertree Grove** and the **Jurassic Nest Food Hall**.
* **Why local quiz logic over AI?** While I initially considered using `CallGPT` to dynamically generate questions, I ultimately decided against it to eliminate the risks of API instability, network latency, and rigid call limitations. Instead, I built a reliable, randomized native Python quiz engine to test core coding fundamentals.
* **The Light Show Challenge:** Programming the mathematical animations for the Supertree Light Show was the most complex part of the project, taking **3 full days of dedicated coding** to perfect the Bezier curves, overlapping sine waves, and twinkling LED coordinate matrices.

In total, this project took **4 to 5 days** of continuous iteration from its initial whiteboard concept to this final, polished copy.
