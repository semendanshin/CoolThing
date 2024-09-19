document.addEventListener("DOMContentLoaded", async () => {
    const typeSelectOptions = document.querySelector(".campaign_type_select .custom-select-options");

    typeSelectOptions.addEventListener('click', async () => {
        let type = document.querySelector("#selected-option").innerText;

        let commonFields = ["name", "scope", "campaign_type", "gpt_settings_id"];
        let niFields = ["script_template", ""]
        let mFields = ["welcome_message", "plus_keywords", "minus_keywords"];

        let fields = document.querySelectorAll(".row");
        fields.forEach((field) => {
            let name = field.querySelector("label").getAttribute("for");
            console.log(name);
            if (!name in ["name", "scope", "campaign_type"]) {

            }
        });

        if (type === "Native integration") {
            console.log('nice');
            let fields
        }
        else {
            console.log(type);
        }
    });
});