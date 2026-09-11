import requests
import pandas as pd
import streamlit as st
import altair as alt

api_url = "http://localhost:8000"

forecast_response = requests.get(
    f"{api_url}/forecast"
)

if forecast_response.status_code == 200:
    forecast = pd.DataFrame(
        forecast_response.json()
    )

    forecast["target_time"] = pd.to_datetime(
        forecast["target_time"], 
        utc = True
    ).dt.tz_localize(None)

    start_date = forecast["target_time"].min().strftime("%d %b %Y")
    end_date = forecast["target_time"].max().strftime("%d %b %Y")
    max_demand = forecast["predicted_demand"].max()
    min_demand = forecast["predicted_demand"].min()
    average_demand = forecast["predicted_demand"].mean()

else:
    detail = forecast_response.json().get(
        "detail",
        "Forecast unavailable."
    )
    st.error(detail)

model_info = requests.get(
    f"{api_url}/model-info"
).json()

st.set_page_config(
    page_title = "UK Electricity Demand Forecast",
    layout = "wide"
)

st.title("UK Electricity Demand Forecast")

st.markdown(
    "24-hour electricity demand forecasts for Great Britain using "
    "Elexon market data, Open-Meteo weather forecasts, and an XGBoost model."
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Model", 
        model_info["model"],
        border = True,
        width = "stretch"
    )

with col2:
    st.metric(
        "Test MAE", 
        f"{model_info["mae"]} MW",
        border = True,
        width = "stretch"
    )

with col3:
    st.metric(
        "Test RMSE", 
        f"{model_info["rmse"]} MW",
        border = True,
        width = "stretch"
    )

with col4:
    st.metric(
        "Forecast Window", 
        "24 hours",
        border = True,
        width = "stretch"
    )

st.divider()

st.info(
    "Data availability: approximately a 1.5-hour delay. "
    "Forecasts begin from the latest available data. "
    "All timestamps are in UTC."
)

chart = alt.Chart(forecast).mark_line(
    strokeWidth = 3
).encode(
    x = alt.X(
        "target_time:T",
        title = f"Time (UTC) | {start_date} – {end_date}"
    ),
    y = alt.Y(
        "predicted_demand:Q",
        title = "Predicted Demand (MW)"
    ),
    tooltip = [
        alt.Tooltip(
            "target_time:T", 
            title = "Time",
            format = "%H:%M %d %B %Y"
        ),
        alt.Tooltip(
            "predicted_demand:Q",
            title = "Predicted Demand (MW)",
            format = ".0f"
        )
    ]
).interactive()

st.altair_chart(
    chart,
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Minimum Demand",
        f"{min_demand:.0f} MW",
        border = True,
        width = "stretch"
    )

with col2:
    st.metric(
        "Average Demand",
        f"{average_demand:.0f} MW",
        border = True,
        width = "stretch"
    )

with col3:
    st.metric(
        "Maximum Demand",
        f"{max_demand:.0f} MW",
        border = True,
        width = "stretch"
    )

st.divider()

horizon_to_time = dict(
    zip(forecast["horizon"], forecast["target_time"])
)

col1, col2 = st.columns([1, 4.5])

with col1:
    selected_horizon = col1.selectbox(
        "Select forecast target time",
        options = range(1, 49),
        format_func = lambda horizon: str(horizon_to_time[horizon])
    )

    horizon_explanation = requests.get(
        f"{api_url}/forecast/explanation/{selected_horizon}"
    ).json()

    st.metric(
        "Predicted Demand",
        f"{horizon_explanation["prediction"]:.0f} MW",
        border = True,
        width = "stretch"
    )

    st.metric(
        "Model Baseline",
        f"{horizon_explanation['base_shap_value']:.0f} MW",
        border = True,
        width = "stretch"
    )

with col2:
    feature_effects = pd.DataFrame(
        horizon_explanation["features"]
    )

    chart = alt.Chart(feature_effects).mark_bar().encode(
        x = alt.X(
            "shap_value:Q",
            title = "SHAP Value"
        ),
        y = alt.Y(
            "feature:N",
            title = "Feature",
            sort = feature_effects["feature"].tolist(),
            axis = alt.Axis(
                labelLimit = 200
            )
        ),
        tooltip = [
            alt.Tooltip(
                "feature:N", 
                title = "Feature"
            ),
            alt.Tooltip(
                "shap_value:Q",
                title = "SHAP Value",
                format = ".0f"
            )
        ]
    )

    st.altair_chart(
        chart,
        height = "stretch"
    )

st.divider()

st.caption(
    "Data sources & attribution"
)

st.markdown(
    """
    <div style="font-size: 0.8rem; color: #777;">
        <p>
            <strong>Elexon Limited</strong> - Electricity market data obtained 
            through the Elexon Insights Solution API. Contains BMRS data © Elexon 
            Limited copyright and database right 2026.
            <a href="https://www.elexon.co.uk/bsc/data/balancing-mechanism-reporting-agent/copyright-licence-bmrs-data/"
                target="_blank">
                BMRS Data License
            </a>
        </p>
        <p>
            <strong>Open-Meteo / UK Met Office</strong> - Weather forecast data 
            obtained through the Open-Meteo API using UK Met Office weather model data.
            UK Met Office data is provided under the CC BY-SA 4.0 licence.
            <a href="https://creativecommons.org/licenses/by-sa/4.0/"
                target="_blank">
                CC BY-SA 4.0 licence
            </a>
        </p>
        <p>
            The underlying training datasets are not distributed with this project. 
            Historical data used for model development is stored separately from the 
            published source code and model. Live prediction inputs are retrieved from the
            respective APIs at inference time. API responses may be temporarily cached server-side 
            to reduce repeated requests.
        </p>
    </div>
    """,
    unsafe_allow_html = True
)