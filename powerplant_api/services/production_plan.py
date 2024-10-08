from typing import Dict,List
from models import FuelData,PowerPlantData

class PowerDistributionCalculator():
    """Class to calculate power distribution among various power plants"""
    def __init__(self, load: int, fuels: FuelData, powerplants: List[PowerPlantData]):
        self.fuels = fuels
        self.powerplants = powerplants
        self.remaining_load = load
        self.response = []

    def _calculate_cost_efficiency(self,plant:Dict) -> float:
        """Cost efficiency evaluation"""
        if plant.type == "windturbine":
            return 0 
        elif plant.type == "gasfired":
            return self.fuels.gas / plant.efficiency
        elif plant.type == "turbojet":
            return self.fuels.kerosine / plant.efficiency
        else: 
            raise ValueError(f"Wrong power plant type, type unknown {plant.type}")
        
    def _sort_by_cost_efficiency(self,powerplants:List) -> List:
        """Sorting power plants based on efficiency
        
        Built-in sorted method with cost_efficiency as parameter"""
        return sorted(powerplants, key=self._calculate_cost_efficiency)
    
    @staticmethod    
    def _get_min_max_power(plant:Dict, load_data: int) -> float:
        """Power to be generated by power plant, taking in account min and max power emission"""
        return min(max(plant.pmin, load_data), plant.pmax)
    
    def _calculate_power(self, plant:Dict) -> float:
        if plant.type == "windturbine":
            power = min(plant.pmax * self.fuels.wind, self.remaining_load) # Calculating power based on wind power
        else:
            power = self._get_min_max_power(plant, self.remaining_load) # Calculating max power output based on remaing load
        return round(power,1)

    def get_response(self):
        """Calculate power distribution to all power plants"""
        sorted_powerplants = self._sort_by_cost_efficiency(self.powerplants)
        for plant in sorted_powerplants:
            if self.remaining_load <= 0: 
                self.response.append({'name':plant.name,'p':0.0}) # Power emission is 0 if the remaining load is 0 or less
                continue
            power = self._calculate_power(plant)
            if self.remaining_load < plant.pmin: # If min power emission is more than remaining load, plant does not emit any power
                power = 0.0
            self.response.append({'name':plant.name,'p':power})
            self.remaining_load -= power # Reducing load on every iteration
        return self.response

