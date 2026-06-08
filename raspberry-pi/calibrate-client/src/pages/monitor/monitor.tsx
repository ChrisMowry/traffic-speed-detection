import axios from "axios";
import { createRef, useContext, useState } from "react";
import Header from "../../components/header/header";
import { SetupContext } from "../../contexts/setup-context";
import { CalibratePostResponseType, SetupContextType } from "../../types";
import { processRefValue, validateReference } from "../../util/util";
import { CAMERA_NAME_QUERY, DISTANCE_RATIO_QUERY, MONITOR_ENDPOINT, RASPBERRY_PI_BASE_URL, SAMPLE_ZONE_QUERY, SPEED_LIMIT_QUERY } from "../../constants/app-constants";
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
        console.log(validateReference(speedLimitRef));
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
        console.log('End!')
    }

    return (
        <>
            <Header />
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
                </div>
        </>
    );
}

export default Monitor;