import axios from 'axios';

/**
 * Contains the common application-wide static environment.
 */
export default class Environment {
  constructor(publicUrl) {
    var url = new URL(publicUrl);
    url.port = 5000; // The port on which the service is running

    this._axiosInstance = axios.create({ baseURL: url.href, timeout: 30000 });
  }

  get axios() {
    return this._axiosInstance;
  }
}
