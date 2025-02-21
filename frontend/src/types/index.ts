// Flight Booking Types

export interface TravelDetails {
  travelType: 'one-way' | 'round-trip' | 'multi-city';
  from: string;
  to: string;
  departureDate: string;
  returnDate?: string;
}

export interface TravelerDetails {
  adults: number;
  children: number;
  infants: number;
  travelClass: 'Economy' | 'Premium Economy' | 'Business' | 'First Class';
}

export interface SpecialFare {
  id: number;
  type: string;
  description: string;
  isSelected: boolean;
}

export interface FlightSearchFormData {
  travel: TravelDetails;
  travelers: TravelerDetails;
  specialFares: SpecialFare[];
}