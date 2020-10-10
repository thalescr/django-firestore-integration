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

  // Initialize collapsible (uncomment the lines below if you use the dropdown variation)
  // var collapsibleElem = document.querySelector('.collapsible');
  // var collapsibleInstance = M.Collapsible.init(collapsibleElem, options);

