document.addEventListener('DOMContentLoaded', function() {
    // Initialize filtering
    initFilters();

    // Initialize sorting
    initSorting();

    // Add event listeners for stop buttons
    const stopButtons = document.querySelectorAll('.stop-button');
    stopButtons.forEach(button => {
        button.addEventListener('click', function() {
            const sfcId = this.getAttribute('data-sfc-id');
            stopScript(sfcId);
        });
    });
});

// Filtering Functionality
function initFilters() {
    const filters = document.querySelectorAll('.filter');
    filters.forEach(filter => {
        const selectWrapper = filter.querySelector('.custom-select-wrapper');
        const options = selectWrapper.querySelectorAll('.custom-select-option');

        options.forEach(option => {
            option.addEventListener('click', function() {
                applyFilters();
            });
        });
    });
}

function applyFilters() {
    const scriptFilterValue = getFilterValue('scriptFilter');
    const campaignFilterValue = getFilterValue('campaignFilter');
    const statusFilterValue = getFilterValue('statusFilter');

    const rows = document.querySelectorAll('#activeScriptsTable tbody tr');
    rows.forEach(row => {
        const scriptId = row.getAttribute('data-script-id');
        const campaignId = row.getAttribute('data-campaign-id');
        const status = row.getAttribute('data-status');

        const scriptMatch = !scriptFilterValue || scriptId === scriptFilterValue;
        const campaignMatch = !campaignFilterValue || campaignId === campaignFilterValue;
        const statusMatch = !statusFilterValue || status === statusFilterValue;

        if (scriptMatch && campaignMatch && statusMatch) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

function getFilterValue(filterId) {
    const selectWrapper = document.getElementById(filterId);

    if (!selectWrapper) {
        console.error(`Select wrapper not found with id: ${filterId}`);
        return '';
    }

    const selectedTextElement = selectWrapper.querySelector('.custom-select span:first-child');

    if (!selectedTextElement) {
        console.error(`Selected text element not found in custom select with id: ${filterId}`);
        return '';
    }

    const selectedText = selectedTextElement.textContent.trim();

    // Find the option element that matches the selected text
    const options = selectWrapper.querySelectorAll('.custom-select-option');
    let selectedValue = '';
    options.forEach(option => {
        if (option.textContent.trim() === selectedText) {
            selectedValue = option.getAttribute('data-value') || '';
        }
    });
    return selectedValue;
}

// Sorting Functionality
function initSorting() {
    const headers = document.querySelectorAll('#activeScriptsTable th[data-sort]');
    headers.forEach(header => {
        header.addEventListener('click', function() {
            sortTable(this.getAttribute('data-sort'), this);
        });
    });
}

function sortTable(sortKey, headerElement) {
    const table = document.getElementById('activeScriptsTable');
    const tbody = table.tBodies[0];
    const rows = Array.from(tbody.rows);

    // Determine sort order
    const currentSortOrder = headerElement.getAttribute('data-sort-order') || 'asc';
    const sortOrder = currentSortOrder === 'asc' ? 'desc' : 'asc';
    headerElement.setAttribute('data-sort-order', sortOrder);

    // Reset other headers
    const headers = table.querySelectorAll('th[data-sort]');
    headers.forEach(header => {
        if (header !== headerElement) {
            header.removeAttribute('data-sort-order');
        }
    });

    // Sort rows
    const sortedRows = rows.sort((a, b) => {
        let aValue = a.getAttribute('data-' + sortKey);
        let bValue = b.getAttribute('data-' + sortKey);

        // For dates, parse them
        if (sortKey === 'created-at') {
            aValue = new Date(aValue);
            bValue = new Date(bValue);
        } else if (sortKey === 'bots-involved' || sortKey === 'sfc-id') {
            aValue = parseInt(aValue);
            bValue = parseInt(bValue);
        } else {
            aValue = aValue.toLowerCase();
            bValue = bValue.toLowerCase();
        }

        if (aValue < bValue) {
            return sortOrder === 'asc' ? -1 : 1;
        }
        if (aValue > bValue) {
            return sortOrder === 'asc' ? 1 : -1;
        }
        return 0;
    });

    // Re-append sorted rows
    sortedRows.forEach(row => {
        tbody.appendChild(row);
    });
}

// Stop Script Functionality
function stopScript(sfcId) {
    fetch('/scripts/active/stop', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ sfc_id: sfcId })
    })
    .then(response => {
        if (response.ok) {
            alert('Script stopped successfully.');
            // Update the status in the UI
            const row = document.querySelector(`tr[data-sfc-id="${sfcId}"]`);
            row.setAttribute('data-status', 'stopped');
            row.querySelector('td:nth-child(5)').textContent = 'Stopped'; // Adjusted for new column order
            const actionCell = row.querySelector('td:nth-child(7)'); // Adjusted for new column order
            actionCell.innerHTML = '<span>N/A</span>';
        } else {
            response.json().then(data => {
                alert('Error stopping script: ' + data.detail);
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An unexpected error occurred.');
    });
}
