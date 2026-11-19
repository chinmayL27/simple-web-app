const itemContainer = document.querySelector("#items");
const itemCount = document.querySelector("#item-count");
const listCount = document.querySelector("#list-count");
const form = document.querySelector("#item-form");
const message = document.querySelector("#form-message");

function renderItems(items) {
  itemCount.textContent = items.length;
  listCount.textContent = `${items.length} ${items.length === 1 ? "item" : "items"}`;

  if (items.length === 0) {
    itemContainer.innerHTML = `
      <div class="empty-state">
        <span class="empty-icon" aria-hidden="true">▤</span>
        <strong>Your inventory is ready</strong>
        <p>Add your first asset using the form.</p>
      </div>`;
    return;
  }

  itemContainer.replaceChildren(...items.map((item) => {
    const row = document.createElement("article");
    row.className = "item-row";
    const icon = document.createElement("span");
    icon.className = "item-icon";
    icon.setAttribute("aria-hidden", "true");
    icon.textContent = "▤";
    const copy = document.createElement("div");
    copy.className = "item-copy";
    const name = document.createElement("strong");
    name.textContent = item.name;
    const description = document.createElement("p");
    description.textContent = item.description || "No description provided";
    const id = document.createElement("span");
    id.className = "item-id";
    id.textContent = `ID ${item.id}`;
    copy.append(name, description);
    row.append(icon, copy, id);
    return row;
  }));
}

async function loadItems() {
  const response = await fetch("/items");
  if (!response.ok) throw new Error("Could not load inventory.");
  renderItems(await response.json());
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = form.querySelector("button");
  button.disabled = true;
  message.textContent = "";
  message.className = "form-message";

  try {
    const formData = new FormData(form);
    const response = await fetch("/items", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: formData.get("name").trim(),
        description: formData.get("description").trim(),
      }),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail?.[0]?.msg || result.detail || "Could not save asset.");
    form.reset();
    message.textContent = "Asset added to inventory.";
    message.classList.add("success");
    await loadItems();
  } catch (error) {
    message.textContent = error.message || "Something went wrong. Please retry.";
  } finally {
    button.disabled = false;
  }
});

loadItems().catch((error) => {
  itemContainer.textContent = error.message;
  itemCount.textContent = "—";
  listCount.textContent = "Unavailable";
});
