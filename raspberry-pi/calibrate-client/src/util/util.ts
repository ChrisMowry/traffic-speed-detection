import { RefObject } from "react";
import { StartEndXCoordinatesType } from "../types";

export const getSampleZoneStartEndXCoordinates = (sampleZonePercent: string) : StartEndXCoordinatesType => {
    const numberValueFloat = parseFloat(sampleZonePercent);
    let startSampleZoneX = 0.0;
    let endSampleZoneX = 0.0;
    if(!isNaN(numberValueFloat)) {
        // Calculates the sample zone start and end lines
        const imageWidthFloat = process.env.REACT_APP_IMG_WIDTH ? parseFloat(process.env.REACT_APP_IMG_WIDTH) : 0.0;
        startSampleZoneX = (imageWidthFloat / 2.0) - ( imageWidthFloat * ((numberValueFloat/2.0) / 100));
        endSampleZoneX = (imageWidthFloat / 2.0) + ( imageWidthFloat * ((numberValueFloat/2.0) / 100));
    }

    return { startX:startSampleZoneX, endX:endSampleZoneX }
}

export const processRefValue = (ref: RefObject<HTMLInputElement>) : string => {
    return ref?.current?.value ? ref?.current?.value  : "";
}

export const validateNumber = (value: string) : boolean => {
    return !isNaN(parseFloat(value)) && parseFloat(value) > 0;
}

export const validateReference = (ref: RefObject<HTMLInputElement>) : boolean => {
    const refValue = processRefValue(ref);
    return validateNumber(refValue);
}