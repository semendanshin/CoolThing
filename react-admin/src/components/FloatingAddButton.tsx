import './FloatingAddButton.css';

interface Props {
    href: string;
}

function FloatingAddButton({href}: Props) {
    return (
        <a href={href} className="floating-button">+</a>
    );
}

export default FloatingAddButton;
