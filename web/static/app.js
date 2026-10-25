/**
 * Client-side game flow: pick action → pick source bucket → (pour) pick destination.
 * State is sent with each POST /api/move so the server stays stateless.
 */

const config = window.WATER_BUCKET_CONFIG;

let state = {
  water: Object.fromEntries(config.bucketIds.map((id) => [id, 0])),
  steps: 0,
};

let selectedAction = "fill";
let pourSource = null;
let won = false;

const stepEl = document.getElementById("step-count");
const hintEl = document.getElementById("hint-text");
const errorEl = document.getElementById("error-text");
const winBanner = document.getElementById("win-banner");
const bucketsRoot = document.getElementById("buckets");

function setError(message) {
  if (!message) {
    errorEl.hidden = true;
    errorEl.textContent = "";
    return;
  }
  errorEl.hidden = false;
  errorEl.textContent = message;
}

function updateHint() {
  if (won) {
    hintEl.textContent = "";
    return;
  }
  if (selectedAction === "pour" && pourSource) {
    hintEl.textContent = `Pouring from ${pourSource} L — choose a destination bucket.`;
    return;
  }
  const verb =
    selectedAction === "fill"
      ? "Fill"
      : selectedAction === "empty"
        ? "Empty"
        : "Pour from";
  hintEl.textContent = `${verb} — click a bucket.`;
}

function render() {
  stepEl.textContent = String(state.steps);
  for (const id of config.bucketIds) {
    const liters = state.water[id] ?? 0;
    const cap = config.capacities[id];
    const fill = document.querySelector(`[data-water="${id}"]`);
    const label = document.querySelector(`[data-liters="${id}"]`);
    if (fill) {
      fill.style.height = `${(liters / cap) * 100}%`;
    }
    if (label) {
      label.textContent = String(liters);
    }
  }
  winBanner.hidden = !won;
  bucketsRoot.querySelectorAll(".bucket").forEach((btn) => {
    btn.disabled = won;
    btn.classList.toggle("is-source", pourSource === btn.dataset.bucket);
  });
  updateHint();
}

async function postJson(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (!res.ok) {
    const detail = data.detail;
    const message =
      typeof detail === "string"
        ? detail
        : Array.isArray(detail)
          ? detail.map((d) => d.msg).join(" ")
          : "Request failed.";
    throw new Error(message);
  }
  return data;
}

async function applyMove(action, source, dest) {
  setError(null);
  const payload = {
    state: { water: state.water, steps: state.steps },
    action,
    source,
  };
  if (dest) payload.dest = dest;

  const data = await postJson("/api/move", payload);
  state.water = data.water;
  state.steps = data.steps;
  won = data.won;
  pourSource = null;
  render();
}

async function resetGame() {
  setError(null);
  const data = await postJson("/api/reset", {});
  state.water = data.water;
  state.steps = data.steps;
  won = data.won;
  pourSource = null;
  selectedAction = "fill";
  document.querySelectorAll(".btn-action").forEach((btn) => {
    btn.classList.toggle("is-active", btn.dataset.action === "fill");
  });
  render();
}

document.querySelectorAll(".btn-action").forEach((btn) => {
  btn.addEventListener("click", () => {
    if (won) return;
    selectedAction = btn.dataset.action;
    pourSource = null;
    document.querySelectorAll(".btn-action").forEach((b) => {
      b.classList.toggle("is-active", b === btn);
    });
    updateHint();
    setError(null);
  });
});

bucketsRoot.addEventListener("click", async (event) => {
  const btn = event.target.closest(".bucket");
  if (!btn || won) return;
  const bucketId = btn.dataset.bucket;

  try {
    if (selectedAction === "pour") {
      if (!pourSource) {
        pourSource = bucketId;
        updateHint();
        return;
      }
      if (pourSource === bucketId) {
        setError("Choose a different bucket to pour into.");
        return;
      }
      await applyMove("pour", pourSource, bucketId);
      return;
    }
    await applyMove(selectedAction, bucketId);
  } catch (err) {
    setError(err.message);
  }
});

document.getElementById("btn-reset").addEventListener("click", () => {
  void resetGame();
});
document.getElementById("btn-play-again").addEventListener("click", () => {
  void resetGame();
});

render();
