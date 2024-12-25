import React from "react";
import "./ViewPort.css";

interface Props {
    children: React.ReactNode;
}


function ViewPort({children}: Props) {
    return (
        <div className="content">
            {children}
        </div>
    );
}

export default ViewPort;