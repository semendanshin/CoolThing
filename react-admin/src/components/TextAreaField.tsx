import React from "react";
import "./TextAreaField.css"

interface TextAreaFieldProps {
    label: string;
    name: string;
    value: string | null;
    onChange: (event: React.ChangeEvent<HTMLTextAreaElement>) => void;
}

const TextAreaField: React.FC<TextAreaFieldProps> = ({ label, name, value, onChange }) => {
    return (
        <div className="row">
            <label htmlFor={name} className="field-label">{label}</label>
            <textarea
                className="input-field"
                id={name}
                name={name}
                value={value || ""}
                onChange={onChange}
            />
        </div>
    );
};

export default TextAreaField;
