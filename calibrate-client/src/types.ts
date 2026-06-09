import { ReactNode } from "react";

export interface IContextProps {
    children?: ReactNode
}

export interface IPosition {
    x: number,
    y: number
}

export interface IPositions {
    values: IPosition[]
}

export interface ISvgProps {
    startPosition: IPosition
    endPosition: IPosition
    viewBoxHeight: number | undefined
    viewBoxWidth: number | undefined
}

export type SetupContextType = {
    cameraName: string,
    speedLimit: string,
    sampleZonePercent: string,
    imageDistanceInches: number,
    actualDistanceFeet: string,
    distanceRatio: number,
    startPosition: IPosition,
    endPosition: IPosition,
    currentPosition: IPosition
    setCameraName: (name: string) => void;
    setSpeedLimit: (value: string) => void;
    setSampleZonePercent: (value: string) => void;
    setActualDistanceFeet: (value: string) => void;
    addPosition: (position: IPosition) => void;
    modifyCurrentPositon: (position: IPosition) => void;
    clearPositions: () => void;
    addActualDistance: (distance: string) => void;
}

export type HeaderContextType = {
    step: number
    setStep: (step: number) => void
}

export type StepType = {
    id: number
    label: string
    path: string
}

export type ImageResponseType = {
    image: string
}

export type CalibratePostResponseType = {
    success: boolean
}

export type StartEndXCoordinatesType = {
    startX: number
    endX: number
}

export type ButtonPropsType = {
    text: string
    onClickMethod: () => void
    additionalClassNames?: string
}

export type InputPropType = {
    label: string
    id: string
    value: string
    isValid: boolean
    onChange: (event: React.ChangeEvent<HTMLInputElement>) => void
    width?: string
    additionalInputClassNames?: string
    additionalLabelClassNames?: string
}