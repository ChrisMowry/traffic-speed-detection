import { useContext, useState } from "react";
import Header from "../../components/header/header";
import { SetupContext } from "../../contexts/setup-context";
import { HeaderContextType, SetupContextType } from "../../types";
import { useNavigate } from 'react-router-dom';
import { HeaderContext } from "../../contexts/header-context";
import Input from "../../components/input/input";

const Introduction: React.FC = () => {

    const { cameraName, setCameraName } = useContext(SetupContext) as SetupContextType;

    const [ errorMessage, setErrorMessage ] = useState<string>("");
    const { setStep } = useContext(HeaderContext) as HeaderContextType;
    const navigate = useNavigate();

    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setCameraName(event.target.value);
    }

    const handleSubmit = () => {
        if (validateName(cameraName)){
            setErrorMessage("");
            setStep(1);
            navigate('/setup');
        } else {
            setErrorMessage("Invalid Camera Name!");
        }
    }

    const validateName = (name: string | undefined) : boolean => {
        return name ? true : false
    }

    return (
        <>
            <Header />
            <div className='flex justify-center p-4 h-full'>
                <div className='w-1/2 h-3/4 border-2 rounded p-2'>
                    <h2 className = 'font-bold p-6 text-center text-lg'>Welcome!</h2>
                    <p className = 'p-6'>
                        This application uses a Raspberry Pi and camera to capture and report the speed of traffic.
                        In order to capture speed accurately, the device needs to be calibrated to the location it is
                        monitoring. You must provide the following information...
                    </p>
                    <ul className='p-6'>
                        <li><b>Camera Name</b> - Identifies the specific camera</li>
                        <li><b>Reference Distance</b> - Used to provide the camera with a real world distance</li>
                        <li><b>Speed Limit</b> - The speed limit of the road being monitored</li>
                        <li><b>Sample Zone %</b> - A percentage of the frame to sample from. This is to reduce errors on the edges</li>
                    </ul>
                    <form className="'w-full flex justify-center p-6">
                        <Input
                            label='Camera Name:'
                            id='camera-name'
                            value={cameraName}
                            onChange={handleChange}
                            isValid={true}
                        />
                        {/* <label htmlFor="camera-name" className='px-2 font-bold'>Camera Name:</label>
                        <input
                            id="camera-name"
                            type="text"
                            required
                            defaultValue={cameraName}
                            onChange={handleChange}
                            className={`rounded px-2 text-white bg-grey focus:outline-none`}/> */}
                        <div className='text-red px-2'>{errorMessage}</div>
                    </form>
                    <div className='flex justify-center py-6'>
                        <button
                            className='my-6 p-2 rounded bg-blue text-white hover:bg-dark-blue'
                            onClick={() => handleSubmit()}>Next</button>
                    </div>
                </div>
            </div>
        </>

    );
}

export default Introduction;