import { HeaderContextType, IContextProps } from '../types';
import { createContext, useState } from 'react';

export const HeaderContext = createContext<HeaderContextType | null> (null);

const HeaderContextProvider = ({ children }: IContextProps) => {

    const [ step, setStep ] = useState<number>(0);

    const values = {
        step,
        setStep
    }

    return (<HeaderContext.Provider value={ values }>{ children }</HeaderContext.Provider>);
}

export default HeaderContextProvider;