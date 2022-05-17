$(document).ready(function () {
    $("#section-topic__table tr.section-topic__table__tr").click(function() {
        var word = $(this).find('td').text();
        console.log(word);
        localStorage.setItem('word',word);
    });

    $('#practice__button').click(function () {
        console.log(localStorage.getItem('word'));
    });
});
