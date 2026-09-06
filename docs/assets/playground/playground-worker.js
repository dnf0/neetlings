/**
 * Pyodide Web Worker Background Engine
 * This worker runs user code in an isolated Pyodide environment.
 */

// Import Pyodide script from CDN
importScripts("https://cdn.jsdelivr.net/pyodide/v0.26.2/full/pyodide.js");

let pyodideReadyPromise = null;
let pyodideInstance = null;

/**
 * Initialize Pyodide, mount the library files, and prepare the evaluate_code function.
 * @param {object} bundle - The playground bundle containing the virtual runtime modules.
 */
async function initPyodide(bundle) {
    self.postMessage({ type: "STATUS", status: "loading" });

    // Load Pyodide environment
    pyodideInstance = await loadPyodide({
        indexURL: "https://cdn.jsdelivr.net/pyodide/v0.26.2/full/"
    });

    self.postMessage({ type: "STATUS", status: "mounting" });

    // Create virtual library directories in Pyodide FS
    pyodideInstance.FS.mkdirTree("/lib/neetlings");
    pyodideInstance.FS.writeFile("/lib/neetlings/__init__.py", "");

    // Populate library files from bundle's runtime modules
    if (bundle && bundle.runtime_modules) {
        for (const [filename, code] of Object.entries(bundle.runtime_modules)) {
            pyodideInstance.FS.writeFile("/lib/neetlings/" + filename, code);
        }
    }

    // Initialize Python bridge and import the core test runner
    await pyodideInstance.runPythonAsync(`
import sys
if "/lib" not in sys.path:
    sys.path.insert(0, "/lib")
from neetlings.test_runner import evaluate_code
`);

    self.postMessage({ type: "STATUS", status: "ready" });
    return pyodideInstance;
}

// Global onmessage handler
self.onmessage = async function (e) {
    const msg = e.data;
    if (!msg) return;

    if (msg.type === "INIT") {
        try {
            pyodideReadyPromise = initPyodide(msg.bundle);
            await pyodideReadyPromise;
        } catch (err) {
            self.postMessage({
                type: "STATUS",
                status: "error",
                error: err.message || String(err)
            });
        }
    } else if (msg.type === "RUN") {
        try {
            if (!pyodideReadyPromise) {
                throw new Error("Pyodide has not been initialized. Please send an INIT message first.");
            }
            const pyodide = await pyodideReadyPromise;

            // Prepare inputs and arguments using Pyodide's toPy to avoid PyProxy limitations
            const pyTestCases = (msg.testCases && msg.testCases.length > 0) ? pyodide.toPy(msg.testCases) : null;
            const pyBannedCalls = (msg.bannedCalls && msg.bannedCalls.length > 0) ? pyodide.toPy(msg.bannedCalls) : null;
            const pyBannedOps = (msg.bannedOps && msg.bannedOps.length > 0) ? pyodide.toPy(msg.bannedOps) : null;
            const evaluate_code_fn = pyodide.globals.get("evaluate_code");

            // Execute the code
            const resultProxy = evaluate_code_fn(
                msg.code,
                pyTestCases,
                msg.methodName,
                pyBannedCalls,
                pyBannedOps,
                msg.solutionCode || null
            );

            // Convert Python dictionary result back to native JS object
            const result = resultProxy.toJs({ dict_converter: Object.fromEntries });

            // Clean up Pyodide proxies to avoid memory leaks
            if (pyTestCases && typeof pyTestCases.destroy === "function") {
                pyTestCases.destroy();
            }
            if (pyBannedCalls && typeof pyBannedCalls.destroy === "function") {
                pyBannedCalls.destroy();
            }
            if (pyBannedOps && typeof pyBannedOps.destroy === "function") {
                pyBannedOps.destroy();
            }
            resultProxy.destroy();

            // Post result back to main thread
            self.postMessage({
                type: "RUN_RESULT",
                exerciseId: msg.exerciseId,
                ...result
            });
        } catch (err) {
            self.postMessage({
                type: "RUN_RESULT",
                exerciseId: msg.exerciseId,
                status: "ERROR",
                passedCount: 0,
                totalCount: msg.testCases ? msg.testCases.length : 0,
                durationMs: 0.0,
                stdout: "",
                error: err.message || String(err),
                cases: [],
                diagnosticDiff: null
            });
        }
    }
};
