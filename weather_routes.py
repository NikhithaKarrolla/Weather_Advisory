from notification_models import (
    WeatherAdvisoryRequest,
    AdvisoryResponse
)

from advisory_engine import generate_personalized_notifications

from fastapi import APIRouter, HTTPException

from weather_service import (
    get_current_weather,
    get_forecast
)

from weather_alerts import generate_weather_alerts


router = APIRouter(
    prefix="/api/weather",
    tags=["Weather Advisory"]
)
@router.post("/advisory", response_model=AdvisoryResponse)
def personalized_weather_advisory(
    request: WeatherAdvisoryRequest
):

    try:

        # -------------------------------------------------
        # GET WEATHER
        # -------------------------------------------------

        current_data = get_current_weather(
            request.lat,
            request.lon
        )

        forecast_data = get_forecast(
            request.lat,
            request.lon
        )

        # -------------------------------------------------
        # CURRENT WEATHER
        # -------------------------------------------------

        current = current_data["main"]

        current_weather = {
            "temperature": current["temp"],
            "feels_like": current["feels_like"],
            "humidity": current["humidity"],
            "wind_speed": current_data["wind"]["speed"],
            "condition": current_data["weather"][0]["main"],
            "description": current_data["weather"][0]["description"]
        }

        # -------------------------------------------------
        # FORECAST
        # -------------------------------------------------

        forecast = []

        for item in forecast_data["list"][:8]:

            forecast.append({
                "date": item["dt_txt"],
                "temperature": item["main"]["temp"],
                "humidity": item["main"]["humidity"],
                "rain_probability": item.get("pop", 0) * 100,
                "rainfall": item.get(
                    "rain", {}
                ).get("3h", 0),
                "condition": item["weather"][0]["description"]
            })

        # -------------------------------------------------
        # PERSONALIZED NOTIFICATIONS
        # -------------------------------------------------

        farmer = request.farmer.model_dump()

        notifications = generate_personalized_notifications(
            farmer=farmer,
            current_weather=current_weather,
            forecast=forecast
        )

        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return {
            "location": request.farmer.location,
            "crop": request.farmer.crop,
            "notifications": notifications
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("")
def weather_advisory(
    lat: float,
    lon: float
):

    try:

        # -------------------------------------------------
        # GET WEATHER DATA
        # -------------------------------------------------

        current_data = get_current_weather(lat, lon)
        forecast_data = get_forecast(lat, lon)

        current = current_data["main"]

        # -------------------------------------------------
        # CURRENT WEATHER
        # -------------------------------------------------

        current_weather = {
            "temperature": current["temp"],
            "feels_like": current["feels_like"],
            "humidity": current["humidity"],
            "wind_speed": current_data["wind"]["speed"],
            "condition": current_data["weather"][0]["main"],
            "description": current_data["weather"][0]["description"]
        }

        # -------------------------------------------------
        # FORECAST
        # -------------------------------------------------

        forecast = []

        for item in forecast_data["list"][:8]:

            forecast.append({
                "date": item["dt_txt"],
                "temperature": item["main"]["temp"],
                "humidity": item["main"]["humidity"],
                "rain_probability": item.get("pop", 0) * 100,
                "rainfall": item.get("rain", {}).get("3h", 0),
                "condition": item["weather"][0]["description"]
            })

        # -------------------------------------------------
        # WEATHER ALERTS
        # -------------------------------------------------

        alerts = generate_weather_alerts(
            current_temperature=current["temp"],
            current_humidity=current["humidity"],
            current_wind_speed=current_data["wind"]["speed"],
            forecast=forecast
        )

        # -------------------------------------------------
        # FINAL RESPONSE
        # -------------------------------------------------

        return {
            "location": current_data["name"],
            "current": current_weather,
            "forecast": forecast,
            "alerts": alerts
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )