$(document).ready(function() {
    var word = localStorage.getItem('word');
    $('#section__word').text(word);
});