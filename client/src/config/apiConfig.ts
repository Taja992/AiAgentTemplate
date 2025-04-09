



export const API_CONFIG = {

baseURL: import.meta.env.PROD
    ? 'https://whateverdeployment.com' // put production URL here
    : 'http://localhost:8000',


    timeout: 30000, // 30 seconds timeout for requests

    withCredentials: true, // include cookies in requests
};