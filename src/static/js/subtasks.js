const API = "/tasks";
const taskList  = document.getElementById("task-list");
const emptyMsg  = document.getElementById("empty-msg");
const errorMsg  = document.getElementById("error-msg");
const pageTitle = document.getElementById("page-title");

function showError(msg) {
  errorMsg.textContent = msg;
  errorMsg.classList.remove("hidden");
  setTimeout(() => errorMsg.classList.add("hidden"), 4000);
}

function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[c]));
}

function renderTasks(tasks) {
  taskList.innerHTML = "";
  // Filter for sub-tasks of current TASK_ID
  const subTasks = tasks.filter(task => task.parent_id === TASK_ID);
  
  if (subTasks.length === 0) {
    emptyMsg.classList.remove("hidden");
  } else {
    emptyMsg.classList.add("hidden");
  }

  subTasks.forEach(task => {
    const li = document.createElement("li");
    const isComplete = task.is_complete || task.completed;
    li.className = "task-item" + (isComplete ? " completed" : "");
    li.dataset.id = task._id;

    li.innerHTML = `
      <label class="checkbox-label">
        <input type="checkbox" class="toggle-cb" ${isComplete ? "checked" : ""} />
        <span class="title-text">${escapeHtml(task.title)}</span>
      </label>
      <div class="actions">
        <button class="btn-delete" title="Delete">&#10005;</button>
      </div>
    `;

    // Toggle completed
    li.querySelector(".toggle-cb").addEventListener("change", () => toggleTask(task._id, !isComplete));

    // Delete
    li.querySelector(".btn-delete").addEventListener("click", () => deleteTask(task._id));

    taskList.appendChild(li);
  });
}

async function loadData() {
    try {
        // Load parent task info to update title
        const taskRes = await fetch(`${API}/${TASK_ID}`);
        if (taskRes.ok) {
            const taskData = await taskRes.json();
            pageTitle.textContent = `Subtasks for: ${taskData.title}`;
        }

        // Load all tasks and filter
        const res = await fetch(API);
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "Failed to load tasks");
        renderTasks(data.tasks || data.data || []);
    } catch (e) {
        showError(e.message);
    }
}

async function toggleTask(id, is_complete) {
  const res  = await fetch(`${API}/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ is_complete }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Failed to update task");
  loadData();
}

async function deleteTask(id) {
  const res  = await fetch(`${API}/${id}`, { method: "DELETE" });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Failed to delete task");
  loadData();
}

loadData();
