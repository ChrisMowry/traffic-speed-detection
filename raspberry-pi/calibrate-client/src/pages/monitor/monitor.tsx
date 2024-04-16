import axios from "axios";
import { createRef, useContext, useState } from "react";
import Header from "../../components/header/header";
import { SetupContext } from "../../contexts/setup-context";
import { CalibratePostResponseType, SetupContextType } from "../../types";
import { processRefValue, validateReference } from "../../util/util";
<<<<<<< HEAD
import { CAMERA_NAME_QUERY, DISTANCE_RATIO_QUERY, MONITOR_ENDPOINT, RASPBERRY_PI_BASE_URL, SAMPLE_ZONE_QUERY, SPEED_LIMIT_QUERY } from "../../constants/app-constants";
=======
import { CAMERA_NAME_QUERY,
    DISTANCE_RATIO_QUERY,
    MONITOR_ENDPOINT,
    RASPBERRY_PI_BASE_URL,
    SAMPLE_ZONE_QUERY,
    SPEED_LIMIT_QUERY,
    STOP_MONITOR
} from "../../constants/app-constants";
>>>>>>> c0022e7d0675fe349908723b66957e4b2de27f64
import Button from "../../components/button/button";
import Input from "../../components/input/input";

const Monitor: React.FC = () => {


    const {
            cameraName,
            speedLimit,
            setSpeedLimit,
            distanceRatio,
            sampleZonePercent
        } = useContext(SetupContext) as SetupContextType;

    const [ isRunning, setIsRunning ] = useState<boolean>(false);
    const [ speedLimitValid, setSpeedLimitValid ] = useState<boolean>(true);
    const speedLimitRef =  createRef<HTMLInputElement>();

    const handleSpeedLimitInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const value = event?.currentTarget?.value;
        setSpeedLimit(value);
    }

    const startMonitor = () => {
<<<<<<< HEAD
        console.log(validateReference(speedLimitRef));
=======
>>>>>>> c0022e7d0675fe349908723b66957e4b2de27f64
        if ( validateReference(speedLimitRef)) {
            setSpeedLimitValid(true);
            let monitorUrl =`${RASPBERRY_PI_BASE_URL}/${MONITOR_ENDPOINT}`
            monitorUrl += `?${CAMERA_NAME_QUERY}=${cameraName}&${SAMPLE_ZONE_QUERY}=${sampleZonePercent}`;
            monitorUrl += `&${SPEED_LIMIT_QUERY}=${processRefValue(speedLimitRef)}&${DISTANCE_RATIO_QUERY}=${distanceRatio}`;
            axios.post<CalibratePostResponseType>( encodeURI(monitorUrl) )
            .then((response) => {
                const { success } = response.data;
                setIsRunning(success);
            })
        } else {
            setSpeedLimitValid(false);
        }
    }

    const stopMonitor = () => {
<<<<<<< HEAD
        console.log('End!')
=======
        let monitorUrl =`${RASPBERRY_PI_BASE_URL}/${MONITOR_ENDPOINT}`
        monitorUrl += `?${STOP_MONITOR}=false`;
        axios.post<CalibratePostResponseType>( encodeURI(monitorUrl) )
        .then((response) => {
            const { success } = response.data;
            if (success){
                setIsRunning(false);
            }
        })

        setIsRunning(false);
>>>>>>> c0022e7d0675fe349908723b66957e4b2de27f64
    }

    return (
        <>
            <Header />
<<<<<<< HEAD
            <div className='flex'>
                <h2>Monitor</h2>
                {
                    isRunning
                        ? <div>Running!</div>
                        : <div>
                            <div>
                                <p>{`Camera Name: ${cameraName}`}</p>
                                <p>{`Distance Ratio: ${distanceRatio}`}</p>
                                <p>{`Sample Zone %: ${sampleZonePercent}`}</p>
                            </div>
                            <div>
                                <Input label='Speed Limit (mph):'
                                    id='speed-limit'
                                    width='w-12'
                                    value={speedLimit}
                                    onChange={handleSpeedLimitInputChange}
                                    isValid={speedLimitValid}
                                    ref={speedLimitRef}
                                />
                            </div>
                            <div>
                                <Button text={'Start'} onClickMethod={startMonitor} />
                                <Button text={'Stop'} onClickMethod={stopMonitor} />
                            </div>
                          </div>
                }
=======
            <div className='flex flex-col justify-center h-full'>
                <h2 className='font-bold p-6 text-center text-lg self-center'>Monitor</h2>
                {
                    isRunning
                        ? <div className='self-center'>Running!</div>
                        : <div className='w-1/2 h-3/4 border-2 rounded p-2 self-center'>
                            <div className='w-1/3 self-center m-auto p-4'>
                                <div>
                                    <p>{`Camera Name: ${cameraName}`}</p>
                                    <p>{`Distance Ratio: ${distanceRatio.toFixed(6)}`}</p>
                                    <p>{`Sample Zone %: ${sampleZonePercent}`}</p>
                                </div>
                                <div>
                                    <Input label='Speed Limit (mph):'
                                        id='speed-limit'
                                        width='w-12'
                                        value={speedLimit}
                                        onChange={handleSpeedLimitInputChange}
                                        isValid={speedLimitValid}
                                        ref={speedLimitRef}
                                    />
                                </div>
                            </div>
                          </div>
                }
                    <div className='p-4 self-center'>
                        <Button text={'Start'} onClickMethod={startMonitor} additionalClassNames={'m-4'}/>
                        <Button text={'Stop'} onClickMethod={stopMonitor}  additionalClassNames={'m-4'}/>
                    </div>
>>>>>>> c0022e7d0675fe349908723b66957e4b2de27f64
                </div>
        </>
    );
}

export default Monitor;