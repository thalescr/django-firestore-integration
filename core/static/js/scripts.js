/* Search bar events */

const searchButton = document.getElementById('search-button')
const searchForm = document.querySelectorAll('.input-field')[0]
const searchBar = document.getElementById('search');

// Shows search bar when clicking on search button
searchButton.addEventListener('click', () => {
    searchButton.style.display = 'none';
    searchForm.style.display = '';
    searchBar.focus();
})

// Hides search bar when focusing out
searchBar.addEventListener('focusout', () => {
    searchButton.style.display = '';
    searchForm.style.display = 'none';
})


/* Side nav */

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems);
});

// List view dropdown button
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.dropdown-trigger');
    var instances = M.Dropdown.init(elems, {});
});

// List view modal delete
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems, {});
});

// Load select input
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems, {});
    document.querySelectorAll('input.select-dropdown').forEach( select => {
        select.classList.add('white-text')
    })
});
