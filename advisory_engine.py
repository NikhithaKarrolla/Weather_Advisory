from crop_profiles import CROP_PROFILES


def generate_personalized_notifications(
    farmer,
    current_weather,
    forecast
):

    notifications = []

    crop = farmer["crop"].lower()
    growth_stage = farmer.get("growth_stage")
    planned_activity = farmer.get("planned_activity")
    location = farmer["location"]

    crop_profile = CROP_PROFILES.get(
        crop,
        {
            "name": farmer["crop"],
            "activities": [],
            "high_humidity_monitoring": False
        }
    )

    crop_name = crop_profile["name"]

    # ---------------------------------------------------------
    # FIND FORECAST CONDITIONS
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

    # ---------------------------------------------------------
    # RAIN + IRRIGATION
    # ---------------------------------------------------------

    if (
        planned_activity == "irrigation"
        and max_rain_probability >= 60
    ):

        notifications.append({

            "type": "irrigation",
            "priority": "medium",

            "title": f"{crop_name} Irrigation Advisory",

            "message": (
                f"Rain probability is {max_rain_probability:.0f}% "
                f"at {location}. Rainfall is expected during the "
                f"upcoming forecast period. Consider delaying the "
                f"planned irrigation for your {crop_name} crop."
            ),

            "action": "Consider delaying irrigation",

            "reason": (
                f"Rain probability: {max_rain_probability:.0f}%, "
                f"expected rainfall: {total_rainfall:.1f} mm"
            ),

            "crop": crop_name,
            "activity": "irrigation"
        })

    # ---------------------------------------------------------
    # RAIN + SPRAYING
    # ---------------------------------------------------------

    if (
        planned_activity == "spraying"
        and max_rain_probability >= 60
    ):

        stage_text = ""

        if growth_stage:
            stage_text = (
                f" Your crop is currently in the "
                f"{growth_stage} stage."
            )

        notifications.append({

            "type": "spraying",
            "priority": "high",

            "title": f"{crop_name} Spraying Advisory",

            "message": (
                f"Rain probability is {max_rain_probability:.0f}% "
                f"in {location}. Avoid scheduling the planned "
                f"spraying close to the expected rainfall."
                f"{stage_text}"
            ),

            "action": "Consider postponing spraying",

            "reason": (
                f"Rain probability: "
                f"{max_rain_probability:.0f}%"
            ),

            "crop": crop_name,
            "activity": "spraying"
        })

    # ---------------------------------------------------------
    # HARVESTING + RAIN
    # ---------------------------------------------------------

    if (
        planned_activity == "harvesting"
        and max_rain_probability >= 70
    ):

        notifications.append({

            "type": "harvesting",
            "priority": "high",

            "title": f"{crop_name} Harvest Advisory",

            "message": (
                f"Rain probability is {max_rain_probability:.0f}% "
                f"in {location}. Review your planned harvesting "
                f"schedule and consider the expected rainfall "
                f"before starting field operations."
            ),

            "action": "Review harvesting schedule",

            "reason": (
                f"Rain probability: "
                f"{max_rain_probability:.0f}%"
            ),

            "crop": crop_name,
            "activity": "harvesting"
        })

    # ---------------------------------------------------------
    # HIGH HUMIDITY
    # ---------------------------------------------------------

    if (
        max_humidity >= 85
        and crop_profile.get("high_humidity_monitoring")
    ):

        notifications.append({

            "type": "humidity",
            "priority": "medium",

            "title": f"{crop_name} Humidity Advisory",

            "message": (
                f"High humidity is expected in {location}. "
                f"Monitor your {crop_name} crop for signs of "
                f"humidity-related disease and adjust field "
                f"activities according to crop requirements."
            ),

            "action": "Monitor crop condition",

            "reason": (
                f"Forecast humidity: {max_humidity}%"
            ),

            "crop": crop_name,
            "activity": None
        })

    return notifications