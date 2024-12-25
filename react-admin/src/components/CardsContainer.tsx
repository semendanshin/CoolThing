import React from "react";
import "./CardsContainer.css";

interface Props {
    children: React.ReactNode;
}

function CardsContainer(
    {children}: Props
) {
    return (
        <div className="cards-container">
            {children}
        </div>
    );
}

export default CardsContainer;