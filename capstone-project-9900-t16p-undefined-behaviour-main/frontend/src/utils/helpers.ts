import config from '../config.json';
// import { getToken } from './token';

export const apiCall = (path: string, data: object, method: string) => {
  // Main function used to interact with the backend
  return new Promise((resolve, reject) => {
    const csrfCookie = document.cookie.replace(/(?:(?:^|.*;\s*)csrf_access_token\s*\=\s*([^;]*).*$)|^.*$/, "$1");
    fetch(`${config.BASE_URL}${config.BACKEND_PORT}${path}/`, {
      method: method,
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRF-TOKEN': csrfCookie,
      },
      body: method !== 'GET' ? JSON.stringify(data) : undefined,
    })
      .then(res => {
        if (res.status === 200) return res.json().then(resolve);
        else if (res.status === 400 || res.status === 401) {
          return res.json().then(err => {
            console.log('Error fetching', err);
            reject(err);
          })
        }
      })
  })
}


export function fileToDataUrl(file: File) {
    const validFileTypes = ['image/jpeg', 'image/png', 'image/jpg']
    if (!validFileTypes.find(type => type === file.type)) {
        throw Error("Invalid file type")
    }
    const reader = new FileReader()
    const dataUrlPromise = new Promise((resolve, reject) => {
        reader.onerror = reject;
        reader.onload = () => resolve(reader.result)
    })
    reader.readAsDataURL(file)
    return dataUrlPromise
}

export function makeRestaurantName(name: string)  {
  return name.replaceAll(' ', '_');
}

export function decodeRestaurantName(name: string | undefined) {
  if (name === undefined) {return ''}
  return name.replaceAll('_', ' ')
}