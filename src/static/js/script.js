const API = "/tasks";

const taskList  = document.getElementById("task-list");
const emptyMsg  = document.getElementById("empty-msg");
const errorMsg  = document.getElementById("error-msg");
const addForm   = document.getElementById("add-form");
const newTitle  = document.getElementById("new-title");

function showError(msg) {
  errorMsg.textContent = msg;
  errorMsg.classList.remove("hidden");
  setTimeout(() => errorMsg.classList.add("hidden"), 4000);
}

function renderTasks(tasks) {
  taskList.innerHTML = "";
  // Filter for top-level tasks (parent_id is "None")
  const topLevelTasks = tasks.filter(task => !task.parent_id || task.parent_id === "None");
  emptyMsg.classList.toggle("hidden", topLevelTasks.length > 0);

  topLevelTasks.forEach(task => {
    const li = document.createElement("li");
    // Backend uses is_complete
    const isComplete = task.is_complete || task.completed;
    li.className = "task-item" + (isComplete ? " completed" : "");
    li.dataset.id = task._id;

    li.innerHTML = `
      <label class="checkbox-label">
        <input type="checkbox" class="toggle-cb" ${isComplete ? "checked" : ""} />
        <span class="title-text">${escapeHtml(task.title)}</span>
      </label>
      <div class="actions">
        <button class="btn-subtasks" title="Subtasks">&#10148;</button>
        <button class="btn-edit" title="Edit">&#9998;</button>
        <button class="btn-delete" title="Delete">&#10005;</button>
      </div>
    `;

    // Toggle completed - backend expects is_complete and PATCH
    li.querySelector(".toggle-cb").addEventListener("change", () => toggleTask(task._id, !isComplete));

    // Delete
    li.querySelector(".btn-delete").addEventListener("click", () => deleteTask(task._id));

    // Edit
    li.querySelector(".btn-edit").onclick = () => startEdit(li, task, task._id);

    // Subtasks
    li.querySelector(".btn-subtasks").onclick = () => {
      window.location.href = `/tasks/${task._id}/subtasks_page`;
    };

    taskList.appendChild(li);
  });
}

function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[c]));
}

async function loadTasks() {
  try {
    const res  = await fetch(API);
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to load tasks");
    // Backend returns tasks in data.tasks or data.data depending on version
    renderTasks(data.tasks || data.data || []);
  } catch (e) {
    showError(e.message);
  }
}

async function createTask(title) {
  const res  = await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Failed to create task");
  return data.task || data.data;
}

async function toggleTask(id, is_complete) {
  const res  = await fetch(`${API}/${id}`, {
    method: "PATCH", // Backend uses PATCH
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ is_complete }), // Backend uses is_complete
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Failed to update task");
  loadTasks();
}

async function deleteTask(id) {
  const res  = await fetch(`${API}/${id}`, { method: "DELETE" });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Failed to delete task");
  loadTasks();
}

async function saveEdit(id, newTitleValue, li) {
  try {
    const res  = await fetch(`${API}/${id}`, {
      method: "PATCH", // Backend uses PATCH
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: newTitleValue }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to update task");
    loadTasks();
  } catch (e) {
    showError(e.message);
  }
}

function startEdit(li, task, id) {
  const label = li.querySelector(".checkbox-label");
  const titleSpan = li.querySelector(".title-text");
  const editBtn = li.querySelector(".btn-edit");

  const input = document.createElement("input");
  input.type = "text";
  input.className = "edit-input";
  input.value = task.title;

  label.replaceChild(input, titleSpan);
  editBtn.textContent = "Save";
  input.focus();

  const finish = () => {
    const val = input.value.trim();
    if (val && val !== task.title) {
      saveEdit(id, val, li);
    } else {
      loadTasks(); // revert
    }
  };

  editBtn.onclick = finish;
  input.addEventListener("keydown", e => {
    if (e.key === "Enter") finish();
    if (e.key === "Escape") loadTasks();
  });
}

addForm.addEventListener("submit", async e => {
  e.preventDefault();
  const title = newTitle.value.trim();
  if (!title) return;
  try {
    await createTask(title);
    newTitle.value = "";
    loadTasks();
  } catch (e) {
    showError(e.message);
  }
});

loadTasks();
