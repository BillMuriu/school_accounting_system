document.getElementById("menu-icon").addEventListener("click", function() {
    document.querySelector(".sidebar .sidebar-menu").classList.toggle("show");
    document.getElementById("menu-icon").textContent = document.querySelector(".sidebar .sidebar-menu").classList.contains("show") ? "close" : "menu";
    
    // Add the following code to hide the sidebar-menu when the menu-icon is clicked
    if (document.querySelector(".sidebar .sidebar-menu").classList.contains("show")) {
        document.querySelector(".sidebar .sidebar-menu").style.display = "block";
    } else {
        document.querySelector(".sidebar .sidebar-menu").style.display = "none";
    }
});

