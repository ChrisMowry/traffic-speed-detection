import { useContext} from 'react';
import { Stepper, Step, StepLabel, Toolbar } from '@mui/material';
import { Link } from 'react-router-dom';
import { HeaderContextType } from '../../types';
import { HeaderContext } from '../../contexts/header-context';
import svgObj from './car-catching-logo.svg';
import { STEPS } from '../../constants/app-constants';


const Header: React.FC = () => {
    const { step, setStep } = useContext( HeaderContext ) as HeaderContextType;

    return (
        <Toolbar className='bg-yellow flex justify-center'>
            <img src={svgObj} alt='logo' className='size-20' />
            <Stepper activeStep={ step } className='w-1/2 self-center'>
            {
                STEPS.map((step) => {
                    return (
                        <Step key={ step.id } className=''>
                            <StepLabel>
                                <Link to={ step.path } onClick={()=>{ setStep(step.id) }} >
                                    { step.label }
                                </Link>
                            </StepLabel>
                        </Step>
                    );
                })
            }
            </Stepper>
        </Toolbar>
    );
}

export default Header;