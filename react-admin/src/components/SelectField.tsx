import React from "react";
import "./SelectField.css"

interface SelectFieldProps {
    label: string;
    name: string;
    value: string | null;
    options: { value: string; label: string }[];
    onChange: (event: React.ChangeEvent<HTMLSelectElement>) => void;
}

const SelectField: React.FC<SelectFieldProps> = ({ label, name, value, options, onChange }) => {
    return (
        <div className="row">
            <label htmlFor={name} className="field-label">{label}</label>
            <select className="select-field" id={name} name={name} value={value || ""} onChange={onChange}>
                <option value="">Select {label.toLowerCase()}</option>
                {options.map(option => (
                    <option key={option.value} value={option.value}>
                        {option.label}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default SelectField;
