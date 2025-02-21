import { create } from 'zustand';
import { TravelDetails, TravelerDetails, SpecialFare } from '../types';

interface FlightSearchState {
  travelDetails: TravelDetails;
  travelerDetails: TravelerDetails;
  specialFares: SpecialFare[];
  setTravelDetails: (details: Partial<TravelDetails>) => void;
  setTravelerDetails: (details: Partial<TravelerDetails>) => void;
  toggleSpecialFare: (fareId: number) => void;
}

export const useFlightSearchStore = create<FlightSearchState>((set) => ({
  travelDetails: {
    travelType: 'one-way',
    from: '',
    to: '',
    departureDate: '',
  },
  travelerDetails: {
    adults: 1,
    children: 0,
    infants: 0,
    travelClass: 'Economy',
  },
  specialFares: [],
  
  setTravelDetails: (details) => set((state) => ({
    travelDetails: { ...state.travelDetails, ...details }
  })),
  
  setTravelerDetails: (details) => set((state) => ({
    travelerDetails: { ...state.travelerDetails, ...details }
  })),
  
  toggleSpecialFare: (fareId) => set((state) => ({
    specialFares: state.specialFares.map(fare => 
      fare.id === fareId ? { ...fare, isSelected: !fare.isSelected } : fare
    )
  }))
}));