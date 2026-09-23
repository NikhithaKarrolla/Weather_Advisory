def generate_personalized_notifications(
    farmer,
    current_weather,
    forecast
):

    notifications = []

    crop = farmer["crop"]
    growth_stage = farmer.get("growth_stage")
    planned_activity = farmer.get("planned_activity")
    location = farmer["location"]

    # ---------------------------------------------------------
    # FORECAST ANALYSIS
    # ---------------------------------------------------------

    max_rain_probability = max(
        item["rain_probability"]
        for item in forecast
    )

    total_rainfall = sum(
        item["rainfall"]
        for item in forecast
    )

    max_humidity = max(
        item["humidity"]
        for item in forecast
    )

    max_wind = max(
        item.get("wind_speed", 0)
        for item in forecast
    ) if forecast else current_weather["wind_speed"]

    # ---------------------------------------------------------
    # IRRIGATION
    # ---------------------------------------------------------

    if (
        planned_activity
        and planned_activity.lower() == "irrigation"
        and max_rain_probability >= 60
    ):

        notifications.append({
            "type": "irrigation",
            "priority": "medium",

            "title": f"{crop} Irrigation Advisory",

            "message": (
                f"Rain probability is {max_rain_probability:.0f}% "
                f"in {location}. Rainfall is expected during the "
                f"upcoming forecast period. Consider delaying "
                f"irrigation for your {crop} crop."
            ),

            "action": "Consider delaying irrigation",

            "reason": (
                f"Rain probability: {max_rain_probability:.0f}%, "
                f"expected rainfall: {total_rainfall:.1f} mm"
            ),

            "crop": crop,
            "activity": "irrigation"
        })

    # ---------------------------------------------------------
    # SPRAYING + RAIN
    # ---------------------------------------------------------

    if (
        planned_activity
        and planned_activity.lower() == "spraying"
        and max_rain_probability >= 60
    ):

        stage_message = ""

        if growth_stage:
            stage_message = (
                f" Your {crop} crop is currently in the "
                f"{growth_stage} stage."
            )

        notifications.append({
            "type": "spraying",
            "priority": "high",

            "title": f"{crop} Spraying Advisory",

            "message": (
                f"Rain probability is {max_rain_probability:.0f}% "
                f"in {location}. Consider postponing the planned "
                f"spraying activity to avoid expected rainfall."
                f"{stage_message}"
            ),

            "action": "Consider postponing spraying",

            "reason": (
                f"Rain probability: "
                f"{max_rain_probability:.0f}%"
            ),

            "crop": crop,
            "activity": "spraying"
        })

    # ---------------------------------------------------------
    # HARVESTING + RAIN
    # ---------------------------------------------------------

    if (
        planned_activity
        and planned_activity.lower() == "harvesting"
        and max_rain_probability >= 70
    ):

        notifications.append({
            "type": "harvesting",
            "priority": "high",

            "title": f"{crop} Harvest Advisory",

            "message": (
                f"Rain probability is {max_rain_probability:.0f}% "
                f"in {location}. Review your planned harvesting "
                f"schedule before starting field operations."
            ),

            "action": "Review harvesting schedule",

            "reason": (
                f"Rain probability: "
                f"{max_rain_probability:.0f}%"
            ),

            "crop": crop,
            "activity": "harvesting"
        })

    # ---------------------------------------------------------
    # HIGH HUMIDITY
    # ---------------------------------------------------------

    if max_humidity >= 85:

        stage_message = ""

        if growth_stage:
            stage_message = (
                f" Your {crop} crop is in the "
                f"{growth_stage} stage."
            )

        notifications.append({
            "type": "humidity",
            "priority": "medium",

            "title": f"{crop} Humidity Advisory",

            "message": (
                f"High humidity is expected in {location}. "
                f"Monitor your {crop} crop for signs of "
                f"humidity-related disease."
                f"{stage_message}"
            ),

            "action": "Monitor crop condition",

            "reason": (
                f"Forecast humidity: {max_humidity}%"
            ),

            "crop": crop,
            "activity": None
        })

    # ---------------------------------------------------------
    # STRONG WIND
    # ---------------------------------------------------------

    if max_wind >= 25:

        notifications.append({
            "type": "wind",
            "priority": "high",

            "title": f"{crop} Wind Advisory",

            "message": (
                f"Strong winds are expected in {location}. "
                f"Consider postponing spraying and other "
                f"wind-sensitive field activities."
            ),

            "action": "Avoid wind-sensitive activities",

            "reason": (
                f"Forecast wind speed: {max_wind:.1f} km/h"
            ),

            "crop": crop,
            "activity": planned_activity
        })

    return notifications