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


    // Function to update bot select options in all messages
    function updateBotOptions() {
        // console.log("update called");
        const botsCount = botsCountInput.value;
        // console.log("bots count", botsCount);
        if (!botsCount) return;  // Exit if bots count is empty or invalid
        const botOptions = Array.from({length: botsCount}, (_, i) => `<option value="bot${i + 1}">Bot ${i + 1}</option>`).join('');

        // console.log(botOptions);
        document.querySelectorAll(".bot-select").forEach(select => {
            const currentSelection = select.value;
            select.innerHTML = botOptions;

            // Restore the previous selection if it is still valid
            if (parseInt(currentSelection.replace('bot', '')) <= botsCount) {
                select.value = currentSelection;
            } else {
                select.value = ''; // Clear the selection if it is no longer valid
            }
        });
        // console.log("update executed");
    }

    addMessageButton.addEventListener("click", () => {
        const newMessage = document.importNode(messageTemplate, true);
        scriptMessages.appendChild(newMessage);
        updateBotOptions();
        addDeleteButtonListeners();
        setupDragAndDrop();
    });

    function addDeleteButtonListeners() {
        const deleteButtons = document.querySelectorAll(".delete-button");
        deleteButtons.forEach(button => {
            button.addEventListener("click", () => {
                button.closest(".message-container").remove();
            });
        });
    }

    // Function to setup drag and drop
    function setupDragAndDrop() {
        let listContainer = document.getElementById("script-messages");
        let draggableItem;
        let pointerStartX, pointerStartY;
        let itemsGap = 0;
        let items = [];
        let prevRect = {};

        function getAllItems() {
            if (!items?.length) {
                items = Array.from(listContainer.querySelectorAll('.message-container'));
            }
            return items;
        }

        function getIdleItems() {
            return getAllItems().filter((item) => item.classList.contains('is-idle'));
        }

        function isItemAbove(item) {
            return item.hasAttribute('data-is-above');
        }

        function isItemToggled(item) {
            return item.hasAttribute('data-is-toggled');
        }

        function dragStart(e) {
            if (e.target.classList.contains('drag-handle')) {
                draggableItem = e.target.closest('.message-container');
            }

            if (!draggableItem) return;

            pointerStartX = e.clientX || e.touches?.[0]?.clientX;
            pointerStartY = e.clientY || e.touches?.[0]?.clientY;

            setItemsGap();
            disablePageScroll();
            initDraggableItem();
            initItemsState();
            prevRect = draggableItem.getBoundingClientRect();

            document.addEventListener('mousemove', drag);
            document.addEventListener('touchmove', drag, {passive: false});
        }

        function setItemsGap() {
            if (getIdleItems().length <= 1) {
                itemsGap = 0;
                return;
            }

            const item1 = getIdleItems()[0];
            const item2 = getIdleItems()[1];

            const item1Rect = item1.getBoundingClientRect();
            const item2Rect = item2.getBoundingClientRect();

            itemsGap = Math.abs(item1Rect.bottom - item2Rect.top);
        }

        function disablePageScroll() {
            document.body.style.overflow = 'hidden';
            document.body.style.touchAction = 'none';
            document.body.style.userSelect = 'none';
        }

        function initItemsState() {
            getIdleItems().forEach((item, i) => {
                if (getAllItems().indexOf(draggableItem) > i) {
                    item.dataset.isAbove = '';
                }
            });
        }

        function initDraggableItem() {
            draggableItem.classList.remove('is-idle');
            draggableItem.classList.add('is-draggable');
        }

        function drag(e) {
            if (!draggableItem) return;

            e.preventDefault();

            const clientX = e.clientX || e.touches[0].clientX;
            const clientY = e.clientY || e.touches[0].clientY;

            const pointerOffsetX = clientX - pointerStartX;
            const pointerOffsetY = clientY - pointerStartY;

            draggableItem.style.transform = `translate(${pointerOffsetX}px, ${pointerOffsetY}px)`;

            updateIdleItemsStateAndPosition();
        }

        function updateIdleItemsStateAndPosition() {
            const draggableItemRect = draggableItem.getBoundingClientRect();
            const draggableItemY = draggableItemRect.top + draggableItemRect.height / 2;

            // Update state
            getIdleItems().forEach((item) => {
                const itemRect = item.getBoundingClientRect();
                const itemY = itemRect.top + itemRect.height / 2;
                if (isItemAbove(item)) {
                    if (draggableItemY <= itemY) {
                        item.dataset.isToggled = '';
                    } else {
                        delete item.dataset.isToggled;
                    }
                } else {
                    if (draggableItemY >= itemY) {
                        item.dataset.isToggled = '';
                    } else {
                        delete item.dataset.isToggled;
                    }
                }
            });

            // Update position
            getIdleItems().forEach((item) => {
                if (isItemToggled(item)) {
                    const direction = isItemAbove(item) ? 1 : -1;
                    item.style.transform = `translateY(${direction * (draggableItemRect.height + itemsGap)}px)`;
                } else {
                    item.style.transform = '';
                }
            });
        }

        function dragEnd(e) {
            if (!draggableItem) return;

            applyNewItemsOrder(e);
            cleanup();
        }

        function applyNewItemsOrder(e) {
            const reorderedItems = [];

            getAllItems().forEach((item, index) => {
                if (item === draggableItem) {
                    return;
                }
                if (!isItemToggled(item)) {
                    reorderedItems[index] = item;
                    return;
                }
                const newIndex = isItemAbove(item) ? index + 1 : index - 1;
                reorderedItems[newIndex] = item;
            });

            for (let index = 0; index < getAllItems().length; index++) {
                const item = reorderedItems[index];
                if (typeof item === 'undefined') {
                    reorderedItems[index] = draggableItem;
                }
            }

            reorderedItems.forEach((item) => {
                listContainer.appendChild(item);
            });

            draggableItem.style.transform = '';

            requestAnimationFrame(() => {
                const rect = draggableItem.getBoundingClientRect();
                const yDiff = prevRect.y - rect.y;
                const currentPositionX = e.clientX || e.changedTouches?.[0]?.clientX;
                const currentPositionY = e.clientY || e.changedTouches?.[0]?.clientY;

                const pointerOffsetX = currentPositionX - pointerStartX;
                const pointerOffsetY = currentPositionY - pointerStartY;

                draggableItem.style.transform = `translate(${pointerOffsetX}px, ${pointerOffsetY + yDiff}px)`;
                requestAnimationFrame(() => {
                    unsetDraggableItem();
                });
            });
        }

        function cleanup() {
            itemsGap = 0;
            items = [];
            unsetItemState();
            enablePageScroll();

            document.removeEventListener('mousemove', drag);
            document.removeEventListener('touchmove', drag);
        }

        function unsetDraggableItem() {
            draggableItem.style = null;
            draggableItem.classList.remove('is-draggable');
            draggableItem.classList.add('is-idle');
            draggableItem = null;
        }

        function unsetItemState() {
            getIdleItems().forEach((item, i) => {
                delete item.dataset.isAbove;
                delete item.dataset.isToggled;
                item.style.transform = '';
            });
        }

        function enablePageScroll() {
            document.body.style.overflow = '';
            document.body.style.touchAction = '';
            document.body.style.userSelect = '';
        }

        listContainer.addEventListener('mousedown', dragStart);
        listContainer.addEventListener('touchstart', dragStart);
        document.addEventListener('mouseup', dragEnd);
        document.addEventListener('touchend', dragEnd);
    }

    botsCountInput.addEventListener("blur", () => {
        if (!botsCountInput.isActive) {
            updateBotOptions();
        }
    });

    addDeleteButtonListeners();
    setupDragAndDrop();

    document.getElementById("cancel-button").addEventListener("click", () => {
        if (confirm("Are you sure you want to cancel? All changes will be lost.")) {
            window.location.reload();
        }
    });
});
