import axios, {AxiosInstance}from "axios";

const urlDjango = "http://127.0.0.1:8000/";
const urlFlask = "http://127.0.0.1:5000/";

const djangoApi = axios.create({
  baseURL: urlDjango,
  timeout: 10000,
  headers: { "Content-Type": "application/json" },
});

const flaskApi = axios.create({
  baseURL: urlFlask,
  timeout: 10000,
  headers: { "Content-Type": "application/json" },
});

function getApiInstance(useDjango: boolean): AxiosInstance {
  return useDjango ? djangoApi : flaskApi;
}

export default getApiInstance;