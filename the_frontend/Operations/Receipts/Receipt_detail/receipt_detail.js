const menuIcon = document.querySelector("#menu-icon");
const closeIcon = document.querySelector("#close-icon");
const sidebarMenu = document.querySelector(".sidebar .sidebar-menu");

// hide the sidebar menu by default when the page loads
sidebarMenu.style.display = "none";

menuIcon.addEventListener("click", function() {
  sidebarMenu.style.display = "block"; // show the sidebar menu when the menu icon is clicked
  menuIcon.style.display = "none"; // hide the menu icon
  closeIcon.style.display = "block"; // show the close icon
});

closeIcon.addEventListener("click", function() {
  sidebarMenu.style.display = "none"; // hide the sidebar menu when the close icon is clicked
  menuIcon.style.display = "block"; // show the menu icon
  closeIcon.style.display = "none"; // hide the close icon
});