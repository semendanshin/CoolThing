import "./UpdateForm.css"
import React from "react";

interface Props {
    header: string;
    entity: string;
    children: React.ReactNode;
    deleteEntity: (id: string) => void;
}

function UpdateForm({ header, entity, children, deleteEntity }: Props) {
    const handleDelete = () => {
        if (window.confirm(`Are you sure you want to delete this ${entity}? This action cannot be undone.`)) {
            deleteEntity(entity);
        }
    };

    return (
        <div className="form-container">
            <div className="form-header-container">
                <div className="form-header">
                    <h1>{header}</h1>
                    <p>Here you can see and edit details about the {entity}.</p>
                </div>
                <div className="delete-button-container">
                    <svg className="delete-button-svg" onClick={handleDelete}>
                        <image className="delete-button" href="/public/assets/icons/trash-solid.svg"></image>
                    </svg>
                </div>
            </div>
            {children}
        </div>
    );
}

export default UpdateForm;