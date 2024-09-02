function openEditModal(todoId, todoTitle, todoDescription) {
    var modal = new bootstrap.Modal(document.getElementById("editModal"));
    var form = document.getElementById("editForm");
    var taskTitleInput = document.getElementById("task_title");
    var taskDescriptionInput = document.getElementById("task_description");

    // Set the form action dynamically
    form.action = "/edit/" + todoId;

    // Set the current task title and description in the input fields
    taskTitleInput.value = todoTitle;
    taskDescriptionInput.value = todoDescription;

    // Show the modal
    modal.show();
}

function openAddSubtaskModal(todoId) {
    var modal = new bootstrap.Modal(document.getElementById("addSubtaskModal"));
    var form = document.getElementById("addSubtaskForm");
    var todoIdInput = document.getElementById("todo_id");

    // Set the form action dynamically
    form.action = "/add_subtask/" + todoId;

    // Set the todo ID in the hidden input field
    todoIdInput.value = todoId;

    // Show the modal
    modal.show();
}

// Add Subtasks for new Todo
let subtasks = [];

function addSubtask() {
    const subtaskInput = document.getElementById("subtaskInput");
    const subtaskText = subtaskInput.value.trim();

    if (subtaskText === "") {
        return;
    }

    subtasks.push(subtaskText);
    renderSubtaskList();

    subtaskInput.value = "";
}

function renderSubtaskList() {
    const subtaskList = document.getElementById("subtaskList");
    subtaskList.innerHTML = "";

    subtasks.forEach((subtask, index) => {
        const li = document.createElement("li");
        li.innerHTML = `
            ${subtask} 
            <button type="button" class="btn btn-sm btn-warning" onclick="editSubtask(${index})">Edit</button>
            <button type="button" class="btn btn-sm btn-danger" onclick="removeSubtask(${index})">Delete</button>
        `;
        subtaskList.appendChild(li);
    });
}

function editSubtask(index) {
    const newSubtaskText = prompt("Edit Subtask:", subtasks[index]);

    if (newSubtaskText !== null) {
        subtasks[index] = newSubtaskText.trim();
        renderSubtaskList();
    }
}

function removeSubtask(index) {
    subtasks.splice(index, 1);
    renderSubtaskList();
}

document.getElementById("addTodoForm").addEventListener("submit", function () {
    subtasks.forEach((subtask) => {
        const input = document.createElement("input");
        input.type = "hidden";
        input.name = "subtask";
        input.value = subtask;
        this.appendChild(input);
    });
});
