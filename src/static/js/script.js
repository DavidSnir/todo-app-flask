const API = "/tasks";
const LIST_API = "/lists";

let currentListId = "all";
let currentListName = "All Tasks";

const taskList  = document.getElementById("task-list");
const emptyMsg  = document.getElementById("empty-msg");
const successMsg = document.getElementById("success-msg");
const errorMsg  = document.getElementById("error-msg");
const addForm   = document.getElementById("add-form");
const newTitle  = document.getElementById("new-title");
const deleteModal = document.getElementById("delete-modal");
const modalConfirm = document.getElementById("modal-confirm");
const modalCancel = document.getElementById("modal-cancel");

// List elements
const listTabs = document.getElementById("list-tabs");
const addListBtn = document.getElementById("add-list-btn");
const addListForm = document.getElementById("add-list-form");
const newListTitle = document.getElementById("new-list-title");
const saveListBtn = document.getElementById("save-list-btn");
const cancelListBtn = document.getElementById("cancel-list-btn");
const currentListDisplay = document.getElementById("current-list-name");

function showError(msg) {
  errorMsg.textContent = msg;
  errorMsg.classList.remove("hidden");
  setTimeout(() => errorMsg.classList.add("hidden"), 4000);
}

function showSuccess(msg) {
  successMsg.textContent = msg;
  successMsg.classList.remove("hidden");
  setTimeout(() => successMsg.classList.add("hidden"), 4000);
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

const deleteListModal = document.getElementById("delete-list-modal");
const modalListMove = document.getElementById("modal-list-move");
const modalListDeleteAll = document.getElementById("modal-list-delete-all");
const modalListCancel = document.getElementById("modal-list-cancel");

function showDeleteListModal() {
  deleteListModal.classList.add("show");
  return new Promise((resolve) => {
    const onMove = () => {
      deleteListModal.classList.remove("show");
      cleanup();
      resolve("move");
    };
    const onDeleteAll = () => {
      deleteListModal.classList.remove("show");
      cleanup();
      resolve("delete-all");
    };
    const onCancel = () => {
      deleteListModal.classList.remove("show");
      cleanup();
      resolve("cancel");
    };
    const cleanup = () => {
      modalListMove.removeEventListener("click", onMove);
      modalListDeleteAll.removeEventListener("click", onDeleteAll);
      modalListCancel.removeEventListener("click", onCancel);
    };
    modalListMove.addEventListener("click", onMove);
    modalListDeleteAll.addEventListener("click", onDeleteAll);
    modalListCancel.addEventListener("click", onCancel);
  });
}

let allListIds = new Set();

function renderLists(lists) {
  allListIds = new Set(lists.map(l => l._id));
  // Keep the "All Tasks" tab
  listTabs.innerHTML = `<li class="list-tab ${currentListId === "all" ? "active" : ""}" data-id="all">All Tasks</li>`;
  
  lists.forEach(list => {
    const li = document.createElement("li");
    li.className = `list-tab ${currentListId === list._id ? "active" : ""}`;
    li.dataset.id = list._id;
    
    li.innerHTML = `
      <span>${escapeHtml(list.title)}</span>
      <button class="btn-delete-list" title="Delete List">&times;</button>
    `;

    li.onclick = (e) => {
      if (e.target.classList.contains("btn-delete-list")) {
        deleteList(list._id);
      } else {
        switchList(list._id, list.title);
      }
    };
    listTabs.appendChild(li);
  });

  // Re-attach "All Tasks" click
  listTabs.querySelector('[data-id="all"]').onclick = () => switchList("all", "All Tasks");
}

async function deleteList(id) {
  const choice = await showDeleteListModal();
  
  if (choice === "cancel") return;

  try {
    let res;
    if (choice === "move") {
      // Standard DELETE route moves tasks to All Tasks (parent_id = "None")
      res = await fetch(`${LIST_API}/${id}`, { method: "DELETE" });
    } else if (choice === "delete-all") {
      // Recursive DELETE route deletes the list and all its tasks
      res = await fetch(`${LIST_API}/${id}/r`, { method: "DELETE" });
      const data = await res.json();
      if (res.ok) {
        showSuccess(`Deleted list and ${data.deleted_tasks_count} tasks.`);
      }
      // Re-fetch since we already consumed the body
      if (currentListId === id) {
        switchList("all", "All Tasks");
      } else {
        loadLists();
        loadTasks();
      }
      return;
    }

    if (!res.ok) {
      const data = await res.json();
      throw new Error(data.message || data.error || "Failed to delete list");
    }

    if (currentListId === id) {
      switchList("all", "All Tasks");
    } else {
      loadLists();
      loadTasks();
    }
  } catch (e) {
    showError(e.message);
  }
}

function switchList(id, name) {
  currentListId = id;
  currentListName = name;
  currentListDisplay.textContent = name;
  
  // Update UI active state
  document.querySelectorAll(".list-tab").forEach(tab => {
    tab.classList.toggle("active", tab.dataset.id === id);
  });
  
  loadTasks();
}

async function loadLists() {
  try {
    const res = await fetch(LIST_API);
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to load lists");
    renderLists(data.lists || []);
  } catch (e) {
    showError(e.message);
  }
}

async function createList(title) {
  try {
    const res = await fetch(LIST_API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to create list");
    newListTitle.value = "";
    addListForm.classList.add("hidden");
    loadLists();
  } catch (e) {
    showError(e.message);
  }
}

function renderTasks(tasks) {
  taskList.innerHTML = "";
  
  // Filter tasks based on current list
  let filteredTasks;
  if (currentListId === "all") {
    // Show all tasks that are NOT subtasks
    // A task is NOT a subtask if its parent_id is "None", null, or a List ID
    filteredTasks = tasks.filter(task => {
      const pId = task.parent_id;
      return !pId || pId === "None" || allListIds.has(pId);
    });
  } else {
    // Show tasks belonging to this specific list
    filteredTasks = tasks.filter(task => task.parent_id === currentListId);
  }

  emptyMsg.classList.toggle("hidden", filteredTasks.length > 0);

  filteredTasks.forEach(task => {
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
  const body = { title };
  if (currentListId !== "all") {
    body.parent_id = currentListId;
  }
  
  const res  = await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
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
          showSuccess(`Deleted task and ${recursiveData.deleted_count - 1} sub-tasks.`);
          loadTasks();
          return;
        } else {
          return;
        }
      }
      throw new Error(data.message || data.error || "Failed to delete task");
    }
    loadTasks();
  } catch (e) {
    showError(e.message);
  }
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

// Event Listeners for Lists
addListBtn.addEventListener("click", () => {
  addListForm.classList.toggle("hidden");
  if (!addListForm.classList.contains("hidden")) {
    newListTitle.focus();
  }
});

cancelListBtn.addEventListener("click", () => {
  addListForm.classList.add("hidden");
  newListTitle.value = "";
});

addListForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = newListTitle.value.trim();
  if (title) {
    await createList(title);
  }
});

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

async function init() {
  await loadLists();
  await loadTasks();
}

init();
