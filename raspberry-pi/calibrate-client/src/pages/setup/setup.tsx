import {useRef, useContext, useState, createRef} from 'react';
import { useNavigate } from 'react-router-dom';
import { SetupContext } from '../../contexts/setup-context';
import { HeaderContext } from "../../contexts/header-context";
import { SetupContextType, IPosition, HeaderContextType, ImageResponseType } from '../../types';
import {getSampleZoneStartEndXCoordinates, processRefValue, validateReference} from '../../util/util';
import { CAMERA_NAME_QUERY, GET_IMAGE_ENDPOINT, IMG_HEIGHT, IMG_WIDTH, RASPBERRY_PI_BASE_URL } from '../../constants/app-constants';
import Header from "../../components/header/header";
import axios from "axios";
import Button from '../../components/button/button';
import Input from '../../components/input/input';


const Setup: React.FC = () => {

    const { cameraName,
        sampleZonePercent,
        startPosition,
        endPosition,
        currentPosition,
        actualDistanceFeet,
        imageDistanceInches,
        setSampleZonePercent,
        modifyCurrentPositon,
        addPosition,
        addActualDistance,
        clearPositions } = useContext(SetupContext) as SetupContextType;

    const { setStep } = useContext(HeaderContext) as HeaderContextType;
    const navigate = useNavigate();

    const {startX, endX} = getSampleZoneStartEndXCoordinates(sampleZonePercent);

    const [ imageFile, setImageFile ] = useState<string>("");
    const [ sampleZoneStartX, setSampleZoneStartX ] = useState<number>(startX);
    const [ sampleZoneEndX, setSampleZoneEndX ] = useState<number>(endX);
    const [ distanceValid, setDistanceValid ] = useState<boolean>(true);
    const [ sampleZoneValid, setSampleZoneValid ] = useState<boolean>(true);
    const [ imageDistanceErrorColor, setImageDistanceErrorColor ] =useState<string>("")

    const actualDistanceRef =  createRef<HTMLInputElement>();
    const sampleZoneRef =  createRef<HTMLInputElement>();
    const svgRef = useRef<SVGSVGElement>(null);

    const getImage = async () => {
        let imageURL = "";
        if(cameraName) {
            imageURL = `${RASPBERRY_PI_BASE_URL}/${GET_IMAGE_ENDPOINT}?${CAMERA_NAME_QUERY}=${cameraName.replace(" ","-")}`;
            axios.get<ImageResponseType>(encodeURI(imageURL))
            .then((response) => {
                const { image } = response.data;
                setImageFile(image);
            })
        }
    }

    const getPosition = ( event: React.MouseEvent<Element> ) : IPosition => {
        let cursorPosition = {x:0, y:0}
        const position = svgRef?.current?.createSVGPoint();
        if(position){
            position.x = event.clientX;
            position.y = event.clientY
            cursorPosition = position.matrixTransform(svgRef?.current?.getScreenCTM()?.inverse()) || {x:0,y:0}
        }

        return {x: Math.floor(cursorPosition.x), y: Math.floor(cursorPosition.y)}
    }

    const handleClick = (event: React.MouseEvent<Element>) => {
        modifyCurrentPositon(getPosition(event));
    }

    const handleDoubleClick = (event: React.MouseEvent<Element>) => {
        addPosition(getPosition(event));
    }

    const handleActualDistanceChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        addActualDistance(event.target.value);
    }

    const handleSampleZonePercentChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setSampleZonePercent(event.target.value);
    }

    const updateZoneDisplay = () => {
        if ( validateReference(sampleZoneRef) ) {
            const {startX, endX} = getSampleZoneStartEndXCoordinates( processRefValue(sampleZoneRef) );
            setSampleZoneStartX(startX);
            setSampleZoneEndX(endX);
        }
    }

    const clear = () => {
        clearPositions();
        addActualDistance("0.0");
    }

    const calibrate = () => {
        const actualDistanceCurrentValue = processRefValue(actualDistanceRef);
        const sampleZoneCurrentValue = processRefValue(sampleZoneRef);
        setDistanceValid(validateReference(actualDistanceRef));
        setSampleZoneValid(validateReference(sampleZoneRef));
        if ( imageDistanceInches <= 0.0 ){
            setImageDistanceErrorColor('bg-red');
        } else {
            setImageDistanceErrorColor('');
        }
        if(parseFloat( actualDistanceCurrentValue ) > 0.0 && parseFloat( sampleZoneCurrentValue ) > 0.0) {
            setSampleZonePercent(sampleZoneCurrentValue);
            addActualDistance(actualDistanceCurrentValue);
            setStep(2);
            navigate('/monitor');
        }
    }

	return (
        <>
        <Header />
        <div className="flex flex-col m-3 justify-center">
            <div className="flex justify-center">
                {
                    imageFile
                        ? <svg className='w-1/2 m-3'
                            onClick={handleClick}
                            onDoubleClick={handleDoubleClick}
                            ref={svgRef}
                            viewBox={`0 0 ${IMG_WIDTH} ${IMG_HEIGHT}`} xmlns="http://www.w3.org/2000/svg">
                            <defs>
                                <rect id="rect" x="0%" y="0%" width="100%" height="100%" rx="30"/>
                                <clipPath id="clip">
                                <use xlinkHref="#rect"/>
                                </clipPath>
                            </defs>
                            <image className='rounded' xlinkHref={imageFile} height={IMG_HEIGHT} width={IMG_WIDTH} clipPath="url(#clip)" />
                            {
                                startPosition.x > 0 && startPosition.y > 0 &&
                                <circle cx={startPosition.x} cy={startPosition.y} r="20" stroke="#FACC15" strokeWidth="3" fill="none"/>
                            }
                            {
                                endPosition.x > 0 && endPosition.y > 0 &&
                                <circle cx={endPosition.x} cy={endPosition.y} r="20" stroke="#FACC15" strokeWidth="3" fill="none"/>
                            }
                            {
                                startPosition.x > 0 && startPosition.y > 0 &&
                                endPosition.x > 0 && endPosition.y > 0 &&
                                <line x1={startPosition.x} y1={startPosition.y} x2={endPosition.x} y2={endPosition.y} stroke="#FACC15" strokeWidth="3"/>
                            }
                            {
                                parseFloat(sampleZonePercent) > 0.0 &&
                                <line x1={sampleZoneStartX} y1={0} x2={sampleZoneStartX} y2={IMG_HEIGHT} stroke="#3C73EF" strokeWidth="3" />
                            }
                            {
                                parseFloat(sampleZonePercent) > 0.0 &&
                                <line x1={sampleZoneEndX} y1={0} x2={sampleZoneEndX} y2={IMG_HEIGHT} stroke="#3C73EF" strokeWidth="3" />
                            }
                        </svg>
                        : <div className='w-1/2 h-[50vh] m-3 bg-grey rounded flex justify-center align-middle'>
                            <Button text='Get Image' onClickMethod={getImage} additionalClassNames='h-10 self-center'/>
                        </div>
                }
            </div>
            <div className='flex w-1/4 flex-col self-center justify-center'>
                <h3 className='text-center'>X: {currentPosition.x}  Y: {currentPosition.y}</h3>
                <div className='flex'>
                    <h3 className='flex-grow text-start'>Start: (x: {startPosition.x}, y: {startPosition.y})</h3>
                    <h3 className='flex-grow text-end'>End: (x: {endPosition.x}, y: {endPosition.y})</h3>
                </div>
                <div className='flex'>
                    <h3 className={`w-1/3 ${imageDistanceErrorColor}`}>Inches: {imageDistanceInches.toFixed(2)}</h3>
                    <div className='flex-grow text-end'>
                        <Input
                            label='Actual Distance (ft):'
                            id='actual-distance'
                            width='w-12'
                            value={actualDistanceFeet}
                            onChange={handleActualDistanceChange}
                            isValid={distanceValid}
                            ref={actualDistanceRef}
                        />
                    </div>
                </div>
                <div className='flex py-2 items-center'>
                    <Input
                        label='Sample Zone %:'
                        id='sample-zone'
                        width='w-12'
                        value={sampleZonePercent}
                        onChange={handleSampleZonePercentChange}
                        isValid={sampleZoneValid}
                        ref={sampleZoneRef}
                    />
                    <div className='flex-grow justify-end text-end'>
                        <Button text='Update Zone' onClickMethod={updateZoneDisplay} />
                    </div>
                </div>
                <div className='flex w-full p-2'>
                    <div className='flex-grow justify-start'>
                        <Button text='Clear' onClickMethod={clear} />
                    </div>
                    <div className='flex-grow justify-end text-end'>
                        <Button text='Next' onClickMethod={calibrate} />
                    </div>
                </div>
            </div>
        </div>
        </>
	);
};

export default Setup;