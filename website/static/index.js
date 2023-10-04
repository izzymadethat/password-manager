const body = document.querySelector("body"),
      sidebar = body.querySelector(".sidebar"),
      toggle = body.querySelector(".toggle"),
      searchBtn = body.querySelector(".search-box"),
      modeSwitch = body.querySelector(".toggle-switch"),
      modeText = body.querySelector(".mode-text"),
      content = body.querySelector("#content"),
      sidebarLinks = body.querySelectorAll(".nav-link a");

    // Toggle switch
    toggle.addEventListener("click", () => {
        sidebar.classList.toggle("close");
        if (sidebar.classList.contains("close")){
            content.classList.remove("sidebar-extended");
            content.classList.add("sidebar-closed");
        }else {
            content.classList.remove("sidebar-closed");
            content.classList.add("sidebar-extended");
        }
    });

    // Open bar again when searching
    searchBtn.addEventListener("click", () => {
        sidebar.classList.remove("close");
    });

    // Dark mode switch
    modeSwitch.addEventListener("click", () => {
        body.classList.toggle("dark");

        if (body.classList.contains("dark")){
            modeText.innerText = "Light Mode"
        }else{
            modeText.innerText = "Dark Mode"
        }
    });

    

