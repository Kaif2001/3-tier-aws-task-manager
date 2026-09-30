const API_URL = "/api/tasks";

async function loadTasks() {
    const response = await fetch(API_URL);
    const tasks = await response.json();

    const list = document.getElementById("taskList");
    list.innerHTML = "";

    tasks.forEach(task => {
        const item = document.createElement("div");
        item.className = "task";

        item.innerHTML = `
            <span>${task.title}</span>
            <button onclick="deleteTask('${task._id}')">Delete</button>
        `;

        list.appendChild(item);
    });
}

async function addTask() {
    const input = document.getElementById("taskInput");
    const title = input.value.trim();

    if (!title) {
        return;
    }

    const response = await fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ title: title })
    });

    if (response.ok) {
        input.value = "";
        document.getElementById("message").textContent = "Task added.";
        loadTasks();
    }
}

async function deleteTask(id) {
    if (!id) {
        return;
    }

    await fetch(`${API_URL}/${id}`, {
        method: "DELETE"
    });

    loadTasks();
}

loadTasks();