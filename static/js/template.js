(function (document) {
    'use strict';

    var TableFilter = (function (searchArray) {
        var searchInput;

        function _onInputSearch(e) {
            searchInput = e.target;
            var tables = document.getElementsByClassName(searchInput.getAttribute('data-table'));
            searchArray.forEach.call(tables, function (table) {
                searchArray.forEach.call(table.tBodies, function (tbody) {
                    searchArray.forEach.call(tbody.rows, function (row) {
                        var textContent = row.textContent.toLowerCase();
                        var searchVal = searchInput.value.toLowerCase();
                        row.style.display = textContent.indexOf(searchVal) > -1 ? '' : 'none';
                    });
                });
            });
        }

        return {
            init: function () {
                var inputs = document.getElementsByClassName('search__input');
                searchArray.forEach.call(inputs, function (input) {
                    input.oninput = _onInputSearch;
                });
            }
        };
    })(Array.prototype);

    document.addEventListener('readystatechange', function () {
        if (document.readyState === 'complete') {
            TableFilter.init();
        }
    });

})(document);

$(document).ready(function () {
    $("#show-search__button").click(function () {
        $("#search-container").removeClass("hide");
        $("#search__input").focus();

        window.addEventListener('click', detectClickOnSearchResults);
    });

});

// if (e.key === "Escape") {
//     // write your logic here.
// }

// function detectClickOnSearchResults(e) {
//     if (document.getElementById('search-results').contains(e.target) || e.key) {
//         console.log("inside");
//     } else {
//         console.log("outside");
//         window.removeEventListener('click', detectClickOnSearchResults);
//     }
// }

// document.addEventListener('click', function handleClickOutsideSearchResults(event) {
//     const box = document.getElementById('search-results');
//     if (!box.contains(event.target)) {
//         box.style.display = 'none';
//     }
// });