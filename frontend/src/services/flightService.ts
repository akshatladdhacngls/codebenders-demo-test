import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

export const flightService = {
  async searchFlights(params: {
    departure_city: string;
    arrival_city: string;
    departure_date: string;
    return_date?: string;
    travel_class?: string;
  }) {
    try {
      const response = await axios.get(`${BASE_URL}/flights`, { params });
      return response.data;
    } catch (error) {
      console.error('Flight search error:', error);
      throw error;
    }
  },

  async getSpecialFares() {
    try {
      const response = await axios.get(`${BASE_URL}/fares`);
      return response.data;
    } catch (error) {
      console.error('Special fares fetch error:', error);
      throw error;
    }
  }
};