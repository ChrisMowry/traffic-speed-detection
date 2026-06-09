import { createContext, useState } from 'react';
import { IPosition, IContextProps, SetupContextType } from '../types';

export const SetupContext = createContext<SetupContextType | null> (null);

const SetupContextProvider = ({ children }: IContextProps) => {

    const SAMPLE_ZONE_PERCENT_DEFAULT = process.env.REACT_APP_SAMPLE_ZONE_DEFAULT_PERCENT
        ? process.env.REACT_APP_SAMPLE_ZONE_DEFAULT_PERCENT
        : "0.0"

    const [ cameraName, setCameraName ] = useState<string>("");
    const [ speedLimit, setSpeedLimit ] = useState<string>("0");
    const [ sampleZonePercent, setSampleZonePercent ] = useState<string>(SAMPLE_ZONE_PERCENT_DEFAULT);
    const [ startPosition, setStartPosition ] = useState<IPosition>({x:0, y:0});
    const [ endPosition, setEndPosition ] = useState<IPosition>({x:0, y:0});
    const [ currentPosition, setCurrentPosition ] = useState<IPosition>({x:0, y:0});
    const [ imageDistanceInches, setImageDistanceInches ] = useState<number>(0);
    const [ actualDistanceFeet, setActualDistanceFeet ] = useState<string>("0");
    const [ distanceRatio, setDistanceRatio ] = useState<number>(0);

    const addPosition = (position: IPosition) => {
        // checks for a starting position, if null adds it.
        if (startPosition.x === 0 && startPosition.y === 0){
            setStartPosition(position);
        } else if (Math.abs(endPosition.x) > 0 && Math.abs(endPosition.y) > 0){
            clearPositions();
        } else {
            setEndPosition(position);

            // calculates distance in image
            const dx = position.x - startPosition.x;
            const dy = position.y - startPosition.y;
            setImageDistanceInches( Math.sqrt( dx*dx + dy*dy ) * 0.0104166667 );

            // set distance ratio
            if (!isNaN(parseFloat(actualDistanceFeet))){
                if ( parseFloat(actualDistanceFeet) > 0.0 ){
                    setDistanceRatio( imageDistanceInches / ( parseFloat(actualDistanceFeet) * 12.0 ));
                }
            }

        }
    }

    const modifyCurrentPositon = (position: IPosition) => {
        setCurrentPosition(position);
    }

    const addActualDistance = (distance: string) => {
        setActualDistanceFeet(distance);
        if (imageDistanceInches > 0 && !isNaN(parseFloat(actualDistanceFeet))){
            setDistanceRatio( imageDistanceInches / ( parseFloat(actualDistanceFeet) * 12.0 ));
        }
    }

    // clears out the positions and returns the distances to their default values
    const clearPositions = () => {
        setStartPosition( {x: 0, y: 0} );
        setEndPosition( {x: 0, y: 0} );
        setCurrentPosition( {x: 0, y: 0} );
        setImageDistanceInches(0);
        setActualDistanceFeet("0");
        setSampleZonePercent(SAMPLE_ZONE_PERCENT_DEFAULT);
        setDistanceRatio(0);
    }

    const values = {
        cameraName,
        setCameraName,
        speedLimit,
        setSpeedLimit,
        sampleZonePercent,
        setSampleZonePercent,
        startPosition,
        setStartPosition,
        endPosition,
        setEndPosition,
        currentPosition,
        setCurrentPosition,
        imageDistanceInches,
        setImageDistanceInches,
        actualDistanceFeet,
        setActualDistanceFeet,
        distanceRatio,
        setDistanceRatio,
        addPosition,
        modifyCurrentPositon,
        addActualDistance,
        clearPositions
    }

    return (<SetupContext.Provider value={ values }>{ children }</SetupContext.Provider>);
}

export default SetupContextProvider;