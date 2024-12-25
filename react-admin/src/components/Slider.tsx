import {useState} from "react";
import "./Slider.css";

interface Props {
    size: "small" | "medium";
    isOn: boolean;
    onSwitch: (isOn: boolean) => void;
}

function Slider(
    {
        size,
        isOn,
        onSwitch,
    }: Props
) {
    const [enabled, setEnabled] = useState(isOn);
    return (
        <label className={`${size == 'small' ? 'small' : ''}-switch`}>
            <input type="checkbox" id="auto_reply" name="auto_reply" checked={enabled} onChange={() => {
                onSwitch(!enabled);
                setEnabled(!enabled);
            }
            }/>
            <span className={`${size == 'small' ? 'small' : ''}-slider round`}></span>
        </label>
    );
}

export default Slider;