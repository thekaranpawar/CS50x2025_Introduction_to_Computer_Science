document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("surpriseBtn");
    if (btn) {
        btn.addEventListener("click", () => {
            alert("Hello! Thanks for visiting my homepage!");
        });
    }
});
