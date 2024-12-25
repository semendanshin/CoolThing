import React from "react";

interface StatusFieldProps {
    status: string;
    onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

const StatusField: React.FC<StatusFieldProps> = ({ status, onChange }) => {
    return (
        <div className="row">
            <label htmlFor="status" className="field-label">Status</label>
            <label className="switch">
                <input
                    type="checkbox"
                    id="status"
                    name="status"
                    checked={status === "active"}
                    onChange={onChange}
                />
                <span className="slider round"></span>
            </label>
        </div>
    );
};

export default StatusField;
