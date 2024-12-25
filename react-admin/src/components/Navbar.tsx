import "./Navbar.css";
import React from "react";

type Item = {
    title: string;
    link: string;
}

interface Props {
    items: Item[];
}

function Navbar({items}: Props) {
    const [responsive, setResponsive] = React.useState(false);

    return (
        <nav className={`navbar ${responsive ? "responsive" : ""}`}>
            {items.map((namItem, index) => (
                <a href={namItem.link} key={index}>{namItem.title}</a>
            ))}
            <a href="#" className="icon" onClick={() => setResponsive(!responsive)}>
                &#9776;
            </a>
        </nav>
    );
}

export default Navbar;