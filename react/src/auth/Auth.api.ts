import axios from 'axios';
declare var csrf_token:string;

export const signIn = (username:string, password:string) => axios.post('/api/token-auth/', {
  username:username,
  password:password
}).then(res => {
  axios.defaults.headers.common['Authorization'] = 'JWT ' + res.data.token;
  sessionStorage.setItem('token', res.data.token);
  return Promise.all([axios.get('/api-user/?self=true'), res]);
})

export const signUp = (username:string, email:string, password:string) => {
  return axios.post('/api-user/', {
    username:username,
    email:email,
    password:password
  })
}

export const setToken = (token:string|null) => {
  axios.defaults.headers.common['X-CSRFToken'] = csrf_token;
  if (token === null) {
    delete axios.defaults.headers.common['Authorization'];
    return Promise.all([null, null]);
  } else {
    axios.defaults.headers.common['Authorization'] = 'JWT ' + token;
    return Promise.all([axios.get('/api-user/?self=true'), token]);
  }
}

export const signOut = () => {
  delete axios.defaults.headers.common['Authorization'];
  sessionStorage.removeItem('token');
  return undefined;
}