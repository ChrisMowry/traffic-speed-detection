import { StepType } from "../types";

export const RASPBERRY_PI_IP = process.env.REACT_APP_PI_IP;
export const CLIENT_PORT = process.env.REACT_APP_PI_CLIENT_PORT;
export const RASPBERRY_PI_BASE_URL = `http://${RASPBERRY_PI_IP}:${CLIENT_PORT}`
export const GET_IMAGE_ENDPOINT = process.env.REACT_APP_PI_CLIENT_CALIBRATE_ENDPOINT;
export const MONITOR_ENDPOINT = process.env.REACT_APP_PI_CLIENT_START_MONITORING_ENDPOINT;
export const CAMERA_NAME_QUERY = process.env.REACT_APP_CALIBRATE_QUERY_CAMERA_NAME;
export const SAMPLE_ZONE_QUERY = process.env.REACT_APP_CALIBRATE_QUERY_SAMPLE_ZONE;
export const SPEED_LIMIT_QUERY = process.env.REACT_APP_CALIBRATE_QUERY_SPEED_LIMIT;
export const STOP_MONITOR = process.env.REACT_APP_CALIBRATE_QUERY_STOP_MONITOR;
export const DISTANCE_RATIO_QUERY = process.env.REACT_APP_CALIBRATE_QUERY_DISTANCE_RATIO;
export const IMG_HEIGHT = process.env.REACT_APP_IMG_HEIGHT || "0";
export const IMG_WIDTH = process.env.REACT_APP_IMG_WIDTH || "0";

export const STEPS : StepType[] = [
    {
        id: 0,
        label: "Introduction",
        path: "/"
    },
    {
        id: 1,
        label: "Setup",
        path: "/setup"
    },
    {
        id: 2,
        label: "Monitor",
        path: "/monitor"
    },
];


