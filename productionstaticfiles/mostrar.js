function desplegar(button, className) {
    const element = button.parentElement.querySelector("." + className);

    if (!element) return;

    if (element.style.display === "block") {
        element.style.display = "none";
        button.innerHTML = button.innerHTML.replace("▼", "▶");
    } else {
        element.style.display = "block";
        button.innerHTML = button.innerHTML.replace("▶", "▼");
    }
}
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(
        ".estantes, .posicion_estante, .racks, .posicion_caja_rack, .cajas, .muestras"
    ).forEach(el => el.style.display = "none");

    document.querySelectorAll(".dropbtn").forEach(btn => {
        btn.innerHTML = btn.innerHTML + " "+ "▶ ";
    });
});
