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