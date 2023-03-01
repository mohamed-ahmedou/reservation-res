var modal = document.getElementById('popup-modal');
var btn = document.getElementById("open-popup-modal");
var span = document.getElementsByClassName("modal-close")[0];
btn.onclick = function() {
modal.style.display = "block";
}
span.onclick = function() {
modal.style.display = "none";
}
window.onload = function() {
setTimeout(function() {
modal.style.display = 'block';
}, 3000);
}
window.onclick = function(event) {
if (event.target == modal) {
modal.style.display = "none";
}
}