import { JSX} from "react";
import './Card.css';

interface Attribute {
    name: string;
    value: string | JSX.Element;
}

interface Props {
    href?: string;
    title: string;
    attributes: Attribute[];
}


function Card(
    {href = "", title, attributes}: Props
) {
    return (
        <a href={href || "#"} className="card-link">
            <div className="item-card">
                <h3>{title}</h3>
                {attributes.map((attribute, index) => (
                    <p key={index}>
                        <strong>{attribute.name}:</strong> {attribute.value}
                    </p>
                ))}
            </div>
        </a>
    );
}

export default Card;