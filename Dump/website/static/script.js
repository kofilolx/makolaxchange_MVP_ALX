let sidebar = document.querySelector(".sidebar");
let closeBtn = document.querySelector("#btn");
let searchBtn = document.querySelector(".bx-search");

closeBtn.addEventListener("click", () => {
    sidebar.classList.toggle("open");
    menuBtnChange();
})

searchBtn.addEventListener("click", () => {
    sidebar.classList.toggle("open");
    menuBtnChange();
})

function menuBtnChange() {
    if (sidebar.classList.contains("open")) {
        closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");
    } else {
        closeBtn.classList.replace("bx-menu-alt-right", "bx-menu");
    }
}

menuBtnChange();

function acceptTerms() {
    var checkbox = document.getElementById('acceptTerms');
    if (checkbox.checked) {
        document.getElementById('termsPopup').style.display = 'none';
    } else {
        alert('You must accept the terms and conditions to proceed.');
    }
}

function closePopup() {
    document.getElementById('termsPopup').style.display = 'none';
}

window.onload = function() {
    document.getElementById('termsPopup').style.display = 'flex';
}