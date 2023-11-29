import axios from 'axios';

class HttpRequestUtils {
  // Set up your default config here
  static axiosInstance = axios.create({
    baseURL: 'http://localhost:8000', // Replace with your API's base URL
    timeout: 1000, // Request timeout
    headers: {
      'Content-Type': 'application/json',
      // Include other headers if needed
    },
  });

  static setToken(token) {
    // Set the token in the default headers
    this.axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }

  static get(url, config = {}) {
    return this.axiosInstance.get(url, config);
  }

  static post(url, data, config = {}) {
    return this.axiosInstance.post(url, data, config);
  }

  static put(url, data, config = {}) {
    return this.axiosInstance.put(url, data, config);
  }

  static delete(url, config = {}) {
    return this.axiosInstance.delete(url, config);
  }

  static patch(url, data, config = {}) {
    return this.axiosInstance.patch(url, data, config);
  }

  // You can also add other utility methods that you think you'll need frequently
}

export default HttpRequestUtils;
