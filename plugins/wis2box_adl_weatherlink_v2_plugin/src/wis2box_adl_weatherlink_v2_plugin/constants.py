CURRENT_CONDITIONS_DATA_STRUCTURES = {
    "2": {
        "description": "WeatherLink IP/Vantage Connect Current Conditions Record - Revision B",
        "data_structure": {
            "bar_trend": {
                "type": "integer",
                "units": "change in inches of mercury"
            },
            "bar": {
                "type": "float",
                "units": "inches of mercury",
                "units_pint": "inHg"
            },
            "temp_in": {
                "type": "float",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "hum_in": {
                "type": "integer",
                "units": "percent relative humidity",
                "units_pint": "percent"
            },
            "temp_out": {
                "type": "float",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "wind_speed": {
                "type": "integer",
                "units": "miles per hour",
                "units_pint": "mph"
            },
            "wind_speed_10_min_avg": {
                "type": "integer",
                "units": "miles per hour",
                "units_pint": "mph"
            },
            "wind_dir": {
                "type": "integer",
                "units": "degrees of compass",
                "units_pint": "degree"
            },
            "temp_extra_1": {
                "type": "integer",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "temp_extra_2": {
                "type": "integer",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "temp_extra_3": {
                "type": "integer",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "temp_extra_4": {
                "type": "integer",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "temp_extra_5": {
                "type": "integer",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "temp_extra_6": {
                "type": "integer",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "temp_extra_7": {
                "type": "integer",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "temp_soil_1": {
                "type": "integer",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "temp_soil_2": {
                "type": "integer",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "temp_soil_3": {
                "type": "integer",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "temp_soil_4": {
                "type": "integer",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "temp_leaf_1": {
                "type": "integer",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "temp_leaf_2": {
                "type": "integer",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "temp_leaf_3": {
                "type": "integer",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "temp_leaf_4": {
                "type": "integer",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "hum_out": {
                "type": "integer",
                "units": "percent relative humidity",
                "units_pint": "percent"
            },
            "hum_extra_1": {
                "type": "integer",
                "units": "percent relative humidity",
                "units_pint": "percent"
            },
            "hum_extra_2": {
                "type": "integer",
                "units": "percent relative humidity",
                "units_pint": "percent"
            },
            "hum_extra_3": {
                "type": "integer",
                "units": "percent relative humidity",
                "units_pint": "percent"
            },
            "hum_extra_4": {
                "type": "integer",
                "units": "percent relative humidity",
                "units_pint": "percent"
            },
            "hum_extra_5": {
                "type": "integer",
                "units": "percent relative humidity",
                "units_pint": "percent"
            },
            "hum_extra_6": {
                "type": "integer",
                "units": "percent relative humidity",
                "units_pint": "percent"
            },
            "hum_extra_7": {
                "type": "integer",
                "units": "percent relative humidity",
                "units_pint": "percent"
            },
            "rain_rate_clicks": {
                "type": "integer",
                "units": "clicks per hour",
            },
            "rain_rate_in": {
                "type": "float",
                "units": "inches per hour",
            },
            "rain_rate_mm": {
                "type": "float",
                "units": "mm per hour",
                "units_pint": "mm/h"
            },
            "uv": {
                "type": "float",
                "units": "ultraviolet index",
            },
            "solar_rad": {
                "type": "integer",
                "units": "watts per square meter"
            },
            "rain_storm_clicks": {
                "type": "integer",
                "units": "clicks"
            },
            "rain_storm_in": {
                "type": "float",
                "units": "inches",
                "units_pint": "in"
            },
            "rain_storm_mm": {
                "type": "float",
                "units": "millimeters",
                "units_pint": "mm"
            },
            "rain_storm_start_date": {
                "type": "integer",
                "units": "seconds",
                "units_pint": "s"
            },
            "rain_day_clicks": {
                "type": "integer",
                "units": "clicks for the day",
            },
            "rain_day_in": {
                "type": "float",
                "units": "inches for the day"
            },
            "rain_day_mm": {
                "type": "float",
                "units": "millimeters for the day",
                "units_pint": "mm"
            },
            "rain_month_clicks": {
                "type": "integer",
                "units": "clicks for the month"
            },
            "rain_month_in": {
                "type": "float",
                "units": "inches for the month",
                "units_pint": "in"
            },
            "rain_month_mm": {
                "type": "float",
                "units": "millimeters for the month",
                "units_pint": "mm"
            },
            "rain_year_clicks": {
                "type": "integer",
                "units": "clicks for the year"
            },
            "rain_year_in": {
                "type": "float",
                "units": "inches for the year",
                "units_pint": "in"
            },
            "rain_year_mm": {
                "type": "float",
                "units": "millimeters for the year",
                "units_pint": "mm"
            },
            "et_day": {
                "type": "float",
                "units": "inches",
                "units_pint": "in"
            },
            "et_month": {
                "type": "float",
                "units": "inches",
                "units_pint": "in"
            },
            "et_year": {
                "type": "float",
                "units": "inches",
                "units_pint": "in"
            },
            "moist_soil_1": {
                "type": "integer",
                "units": "centibars"
            },
            "moist_soil_2": {
                "type": "integer",
                "units": "centibars",
                "units_pint": "centibar"
            },
            "moist_soil_3": {
                "type": "integer",
                "units": "centibars",
                "units_pint": "centibar"
            },
            "moist_soil_4": {
                "type": "integer",
                "units": "centibars",
                "units_pint": "centibar"
            },
            "wet_leaf_1": {
                "type": "integer",
                "units": "wetness scale from 0 to 15"
            },
            "wet_leaf_2": {
                "type": "integer",
                "units": "wetness scale from 0 to 15"
            },
            "wet_leaf_3": {
                "type": "integer",
                "units": "wetness scale from 0 to 15"
            },
            "wet_leaf_4": {
                "type": "integer",
                "units": "wetness scale from 0 to 15"
            },
            "forecast_rule": {
                "type": "integer",
                "units": ""
            },
            "forecast_desc": {
                "type": "string",
                "units": "forecast messages if available"
            },
            "dew_point": {
                "type": "float",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "heat_index": {
                "type": "float",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "wind_chill": {
                "type": "float",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "wind_gust_10_min": {
                "type": "integer",
                "units": "miles per hour",
                "units_pint": "mph"
            }
        }
    },
    "10": {
        "data_structure_type": "10",
        "description": "WeatherLink Live ISS Current Conditions Record",
        "data_structure": {
            "temp": {
                "type": "float",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "hum": {
                "type": "float",
                "units": "percent relative humidity",
                "units_pint": "percent"
            },
            "dew_point": {
                "type": "float",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "wet_bulb": {
                "type": "float",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "heat_index": {
                "type": "float",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "wind_chill": {
                "type": "float",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "thw_index": {
                "type": "float",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "thsw_index": {
                "type": "float",
                "units": "degrees Fahrenheit",
                "units_pint": "degF"
            },
            "wind_speed_last": {
                "type": "float",
                "units": "miles per hour",
                "units_pint": "mph"
            },
            "wind_dir_last": {
                "type": "integer",
                "units": "degrees",
                "units_pint": "degree"
            },
            "wind_speed_avg_last_1_min": {
                "type": "float",
                "units": "miles per hour",
                "units_pint": "mph"
            },
            "wind_dir_scalar_avg_last_1_min": {
                "type": "integer",
                "units": "degrees",
                "units_pint": "degree"
            },
            "wind_speed_avg_last_2_min": {
                "type": "float",
                "units": "miles per hour",
                "units_pint": "mph"
            },
            "wind_dir_scalar_avg_last_2_min": {
                "type": "integer",
                "units": "degrees",
                "units_pint": "degree"
            },
            "wind_speed_hi_last_2_min": {
                "type": "float",
                "units": "miles per hour",
                "units_pint": "mph"
            },
            "wind_dir_at_hi_speed_last_2_min": {
                "type": "integer",
                "units": "degrees",
                "units_pint": "degree"
            },
            "wind_speed_avg_last_10_min": {
                "type": "float",
                "units": "miles per hour",
                "units_pint": "mph"
            },
            "wind_dir_scalar_avg_last_10_min": {
                "type": "integer",
                "units": "degrees",
                "units_pint": "degree"
            },
            "wind_speed_hi_last_10_min": {
                "type": "float",
                "units": "miles per hour",
                "units_pint": "mph"
            },
            "wind_dir_at_hi_speed_last_10_min": {
                "type": "integer",
                "units": "degrees",
                "units_pint": "degree"
            },
            "rain_size": {
                "type": "integer",
                "units": "1 = 0.01 inch; 2 = 0.2 mm; 3 = 0.1 mm; 4 = 0.001 inch"
            },
            "rain_rate_last_clicks": {
                "type": "integer",
                "units": "clicks"
            },
            "rain_rate_last_in": {
                "type": "float",
                "units": "inches",
                "units_pint": "in"
            },
            "rain_rate_last_mm": {
                "type": "float",
                "units": "millimeters",
                "units_pint": "mm"
            },
            "rain_rate_hi_clicks": {
                "type": "integer",
                "units": "clicks"
            },
            "rain_rate_hi_in": {
                "type": "float",
                "units": "inches",
                "units_pint": "in"
            },
            "rain_rate_hi_mm": {
                "type": "float",
                "units": "millimeters",
                "units_pint": "mm"
            },
            "rainfall_last_15_min_clicks": {
                "type": "integer",
                "units": "clicks"
            },
            "rainfall_last_15_min_in": {
                "type": "float",
                "units": "inches",
                "units_pint": "in"
            },
            "rainfall_last_15_min_mm": {
                "type": "float",
                "units": "millimeters",
                "units_pint": "mm"
            },
            "rain_rate_hi_last_15_min_clicks": {
                "type": "integer",
                "units": "clicks"
            },
            "rain_rate_hi_last_15_min_in": {
                "type": "float",
                "units": "inches",
                "units_pint": "in"
            },
            "rain_rate_hi_last_15_min_mm": {
                "type": "float",
                "units": "millimeters",
                "units_pint": "mm"
            },
            "rainfall_last_60_min_clicks": {
                "type": "integer",
                "units": "clicks"
            },
            "rainfall_last_60_min_in": {
                "type": "float",
                "units": "inches",
                "units_pint": "in"
            },
            "rainfall_last_60_min_mm": {
                "type": "float",
                "units": "millimeters",
                "units_pint": "mm"
            },
            "rainfall_last_24_hr_clicks": {
                "type": "integer",
                "units": "clicks"
            },
            "rainfall_last_24_hr_in": {
                "type": "float",
                "units": "inches",
                "units_pint": "in"
            },
            "rainfall_last_24_hr_mm": {
                "type": "float",
                "units": "millimeters",
                "units_pint": "mm"
            },
            "rain_storm_clicks": {
                "type": "integer",
                "units": "clicks"
            },
            "rain_storm_in": {
                "type": "float",
                "units": "inches",
                "units_pint": "in"
            },
            "rain_storm_mm": {
                "type": "float",
                "units": "millimeters",
                "units_pint": "mm"
            },
            "rain_storm_start_at": {
                "type": "long",
                "units": "seconds",
                "units_pint": "s"
            },
            "solar_rad": {
                "type": "integer",
                "units": "watts per square meter",
                "units_pint": "W/m**2"
            },
            "uv_index": {
                "type": "float",
                "units": "ultraviolet index",
            },
            "rx_state": {
                "type": "integer",
                "units": "configured receiver state at end of interval: 0 = synched and receiving; 1 = rescan; 2 = lost"
            },
            "trans_battery_flag": {
                "type": "integer",
                "units": "0 = battery ok; 1 = battery low"
            },
            "rainfall_daily_clicks": {
                "type": "integer",
                "units": "clicks"
            },
            "rainfall_daily_in": {
                "type": "float",
                "units": "inches",
                "units_pint": "in"
            },
            "rainfall_daily_mm": {
                "type": "float",
                "units": "millimeters",
                "units_pint": "mm"
            },
            "rainfall_monthly_clicks": {
                "type": "integer",
                "units": "clicks"
            },
            "rainfall_monthly_in": {
                "type": "float",
                "units": "inches",
                "units_pint": "in"
            },
            "rainfall_monthly_mm": {
                "type": "float",
                "units": "millimeters",
                "units_pint": "mm"
            },
            "rainfall_year_clicks": {
                "type": "integer",
                "units": "clicks",
            },
            "rainfall_year_in": {
                "type": "float",
                "units": "inches",
                "units_pint": "in"
            },
            "rainfall_year_mm": {
                "type": "float",
                "units": "millimeters",
                "units_pint": "mm"
            },
            "rain_storm_last_clicks": {
                "type": "integer",
                "units": "clicks"
            },
            "rain_storm_last_in": {
                "type": "float",
                "units": "inches",
                "units_pint": "in"
            },
            "rain_storm_last_mm": {
                "type": "float",
                "units": "millimeters",
                "units_pint": "mm"
            },
            "rain_storm_last_start_at": {
                "type": "integer",
                "units": "seconds",
                "units_pint": "s"
            },
            "rain_storm_last_end_at": {
                "type": "integer",
                "units": "seconds",
                "units_pint": "s"
            }
        }
    },
}
