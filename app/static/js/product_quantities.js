// Function to filter products based on search input
function filterProducts() {
    const searchTerm = $('#searchInput').val().toLowerCase();
    $('#productTable tbody tr').each(function() {
        const name = $(this).find('td:eq(2)').text().toLowerCase();
        const id = $(this).find('td:eq(1)').text().toLowerCase();
        if (name.includes(searchTerm) || id.includes(searchTerm)) {
            $(this).show();
        } else {
            $(this).hide();
        }
    });
}

// Attach a listener to the search input
$('#searchInput').on('input', filterProducts);



// Define an object to keep track of the sorting order for each column
const sortingOrder = {};

// Function to sort the table by column
function sortTable(column) {
    const table = $('#productTable');
    const rows = table.find('tbody tr').toArray();

    // Toggle sorting order between ascending (asc) and descending (desc)
    if (sortingOrder[column] === 'asc') {
        sortingOrder[column] = 'desc';
    } else {
        sortingOrder[column] = 'asc';
    }

    // Remove sorting indicators from all headers
    $('#productTable thead th').each(function() {
        $(this).removeClass('sorting-asc sorting-desc');
    });

    // Add the appropriate sorting indicator to the sorted column header
    const header = $('#productTable thead th:eq(' + column + ')');
    header.addClass('sorting-' + sortingOrder[column]);

    rows.sort((a, b) => {
        const aValue = $(a).find(`td:eq(${column})`).text();
        const bValue = $(b).find(`td:eq(${column})`).text();

        // Convert text content to numbers for columns containing numeric data
        const isNumericColumn = [1, 4, 6].includes(column); // Specify the numeric columns
        if (isNumericColumn) {
            const aNumeric = parseFloat(aValue.replace(/[^0-9.-]+/g,""));
            const bNumeric = parseFloat(bValue.replace(/[^0-9.-]+/g,""));
            if (sortingOrder[column] === 'asc') {
                return aNumeric - bNumeric;
            } else {
                return bNumeric - aNumeric;
            }
        } else {
            if (sortingOrder[column] === 'asc') {
                return aValue.localeCompare(bValue);
            } else {
                return bValue.localeCompare(aValue);
            }
        }
    });

    table.find('tbody').empty().append(rows);
}

// Attach event listeners to table headers for sorting
$('#productTable thead th').click(function() {
    const columnIndex = $(this).index();
    sortTable(columnIndex);
});

// Initially sort by the ID column in ascending order
sortingOrder[1] = 'asc';
sortTable(1);
