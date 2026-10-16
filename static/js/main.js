// CampusFind client-side behaviour. No dependencies.
document.addEventListener("DOMContentLoaded", function () {
  // Mobile navigation toggle
  var navToggle = document.querySelector(".nav-toggle");
  var navMenu = document.getElementById("nav-menu");
  if (navToggle && navMenu) {
    navToggle.addEventListener("click", function () {
      var open = navMenu.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Dismissible flash messages (success ones auto-hide after 5s)
  document.querySelectorAll(".alert").forEach(function (alert) {
    var dismiss = function () {
      alert.style.opacity = "0";
      setTimeout(function () { alert.remove(); }, 250);
    };
    var btn = alert.querySelector(".alert-close");
    if (btn) btn.addEventListener("click", dismiss);
    if (alert.classList.contains("alert-success")) setTimeout(dismiss, 5000);
  });

  // Filter panel toggle
  var filterToggle = document.querySelector(".filter-toggle");
  var filterPanel = document.getElementById("filter-panel");
  if (filterToggle && filterPanel) {
    filterToggle.addEventListener("click", function () {
      var open = filterPanel.classList.toggle("open");
      filterToggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Live filtering: submit the search form as soon as a dropdown changes
  document.querySelectorAll(".auto-submit").forEach(function (select) {
    select.addEventListener("change", function () { select.form.submit(); });
  });

  // Confirmation dialogs for destructive actions
  document.querySelectorAll("form[data-confirm]").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      if (!window.confirm(form.getAttribute("data-confirm"))) event.preventDefault();
    });
  });

  // Character counter for textareas
  document.querySelectorAll("textarea[data-counter]").forEach(function (area) {
    var target = document.getElementById(area.getAttribute("data-counter"));
    var update = function () { if (target) target.textContent = area.value.length; };
    area.addEventListener("input", update);
    update();
  });
});
