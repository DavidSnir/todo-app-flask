const API = "/tasks";
const taskList  = document.getElementById("task-list");
const emptyMsg  = document.getElementById("empty-msg");
const errorMsg  = document.getElementById("error-msg");
const pageTitle = document.getElementById("page-title");
const backLink  = document.getElementById("back-link");
const addForm   = document.getElementById("add-form");
const newTitle  = document.getElementById("new-title");
const deleteModal = document.getElementById("delete-modal");
const modalConfirm = document.getElementById("modal-confirm");
const modalCancel = document.getElementById("modal-cancel");

function showError(msg) {
  errorMsg.textContent = msg;
  errorMsg.classList.remove("hidden");
  setTimeout(() => errorMsg.classList.add("hidden"), 4000);
}

function showDeleteModal() {
  deleteModal.classList.add("show");
  return new Promise((resolve) => {
    const onConfirm = () => {
      deleteModal.classList.remove("show");
      cleanup();
      resolve(true);
    };
    const onCancel = () => {
      deleteModal.classList.remove("show");
      cleanup();
      resolve(false);
    };
    const cleanup = () => {
      modalConfirm.removeEventListener("click", onConfirm);
      modalCancel.removeEventListener("click", onCancel);
    };
    modalConfirm.addEventListener("click", onConfirm);
    modalCancel.addEventListener("click", onCancel);
  });
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
        <button class="btn-subtasks" title="Subtasks">&#10148;</button>
        <button class="btn-edit" title="Edit">&#9998;</button>
        <button class="btn-delete" title="Delete">&#10005;</button>
      </div>
    `;

    // Toggle completed
    li.querySelector(".toggle-cb").addEventListener("change", () => toggleTask(task._id, !isComplete));

    // Delete
    li.querySelector(".btn-delete").addEventListener("click", () => deleteTask(task._id));

    // Edit
    li.querySelector(".btn-edit").onclick = () => startEdit(li, task, task._id);

    // Subtasks (Go into)
    li.querySelector(".btn-subtasks").onclick = () => {
      window.location.href = `/tasks/${task._id}/subtasks_page`;
    };

    taskList.appendChild(li);
  });
}

async function loadData() {
    try {
        // Load parent task info to update title and back link
        const taskRes = await fetch(`${API}/${TASK_ID}`);
        if (taskRes.ok) {
            const taskData = await taskRes.json();
            pageTitle.textContent = `Subtasks for: ${taskData.title}`;
            
            if (taskData.parent_id && taskData.parent_id !== "None") {
                backLink.href = `/tasks/${taskData.parent_id}/subtasks_page`;
            } else {
                backLink.href = "/";
            }
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

async function createSubTask(title) {
  const res  = await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, parent_id: TASK_ID }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Failed to create task");
  return data.task || data.data;
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
  try {
    const res  = await fetch(`${API}/${id}`, { method: "DELETE" });
    const data = await res.json();

    if (!res.ok) {
      if (data.message === "Task have sub tasks") {
        const confirmDelete = await showDeleteModal();
        if (confirmDelete) {
          const recursiveRes = await fetch(`${API}/${id}/r`, { method: "DELETE" });
          const recursiveData = await recursiveRes.json();
          if (!recursiveRes.ok) throw new Error(recursiveData.message || "Failed to delete task and sub-tasks");
          loadData();
          return;
        } else {
          return;
        }
      }
      throw new Error(data.message || data.error || "Failed to delete task");
    }
    loadData();
  } catch (e) {
    showError(e.message);
  }
}


async function saveEdit(id, newTitleValue, li) {
  try {
    const res  = await fetch(`${API}/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: newTitleValue }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to update task");
    loadData();
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
      loadData(); // revert
    }
  };

  editBtn.onclick = finish;
  input.addEventListener("keydown", e => {
    if (e.key === "Enter") finish();
    if (e.key === "Escape") loadData();
  });
}

addForm.addEventListener("submit", async e => {
  e.preventDefault();
  const title = newTitle.value.trim();
  if (!title) return;
  try {
    await createSubTask(title);
    newTitle.value = "";
    loadData();
  } catch (e) {
    showError(e.message);
  }
});

loadData();
