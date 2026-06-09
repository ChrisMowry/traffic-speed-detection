import { Ref, forwardRef } from "react";
import { InputPropType } from "../../types";

const Input = forwardRef(function Input(props: InputPropType, ref: Ref<HTMLInputElement> ) {
    const validColor = props.isValid ? 'bg-grey' : 'bg-red';
    const width = props.width ? props.width : ''
    return(
        <>
            <label className={`pr-2 ${props.additionalLabelClassNames}`} htmlFor={props.id}>{props.label}</label>
            <input type='text'
                id={props.id}
                name={props.id}
                className={`${width} px-2 rounded focus:outline-none text-end ${validColor} ${props.additionalInputClassNames}`}
                onChange={props.onChange}
                ref={ref}
                value={props.value}
            />
        </>
    );
});


export default Input;