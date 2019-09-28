import axios from 'axios';

/**
 * Contains the common application-wide static environment.
 */
export default class Environment {
  constructor(publicUrl) {
    this._axiosInstance = axios.create({ baseURL: 'http://localhost:5000', timeout: 30000 });
  }

  get axios() {
    return this._axiosInstance;
  }
}
