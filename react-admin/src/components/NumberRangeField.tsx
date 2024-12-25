import React from "react";

interface NumberRangeFieldProps {
    id: string;
    label: string;
    labelStart: string;
    labelEnd: string;
    startValue: string;
    endValue: string;
    onChangeStart: (event: React.ChangeEvent<HTMLInputElement>) => void;
    onChangeEnd: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

const NumberRangeField: React.FC<NumberRangeFieldProps> = ({
                                                               id,
                                                               label,
                                                               labelStart,
                                                               labelEnd,
                                                               startValue,
                                                               endValue,
                                                               onChangeStart,
                                                               onChangeEnd,
                                                           }) => {
    return (
        <div className="row">
            <label className="field-label">{label}</label>
            <div className="splitted-row">
                <div className="splitted-row-element">
                    <label htmlFor={`${id}_start`} className="field-label sub-field-label">
                        {labelStart}:
                    </label>
                    <input
                        type="number"
                        className="input-field"
                        id={`${id}_start`}
                        name={`${id}_start`}
                        value={startValue}
                        onChange={onChangeStart}
                    />
                </div>

                <div className="splitted-row-element">
                    <label htmlFor={`${id}_end`} className="field-label sub-field-label">
                        {labelEnd}:
                    </label>
                    <input
                        type="number"
                        className="input-field"
                        id={`${id}_end`}
                        name={`${id}_end`}
                        value={endValue}
                        onChange={onChangeEnd}
                    />
                </div>
            </div>
        </div>
    );
};

export default NumberRangeField;
