const toggleBtn = document.getElementById("toggle-btn");
const editBtn = document.getElementById("edit-btn");
const cancelBtn = document.getElementById("cancel-btn");
const checkCols = document.querySelectorAll(".checkbox-col");
const selectAll = document.getElementById("select-all");
const deleteForm = document.getElementById("book-form");
const editForm = document.getElementById("edit-form");
const booksDataInput = document.getElementById("books-data");

let selecting = false;
let editing = false;

// ----- SELECT / DELETE -----
toggleBtn.addEventListener("click", () => {
  if (editing) return; // prevent conflict
  selecting = !selecting;
  cancelBtn.classList.toggle("d-none", !selecting);

  checkCols.forEach((col) => col.classList.toggle("hidden-checkbox", !selecting));

  if (selecting) {
    toggleBtn.textContent = "Delete Selected";
  } else {
    const selected = document.querySelectorAll('input[name="selected_books"]:checked');
    if (selected.length > 0) {
      const modal = new bootstrap.Modal(document.getElementById("confirmDeleteModal"));
      modal.show();
    } else {
      toggleBtn.textContent = "Select";
      document.querySelectorAll('input[name="selected_books"]').forEach((cb) => (cb.checked = false));
    }
  }
});

// ----- SELECT ALL -----
if (selectAll) {
  selectAll.addEventListener("click", (e) => {
    const checkboxes = document.querySelectorAll('input[name="selected_books"]');
    checkboxes.forEach((cb) => (cb.checked = e.target.checked));
  });
}

// ----- EDIT / SAVE -----
editBtn.addEventListener("click", () => {
  if (selecting) return; // prevent conflict
  editing = !editing;
  cancelBtn.classList.toggle("d-none", !editing);

  const cells = document.querySelectorAll(".editable");

  if (editing) {
    editBtn.textContent = "Save Changes";
    editBtn.classList.replace("btn-primary", "btn-success");

    cells.forEach((cell) => {
      const value = cell.textContent.trim();
      cell.innerHTML = `<input type="text" class="form-control form-control-sm" value="${value}">`;
    });
  } else {
    const rows = document.querySelectorAll("tbody tr");
    const booksData = [];

    rows.forEach((row) => {
      const id = row.getAttribute("data-id");
      const fields = row.querySelectorAll(".editable input");
      const bookObj = {
        id: id,
        name: fields[0].value,
        quantity: fields[1].value,
        author: fields[2].value,
        category: fields[3].value,
        language: fields[4].value,
      };
      booksData.push(bookObj);
    });

    booksDataInput.value = JSON.stringify(booksData);
    editForm.submit();
  }
});

// ----- CANCEL BUTTON -----
cancelBtn.addEventListener("click", () => {
  if (editing) {
    editing = false;
    cancelBtn.classList.add("d-none");
    editBtn.textContent = "Edit";
    editBtn.classList.replace("btn-success", "btn-primary");

    const cells = document.querySelectorAll(".editable");
    cells.forEach((cell) => {
      const input = cell.querySelector("input");
      if (input) cell.textContent = input.value;
    });
  } else if (selecting) {
    selecting = false;
    cancelBtn.classList.add("d-none");
    toggleBtn.textContent = "Select";
    checkCols.forEach((col) => col.classList.add("hidden-checkbox"));
  }
});

// ----- CONFIRM DELETE -----
document.getElementById("confirmDeleteBtn").addEventListener("click", () => {
  deleteForm.submit();
});
