import axios from 'axios';
export const api=axios.create({baseURL:'http://localhost:8000/api/v1'});
api.interceptors.request.use(c=>{const t=localStorage.getItem('token'); if(t)c.headers.Authorization=`Bearer ${t}`; return c});
