import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000/api';

export async function getAllUsers() {
  const response = await axios.get(`${API_URL}/users`);
  return response.data; 
}

export async function getUserById(userId) {
  const response = await axios.get(`${API_URL}/users/${userId}`);
  return response.data; 
}

export async function createUser(userData) {
  const response = await axios.post(`${API_URL}/users`, userData);
  return response.data;
}

export async function updateUser(userId, userData) {
  const response = await axios.put(`${API_URL}/users/${userId}`, userData);
  return response.data;
}

export async function deleteUser(userId) {
  const response = await axios.delete(`${API_URL}/users/${userId}`);
  return response.data;
}
