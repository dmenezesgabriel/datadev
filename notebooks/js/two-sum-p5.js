// ╔══════════════════════════════════════════════════════════════════╗
//  p5.js ALGORITHM VISUALIZER  —  Two Sum with strategy selector
//  Paste into https://editor.p5js.org and hit Run.
//
//  ARCHITECTURE:
//    Strategy   — one algorithm approach (brute force, hash map, etc.)
//                 Owns: name, complexity tag, and steps() generation.
//    Problem    — groups strategies for the same problem + shared data.
//                 Owns: title, input array, target, and its strategies.
//    Renderer   — pure drawing; knows nothing about algorithms.
//    Visualizer — engine: owns playback state, UI, and wires everything.
//
//  TO ADD A NEW STRATEGY to an existing problem:
//    1. Write a class that extends Strategy, implement steps().
//    2. Add an instance to the problem's strategies array.
//    Done — the dropdown updates automatically.
//
//  TO ADD A COMPLETELY NEW PROBLEM:
//    1. Extend Problem, define your strategies inside it.
//    2. Swap ACTIVE_PROBLEM at the bottom.
// ╚══════════════════════════════════════════════════════════════════╝

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  Step  —  a single animation frame produced by a Strategy
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Step {
  // pointers  : { i, j }  indices to highlight in the array (nullable)
  // label     : string    "what is being checked = value"  (panel line 1)
  // result    : string    outcome of this check            (panel line 2)
  // found     : bool      true → green theme, false → red/blue theme
  // logEntry  : string    compact text for the history log (nullable)
  // done      : bool      true → terminal no-solution state
  constructor({ pointers, label, result, found, logEntry, done = false }) {
    this.pointers = pointers;
    this.label = label;
    this.result = result;
    this.found = found;
    this.logEntry = logEntry;
    this.done = done;
  }
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  Strategy  —  base class for one algorithm approach
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Strategy {
  get name() {
    return "Unnamed Strategy";
  }
  get complexity() {
    return "";
  } // e.g. 'O(n2) time · O(1) space'
  get logHeader() {
    return "Steps:";
  }

  // Receives the problem's shared data and returns Step[].
  // Subclasses implement this with the actual algorithm.
  steps(data) {
    return [];
  }
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  Problem  —  groups strategies for the same problem + shared input
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Problem {
  // Subclasses override these getters for title, inputLine, array.
  // strategies must NOT be a getter — subclasses assign it directly in
  // their constructor (this.strategies = [...]), and a prototype getter
  // would block that instance assignment with a TypeError.
  get title() {
    return "Untitled Problem";
  }
  get inputLine() {
    return "";
  }
  get array() {
    return [];
  }
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  TWO SUM — strategies
//  Each class is one algorithm. They only differ in steps().
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TwoSumBruteForce extends Strategy {
  get name() {
    return "Brute Force";
  }
  get complexity() {
    return "O(n2) time  ·  O(1) space";
  }
  get logHeader() {
    return "Pairs checked:";
  }

  steps({ nums, target }) {
    const result = [];

    for (let i = 0; i < nums.length; i++) {
      for (let j = i + 1; j < nums.length; j++) {
        const sum = nums[i] + nums[j];
        const found = sum === target;

        result.push(
          new Step({
            pointers: { i, j },
            label:
              "nums[" +
              i +
              "] + nums[" +
              j +
              "] = " +
              nums[i] +
              " + " +
              nums[j] +
              " = " +
              sum,
            result: found
              ? "FOUND!  Answer = [" + i + ", " + j + "]"
              : sum + " != " + target + "  — not a match, continue...",
            found,
            logEntry:
              "[" + i + "," + j + "] " + nums[i] + "+" + nums[j] + "=" + sum,
          }),
        );

        if (found) return result;
      }
    }

    result.push(
      new Step({
        pointers: null,
        label: "All pairs exhausted.",
        result: "No solution found.",
        found: false,
        logEntry: null,
        done: true,
      }),
    );
    return result;
  }
}

// ──────────────────────────────────────────────────────────────────

class TwoSumHashMap extends Strategy {
  get name() {
    return "Hash Map";
  }
  get complexity() {
    return "O(n) time  ·  O(n) space";
  }
  get logHeader() {
    return "Map state:";
  }

  steps({ nums, target }) {
    const result = [];
    const seen = {}; // value → index

    for (let i = 0; i < nums.length; i++) {
      const complement = target - nums[i];
      const compIdx = seen[complement];
      const found = compIdx !== undefined;

      // Show what the map contains BEFORE this lookup
      const mapSnap =
        Object.entries(seen)
          .map(([v, idx]) => v + "→" + idx)
          .join(", ") || "(empty)";

      result.push(
        new Step({
          pointers: found ? { i: compIdx, j: i } : { i, j: i },
          label:
            "Look up complement " +
            complement +
            " in map  |  map: {" +
            mapSnap +
            "}",
          result: found
            ? "FOUND! " +
              complement +
              " is at index " +
              compIdx +
              "  →  Answer = [" +
              compIdx +
              ", " +
              i +
              "]"
            : complement +
              " not in map  — store " +
              nums[i] +
              "→" +
              i +
              " and advance",
          found,
          logEntry:
            "i=" +
            i +
            " val=" +
            nums[i] +
            " comp=" +
            complement +
            (found ? " HIT" : " miss"),
        }),
      );

      if (found) return result;
      seen[nums[i]] = i;
    }

    result.push(
      new Step({
        pointers: null,
        label: "All elements visited.",
        result: "No solution found.",
        found: false,
        logEntry: null,
        done: true,
      }),
    );
    return result;
  }
}

// ──────────────────────────────────────────────────────────────────

class TwoSumTwoPointers extends Strategy {
  get name() {
    return "Two Pointers";
  }
  get complexity() {
    return "O(n log n) time  ·  O(n) space  (requires sorted array)";
  }
  get logHeader() {
    return "Pointer moves:";
  }

  steps({ nums, target }) {
    const result = [];

    // Build index-annotated copy and sort it
    const sorted = nums
      .map((val, origIdx) => ({ val, origIdx }))
      .sort((a, b) => a.val - b.val);

    // Show the sort step — point at leftmost and rightmost of the ORIGINAL array
    result.push(
      new Step({
        pointers: {
          i: sorted[0].origIdx,
          j: sorted[sorted.length - 1].origIdx,
        },
        label:
          "Sort array first: [" + sorted.map((x) => x.val).join(", ") + "]",
        result:
          "Left pointer (L) starts at smallest, right pointer (R) at largest",
        found: false,
        logEntry: "sorted: [" + sorted.map((x) => x.val).join(",") + "]",
      }),
    );

    let left = 0;
    let right = sorted.length - 1;

    while (left < right) {
      const sum = sorted[left].val + sorted[right].val;
      const found = sum === target;

      result.push(
        new Step({
          pointers: { i: sorted[right].origIdx, j: sorted[left].origIdx },
          label:
            "sorted[" +
            left +
            "] + sorted[" +
            right +
            "] = " +
            sorted[left].val +
            " + " +
            sorted[right].val +
            " = " +
            sum,
          result: found
            ? "FOUND!  Original indices = [" +
              sorted[left].origIdx +
              ", " +
              sorted[right].origIdx +
              "]"
            : sum < target
              ? sum + " < " + target + "  — move left pointer right"
              : sum + " > " + target + "  — move right pointer left",
          found,
          logEntry:
            "L=" +
            left +
            " R=" +
            right +
            " sum=" +
            sum +
            (found ? " HIT" : sum < target ? " →L" : " ←R"),
        }),
      );

      if (found) return result;
      if (sum < target) left++;
      else right--;
    }

    result.push(
      new Step({
        pointers: null,
        label: "Pointers crossed — no solution.",
        result: "No solution found.",
        found: false,
        logEntry: null,
        done: true,
      }),
    );
    return result;
  }
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  TWO SUM — Problem
//  Holds shared input data and registers all strategies.
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TwoSum extends Problem {
  constructor(nums, target) {
    super();
    this.nums = nums;
    this.target = target;
    this.strategies = [
      new TwoSumBruteForce(),
      new TwoSumHashMap(),
      new TwoSumTwoPointers(),
    ];
  }

  get title() {
    return "Two Sum";
  }
  get inputLine() {
    return "nums = [" + this.nums.join(", ") + "]     target = " + this.target;
  }
  get array() {
    return this.nums;
  }

  // Convenience: returns the Step[] for the given strategy index
  stepsFor(strategyIndex) {
    return this.strategies[strategyIndex].steps({
      nums: this.nums,
      target: this.target,
    });
  }
}

// ── Change input here ──────────────────────────────────────────────
const ACTIVE_PROBLEM = new TwoSum([3, 5, 4, 8, 2, 1, 6], 9);
// ──────────────────────────────────────────────────────────────────

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  Renderer  —  pure drawing, no algorithm logic
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Renderer {
  constructor(canvasW) {
    this.canvasW = canvasW;

    this.layout = {
      arrayY: 158,
      boxW: 72,
      boxH: 66,
      boxGap: 10,
      arrowOffset: 22,
      panelY: 268,
      panelH: 112,
    };

    this.palette = {
      boxDefault: () => color(28, 32, 62),
      boxActive: () => color(0, 190, 255, 38),
      boxFound: () => color(0, 180, 100, 60),
      strokeDefault: () => color(55, 65, 110),
      strokeActive: () => color(0, 210, 255),
      strokeFound: () => color(0, 230, 130),
      numDefault: () => color(190, 205, 240),
      numActive: () => color(0, 220, 255),
      numFound: () => color(0, 255, 150),
      indexLabel: () => color(85, 108, 155),
      arrowI: () => color(0, 200, 255),
      arrowJ: () => color(255, 170, 50),
      arrowFound: () => color(0, 230, 130),
      panelBg: () => color(18, 22, 50),
      panelBorder: () => color(48, 58, 105),
      labelText: () => color(140, 162, 210),
      dimText: () => color(70, 90, 140),
      successText: () => color(0, 230, 130),
      failText: () => color(255, 100, 100),
      idleText: () => color(100, 120, 170),
      warningText: () => color(255, 170, 50),
      activeLogText: () => color(0, 210, 255),
      badge: () => color(30, 36, 80),
      badgeText: () => color(110, 140, 220),
    };
  }

  arrayStartX(len) {
    const { boxW, boxGap } = this.layout;
    return floor((this.canvasW - (len * boxW + (len - 1) * boxGap)) / 2);
  }

  boxCenterX(k, len) {
    const { boxW, boxGap } = this.layout;
    return this.arrayStartX(len) + k * (boxW + boxGap) + boxW / 2;
  }

  renderFrame(problem, strategy, currentStep, steps, stepDelay) {
    background(12, 12, 30);
    this.renderTitle(problem, strategy);
    this.renderInputLine(problem);
    this.renderArrayBoxes(problem, steps, currentStep);
    this.renderPointers(problem, steps, currentStep);
    this.renderStatusPanel(problem, strategy, steps, currentStep);
    this.renderStepLog(strategy, steps, currentStep);
    this.renderSpeedLabel(stepDelay);
  }

  renderTitle(problem, strategy) {
    noStroke();
    fill(255);
    textSize(21);
    textStyle(BOLD);
    text(problem.title, 40, 44);

    // complexity badge (below title, left-aligned)
    const badge = strategy.complexity;
    const bx = 40,
      by = 52,
      bpad = 8;
    textSize(11);
    textStyle(NORMAL);
    const bw = textWidth(badge) + bpad * 2;
    fill(this.palette.badge());
    noStroke();
    rect(bx, by, bw, 20, 4);
    fill(this.palette.badgeText());
    text(badge, bx + bpad, by + 14);

    // "Algorithm:" label drawn on canvas, top-right, just above the dropdown
    fill(this.palette.dimText());
    textSize(11);
    textStyle(NORMAL);
    textAlign(RIGHT, BASELINE);
    text("Algorithm:", 728, 15);
    textAlign(LEFT, BASELINE);
  }

  renderInputLine(problem) {
    noStroke();
    fill(175, 200, 255);
    textSize(14);
    textStyle(NORMAL);
    text(problem.inputLine, 40, 100);
  }

  renderArrayBoxes(problem, steps, currentStep) {
    const { layout, palette } = this;
    const arr = problem.array;
    const activeFrame = currentStep >= 0 ? steps[currentStep] : null;
    const ptrs = activeFrame ? activeFrame.pointers : null;

    for (let k = 0; k < arr.length; k++) {
      const x =
        this.arrayStartX(arr.length) + k * (layout.boxW + layout.boxGap);
      const isActive = ptrs && (k === ptrs.i || k === ptrs.j);
      const isFound = isActive && activeFrame.found;

      fill(
        isFound
          ? palette.boxFound()
          : isActive
            ? palette.boxActive()
            : palette.boxDefault(),
      );
      stroke(
        isFound
          ? palette.strokeFound()
          : isActive
            ? palette.strokeActive()
            : palette.strokeDefault(),
      );
      strokeWeight(2);
      rect(x, layout.arrayY, layout.boxW, layout.boxH, 9);

      noStroke();
      fill(
        isFound
          ? palette.numFound()
          : isActive
            ? palette.numActive()
            : palette.numDefault(),
      );
      textSize(26);
      textStyle(BOLD);
      textAlign(CENTER, CENTER);
      text(arr[k], x + layout.boxW / 2, layout.arrayY + layout.boxH / 2);

      fill(palette.indexLabel());
      textSize(11);
      textStyle(NORMAL);
      text(k, x + layout.boxW / 2, layout.arrayY + layout.boxH + 16);
    }
    textAlign(LEFT, BASELINE);
  }

  renderPointers(problem, steps, currentStep) {
    if (currentStep < 0) return;
    const frame = steps[currentStep];
    if (!frame || !frame.pointers) return;

    const { i, j } = frame.pointers;
    const arrowY = this.layout.arrayY - this.layout.arrowOffset;
    const len = problem.array.length;

    this._drawArrow(
      this.boxCenterX(i, len),
      arrowY,
      this.palette.arrowI(),
      "i",
    );
    this._drawArrow(
      this.boxCenterX(j, len),
      arrowY,
      frame.found ? this.palette.arrowFound() : this.palette.arrowJ(),
      "j",
    );
  }

  _drawArrow(x, y, col, label) {
    fill(col);
    noStroke();
    textSize(13);
    textStyle(BOLD);
    textAlign(CENTER, BOTTOM);
    text(label, x, y - 2);
    triangle(x - 7, y, x + 7, y, x, y + 12);
    textAlign(LEFT, BASELINE);
    textStyle(NORMAL);
  }

  renderStatusPanel(problem, strategy, steps, currentStep) {
    const { layout, palette } = this;
    const px = 30,
      py = layout.panelY,
      pw = 460,
      ph = layout.panelH;

    fill(palette.panelBg());
    stroke(palette.panelBorder());
    strokeWeight(1.5);
    rect(px, py, pw, ph, 10);
    noStroke();

    if (currentStep < 0) {
      fill(palette.idleText());
      textSize(15);
      text("Press Play to start.", px + 20, py + 54);
      return;
    }

    const frame = steps[currentStep];

    if (frame.done) {
      fill(palette.failText());
      textSize(15);
      textStyle(BOLD);
      text(frame.result, px + 20, py + 54);
      textStyle(NORMAL);
      return;
    }

    // Line 1 — dim prefix, coloured value (split on last '=')
    const splitAt = frame.label.lastIndexOf("=") + 1;
    const prefix = frame.label.slice(0, splitAt) + "  ";
    const value = frame.label.slice(splitAt).trim();

    fill(palette.labelText());
    textSize(13);
    text(prefix, px + 20, py + 36);
    fill(frame.found ? palette.successText() : palette.warningText());
    textStyle(BOLD);
    text(value, px + 20 + textWidth(prefix), py + 36);
    textStyle(NORMAL);

    // Line 2 — outcome
    fill(frame.found ? palette.successText() : palette.failText());
    textSize(frame.found ? 16 : 13);
    textStyle(frame.found ? BOLD : NORMAL);
    text(frame.result, px + 20, py + 72);
    textStyle(NORMAL);

    fill(palette.dimText());
    textSize(11);
    text("Step " + (currentStep + 1) + " / " + steps.length, px + 20, py + 100);
  }

  renderStepLog(strategy, steps, currentStep) {
    const { layout, palette } = this;
    const px = 506,
      py = layout.panelY,
      pw = 208,
      ph = layout.panelH;

    fill(palette.panelBg());
    stroke(palette.panelBorder());
    strokeWeight(1.5);
    rect(px, py, pw, ph, 10);
    noStroke();

    fill(palette.labelText());
    textSize(12);
    textStyle(BOLD);
    text(strategy.logHeader, px + 14, py + 26);
    textStyle(NORMAL);

    if (currentStep < 0) {
      fill(palette.dimText());
      textSize(12);
      text("none yet", px + 14, py + 50);
      return;
    }

    const maxVisible = 4;
    const firstVisible = max(0, currentStep - maxVisible + 1);

    textSize(12);
    for (let k = firstVisible; k <= currentStep; k++) {
      const frame = steps[k];
      const isLast = k === currentStep;
      if (!frame || !frame.logEntry) continue;
      fill(
        isLast
          ? frame.found
            ? palette.successText()
            : palette.activeLogText()
          : palette.dimText(),
      );
      text(frame.logEntry, px + 14, py + 46 + (k - firstVisible) * 17);
    }
  }

  renderSpeedLabel(stepDelay) {
    noStroke();
    fill(this.palette.indexLabel());
    textSize(11);
    textStyle(NORMAL);
    text("Delay: " + stepDelay + "ms / step", 524, 446);
  }
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  Visualizer  —  engine: playback state, UI controls, p5 hooks
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Visualizer {
  constructor(problem) {
    this.problem = problem;
    this.renderer = new Renderer(740);
    this.strategyIndex = 0;
    this.activeStrategy = problem.strategies[0];
    this.steps = problem.stepsFor(0);

    this.currentStep = -1;
    this.isPlaying = false;
    this.lastTick = 0;
    this.stepDelay = 900;

    this.btnPlay = null;
    this.btnReset = null;
    this.speedSlider = null;
    this.strategyMenu = null;
  }

  setup() {
    createCanvas(740, 490);
    textFont("monospace");

    this.btnPlay = createButton("Play");
    this.btnPlay.position(40, 428);
    this.btnPlay.size(110, 40);
    this._styleButton(this.btnPlay, "#00e5ff");
    this.btnPlay.mousePressed(() => this.togglePlayPause());

    this.btnReset = createButton("Reset");
    this.btnReset.position(162, 428);
    this.btnReset.size(110, 40);
    this._styleButton(this.btnReset, "#ff4081");
    this.btnReset.mousePressed(() => this.resetToIdle());

    this.speedSlider = createSlider(300, 3000, this.stepDelay, 100);
    this.speedSlider.position(290, 438);
    this.speedSlider.size(200);
    this.speedSlider.style("accent-color", "#00e5ff");

    // Strategy selector dropdown
    this.strategyMenu = createSelect();
    this.strategyMenu.position(518, 18);
    this.strategyMenu.size(210, 32);
    this._styleSelect(this.strategyMenu);
    this.problem.strategies.forEach((s, idx) => {
      this.strategyMenu.option(s.name, idx);
    });
    this.strategyMenu.changed(() => this._onStrategyChanged());
  }

  draw() {
    this.stepDelay = this.speedSlider.value();
    this.renderer.renderFrame(
      this.problem,
      this.activeStrategy,
      this.currentStep,
      this.steps,
      this.stepDelay,
    );
    this._tick();
  }

  mousePressed() {
    this._handleBoxClick();
  }

  // ── Playback ────────────────────────────────────────────────────

  togglePlayPause() {
    if (this.isPlaying) {
      this.isPlaying = false;
      this.btnPlay.html("Play");
      return;
    }
    if (this.currentStep >= this.steps.length - 1) this.currentStep = -1;
    this.isPlaying = true;
    this.lastTick = millis();
    this.btnPlay.html("Pause");
  }

  resetToIdle() {
    this.isPlaying = false;
    this.currentStep = -1;
    this.btnPlay.html("Play");
  }

  // ── Private ─────────────────────────────────────────────────────

  _onStrategyChanged() {
    this.strategyIndex = int(this.strategyMenu.value());
    this.activeStrategy = this.problem.strategies[this.strategyIndex];
    this.steps = this.problem.stepsFor(this.strategyIndex);
    this.resetToIdle();
  }

  _tick() {
    if (!this.isPlaying) return;
    if (millis() - this.lastTick < this.stepDelay) return;
    this.lastTick = millis();
    this.currentStep += 1;
    if (this.currentStep >= this.steps.length) {
      this.currentStep = this.steps.length - 1;
      this.isPlaying = false;
      this.btnPlay.html("Play");
    }
  }

  _handleBoxClick() {
    const { layout } = this.renderer;
    const arr = this.problem.array;
    const startX = this.renderer.arrayStartX(arr.length);

    for (let k = 0; k < arr.length; k++) {
      const bx = startX + k * (layout.boxW + layout.boxGap);
      if (
        mouseX > bx &&
        mouseX < bx + layout.boxW &&
        mouseY > layout.arrayY &&
        mouseY < layout.arrayY + layout.boxH
      ) {
        for (let s = 0; s < this.steps.length; s++) {
          const ptrs = this.steps[s].pointers;
          if (ptrs && (ptrs.i === k || ptrs.j === k)) {
            this.currentStep = s;
            this.isPlaying = false;
            this.btnPlay.html("Play");
            break;
          }
        }
      }
    }
  }

  _styleButton(btn, bgColor) {
    btn.style("background", bgColor);
    btn.style("color", "#0a0a1a");
    btn.style("border", "none");
    btn.style("border-radius", "8px");
    btn.style("font-size", "15px");
    btn.style("font-weight", "700");
    btn.style("cursor", "pointer");
    btn.style("font-family", "monospace");
  }

  _styleSelect(sel) {
    sel.style("background", "#1a1e40");
    sel.style("color", "#a0b4e0");
    sel.style("border", "1.5px solid #303870");
    sel.style("border-radius", "8px");
    sel.style("font-size", "14px");
    sel.style("font-family", "monospace");
    sel.style("font-weight", "600");
    sel.style("padding", "0 10px");
    sel.style("cursor", "pointer");
    sel.style("outline", "none");
  }
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
//  p5.js entry points
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

// viz is declared with let here so that the function declarations below
// (which are hoisted) can safely reference it at call time.
// Using const would cause a temporal dead zone error because p5 calls
// setup() before the const initializer runs in some environments.
let viz;

function setup() {
  viz = new Visualizer(ACTIVE_PROBLEM);
  viz.setup();
}
function draw() {
  viz.draw();
}
function mousePressed() {
  viz.mousePressed();
}
