from pydantic import BaseModel
from typing import List, Optional


class CurrentWeather(BaseModel):
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    condition: str
    description: str


class ForecastItem(BaseModel):
    date: str
    temperature: float
    humidity: int
    rain_probability: float
    rainfall: float
    condition: str


class WeatherAlert(BaseModel):
    type: str
    severity: str
    message: str


class WeatherResponse(BaseModel):
    location: str
    current: CurrentWeather
    forecast: List[ForecastItem]
    alerts: List[WeatherAlert]