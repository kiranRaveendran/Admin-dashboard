document.getElementById('toggleButton').addEventListener('click', function(){
var hiddenButtonsContainer = document.getElementById ('hiddenButtonsContainer');
if (hiddenButtonsContainer.classList.contains ('hidden')) {
    hiddenButtonsContainer.classList.remove ('hidden');
} else {
    hiddenButtonsContainer.classList.add('hidden');
}
});


document.getElementById('adminRest_button').addEventListener('click', function(){
var hiddenButtonsContainer = document.getElementById ('hiddenButtonsContainer2');
if (hiddenButtonsContainer.classList.contains ('hidden')) {
    hiddenButtonsContainer.classList.remove ('hidden');
} else {
    hiddenButtonsContainer.classList.add('hidden');
}
});
