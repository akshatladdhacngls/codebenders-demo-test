import React, { useState, useEffect } from 'react';
import { 
  Box, 
  TextField, 
  Button, 
  Radio, 
  RadioGroup, 
  FormControlLabel, 
  FormControl, 
  FormLabel,
  Modal,
  Typography,
  Checkbox
} from '@mui/material';
import { SwapHoriz, Search } from '@mui/icons-material';
import { useForm, Controller } from 'react-hook-form';
import { useFlightSearchStore } from '../stores/flightSearchStore';
import { flightService } from '../services/flightService';
import { SpecialFare } from '../types';

const FlightSearchForm: React.FC = () => {
  const { 
    travelDetails, 
    travelerDetails, 
    specialFares, 
    setTravelDetails, 
    setTravelerDetails 
  } = useFlightSearchStore();

  const [openTravelersModal, setOpenTravelersModal] = useState(false);
  const [availableSpecialFares, setAvailableSpecialFares] = useState<SpecialFare[]>([]);

  const { control, handleSubmit, setValue, watch } = useForm({
    defaultValues: {
      travelType: 'one-way',
      from: '',
      to: '',
      departureDate: '',
      returnDate: '',
      adults: 1,
      children: 0,
      infants: 0,
      travelClass: 'Economy'
    }
  });

  useEffect(() => {
    const fetchSpecialFares = async () => {
      try {
        const fares = await flightService.getSpecialFares();
        setAvailableSpecialFares(fares.map((fare: any) => ({
          ...fare,
          isSelected: false
        })));
      } catch (error) {
        console.error('Failed to fetch special fares');
      }
    };

    fetchSpecialFares();
  }, []);

  const onSubmit = async (data: any) => {
    try {
      const searchParams = {
        departure_city: data.from,
        arrival_city: data.to,
        departure_date: data.departureDate,
        return_date: data.returnDate,
        travel_class: data.travelClass
      };

      const flights = await flightService.searchFlights(searchParams);
      console.log('Flight search results:', flights);
    } catch (error) {
      console.error('Flight search failed');
    }
  };

  const swapLocations = () => {
    const currentFrom = watch('from');
    const currentTo = watch('to');
    setValue('from', currentTo);
    setValue('to', currentFrom);
  };

  return (
    <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ maxWidth: 600, margin: 'auto' }}>
      <FormControl>
        <FormLabel>Travel Type</FormLabel>
        <Controller
          name="travelType"
          control={control}
          render={({ field }) => (
            <RadioGroup 
              row 
              {...field} 
              onChange={(e) => {
                field.onChange(e);
                setTravelDetails({ travelType: e.target.value });
              }}
            >
              <FormControlLabel value="one-way" control={<Radio />} label="One Way" />
              <FormControlLabel value="round-trip" control={<Radio />} label="Round Trip" />
              <FormControlLabel value="multi-city" control={<Radio />} label="Multi-City" />
            </RadioGroup>
          )}
        />
      </FormControl>

      <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
        <Controller
          name="from"
          control={control}
          render={({ field }) => (
            <TextField 
              {...field} 
              label="From" 
              variant="outlined" 
              fullWidth 
              onChange={(e) => {
                field.onChange(e);
                setTravelDetails({ from: e.target.value });
              }}
            />
          )}
        />
        <Button onClick={swapLocations} variant="outlined" sx={{ minWidth: 50 }}>
          <SwapHoriz />
        </Button>
        <Controller
          name="to"
          control={control}
          render={({ field }) => (
            <TextField 
              {...field} 
              label="To" 
              variant="outlined" 
              fullWidth 
              onChange={(e) => {
                field.onChange(e);
                setTravelDetails({ to: e.target.value });
              }}
            />
          )}
        />
      </Box>

      <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
        <Controller
          name="departureDate"
          control={control}
          render={({ field }) => (
            <TextField 
              {...field} 
              label="Departure Date" 
              type="date" 
              variant="outlined" 
              fullWidth 
              InputLabelProps={{ shrink: true }}
              onChange={(e) => {
                field.onChange(e);
                setTravelDetails({ departureDate: e.target.value });
              }}
            />
          )}
        />
        {travelDetails.travelType !== 'one-way' && (
          <Controller
            name="returnDate"
            control={control}
            render={({ field }) => (
              <TextField 
                {...field} 
                label="Return Date" 
                type="date" 
                variant="outlined" 
                fullWidth 
                InputLabelProps={{ shrink: true }}
                onChange={(e) => {
                  field.onChange(e);
                  setTravelDetails({ returnDate: e.target.value });
                }}
              />
            )}
          />
        )}
      </Box>

      <Button 
        onClick={() => setOpenTravelersModal(true)} 
        variant="outlined" 
        fullWidth 
        sx={{ mt: 2 }}
      >
        {`${travelerDetails.adults} Adults, ${travelerDetails.children} Children, ${travelerDetails.infants} Infants, ${travelerDetails.travelClass}`}
      </Button>

      <Modal open={openTravelersModal} onClose={() => setOpenTravelersModal(false)}>
        <Box sx={{ 
          position: 'absolute', 
          top: '50%', 
          left: '50%', 
          transform: 'translate(-50%, -50%)', 
          width: 400, 
          bgcolor: 'background.paper', 
          boxShadow: 24, 
          p: 4 
        }}>
          <Typography variant="h6">Travelers & Class</Typography>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 2 }}>
            <Typography>Adults</Typography>
            <Box>
              <Button 
                onClick={() => {
                  const currentAdults = watch('adults');
                  setValue('adults', Math.max(1, currentAdults - 1));
                  setTravelerDetails({ adults: Math.max(1, currentAdults - 1) });
                }}
              >
                -
              </Button>
              {watch('adults')}
              <Button 
                onClick={() => {
                  const currentAdults = watch('adults');
                  setValue('adults', currentAdults + 1);
                  setTravelerDetails({ adults: currentAdults + 1 });
                }}
              >
                +
              </Button>
            </Box>
          </Box>
          {/* Similar controls for children and infants */}
          <FormControl fullWidth sx={{ mt: 2 }}>
            <FormLabel>Travel Class</FormLabel>
            <Controller
              name="travelClass"
              control={control}
              render={({ field }) => (
                <RadioGroup 
                  row 
                  {...field} 
                  onChange={(e) => {
                    field.onChange(e);
                    setTravelerDetails({ travelClass: e.target.value });
                  }}
                >
                  <FormControlLabel value="Economy" control={<Radio />} label="Economy" />
                  <FormControlLabel value="Business" control={<Radio />} label="Business" />
                </RadioGroup>
              )}
            />
          </FormControl>
          <Button 
            onClick={() => setOpenTravelersModal(false)} 
            variant="contained" 
            fullWidth 
            sx={{ mt: 2 }}
          >
            Done
          </Button>
        </Box>
      </Modal>

      <Box sx={{ mt: 2 }}>
        <Typography variant="h6">Special Fares</Typography>
        {availableSpecialFares.map((fare) => (
          <FormControlLabel
            key={fare.id}
            control={
              <Checkbox
                checked={fare.isSelected}
                onChange={() => {
                  const updatedFares = availableSpecialFares.map(f => 
                    f.id === fare.id ? { ...f, isSelected: !f.isSelected } : f
                  );
                  setAvailableSpecialFares(updatedFares);
                }}
              />
            }
            label={`${fare.type} - ${fare.description}`}
          />
        ))}
      </Box>

      <Button 
        type="submit" 
        variant="contained" 
        color="primary" 
        fullWidth 
        sx={{ mt: 2 }}
        startIcon={<Search />}
      >
        Search Flights
      </Button>
    </Box>
  );
};

export default FlightSearchForm;