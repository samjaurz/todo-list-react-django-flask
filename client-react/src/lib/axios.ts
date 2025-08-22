import axios, { AxiosInstance  } from 'axios';

const urlDjango = "http://127.0.0.1:8000/";
const urlFlask = "http://127.0.0.1:5000/";

const djangoApi = axios.create({
    baseURL: urlDjango,
    timeout: 10000,
    headers: {"Content-Type": "application/json"},
});

const flaskApi = axios.create({
    baseURL: urlFlask,
    withCredentials: true,
    timeout: 10000,
    headers: {
        "Content-Type": "application/json"
    },
});


flaskApi.interceptors.request.use(
    (config) => {
        const token = sessionStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    }
);


function getApiInstance(useDjango: boolean): AxiosInstance {
    return useDjango ? djangoApi : flaskApi;
}

export default getApiInstance;