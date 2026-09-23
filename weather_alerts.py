def generate_weather_alerts(
    current_temperature: float,
    current_humidity: int,
    current_wind_speed: float,
    forecast: list
):

    alerts = []

    # ---------------------------------------------------------
    # CURRENT WEATHER ALERTS
    # ---------------------------------------------------------

    # Heat alert
    if current_temperature >= 38:
        alerts.append({
            "type": "heat",
            "severity": "high",
            "message": (
                "High temperature detected. "
                "Monitor crops for heat stress and water requirements."
            )
        })

    # High humidity
    if current_humidity >= 85:
        alerts.append({
            "type": "humidity",
            "severity": "medium",
            "message": (
                "High humidity detected. "
                "Monitor crops for fungal disease symptoms."
            )
        })

    # Strong wind
    if current_wind_speed >= 25:
        alerts.append({
            "type": "strong_wind",
            "severity": "high",
            "message": (
                "Strong winds are expected. "
                "Avoid pesticide or foliar spraying."
            )
        })

    # ---------------------------------------------------------
    # FORECAST ANALYSIS
    # ---------------------------------------------------------

    if forecast:

        # Highest rain probability in forecast
        max_rain_probability = max(
            item["rain_probability"]
            for item in forecast
        )

        # Total forecast rainfall
        total_rainfall = sum(
            item["rainfall"]
            for item in forecast
        )

        # Highest forecast humidity
        max_humidity = max(
            item["humidity"]
            for item in forecast
        )

        # -----------------------------------------------------
        # HEAVY RAIN ALERT
        # -----------------------------------------------------

        if max_rain_probability >= 70 and total_rainfall >= 10:

            alerts.append({
                "type": "heavy_rain",
                "severity": "high",
                "message": (
                    "Significant rainfall is expected in the "
                    "upcoming forecast period. Consider postponing "
                    "planned field activities."
                )
            })

        # -----------------------------------------------------
        # RAIN ALERT
        # -----------------------------------------------------

        elif max_rain_probability >= 60:

            alerts.append({
                "type": "rain",
                "severity": "medium",
                "message": (
                    "Rain is likely in the upcoming forecast. "
                    "Plan field activities accordingly."
                )
            })

        # -----------------------------------------------------
        # IRRIGATION ADVISORY
        # -----------------------------------------------------

        if max_rain_probability >= 60 and total_rainfall >= 5:

            alerts.append({
                "type": "irrigation",
                "severity": "medium",
                "message": (
                    "Rainfall is expected. Consider delaying "
                    "irrigation to avoid unnecessary water application."
                )
            })

        # -----------------------------------------------------
        # HIGH HUMIDITY / FUNGAL RISK
        # -----------------------------------------------------

        if max_humidity >= 85:

            alerts.append({
                "type": "humidity",
                "severity": "medium",
                "message": (
                    "High humidity is expected. "
                    "Monitor crops for fungal disease symptoms."
                )
            })

    return alerts