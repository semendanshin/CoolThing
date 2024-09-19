document.addEventListener("DOMContentLoaded", async () => {
    const customSelects = document.querySelectorAll('.custom-select-wrapper');

    customSelects.forEach(selectWrapper => {
        const select = selectWrapper.querySelector('.custom-select');
        const options = selectWrapper.querySelector('.custom-select-options');

        select.addEventListener('click', function () {
            console.log(select);
            options.classList.toggle('active');
        });

        options.querySelectorAll('.custom-select-option').forEach(option => {
            option.addEventListener('click', function () {
                const selectedOption = select.querySelector('span');
                selectedOption.textContent = this.textContent;
                options.classList.remove('active');
            });
        });
    });

    document.addEventListener('click', function (e) {
        customSelects.forEach(selectWrapper => {
            const select = selectWrapper.querySelector('.custom-select');
            const options = selectWrapper.querySelector('.custom-select-options');
            if (!select.contains(e.target)) {
                options.classList.remove('active');
            }
        });
    });
});