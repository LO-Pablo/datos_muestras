// Función para abrir/cerrar el dropdown asociado al botón clickeado
function desplegar(btn,id) {
  // Primero, cerrar todos los dropdowns abiertos excepto el actual
  cerrarTodosLosEstantes(btn);

  // Luego, obtener el dropdown asociado al botón clickeado
  var dropdownContent = btn.nextElementSibling;

  // Cambiar la visibilidad del dropdown asociado
  if (dropdownContent && dropdownContent.classList.contains(id)) {
    dropdownContent.classList.toggle("show");
  }
}

// Función para cerrar todos los dropdowns excepto el asociado al botón clickeado
function cerrarTodosLosEstantes(exceptBtn,id) {
  var dropdowns = document.getElementsByClassName(id);
  var i;

  for (i = 0; i < dropdowns.length; i++) {
    var openDropdown = dropdowns[i];
    
    // Comprobar que no es el dropdown asociado al botón que se acaba de clicar
    if (exceptBtn && openDropdown === exceptBtn.nextElementSibling) {
      continue; // Saltar este dropdown
    }
    
    // Cerrar el dropdown si está abierto
    if (openDropdown.classList.contains('show')) {
      openDropdown.classList.remove('show');
    }
  }
}

//  Cerrar los dropdowns si se hace clic fuera de ellos
window.onclick = function(event) {
  // Comprobar que el clic no fue en un botón de dropdown
  if (!event.target.matches('.dropbtn')) {
    cerrarTodosLosEstantes(null); // Cerrar todos los dropdowns
  }
}