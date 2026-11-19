const recordContainer = document.querySelector("#records");
const recordCount = document.querySelector("#record-count");
const listCount = document.querySelector("#list-count");
const form = document.querySelector("#record-form");
const message = document.querySelector("#form-message");

function renderRecords(records) {
  recordCount.textContent = records.length;
  listCount.textContent = `${records.length} ${records.length === 1 ? "record" : "records"}`;

  if (records.length === 0) {
    recordContainer.innerHTML = `
      <div class="empty-state">
        <span class="empty-icon" aria-hidden="true">▤</span>
        <strong>Your database is ready</strong>
        <p>Add your first record using the form.</p>
      </div>`;
    return;
  }

  recordContainer.replaceChildren(...records.map((record) => {
    const row = document.createElement("article");
    row.className = "record-row";
    const icon = document.createElement("span");
    icon.className = "record-icon";
    icon.setAttribute("aria-hidden", "true");
    icon.textContent = "▤";
    const copy = document.createElement("div");
    copy.className = "record-copy";
    const name = document.createElement("strong");
    name.textContent = record.name;
    const description = document.createElement("p");
    description.textContent = record.description || "No description provided";
    const id = document.createElement("span");
    id.className = "record-id";
    id.textContent = `ID ${record.id}`;
    copy.append(name, description);
    row.append(icon, copy, id);
    return row;
  }));
}

async function loadRecords() {
  const response = await fetch("/records");
  if (!response.ok) throw new Error("Could not load records.");
  renderRecords(await response.json());
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = form.querySelector("button");
  button.disabled = true;
  message.textContent = "";
  message.className = "form-message";

  try {
    const formData = new FormData(form);
    const response = await fetch("/records", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: formData.get("name").trim(),
        description: formData.get("description").trim(),
      }),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail?.[0]?.msg || result.detail || "Could not save record.");
    form.reset();
    message.textContent = "Asset added to records.";
    message.classList.add("success");
    await loadRecords();
  } catch (error) {
    message.textContent = error.message || "Something went wrong. Please retry.";
  } finally {
    button.disabled = false;
  }
});

loadRecords().catch((error) => {
  recordContainer.textContent = error.message;
  recordCount.textContent = "—";
  listCount.textContent = "Unavailable";
});
