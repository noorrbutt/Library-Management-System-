// static/student/js/viewstudent.js
document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.getElementById("toggle-btn");
  const editBtn = document.getElementById("edit-btn");
  const cancelBtn = document.getElementById("cancel-btn");
  const checkCols = document.querySelectorAll(".checkbox-col");
  const selectAll = document.getElementById("select-all");
  const deleteForm = document.getElementById("student-form");
  const editForm = document.getElementById("edit-form");
  const studentsDataInput = document.getElementById("students-data");
  const confirmDeleteBtn = document.getElementById("confirmDeleteBtn");
  const confirmDeleteModal = new bootstrap.Modal(
    document.getElementById("confirmDeleteModal")
  );

  // Toast initialization
  const actionToast = document.getElementById('actionToast');
  const toastMessage = document.getElementById('toastMessage');
  const bootstrapToast = actionToast ? new bootstrap.Toast(actionToast, {delay: 4000}) : null;

  let selecting = false;
  let editing = false;

  function showToast(message, type = 'success') {
    if (!bootstrapToast || !actionToast || !toastMessage) return;
    
    // Update toast color based on type
    actionToast.className = `toast align-items-center text-white border-0`;
    if (type === 'success') {
      actionToast.classList.add('bg-success');
    } else if (type === 'error') {
      actionToast.classList.add('bg-danger');
    }
    
    toastMessage.textContent = message;
    bootstrapToast.show();
  }

  // ----- SELECT / DELETE -----
  toggleBtn.addEventListener("click", () => {
    if (editing) return;
    selecting = !selecting;
    cancelBtn.classList.toggle("d-none", !selecting);

    checkCols.forEach((col) =>
      col.classList.toggle("hidden-checkbox", !selecting)
    );

    if (selecting) {
      toggleBtn.textContent = "Delete Selected";
    } else {
      const selected = document.querySelectorAll(
        'input[name="selected_students"]:checked'
      );
      if (selected.length > 0) {
        confirmDeleteModal.show();
      } else {
        toggleBtn.textContent = "Select";
      }
    }
  });

  // ----- CONFIRM DELETION -----
  confirmDeleteBtn.addEventListener("click", () => {
    const selectedCount = document.querySelectorAll('input[name="selected_students"]:checked').length;
    showToast(`Student(s) deleted successfully`, 'success');
    deleteForm.submit();
  });

  // ----- SELECT ALL -----
  if (selectAll) {
    selectAll.addEventListener("click", (e) => {
      const checkboxes = document.querySelectorAll(
        'input[name="selected_students"]'
      );
      checkboxes.forEach((cb) => (cb.checked = e.target.checked));
    });
  }

  // ----- EDIT / SAVE -----
  editBtn.addEventListener("click", () => {
    if (selecting) return;
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
      const studentsData = [];

      rows.forEach((row) => {
        const id = row.getAttribute("data-id");
        const fields = row.querySelectorAll(".editable input");
        const studentObj = {
          id: id,
          name: fields[0].value,
          enrollment: fields[1].value,
          address: fields[2].value,
          phone: fields[3].value,
          gender: fields[4].value,
        };
        studentsData.push(studentObj);
      });

      studentsDataInput.value = JSON.stringify(studentsData);
      showToast('Student(s) edited successfully', 'success');
      editForm.submit();

      // Reset UI after submitting
      editing = false;
      cancelBtn.classList.add("d-none");
      editBtn.textContent = "Edit";
      editBtn.classList.replace("btn-success", "btn-primary");
      cells.forEach(
        (cell) => (cell.textContent = cell.querySelector("input").value)
      );
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
});