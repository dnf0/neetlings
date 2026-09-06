/**
 * Neetlings WebAssembly Playground UI Controller & State Engine
 *
 * 100% Client-Side NeetCode 150 learning platform powered by Pyodide v0.26 WebAssembly.
 * Features Monaco Editor, 3-pane responsive layout, progressive hint ladder,
 * side-by-side solution diffs, and local storage state persistence.
 */

(function () {
  "use strict";

  const STORAGE_KEY = "neetlings_learning_state_v1";

  /**
   * ==========================================================================
   * NeetlingsStorage: Client-Side Progress & Code Persistence
   * ==========================================================================
   */
  const NeetlingsStorage = {
    state: null,

    init(bundle) {
      let saved = null;
      try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (raw) saved = JSON.parse(raw);
      } catch (e) {
        console.warn("Failed to read Neetlings state from localStorage:", e);
      }

      const totalExercises = bundle && bundle.exercises ? Object.keys(bundle.exercises).length : 18;

      if (!saved || saved.version !== 1 || !saved.exercises) {
        saved = {
          version: 1,
          lastActiveExerciseId: "01_contains_duplicate",
          exercises: {},
          stats: {
            completedCount: 0,
            totalCount: totalExercises,
          },
        };
      }

      if (bundle && bundle.exercises) {
        for (const [id, ex] of Object.entries(bundle.exercises)) {
          if (!saved.exercises[id]) {
            saved.exercises[id] = {
              status: "unsolved",
              userCode: ex.code || "",
              hintsRevealed: 0,
            };
          }
        }
      }

      this.state = saved;
      this.recalculateStats(bundle);
      this.persist();
      return this.state;
    },

    recalculateStats(bundle) {
      if (!this.state || !this.state.exercises) return;
      let completed = 0;
      const total = bundle && bundle.exercises ? Object.keys(bundle.exercises).length : Object.keys(this.state.exercises).length;
      for (const exState of Object.values(this.state.exercises)) {
        if (exState.status === "solved") completed++;
      }
      this.state.stats = {
        completedCount: completed,
        totalCount: total,
      };
    },

    persist() {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(this.state));
      } catch (e) {
        console.warn("Failed to persist Neetlings state:", e);
      }
    },

    getExerciseState(exerciseId) {
      return this.state?.exercises?.[exerciseId] || null;
    },

    saveUserCode(exerciseId, code) {
      if (!this.state.exercises[exerciseId]) {
        this.state.exercises[exerciseId] = { status: "unsolved", userCode: code, hintsRevealed: 0 };
      } else {
        this.state.exercises[exerciseId].userCode = code;
      }
      this.persist();
    },

    markSolved(exerciseId, bundle) {
      if (!this.state.exercises[exerciseId]) {
        this.state.exercises[exerciseId] = { status: "solved", userCode: "", hintsRevealed: 0 };
      } else {
        this.state.exercises[exerciseId].status = "solved";
      }
      this.recalculateStats(bundle);
      this.persist();
    },

    revealHint(exerciseId, hintIndex) {
      const ex = this.state.exercises[exerciseId];
      if (ex && ex.hintsRevealed < hintIndex) {
        ex.hintsRevealed = hintIndex;
        this.persist();
      }
    },

    exportJSON() {
      return JSON.stringify(this.state, null, 2);
    },

    importJSON(jsonStr, bundle) {
      try {
        const parsed = JSON.parse(jsonStr);
        if (parsed && parsed.version === 1 && parsed.exercises) {
          this.state = parsed;
          this.recalculateStats(bundle);
          this.persist();
          return true;
        }
      } catch (e) {
        console.error("Invalid state JSON:", e);
      }
      return false;
    },
  };

  /**
   * ==========================================================================
   * NeetlingsApp Controller
   * ==========================================================================
   */
  const NeetlingsApp = {
    bundle: null,
    worker: null,
    editor: null,
    diffEditor: null,
    isDiffMode: false,
    activeExerciseId: null,

    async init() {
      this.initTheme();

      // 1. Fetch Bundle
      try {
        const resp = await fetch("../assets/playground/playground-bundle.json");
        this.bundle = await resp.json();
      } catch (e) {
        console.error("Failed to load playground bundle:", e);
        this.renderError("Failed to load exercises bundle. Please check your network or local build.");
        return;
      }

      // 2. Init Storage
      NeetlingsStorage.init(this.bundle);

      // 3. Init Worker
      this.initWorker();

      // 4. Init Monaco Editor
      this.initMonaco(() => {
        this.setupUI();
        const initialId = this.bundle.exercises[NeetlingsStorage.state.lastActiveExerciseId]
          ? NeetlingsStorage.state.lastActiveExerciseId
          : Object.keys(this.bundle.exercises)[0];
        this.selectExercise(initialId);
      });
    },

    initTheme() {
      const savedTheme = localStorage.getItem("neetlings-theme") || "dark";
      document.documentElement.setAttribute("data-theme", savedTheme);

      const themeBtn = document.getElementById("theme-toggle-btn");
      if (themeBtn) {
        themeBtn.addEventListener("click", () => {
          const current = document.documentElement.getAttribute("data-theme");
          const next = current === "dark" ? "light" : "dark";
          document.documentElement.setAttribute("data-theme", next);
          localStorage.setItem("neetlings-theme", next);
          if (window.monaco) {
            window.monaco.editor.setTheme(next === "dark" ? "vs-dark" : "vs");
          }
        });
      }
    },

    initWorker() {
      this.updateStatusBadge("INITIALIZING", "running");
      this.worker = new Worker("../assets/playground/playground-worker.js");

      this.worker.onmessage = (e) => {
        const msg = e.data;
        if (!msg) return;

        if (msg.type === "STATUS") {
          if (msg.stage === "ready") {
            this.updateStatusBadge("READY", "ready");
            this.logOutput("⚡ Python 3.12 WebAssembly environment loaded and ready.");
          } else {
            this.logOutput(`[Worker] ${msg.message}`);
          }
        } else if (msg.type === "RUN_RESULT") {
          this.handleRunResult(msg);
        }
      };

      this.worker.postMessage({
        type: "INIT",
        bundle: this.bundle,
      });
    },

    initMonaco(callback) {
      if (window.require) {
        window.require.config({
          paths: { vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs" },
        });

        window.require(["vs/editor/editor.main"], () => {
          const isDark = document.documentElement.getAttribute("data-theme") !== "light";
          const editorElem = document.getElementById("monaco-editor-container");
          const diffElem = document.getElementById("monaco-diff-container");

          this.editor = window.monaco.editor.create(editorElem, {
            value: "",
            language: "python",
            theme: isDark ? "vs-dark" : "vs",
            fontSize: 13,
            lineNumbers: "on",
            minimap: { enabled: false },
            automaticLayout: true,
            tabSize: 4,
            scrollBeyondLastLine: false,
          });

          this.diffEditor = window.monaco.editor.createDiffEditor(diffElem, {
            theme: isDark ? "vs-dark" : "vs",
            fontSize: 13,
            automaticLayout: true,
            readOnly: true,
          });

          // Ctrl+Enter to Run
          this.editor.addCommand(
            window.monaco.KeyMod.CtrlCmd | window.monaco.KeyCode.Enter,
            () => this.runCode()
          );

          // Auto-save user edits
          this.editor.onDidChangeModelContent(() => {
            if (this.activeExerciseId && !this.isDiffMode) {
              NeetlingsStorage.saveUserCode(this.activeExerciseId, this.editor.getValue());
            }
          });

          if (callback) callback();
        });
      }
    },

    setupUI() {
      const catSelect = document.getElementById("category-select");
      const exSelect = document.getElementById("exercise-select");
      const runBtn = document.getElementById("btn-run");
      const resetBtn = document.getElementById("btn-reset");
      const diffBtn = document.getElementById("btn-diff");
      const exportBtn = document.getElementById("btn-export");
      const importBtn = document.getElementById("btn-import");

      // Populate Categories
      catSelect.innerHTML = "";
      for (const ch of this.bundle.chapters) {
        const opt = document.createElement("option");
        opt.value = ch.id;
        opt.textContent = `${ch.number}. ${ch.title}`;
        catSelect.appendChild(opt);
      }

      catSelect.addEventListener("change", () => {
        const chId = catSelect.value;
        const ch = this.bundle.chapters.find((c) => c.id === chId);
        if (ch && ch.exerciseIds.length > 0) {
          this.populateExercises(ch.exerciseIds);
          this.selectExercise(ch.exerciseIds[0]);
        }
      });

      exSelect.addEventListener("change", () => {
        this.selectExercise(exSelect.value);
      });

      if (runBtn) runBtn.addEventListener("click", () => this.runCode());

      if (resetBtn) {
        resetBtn.addEventListener("click", () => {
          if (!this.activeExerciseId) return;
          const ex = this.bundle.exercises[this.activeExerciseId];
          if (ex && confirm("Reset your code to starter template?")) {
            this.editor.setValue(ex.code || "");
            NeetlingsStorage.saveUserCode(this.activeExerciseId, ex.code || "");
          }
        });
      }

      if (diffBtn) {
        diffBtn.addEventListener("click", () => this.toggleSolutionDiff());
      }

      if (exportBtn) {
        exportBtn.addEventListener("click", () => {
          const json = NeetlingsStorage.exportJSON();
          const blob = new Blob([json], { type: "application/json" });
          const url = URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = `neetlings-progress-${new Date().toISOString().slice(0, 10)}.json`;
          a.click();
          URL.revokeObjectURL(url);
        });
      }

      if (importBtn) {
        importBtn.addEventListener("click", () => {
          const input = document.createElement("input");
          input.type = "file";
          input.accept = ".json";
          input.onchange = (e) => {
            const file = e.target.files[0];
            if (file) {
              const reader = new FileReader();
              reader.onload = (evt) => {
                if (NeetlingsStorage.importJSON(evt.target.result, this.bundle)) {
                  alert("Progress imported successfully!");
                  this.updateProgressBadge();
                  this.selectExercise(this.activeExerciseId);
                } else {
                  alert("Failed to import: invalid JSON structure.");
                }
              };
              reader.readAsText(file);
            }
          };
          input.click();
        });
      }
    },

    populateExercises(exerciseIds) {
      const exSelect = document.getElementById("exercise-select");
      exSelect.innerHTML = "";
      for (const id of exerciseIds) {
        const ex = this.bundle.exercises[id];
        const exState = NeetlingsStorage.getExerciseState(id);
        const opt = document.createElement("option");
        opt.value = id;
        const icon = exState && exState.status === "solved" ? "✓ " : "• ";
        opt.textContent = `${icon}${ex ? ex.title : id}`;
        exSelect.appendChild(opt);
      }
    },

    selectExercise(exerciseId) {
      if (!this.bundle.exercises[exerciseId]) return;
      this.activeExerciseId = exerciseId;
      NeetlingsStorage.state.lastActiveExerciseId = exerciseId;
      NeetlingsStorage.persist();

      const ex = this.bundle.exercises[exerciseId];
      const exState = NeetlingsStorage.getExerciseState(exerciseId);

      // Synchronize category dropdown
      const catSelect = document.getElementById("category-select");
      if (catSelect.value !== ex.categoryId) {
        catSelect.value = ex.categoryId;
        const ch = this.bundle.chapters.find((c) => c.id === ex.categoryId);
        if (ch) this.populateExercises(ch.exerciseIds);
      }

      const exSelect = document.getElementById("exercise-select");
      exSelect.value = exerciseId;

      // Update Editor
      const codeToLoad = exState?.userCode || ex.code || "";
      if (this.editor) {
        this.editor.setValue(codeToLoad);
      }

      if (this.isDiffMode) {
        this.toggleSolutionDiff(false);
      }

      // Render Description & Hints
      this.renderProblemPane(ex, exState);
      this.updateProgressBadge();
      this.updateStatusBadge("READY", "ready");
      this.clearDiagnostics();
    },

    renderProblemPane(ex, exState) {
      const titleElem = document.getElementById("problem-title");
      const categoryTag = document.getElementById("problem-category-tag");
      const statusPill = document.getElementById("problem-status-pill");
      const bodyElem = document.getElementById("problem-body");
      const hintLadderElem = document.getElementById("hint-ladder");

      titleElem.textContent = ex.title;
      const ch = this.bundle.chapters.find((c) => c.id === ex.categoryId);
      categoryTag.textContent = ch ? ch.title : ex.categoryId;

      const isSolved = exState && exState.status === "solved";
      statusPill.textContent = isSolved ? "Solved ✓" : "Unsolved";
      statusPill.className = `status-pill-small ${isSolved ? "solved" : "unsolved"}`;

      // Extract docstring from code
      const docstring = this.extractDocstring(ex.code);
      bodyElem.innerHTML = `<pre>${this.escapeHTML(docstring)}</pre>`;

      // Render Hint Ladder from bundle hints or solution
      const hints = ex.hints && ex.hints.length > 0 ? ex.hints : this.extractHints(ex.solution || ex.code);
      hintLadderElem.innerHTML = "";
      if (hints.length === 0) {
        hintLadderElem.innerHTML = "<p style='color: var(--text-muted); font-size: 12px;'>No hints available for this exercise.</p>";
        return;
      }

      const revealedCount = exState ? exState.hintsRevealed : 0;

      hints.forEach((hintText, idx) => {
        const tier = idx + 1;
        const isRevealed = tier <= revealedCount;

        const hintItem = document.createElement("div");
        hintItem.className = "hint-item";

        const hintHeader = document.createElement("div");
        hintHeader.className = "hint-header";
        hintHeader.innerHTML = `
          <span>Tier ${tier}: Hint</span>
          <button class="hint-lock-btn">${isRevealed ? "Revealed" : "Reveal Hint"}</button>
        `;

        const hintContent = document.createElement("div");
        hintContent.className = `hint-content ${isRevealed ? "revealed" : ""}`;
        hintContent.textContent = hintText;

        hintHeader.addEventListener("click", () => {
          if (!hintContent.classList.contains("revealed")) {
            hintContent.classList.add("revealed");
            hintHeader.querySelector(".hint-lock-btn").textContent = "Revealed";
            NeetlingsStorage.revealHint(ex.id, tier);
          } else {
            hintContent.classList.toggle("revealed");
          }
        });

        hintItem.appendChild(hintHeader);
        hintItem.appendChild(hintContent);
        hintLadderElem.appendChild(hintItem);
      });
    },

    extractDocstring(code) {
      if (!code) return "";
      const match = code.match(/"""([\s\S]*?)"""/);
      return match ? match[1].trim() : "No problem description docstring provided.";
    },

    extractHints(code) {
      if (!code) return [];
      const match = code.match(/HINTS\s*=\s*\[([\s\S]*?)\]\n/);
      if (!match) return [];
      const raw = match[1];
      const items = [];
      const regex = /"([^"\\]*(?:\\.[^"\\]*)*)"|'([^'\\]*(?:\\.[^'\\]*)*)'/g;
      let m;
      while ((m = regex.exec(raw)) !== null) {
        items.push(m[1] || m[2]);
      }
      return items;
    },

    runCode() {
      if (!this.worker || !this.activeExerciseId) return;
      const userCode = this.editor.getValue();
      const ex = this.bundle.exercises[this.activeExerciseId];

      this.updateStatusBadge("RUNNING...", "running");
      this.clearDiagnostics();

      // Extract method name from starter code
      const methodMatch = ex.code.match(/def\s+([a-zA-Z0-9_]+)\s*\(/);
      const methodName = methodMatch ? methodMatch[1] : "solution";

      this.worker.postMessage({
        type: "RUN",
        exerciseId: this.activeExerciseId,
        code: userCode,
        solutionCode: ex.solution || ex.code,
        methodName: methodName,
        bannedCalls: ex.bannedCalls || [],
        bannedOps: ex.bannedOps || [],
      });
    },

    handleRunResult(result) {
      const isPassed = result.status === "PASSED";
      this.updateStatusBadge(result.status, isPassed ? "passed" : "failed");

      const diagBody = document.getElementById("diagnostics-body");
      diagBody.innerHTML = "";

      // 1. Summary Card
      const summaryCard = document.createElement("div");
      summaryCard.className = "test-summary-card";
      summaryCard.innerHTML = `
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
          <strong>Status:</strong>
          <span style="color: ${isPassed ? "var(--success-color)" : "var(--error-color)"}; font-weight: 700;">
            ${result.status}
          </span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
          <span>Execution Time:</span>
          <span>${result.durationMs || 0} ms</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
          <span>Passed Test Cases:</span>
          <span>${result.passedCount || 0} / ${result.totalCount || 0}</span>
        </div>
      `;
      diagBody.appendChild(summaryCard);

      // 2. Error message
      if (result.error) {
        const errBox = document.createElement("div");
        errBox.className = "test-case-item failed";
        errBox.innerHTML = `<strong>Error:</strong><pre style="margin: 4px 0 0; color: var(--error-color);">${this.escapeHTML(result.error)}</pre>`;
        diagBody.appendChild(errBox);
      }

      // 3. Test Cases List
      if (result.cases && result.cases.length > 0) {
        result.cases.forEach((c) => {
          const item = document.createElement("div");
          item.className = `test-case-item ${c.status === "PASSED" ? "passed" : "failed"}`;
          item.innerHTML = `
            <div style="display: flex; justify-content: space-between;">
              <strong>${this.escapeHTML(c.name)}</strong>
              <span>${c.durationMs || 0} ms</span>
            </div>
            ${c.expected ? `<div>Expected: <code>${this.escapeHTML(c.expected)}</code></div>` : ""}
            ${c.actual ? `<div>Actual: <code>${this.escapeHTML(c.actual)}</code></div>` : ""}
          `;
          diagBody.appendChild(item);
        });
      }

      // 4. Diagnostic Diff Visualizer
      if (result.diagnosticDiff) {
        const diffTitle = document.createElement("div");
        diffTitle.style.marginTop = "10px";
        diffTitle.style.fontWeight = "700";
        diffTitle.textContent = "🔍 Data Structure Visualizer Diff:";
        diagBody.appendChild(diffTitle);

        const diffBox = document.createElement("div");
        diffBox.className = "diff-visualizer-box";
        diffBox.textContent = result.diagnosticDiff;
        diagBody.appendChild(diffBox);
      }

      // 5. Stdout Box
      if (result.stdout && result.stdout.trim()) {
        const stdoutTitle = document.createElement("div");
        stdoutTitle.style.marginTop = "10px";
        stdoutTitle.style.fontWeight = "700";
        stdoutTitle.textContent = "Standard Output (stdout):";
        diagBody.appendChild(stdoutTitle);

        const outBox = document.createElement("div");
        outBox.className = "stdout-box";
        outBox.textContent = result.stdout;
        diagBody.appendChild(outBox);
      }

      if (isPassed && this.activeExerciseId) {
        NeetlingsStorage.markSolved(this.activeExerciseId, this.bundle);
        this.updateProgressBadge();
        const statusPill = document.getElementById("problem-status-pill");
        if (statusPill) {
          statusPill.textContent = "Solved ✓";
          statusPill.className = "status-pill-small solved";
        }
      }
    },

    toggleSolutionDiff(forceState) {
      this.isDiffMode = typeof forceState === "boolean" ? forceState : !this.isDiffMode;
      const editorContainer = document.getElementById("monaco-editor-container");
      const diffContainer = document.getElementById("monaco-diff-container");
      const diffBtn = document.getElementById("btn-diff");

      if (this.isDiffMode) {
        const ex = this.bundle.exercises[this.activeExerciseId];
        const userCode = this.editor.getValue();
        const solCode = ex ? ex.solution || "# Solution not available" : "";

        const originalModel = window.monaco.editor.createModel(solCode, "python");
        const modifiedModel = window.monaco.editor.createModel(userCode, "python");
        this.diffEditor.setModel({ original: originalModel, modified: modifiedModel });

        editorContainer.style.display = "none";
        diffContainer.style.display = "block";
        if (diffBtn) diffBtn.textContent = "Close Diff";
      } else {
        editorContainer.style.display = "block";
        diffContainer.style.display = "none";
        if (diffBtn) diffBtn.textContent = "Solution Diff";
      }
    },

    updateStatusBadge(text, type) {
      const badge = document.getElementById("diagnostics-status-badge");
      if (badge) {
        badge.textContent = text;
        badge.className = `result-badge ${type}`;
      }
    },

    updateProgressBadge() {
      const badge = document.getElementById("progress-badge");
      if (badge && NeetlingsStorage.state) {
        const { completedCount, totalCount } = NeetlingsStorage.state.stats;
        badge.textContent = `${completedCount} / ${totalCount} Solved`;
      }
    },

    clearDiagnostics() {
      const diagBody = document.getElementById("diagnostics-body");
      if (diagBody) diagBody.innerHTML = "<p style='color: var(--text-muted);'>Run code (Ctrl+Enter) to execute against test suite.</p>";
    },

    logOutput(str) {
      const diagBody = document.getElementById("diagnostics-body");
      if (diagBody) {
        const line = document.createElement("div");
        line.style.color = "var(--text-muted)";
        line.style.marginBottom = "4px";
        line.textContent = str;
        diagBody.appendChild(line);
      }
    },

    escapeHTML(str) {
      if (!str) return "";
      return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
    },
  };

  window.NeetlingsApp = NeetlingsApp;
  window.NeetlingsStorage = NeetlingsStorage;

  document.addEventListener("DOMContentLoaded", () => {
    NeetlingsApp.init();
  });
})();
