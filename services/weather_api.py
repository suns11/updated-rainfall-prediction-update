# ============================================================
# WEATHER API & ON-DEMAND HISTORY MODULE
# ============================================================
#
# PURPOSE
# ============================================================
#
# This module:
#
# 1. Reads weather data from local CSV.
# 2. Uses Open-Meteo Archive API for past missing dates.
# 3. Uses Open-Meteo Forecast API for today / near future.
# 4. Uses Open-Meteo Climate API for long-range future.
# 5. Keeps LOCAL CSV data as the highest priority.
# 6. Builds complete history for the existing rainfall model.
#
# IMPORTANT
# ============================================================
#
# Existing CatBoost model logic is NOT changed.
#
# Existing:
#
# - rain_lag_1
# - rain_lag_2
# - rain_lag_3
# - rain_lag_5
# - rain_lag_7
# - rain_lag_14
# - rain_lag_21
# - rain_lag_30
# - rolling rainfall features
# - weather lag features
# - station features
#
# remain outside this module.
#
# ============================================================
#
# DATA ROUTING
# ============================================================
#
# LOCAL CSV
#    ↓
# CSV data has highest priority
#
# Missing data:
#
# Past
#    ↓
# Archive API
#
# Today / Near Future
#    ↓
# Forecast API
#
# Beyond Forecast Range
#    ↓
# Climate API
#
# If rainfall is missing:
#    ↓
# precipitation_sum fallback
#
# If climate model is incomplete:
#    ↓
# alternate climate model
#
# ============================================================


# ============================================================
# [01] IMPORTS
# ============================================================

import streamlit as st
import pandas as pd
import requests


from config.settings import (
    OPEN_METEO_ARCHIVE_URL,
    TIMEZONE
)


# ============================================================
# [02] OPEN-METEO URLs
# ============================================================

OPEN_METEO_FORECAST_URL = (
    "https://api.open-meteo.com/v1/forecast"
)


OPEN_METEO_CLIMATE_URL = (
    "https://climate-api.open-meteo.com/v1/climate"
)


# ============================================================
# [03] NORMAL WEATHER VARIABLES
# ============================================================
#
# Existing application variables are preserved.
#
# precipitation_sum is additionally requested as a
# rainfall recovery source.
#
# It does NOT replace rain_sum when rain_sum is available.
#
# ============================================================

DAILY_VARIABLES = [

    "rain_sum",

    "precipitation_sum",

    "temperature_2m_mean",

    "temperature_2m_max",

    "temperature_2m_min",

    "apparent_temperature_mean",

    "sunshine_duration",

    "daylight_duration",

    "wind_speed_10m_max",

    "wind_gusts_10m_max",

    "wind_direction_10m_dominant",

    "shortwave_radiation_sum",

    "weather_code",

    "et0_fao_evapotranspiration"

]


# ============================================================
# [04] CLIMATE API VARIABLES
# ============================================================
#
# Climate API supports rain_sum and precipitation_sum.
#
# Both are requested so that missing rain_sum can be recovered
# without changing the model's expected rainfall column.
#
# ============================================================

CLIMATE_DAILY_VARIABLES = [

    "rain_sum",

    "precipitation_sum",

    "temperature_2m_mean",

    "temperature_2m_max",

    "temperature_2m_min",

    "wind_speed_10m_max",

    "shortwave_radiation_sum",

    "et0_fao_evapotranspiration"

]


# ============================================================
# [05] CLIMATE SETTINGS
# ============================================================

CLIMATE_MODEL = (
    "EC_Earth3P_HR"
)


# ------------------------------------------------------------
# Alternate climate models
# ------------------------------------------------------------
#
# If one climate model returns incomplete rainfall data,
# another model can be tried.
#
# ============================================================

CLIMATE_FALLBACK_MODELS = [

    "EC_Earth3P_HR",

    "CMCC_CM2_VHR4",

    "FGOALS_f3_H",

    "HiRAM_SIT_HR",

    "MRI_AGCM3_2_S",

    "MPI_ESM1_2_XR",

    "NICAM16_8S"

]


CLIMATE_MIN_DATE = pd.Timestamp(
    "1950-01-01"
)


CLIMATE_MAX_DATE = pd.Timestamp(
    "2050-01-01"
)


# ============================================================
# [06] FORECAST SETTINGS
# ============================================================

FORECAST_HORIZON_DAYS = 16


# ============================================================
# [07] LOCAL TODAY HELPER
# ============================================================

def _get_today():

    try:

        today = (

            pd.Timestamp
            .now(tz=TIMEZONE)
            .normalize()
            .tz_localize(None)

        )

    except Exception:

        today = (

            pd.Timestamp("today")
            .normalize()

        )

    return today


# ============================================================
# [08] STATION VALUE HELPER
# ============================================================

def _station_value(
    station,
    key,
    default=None
):

    try:

        if hasattr(station, "get"):

            return station.get(
                key,
                default
            )

    except Exception:

        pass


    try:

        return station[key]

    except Exception:

        return default


# ============================================================
# [09] ENSURE WEATHER COLUMNS
# ============================================================

def _ensure_weather_columns(
    weather_df
):

    if weather_df is None:

        return pd.DataFrame()


    if weather_df.empty:

        return weather_df


    weather_df = weather_df.copy()


    for column in DAILY_VARIABLES:

        if column not in weather_df.columns:

            weather_df[column] = pd.NA


    return weather_df


# ============================================================
# [10] RAINFALL RECOVERY
# ============================================================
#
# IMPORTANT FIX
# ============================================================
#
# Sometimes an API response contains a valid Date but
# rain_sum is NaN.
#
# This function:
#
# 1. Keeps valid rain_sum unchanged.
# 2. Uses precipitation_sum only where rain_sum is missing.
# 3. Never overwrites an existing rain_sum value.
#
# For Bangladesh rainfall data this provides a practical
# precipitation fallback because snow contribution is not
# relevant to the Bangladesh station dataset.
#
# ============================================================

def _repair_rainfall_column(
    weather_df
):

    if weather_df is None:

        return pd.DataFrame()


    if weather_df.empty:

        return weather_df


    weather_df = weather_df.copy()


    # --------------------------------------------------------
    # Ensure rain_sum exists
    # --------------------------------------------------------

    if "rain_sum" not in weather_df.columns:

        weather_df["rain_sum"] = pd.NA


    # --------------------------------------------------------
    # Numeric conversion
    # --------------------------------------------------------

    weather_df["rain_sum"] = pd.to_numeric(

        weather_df["rain_sum"],

        errors="coerce"

    )


    # --------------------------------------------------------
    # precipitation_sum fallback
    # --------------------------------------------------------

    if "precipitation_sum" in weather_df.columns:

        precipitation = pd.to_numeric(

            weather_df["precipitation_sum"],

            errors="coerce"

        )


        missing_rain = (
            weather_df["rain_sum"].isna()
        )


        recoverable = (

            missing_rain

            &

            precipitation.notna()

        )


        weather_df.loc[
            recoverable,
            "rain_sum"
        ] = precipitation.loc[
            recoverable
        ]


    return weather_df


# ============================================================
# [11] COMMON OPEN-METEO REQUEST
# ============================================================

def _fetch_open_meteo(
    url,
    lat,
    lon,
    start_date,
    end_date,
    daily_variables,
    extra_params=None
):

    # --------------------------------------------------------
    # Normalize dates
    # --------------------------------------------------------

    start_date = (

        pd.Timestamp(start_date)
        .normalize()

    )


    end_date = (

        pd.Timestamp(end_date)
        .normalize()

    )


    # --------------------------------------------------------
    # Invalid date range
    # --------------------------------------------------------

    if start_date > end_date:

        return pd.DataFrame()


    # --------------------------------------------------------
    # Coordinates
    # --------------------------------------------------------

    try:

        latitude = float(lat)

        longitude = float(lon)

    except Exception as exc:

        raise ValueError(

            "Invalid station Latitude/Longitude."

        ) from exc


    # --------------------------------------------------------
    # Variables
    # --------------------------------------------------------

    variables = [

        str(variable).strip()

        for variable in daily_variables

        if variable is not None

        and str(variable).strip()

    ]


    if not variables:

        raise ValueError(

            "No Open-Meteo daily weather variables "
            "were specified."

        )


    # ========================================================
    # Build parameters
    # ========================================================

    params = {

        "latitude": latitude,

        "longitude": longitude,

        "daily": ",".join(
            variables
        ),

        "timezone": TIMEZONE,

        "start_date": (

            start_date.strftime(
                "%Y-%m-%d"
            )

        ),

        "end_date": (

            end_date.strftime(
                "%Y-%m-%d"
            )

        )

    }


    # --------------------------------------------------------
    # Additional parameters
    # --------------------------------------------------------

    if extra_params:

        params.update(
            extra_params
        )


    # ========================================================
    # Request
    # ========================================================

    response = requests.get(

        url,

        params=params,

        timeout=60

    )


    # ========================================================
    # HTTP error
    # ========================================================

    try:

        response.raise_for_status()

    except requests.RequestException as exc:

        try:

            error_data = response.json()

            reason = error_data.get(

                "reason",

                str(exc)

            )

            raise ValueError(

                f"Open-Meteo API error: {reason}"

            ) from exc

        except ValueError:

            raise ValueError(

                f"Open-Meteo request failed: {exc}"

            ) from exc


    # ========================================================
    # JSON
    # ========================================================

    try:

        data = response.json()

    except Exception as exc:

        raise ValueError(

            "Open-Meteo returned invalid JSON."

        ) from exc


    # ========================================================
    # API-level error
    # ========================================================

    if data.get("error"):

        reason = data.get(

            "reason",

            "Open-Meteo API returned an error."

        )

        raise ValueError(
            str(reason)
        )


    # ========================================================
    # Daily data
    # ========================================================

    daily_data = data.get(

        "daily",

        {}

    )


    if not daily_data:

        raise ValueError(

            "Open-Meteo returned no daily weather data."

        )


    # ========================================================
    # Time
    # ========================================================

    if "time" not in daily_data:

        raise ValueError(

            "Open-Meteo response has no time data."

        )


    # ========================================================
    # DataFrame
    # ========================================================

    try:

        out = pd.DataFrame(
            daily_data
        )

    except Exception as exc:

        raise ValueError(

            "Could not convert Open-Meteo daily "
            "data to DataFrame."

        ) from exc


    # ========================================================
    # Rename time → Date
    # ========================================================

    out = out.rename(

        columns={

            "time": "Date"

        }

    )


    # ========================================================
    # Normalize Date
    # ========================================================

    out["Date"] = pd.to_datetime(

        out["Date"],

        errors="coerce"

    ).dt.normalize()


    # ========================================================
    # Remove invalid dates
    # ========================================================

    out = out[

        out["Date"].notna()

    ].copy()


    # ========================================================
    # Ensure application columns
    # ========================================================

    out = _ensure_weather_columns(
        out
    )


    # ========================================================
    # Repair rainfall
    # ========================================================

    out = _repair_rainfall_column(
        out
    )


    return out


# ============================================================
# [12] ARCHIVE API
# ============================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def fetch_open_meteo_range(
    lat,
    lon,
    start_date,
    end_date
):

    return _fetch_open_meteo(

        url=OPEN_METEO_ARCHIVE_URL,

        lat=lat,

        lon=lon,

        start_date=start_date,

        end_date=end_date,

        daily_variables=DAILY_VARIABLES

    )


# ============================================================
# [13] FORECAST API
# ============================================================

@st.cache_data(
    ttl=900,
    show_spinner=False
)
def fetch_open_meteo_forecast_range(
    lat,
    lon,
    start_date,
    end_date
):

    return _fetch_open_meteo(

        url=OPEN_METEO_FORECAST_URL,

        lat=lat,

        lon=lon,

        start_date=start_date,

        end_date=end_date,

        daily_variables=DAILY_VARIABLES

    )


# ============================================================
# [14] CLIMATE API — SINGLE MODEL
# ============================================================

@st.cache_data(
    ttl=21600,
    show_spinner=False
)
def fetch_open_meteo_climate_range(
    lat,
    lon,
    start_date,
    end_date,
    model=CLIMATE_MODEL
):

    # --------------------------------------------------------
    # Normalize dates
    # --------------------------------------------------------

    start_date = (

        pd.Timestamp(start_date)
        .normalize()

    )


    end_date = (

        pd.Timestamp(end_date)
        .normalize()

    )


    # --------------------------------------------------------
    # Invalid range
    # --------------------------------------------------------

    if start_date > end_date:

        return pd.DataFrame()


    # ========================================================
    # Climate supported range
    # ========================================================

    if start_date < CLIMATE_MIN_DATE:

        raise ValueError(

            "Climate API cannot provide data before "
            "1950-01-01."

        )


    if end_date > CLIMATE_MAX_DATE:

        raise ValueError(

            "Climate API cannot provide data after "
            "2050-01-01."

        )


    # ========================================================
    # Request
    # ========================================================

    climate_data = _fetch_open_meteo(

        url=OPEN_METEO_CLIMATE_URL,

        lat=lat,

        lon=lon,

        start_date=start_date,

        end_date=end_date,

        daily_variables=CLIMATE_DAILY_VARIABLES,

        extra_params={

            "models": model

        }

    )


    # ========================================================
    # Ensure normal application columns
    # ========================================================

    climate_data = _ensure_weather_columns(

        climate_data

    )


    # ========================================================
    # Rainfall recovery
    # ========================================================

    climate_data = _repair_rainfall_column(

        climate_data

    )


    # ========================================================
    # Keep requested range only
    # ========================================================

    if not climate_data.empty:

        climate_data = climate_data[

            (

                climate_data["Date"]
                >= start_date

            )

            &

            (

                climate_data["Date"]
                <= end_date

            )

        ].copy()


    return climate_data


# ============================================================
# [15] CLIMATE MULTI-MODEL RECOVERY
# ============================================================
#
# This is the main future-rainfall protection.
#
# If the first climate model returns a row but rain_sum is
# missing, another supported climate model is tried.
#
# Existing valid values are always preserved.
#
# ============================================================

def _fetch_climate_with_rainfall_fallback(
    station,
    missing_dates
):

    if not missing_dates:

        return pd.DataFrame()


    normalized_dates = [

        pd.Timestamp(day)
        .normalize()

        for day in missing_dates

    ]


    normalized_dates = list(
        dict.fromkeys(
            normalized_dates
        )
    )


    climate_dates = [

        day

        for day in normalized_dates

        if (

            day >= CLIMATE_MIN_DATE

            and

            day <= CLIMATE_MAX_DATE

        )

    ]


    if not climate_dates:

        return pd.DataFrame()


    # --------------------------------------------------------
    # Coordinates
    # --------------------------------------------------------

    try:

        lat = float(

            _station_value(
                station,
                "Latitude"
            )

        )

        lon = float(

            _station_value(
                station,
                "Longitude"
            )

        )

    except Exception:

        return pd.DataFrame()


    start_date = min(
        climate_dates
    )

    end_date = max(
        climate_dates
    )


    combined = pd.DataFrame()


    # ========================================================
    # Try climate models
    # ========================================================

    for model in CLIMATE_FALLBACK_MODELS:

        try:

            api_data = (

                fetch_open_meteo_climate_range(

                    lat=lat,

                    lon=lon,

                    start_date=start_date,

                    end_date=end_date,

                    model=model

                )

            )

        except Exception:

            continue


        if api_data is None or api_data.empty:

            continue


        api_data = _repair_rainfall_column(
            api_data
        )


        api_data = api_data[

            api_data["Date"].isin(
                climate_dates
            )

        ].copy()


        if api_data.empty:

            continue


        # ----------------------------------------------------
        # Add station metadata
        # ----------------------------------------------------

        api_data = _add_station_info(

            api_data,

            station

        )


        # ----------------------------------------------------
        # First model
        # ----------------------------------------------------

        if combined.empty:

            combined = api_data.copy()

        else:

            combined = pd.concat(

                [
                    combined,
                    api_data
                ],

                ignore_index=True,

                sort=False

            )


        # ----------------------------------------------------
        # Keep best row for each date.
        #
        # Valid rainfall is preferred.
        # ----------------------------------------------------

        combined = _prefer_valid_rainfall_rows(
            combined
        )


        # ----------------------------------------------------
        # Stop when all requested dates have valid rainfall.
        # ----------------------------------------------------

        if _all_dates_have_valid_rainfall(

            combined,

            climate_dates

        ):

            break


    return combined


# ============================================================
# [16] PREFER VALID RAINFALL ROWS
# ============================================================

def _prefer_valid_rainfall_rows(
    weather_df
):

    if weather_df is None or weather_df.empty:

        return (

            weather_df
            if weather_df is not None
            else pd.DataFrame()

        )


    data = weather_df.copy()


    if "rain_sum" not in data.columns:

        data["rain_sum"] = pd.NA


    data["rain_sum"] = pd.to_numeric(

        data["rain_sum"],

        errors="coerce"

    )


    # --------------------------------------------------------
    # Valid rainfall rows first
    # --------------------------------------------------------

    data["_rain_valid"] = (

        data["rain_sum"].notna()

    )


    data = data.sort_values(

        [

            "Date",

            "_rain_valid"

        ],

        ascending=[

            True,

            False

        ]

    )


    data = data.drop_duplicates(

        subset=[

            "Station_ID",
            "Date"

        ],

        keep="first"

    )


    data = data.drop(

        columns=[

            "_rain_valid"

        ],

        errors="ignore"

    )


    return data.reset_index(
        drop=True
    )


# ============================================================
# [17] ALL DATES HAVE VALID RAINFALL
# ============================================================

def _all_dates_have_valid_rainfall(
    weather_df,
    expected_dates
):

    if weather_df is None or weather_df.empty:

        return False


    if "Date" not in weather_df.columns:

        return False


    if "rain_sum" not in weather_df.columns:

        return False


    valid = weather_df.copy()


    valid["rain_sum"] = pd.to_numeric(

        valid["rain_sum"],

        errors="coerce"

    )


    valid = valid[
        valid["rain_sum"].notna()
    ]


    valid_dates = set(

        pd.to_datetime(
            valid["Date"]
        )
        .dt.normalize()

    )


    return all(

        day in valid_dates

        for day in expected_dates

    )


# ============================================================
# [18] SINGLE-DATE WEATHER
# ============================================================

def fetch_target_weather(
    station,
    target_date
):

    target_date = (

        pd.Timestamp(target_date)
        .normalize()

    )


    today = _get_today()


    try:

        lat = float(

            _station_value(
                station,
                "Latitude"
            )

        )

        lon = float(

            _station_value(
                station,
                "Longitude"
            )

        )

    except Exception as exc:

        raise ValueError(

            "Selected station has invalid "
            "Latitude/Longitude."

        ) from exc


    # ========================================================
    # PAST
    # ========================================================

    if target_date < today:

        try:

            weather_df = (

                fetch_open_meteo_range(

                    lat=lat,

                    lon=lon,

                    start_date=target_date,

                    end_date=target_date

                )

            )

        except Exception as archive_error:

            try:

                weather_df = (

                    fetch_open_meteo_climate_range(

                        lat=lat,

                        lon=lon,

                        start_date=target_date,

                        end_date=target_date

                    )

                )

            except Exception as climate_error:

                raise ValueError(

                    "Could not fetch weather data "
                    f"for {target_date.strftime('%Y-%m-%d')}. "
                    f"Archive error: {archive_error}. "
                    f"Climate fallback error: {climate_error}."

                ) from climate_error


    # ========================================================
    # TODAY / NEAR FUTURE
    # ========================================================

    elif (

        target_date
        <=
        today
        +
        pd.Timedelta(
            days=FORECAST_HORIZON_DAYS
        )

    ):

        try:

            weather_df = (

                fetch_open_meteo_forecast_range(

                    lat=lat,

                    lon=lon,

                    start_date=target_date,

                    end_date=target_date

                )

            )

        except Exception:

            weather_df = (

                fetch_open_meteo_climate_range(

                    lat=lat,

                    lon=lon,

                    start_date=target_date,

                    end_date=target_date

                )

            )


    # ========================================================
    # LONG-RANGE FUTURE
    # ========================================================

    else:

        weather_df = (

            _fetch_climate_with_rainfall_fallback(

                station=station,

                missing_dates=[
                    target_date
                ]

            )

        )


    # ========================================================
    # Empty
    # ========================================================

    if weather_df is None or weather_df.empty:

        raise ValueError(

            "Could not fetch weather data "
            "for selected date."

        )


    # ========================================================
    # Rainfall repair
    # ========================================================

    weather_df = _repair_rainfall_column(
        weather_df
    )


    # ========================================================
    # Exact target date
    # ========================================================

    weather_df = weather_df[

        weather_df["Date"]
        == target_date

    ].copy()


    # ========================================================
    # Final future fallback
    # ========================================================

    if weather_df.empty:

        try:

            fallback_df = (

                _fetch_climate_with_rainfall_fallback(

                    station=station,

                    missing_dates=[
                        target_date
                    ]

                )

            )

            if (

                fallback_df is not None

                and

                not fallback_df.empty

            ):

                weather_df = fallback_df[

                    fallback_df["Date"]
                    == target_date

                ].copy()

        except Exception:

            pass


    # ========================================================
    # Final empty check
    # ========================================================

    if weather_df.empty:

        raise ValueError(

            "Selected date was not returned "
            "by the weather API."

        )


    # ========================================================
    # Final rainfall repair
    # ========================================================

    weather_df = _repair_rainfall_column(
        weather_df
    )


    # ========================================================
    # Rainfall availability
    # ========================================================

    if (

        "rain_sum" not in weather_df.columns

        or

        pd.isna(
            pd.to_numeric(
                weather_df.iloc[0]["rain_sum"],
                errors="coerce"
            )
        )

    ):

        raise ValueError(

            "Rainfall data was not available "
            "for the selected date."

        )


    return (

        weather_df
        .iloc[0]
        .to_dict()

    )


# ============================================================
# [19] PREPARE LOCAL HISTORY
# ============================================================

def prepare_local_history(
    df,
    station_id,
    start_date,
    end_date
):

    local = df.copy()


    if "Date" not in local.columns:

        raise ValueError(

            "Date column not found in local "
            "weather data."

        )


    if "Station_ID" not in local.columns:

        raise ValueError(

            "Station_ID column not found in local "
            "weather data."

        )


    local["Date"] = pd.to_datetime(

        local["Date"],

        errors="coerce"

    ).dt.normalize()


    local = local[

        local["Date"].notna()

    ].copy()


    start_date = (

        pd.Timestamp(start_date)
        .normalize()

    )


    end_date = (

        pd.Timestamp(end_date)
        .normalize()

    )


    local = local[

        (

            local["Station_ID"]
            == station_id

        )

        &

        (

            local["Date"]
            >= start_date

        )

        &

        (

            local["Date"]
            <= end_date

        )

    ].copy()


    # --------------------------------------------------------
    # Repair local rainfall numeric type.
    # --------------------------------------------------------

    if "rain_sum" in local.columns:

        local["rain_sum"] = pd.to_numeric(

            local["rain_sum"],

            errors="coerce"

        )


    return local


# ============================================================
# [20] ADD STATION INFORMATION
# ============================================================

def _add_station_info(
    api_data,
    station
):

    if api_data is None or api_data.empty:

        return (

            api_data
            if api_data is not None
            else pd.DataFrame()

        )


    api_data = api_data.copy()


    station_id = _station_value(

        station,

        "Station_ID"

    )


    if station_id is None:

        raise ValueError(

            "Selected station has no Station_ID."

        )


    api_data["Station_ID"] = station_id


    try:

        api_data["Latitude"] = float(

            _station_value(
                station,
                "Latitude"
            )

        )

        api_data["Longitude"] = float(

            _station_value(
                station,
                "Longitude"
            )

        )

    except Exception as exc:

        raise ValueError(

            "Selected station has invalid "
            "Latitude/Longitude."

        ) from exc


    station_name = _station_value(

        station,

        "Station",

        None

    )


    if station_name is not None:

        api_data["Station"] = station_name


    district = _station_value(

        station,

        "District",

        None

    )


    if district is not None:

        api_data["District"] = district


    division = _station_value(

        station,

        "Division",

        None

    )


    if division is not None:

        api_data["Division"] = division


    return api_data


# ============================================================
# [21] FETCH PAST MISSING HISTORY
# ============================================================

def _fetch_missing_history(
    station,
    missing_dates
):

    if not missing_dates:

        return pd.DataFrame()


    normalized_dates = [

        pd.Timestamp(day)
        .normalize()

        for day in missing_dates

    ]


    start_date = min(
        normalized_dates
    )


    end_date = max(
        normalized_dates
    )


    try:

        api_data = (

            fetch_open_meteo_range(

                lat=float(

                    _station_value(
                        station,
                        "Latitude"
                    )

                ),

                lon=float(

                    _station_value(
                        station,
                        "Longitude"
                    )

                ),

                start_date=start_date,

                end_date=end_date

            )

        )

    except Exception:

        return pd.DataFrame()


    if api_data is None or api_data.empty:

        return pd.DataFrame()


    api_data = _repair_rainfall_column(
        api_data
    )


    api_data = api_data[

        api_data["Date"].isin(
            normalized_dates
        )

    ].copy()


    if api_data.empty:

        return pd.DataFrame()


    return _add_station_info(

        api_data,

        station

    )


# ============================================================
# [22] FETCH FORECAST MISSING HISTORY
# ============================================================

def _fetch_missing_recent_history(
    station,
    missing_dates
):

    if not missing_dates:

        return pd.DataFrame()


    today = _get_today()


    forecast_last_date = (

        today
        +
        pd.Timedelta(
            days=FORECAST_HORIZON_DAYS
        )

    )


    forecast_dates = [

        pd.Timestamp(day).normalize()

        for day in missing_dates

        if (

            pd.Timestamp(day).normalize()
            >= today

            and

            pd.Timestamp(day).normalize()
            <= forecast_last_date

        )

    ]


    if not forecast_dates:

        return pd.DataFrame()


    start_date = min(
        forecast_dates
    )


    end_date = max(
        forecast_dates
    )


    try:

        api_data = (

            fetch_open_meteo_forecast_range(

                lat=float(

                    _station_value(
                        station,
                        "Latitude"
                    )

                ),

                lon=float(

                    _station_value(
                        station,
                        "Longitude"
                    )

                ),

                start_date=start_date,

                end_date=end_date

            )

        )

    except Exception:

        return pd.DataFrame()


    if api_data is None or api_data.empty:

        return pd.DataFrame()


    api_data = _repair_rainfall_column(
        api_data
    )


    api_data = api_data[

        api_data["Date"].isin(
            forecast_dates
        )

    ].copy()


    if api_data.empty:

        return pd.DataFrame()


    return _add_station_info(

        api_data,

        station

    )


# ============================================================
# [23] FETCH LONG-RANGE CLIMATE HISTORY
# ============================================================

def _fetch_missing_climate_history(
    station,
    missing_dates
):

    if not missing_dates:

        return pd.DataFrame()


    normalized_dates = [

        pd.Timestamp(day)
        .normalize()

        for day in missing_dates

    ]


    return _fetch_climate_with_rainfall_fallback(

        station=station,

        missing_dates=normalized_dates

    )


# ============================================================
# [24] BUILD ON-DEMAND HISTORY
# ============================================================

def build_on_demand_history(
    df,
    station,
    target_date,
    history_days
):

    # ========================================================
    # [24-A] TARGET DATE
    # ========================================================

    target_date = (

        pd.Timestamp(target_date)
        .normalize()

    )


    # ========================================================
    # [24-B] HISTORY DAYS
    # ========================================================

    try:

        history_days = int(
            history_days
        )

    except (
        TypeError,
        ValueError
    ):

        history_days = 30


    # ========================================================
    # [24-C] MINIMUM 30 DAYS
    # ========================================================

    if history_days < 30:

        history_days = 30


    # ========================================================
    # [24-D] HISTORY RANGE
    # ========================================================

    start_date = (

        target_date
        -
        pd.Timedelta(
            days=history_days
        )

    )


    end_date = (

        target_date
        -
        pd.Timedelta(
            days=1
        )

    )


    # ========================================================
    # [24-E] STATION ID
    # ========================================================

    station_id = _station_value(

        station,

        "Station_ID"

    )


    if station_id is None:

        raise ValueError(

            "Selected station has no Station_ID."

        )


    # ========================================================
    # [24-F] TODAY
    # ========================================================

    today = _get_today()


    # ========================================================
    # [24-G] LOCAL CSV
    # ========================================================

    local = prepare_local_history(

        df=df,

        station_id=station_id,

        start_date=start_date,

        end_date=end_date

    )


    # ========================================================
    # [24-H] EXPECTED DATES
    # ========================================================

    expected_dates = pd.date_range(

        start=start_date,

        end=end_date,

        freq="D"

    )


    # ========================================================
    # [24-I] LOCAL DATES
    # ========================================================

    if not local.empty:

        local_dates = set(

            pd.to_datetime(
                local["Date"]
            )
            .dt.normalize()

        )

    else:

        local_dates = set()


    # ========================================================
    # [24-J] MISSING DATES
    # ========================================================

    missing_dates = [

        day

        for day in expected_dates

        if day not in local_dates

    ]


    # ========================================================
    # [24-K] INITIAL DATE GROUPS
    # ========================================================

    forecast_last_date = (

        today
        +
        pd.Timedelta(
            days=FORECAST_HORIZON_DAYS
        )

    )


    past_missing = [

        day

        for day in missing_dates

        if day < today

    ]


    forecast_missing = [

        day

        for day in missing_dates

        if (

            day >= today

            and

            day <= forecast_last_date

        )

    ]


    climate_missing = [

        day

        for day in missing_dates

        if day > forecast_last_date

    ]


    # ========================================================
    # [24-L] API DATA INITIALIZATION
    # ========================================================

    fetched_archive = pd.DataFrame()

    fetched_recent = pd.DataFrame()

    fetched_climate = pd.DataFrame()


    # ========================================================
    # [24-M] PAST → ARCHIVE
    # ========================================================

    if past_missing:

        fetched_archive = (

            _fetch_missing_history(

                station=station,

                missing_dates=past_missing

            )

        )


    # ========================================================
    # [24-N] TODAY / NEAR FUTURE → FORECAST
    # ========================================================

    if forecast_missing:

        fetched_recent = (

            _fetch_missing_recent_history(

                station=station,

                missing_dates=forecast_missing

            )

        )


    # ========================================================
    # [24-O] FIND FORECAST DATES STILL MISSING
    # ========================================================

    forecast_fetched_dates = set()


    if not fetched_recent.empty:

        forecast_fetched_dates = set(

            pd.to_datetime(
                fetched_recent["Date"]
            )
            .dt.normalize()

        )


    remaining_forecast_dates = [

        day

        for day in forecast_missing

        if day not in forecast_fetched_dates

    ]


    # ========================================================
    # [24-P] REMAINING FUTURE → CLIMATE
    # ========================================================

    climate_fallback_dates = [

        day

        for day in remaining_forecast_dates

        if (

            day >= CLIMATE_MIN_DATE

            and

            day <= CLIMATE_MAX_DATE

        )

    ]


    all_climate_missing = (

        climate_missing
        +
        climate_fallback_dates

    )


    all_climate_missing = list(

        dict.fromkeys(
            all_climate_missing
        )

    )


    # ========================================================
    # [24-Q] LONG FUTURE → CLIMATE
    # ========================================================

    if all_climate_missing:

        fetched_climate = (

            _fetch_missing_climate_history(

                station=station,

                missing_dates=all_climate_missing

            )

        )


    # ========================================================
    # [24-R] MERGE
    # ========================================================
    #
    # IMPORTANT:
    #
    # LOCAL
    # ARCHIVE
    # FORECAST
    # CLIMATE
    #
    # Local CSV remains highest priority.
    #
    # ========================================================

    history = pd.concat(

        [

            local,

            fetched_archive,

            fetched_recent,

            fetched_climate

        ],

        ignore_index=True,

        sort=False

    )


    # ========================================================
    # [24-S] EMPTY CHECK
    # ========================================================

    if history.empty:

        raise ValueError(

            "No historical weather data available. "
            "Local CSV and all available Open-Meteo "
            "API sources returned no usable data."

        )


    # ========================================================
    # [24-T] NORMALIZE FINAL DATES
    # ========================================================

    history["Date"] = pd.to_datetime(

        history["Date"],

        errors="coerce"

    ).dt.normalize()


    history = history[

        history["Date"].notna()

    ].copy()


    # ========================================================
    # [24-U] REQUIRED STATION ID
    # ========================================================

    if "Station_ID" not in history.columns:

        raise ValueError(

            "Station_ID column not found in history."

        )


    # ========================================================
    # [24-V] REPAIR RAINFALL BEFORE DUPLICATES
    # ========================================================

    history = _repair_rainfall_column(
        history
    )


    # ========================================================
    # [24-W] REMOVE DUPLICATES
    # ========================================================
    #
    # Existing CSV/API priority remains.
    #
    # ========================================================

    history = _prefer_valid_rainfall_rows(
        history
    )


    # ========================================================
    # [24-X] SORT
    # ========================================================

    history = history.sort_values(

        [

            "Station_ID",

            "Date"

        ]

    ).reset_index(
        drop=True
    )


    # ========================================================
    # [24-Y] COMPLETE HISTORY CHECK
    # ========================================================

    actual_dates = set(

        pd.to_datetime(
            history["Date"]
        )
        .dt.normalize()

    )


    still_missing = [

        day

        for day in expected_dates

        if day not in actual_dates

    ]


    # ========================================================
    # [24-Z] LAST RESORT API RECOVERY
    # ========================================================
    #
    # Every remaining date is tried again.
    #
    # ========================================================

    if still_missing:

        remaining_past = [

            day

            for day in still_missing

            if day < today

        ]


        remaining_future = [

            day

            for day in still_missing

            if day >= today

        ]


        extra_archive = pd.DataFrame()

        if remaining_past:

            extra_archive = (

                _fetch_missing_history(

                    station=station,

                    missing_dates=remaining_past

                )

            )


        extra_recent = pd.DataFrame()

        recent_remaining = [

            day

            for day in remaining_future

            if (

                day <= forecast_last_date

            )

        ]


        if recent_remaining:

            extra_recent = (

                _fetch_missing_recent_history(

                    station=station,

                    missing_dates=recent_remaining

                )

            )


        extra_climate = pd.DataFrame()

        climate_remaining = [

            day

            for day in remaining_future

            if (

                day > forecast_last_date

            )

        ]


        if climate_remaining:

            extra_climate = (

                _fetch_missing_climate_history(

                    station=station,

                    missing_dates=climate_remaining

                )

            )


        # ----------------------------------------------------
        # Merge
        # ----------------------------------------------------

        additions = [

            extra_archive,

            extra_recent,

            extra_climate

        ]


        for addition in additions:

            if (

                addition is not None

                and

                not addition.empty

            ):

                history = pd.concat(

                    [

                        history,

                        addition

                    ],

                    ignore_index=True,

                    sort=False

                )


        # ----------------------------------------------------
        # Repair rainfall again
        # ----------------------------------------------------

        history = _repair_rainfall_column(
            history
        )


        # ----------------------------------------------------
        # Deduplicate
        # ----------------------------------------------------

        history = _prefer_valid_rainfall_rows(
            history
        )


        history = history.sort_values(

            [

                "Station_ID",

                "Date"

            ]

        ).reset_index(
            drop=True
        )


        # ----------------------------------------------------
        # Recalculate missing dates
        # ----------------------------------------------------

        actual_dates = set(

            pd.to_datetime(
                history["Date"]
            )
            .dt.normalize()

        )


        still_missing = [

            day

            for day in expected_dates

            if day not in actual_dates

        ]


    # ========================================================
    # [24-Z1] FINAL COMPLETE HISTORY CHECK
    # ========================================================

    if still_missing:

        preview = [

            day.strftime(
                "%Y-%m-%d"
            )

            for day in still_missing[:10]

        ]


        extra_count = (

            len(still_missing)
            -
            len(preview)

        )


        message = (

            "Historical data incomplete: "

            +

            ", ".join(
                preview
            )

        )


        if extra_count > 0:

            message += (

                f" and {extra_count} more date(s)."

            )


        raise ValueError(
            message
        )


    # ========================================================
    # [24-Z2] RAINFALL COLUMN
    # ========================================================

    if "rain_sum" not in history.columns:

        raise ValueError(

            "rain_sum column not found in history."

        )


    # ========================================================
    # [24-Z3] RAINFALL NUMERIC
    # ========================================================

    history["rain_sum"] = pd.to_numeric(

        history["rain_sum"],

        errors="coerce"

    )


    # ========================================================
    # [24-Z4] FINAL RAINFALL RECOVERY
    # ========================================================

    history = _repair_rainfall_column(
        history
    )


    history["rain_sum"] = pd.to_numeric(

        history["rain_sum"],

        errors="coerce"

    )


    # ========================================================
    # [24-Z5] RAINFALL MISSING CHECK
    # ========================================================

    if history["rain_sum"].isna().any():

        missing_rain_dates = (

            history.loc[

                history["rain_sum"].isna(),

                "Date"

            ]

            .dt.strftime(
                "%Y-%m-%d"
            )

            .tolist()

        )


        preview = (

            missing_rain_dates[:10]

        )


        extra_count = (

            len(missing_rain_dates)
            -
            len(preview)

        )


        message = (

            "Historical rainfall contains "
            "missing values: "

            +

            ", ".join(
                preview
            )

        )


        if extra_count > 0:

            message += (

                f" and {extra_count} more date(s)."

            )


        raise ValueError(
            message
        )


    # ========================================================
    # [24-Z6] SOURCE COUNTS
    # ========================================================

    local_count = len(
        local
    )


    archive_count = len(
        fetched_archive
    )


    recent_count = len(
        fetched_recent
    )


    climate_count = len(
        fetched_climate
    )


    # ========================================================
    # [24-Z7] NOTE
    # ========================================================

    note = (

        f"Model needs {history_days} previous days. "

        f"Used {local_count} local CSV days, "

        f"{archive_count} archive API days, "

        f"{recent_count} forecast API days "

        f"and {climate_count} long-range climate API days."

    )


    # ========================================================
    # [24-Z8] FUTURE PREVIOUS-DAY CHECK
    # ========================================================

    if target_date > today:

        previous_day = (

            target_date
            -
            pd.Timedelta(
                days=1
            )

        )


        # ====================================================
        # Find previous day
        # ====================================================

        previous_row = history[

            (

                history["Date"]
                == previous_day

            )

            &

            (

                history["Station_ID"]
                == station_id

            )

        ]


        # ====================================================
        # Previous day missing
        # ====================================================

        if previous_row.empty:

            raise ValueError(

                "Previous day data is missing. "
                "Future prediction cannot be created."

            )


        # ====================================================
        # Previous rainfall
        # ====================================================

        previous_rain = pd.to_numeric(

            previous_row.iloc[0][
                "rain_sum"
            ],

            errors="coerce"

        )


        if pd.isna(
            previous_rain
        ):

            raise ValueError(

                "Previous day rainfall is missing. "
                "Future prediction cannot use rain_lag_1."

            )


        # ====================================================
        # Determine source
        # ====================================================

        if previous_day in local_dates:

            previous_source = "CSV"


        elif (

            not fetched_archive.empty

            and

            previous_day
            in
            set(

                pd.to_datetime(
                    fetched_archive["Date"]
                )
                .dt.normalize()

            )

        ):

            previous_source = (
                "Archive API"
            )


        elif (

            not fetched_recent.empty

            and

            previous_day
            in
            set(

                pd.to_datetime(
                    fetched_recent["Date"]
                )
                .dt.normalize()

            )

        ):

            previous_source = (
                "Forecast API"
            )


        elif (

            not fetched_climate.empty

            and

            previous_day
            in
            set(

                pd.to_datetime(
                    fetched_climate["Date"]
                )
                .dt.normalize()

            )

        ):

            previous_source = (
                "Climate API"
            )


        else:

            previous_source = "API"


        # ====================================================
        # Previous-day information
        # ====================================================

        note += (

            f" Previous day rainfall "
            f"({previous_day.strftime('%Y-%m-%d')}) "
            f"= {float(previous_rain):.2f} mm "
            f"from {previous_source}; "
            f"this value is used for rain_lag_1 "
            f"and rolling rainfall features."

        )


        # ====================================================
        # Today warning
        # ====================================================

        if previous_day == today:

            if previous_day not in local_dates:

                note += (

                    " WARNING: Today's rainfall was not "
                    "available in the CSV, so an API "
                    "value was used."

                )


        # ====================================================
        # Climate information
        # ========================================================

        if previous_source == "Climate API":

            note += (

                " The previous-day weather value comes "
                "from long-range climate-model data."

            )


    # ========================================================
    # [24-Z9] LONG-RANGE TARGET INFORMATION
    # ========================================================

    if target_date > forecast_last_date:

        note += (

            " Long-range future weather data is sourced "
            "from the Open-Meteo Climate API."

        )


    # ========================================================
    # [24-Z10] RETURN
    # ========================================================

    return history, note