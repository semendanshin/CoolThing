document.addEventListener("DOMContentLoaded", function () {
    const customSelects = document.querySelectorAll('.custom-select-wrapper');

    customSelects.forEach(selectWrapper => {
        const select = selectWrapper.querySelector('.custom-select');
        const options = selectWrapper.querySelector('.custom-select-options');

        select.addEventListener('click', function () {
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

    const addMessageButton = document.getElementById("add-message-button");
    const scriptMessages = document.getElementById("script-messages");
    const messageTemplate = document.getElementById("message-template").content;
    const botsCountInput = document.getElementById("bots-count");

    document.addEventListener('click', function (e) {
        customSelects.forEach(selectWrapper => {
            const select = selectWrapper.querySelector('.custom-select');
            const options = selectWrapper.querySelector('.custom-select-options');
            if (!select.contains(e.target)) {
                options.classList.remove('active');
            }
        });
    });
    // new Sortable(scriptMessages, {
    //      multiDrag: true, // Enable multi-drag
    //      selectedClass: 'selected', // The class applied to the selected items
    //      fallbackTolerance: 3, // So that we can select items on mobile
    //      animation: 150
    // });
    // new Sortable(scriptMessages, {
    //      // multiDrag: true, // Enable multi-drag
    //      selectedClass: 'selected', // The class applied to the selected items
    //      fallbackTolerance: 3, // So that we can select items on mobile
    //      animation: 300
    // });
//     new Sortable(scriptMessages, {
//         animation: 300,  // Анимация при перемещении
//         easing: "cubic-bezier(0.25, 1, 0.5, 1)",  // Настройка плавности анимации
//         ghostClass: 'sortable-ghost',  // Класс для "призрака" перетаскиваемого элемента
//         chosenClass: 'sortable-chosen',  // Класс для выбранного элемента
//         dragClass: 'sortable-drag',  // Класс для элемента во время перетаскивания
//         swapThreshold: 1,  // Порог для срабатывания смены местоположения элементов
//         onEnd: function (/**Event*/evt) {
//             const itemEl = evt.item;  // Перетаскиваемый элемент
//             // Можно добавить дополнительную логику после завершения перетаскивания
//         },
//         onChoose: function(evt) {
//             const itemEl = evt.item;
//             itemEl.classList.add('is-draggable');
//         },
//         onUnchoose: function(evt) {
//             const itemEl = evt.item;
//             itemEl.classList.remove('is-draggable');
//         },
//         onStart: function(evt) {
//             const items = evt.from.querySelectorAll('.js-item');
//             items.forEach(item => {
//                 if (item !== evt.item) {
//                     item.classList.add('is-idle');
//                 }
//             });
//         },
//         onEnd: function(evt) {
//             const items = evt.from.querySelectorAll('.js-item');
//             items.forEach(item => {
//                 item.classList.remove('is-idle');
//                 item.style.transform = '';
//             });
//         },
//         setData: function (dataTransfer, dragEl) {
//             dataTransfer.setData('Text', dragEl.textContent); // Данные для drag-and-drop
//         }
// });
//     new Sortable(scriptMessages, {
//         animation: 300,  // Анимация при перемещении
//         easing: "cubic-bezier(0.25, 1, 0.5, 1)",  // Плавность анимации
//         ghostClass: 'sortable-ghost',  // Класс для элемента-призрака
//         chosenClass: 'sortable-chosen',  // Класс для выбранного элемента
//         dragClass: 'sortable-drag',  // Класс для перетаскиваемого элемента
//         swapThreshold: 1,  // Порог для смены местоположения элементов
//         onStart: function (evt) {
//             // Скрываем оригинальный элемент на старом месте
//             evt.item.style.opacity = '0';
//         },
//         onEnd: function (evt) {
//             // Восстанавливаем оригинальный элемент после перемещения
//             evt.item.style.opacity = '';
//             // Можно добавить дополнительную логику после завершения перетаскивания
//         },
//         setData: function (dataTransfer, dragEl) {
//             dataTransfer.setData('Text', dragEl.textContent);  // Данные для drag-and-drop
//         }
// });
    new Sortable(scriptMessages, {
        animation: 300,  // Анимация при перемещении
        easing: "cubic-bezier(0, 0, 0, 0)",  // Плавность анимации
        // easing: "cubic-bezier(0.25, 1, 0.5, 1)",  // Плавность анимации
        ghostClass: 'sortable-ghost',  // Класс для элемента-призрака
        chosenClass: 'sortable-chosen',  // Класс для выбранного элемента
        dragClass: 'sortable-drag',  // Класс для перетаскиваемого элемента
        swapThreshold: 1,  // Порог для смены местоположения элементов
        onStart: function (evt) {
            // Скрываем оригинальный элемент на старом месте
            evt.item.style.visibility = 'hidden';
        },
        onEnd: function (evt) {
            // Восстанавливаем оригинальный элемент после перемещения
            evt.item.style.visibility = 'visible';
        },
        setData: function (dataTransfer, dragEl) {
            dataTransfer.setData('Text', dragEl.textContent);  // Данные для drag-and-drop
        }
});




    function updateBotOptions() {
        const botsCount = botsCountInput.value;
        if (!botsCount) return;
        const botOptions = Array.from({length: botsCount}, (_, i) => `<option value="bot${i + 1}">Bot ${i + 1}</option>`).join('');

        document.querySelectorAll(".bot-select").forEach(select => {
            const currentSelection = select.value;
            select.innerHTML = botOptions;

            if (parseInt(currentSelection.replace('bot', '')) <= botsCount) {
                select.value = currentSelection;
            } else {
                select.value = '';
            }
        });
    }

    addMessageButton.addEventListener("click", () => {
        const newMessage = document.importNode(messageTemplate, true);
        scriptMessages.appendChild(newMessage);
        updateBotOptions();
        addDeleteButtonListeners();
    });

    function addDeleteButtonListeners() {
        const deleteButtons = document.querySelectorAll(".delete-button");
        deleteButtons.forEach(button => {
            button.addEventListener("click", () => {
                button.closest(".message-container").remove();
            });
        });
    }

    botsCountInput.addEventListener("blur", () => {
        if (!botsCountInput.isActive) {
            updateBotOptions();
        }
    });

    addDeleteButtonListeners();

    document.getElementById("cancel-button").addEventListener("click", () => {
        if (confirm("Are you sure you want to cancel? All changes will be lost.")) {
            window.location.reload();
        }
    });

    // Инициализация SortableJS для перетаскивания сообщений
    const sortable = new Sortable(scriptMessages, {
        handle: '.drag-handle', // Перетаскивание будет возможно только за этот элемент
        animation: 150 // Анимация при перемещении
    });
});
