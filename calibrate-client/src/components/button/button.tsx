import { ButtonPropsType } from "../../types";

const Button: React.FC<ButtonPropsType> = ({ text, onClickMethod, additionalClassNames }) => {
    const classNameString = additionalClassNames
        ? `bg-blue text-white p-2 rounded hover:bg-dark-blue ${additionalClassNames}`
        : 'bg-blue text-white p-2 rounded hover:bg-dark-blue';

    return(
        <button onClick={onClickMethod} className={`${classNameString}`}>{text}</button>
    );
}

export default Button;