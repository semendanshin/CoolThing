import React from "react";
import "./TextInputField.css"

interface TextInputFieldProps {
    label: string;
    name: string;
    value: string;
    onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
    placeholder?: string;
    required?: boolean;
}

const TextInputField: React.FC<TextInputFieldProps> = ({ label, name, value, onChange, placeholder, required }) => {
    return (
        <div className="row">
            <label htmlFor={name} className="field-label">{label}</label>
            <input
                className="input-field"
                type="text"
                id={name}
                name={name}
                value={value}
                onChange={onChange}
                required={required}
                placeholder={placeholder}
            />
        </div>
    );
};

export default TextInputField;
