document.addEventListener('DOMContentLoaded', function () {
    const filters = {
        type: document.getElementById('custom-select-type'),
    };

    const scriptNameInput = document.getElementById('script-name');
    const scriptItems = document.querySelectorAll('a .item-card');

    Object.values(filters).forEach(filter => {
        filter.addEventListener('click', function () {
            const options = this.nextElementSibling;
            options.classList.toggle('active');
        });
    });

    document.querySelectorAll('.custom-select-option').forEach(option => {
        option.addEventListener('click', function () {
            const filterType = this.closest('.custom-select-wrapper').querySelector('.custom-select').id.split('-').pop();
            document.getElementById(`selected-option-${filterType}`).textContent = this.textContent;
            this.closest('.custom-select-options').classList.remove('active');
            filterScripts();
        });
    });

    document.addEventListener('click', function (e) {
        Object.values(filters).forEach(filter => {
            if (!filter.contains(e.target)) {
                filter.nextElementSibling.classList.remove('active');
            }
        });
    });

    function filterScripts() {
        const selectedType = document.getElementById('selected-option-type').textContent.toLowerCase();
        const searchName = scriptNameInput.value.toLowerCase();

        scriptItems.forEach(item => {
            const itemType = item.getAttribute('data-type').toLowerCase();
            const itemName = item.getAttribute('data-name').toLowerCase();

            const matchesType = selectedType === 'all' || itemType === selectedType;
            const matchesName = itemName.includes(searchName);

            if (matchesType && matchesName) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    }

    scriptNameInput.addEventListener('input', filterScripts);
});
