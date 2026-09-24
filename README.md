# UK Electricity Demand Forecasting

This project develops and deploys a machine learning application for forecasting Great Britain’s electricity demand over the next 24 hours at half-hourly intervals.

The project covers data collection, PostgreSQL storage, feature engineering, model training and evaluation, live inference through a FastAPI backend, and an interactive Streamlit application. 

The forecasting pipeline combines historical electricity demand, historical electricity generation, and weather forecasts to generate 48 future demand predictions. Several machine learning models were evaluated, with XGBoost selected as the final deployed model.

## Project Links

- Live Application: [Streamlit App](https://uk-electricity-demand-forecasting-eypjsess6mtpzorjkmwdxy.streamlit.app/)
- Electricity Data: [Elexon Insights Solution API](https://developer.data.elexon.co.uk/api-details#api=prod-insol-insights-api&operation=get-generation-availability-summary-14d)
- Weather Data: [Open-Meteo](https://open-meteo.com/en/docs/ukmo-api)

## Application

The app uses a Streamlit frontend with a FastAPI backend deployed on Render. The backend retrieves electricity and weather data, prepares the model input data, generates forecasts, and returns the results to the Streamlit interface.

### Live Forecast Dashboard

### Model Performance

### Prediction Explanations

### Live Data and Refresh Behaviour

## Development

### Data Collection

Historical electricty market data was collected from the Elexon Insights Solution API, including electricty demand, generation by fuel type (including interconnectors and generation fuels), and published demand forecasts. Weather forecast data was collected from Open-Meteo using the UK Met Office forecast model across eight locations (Manchester, Plymouth, Norwich, Edinburgh, Cardiff, London, Inverness, and Newcastle) in Great Britain.

The data was stored in PostgreSQL, with separate tables used for demand, generation, forecasts, and weather. An additional locations table was used to provide location keys for the weather data. The database was then used to create the modelling dataset, while also making it easier to explore and analyse the data using SQL.

### Feature Engineering

### Model Training

### Model Evaluation

## Repository Structure

## Requirements and Local Setup

### Running the API

### Running the Streamlit App

### Docker

## Limitations and Future Improvements

## Data Sources & Attribution

This project uses electricity market and weather data from the following sources:

- Elexon Limited - Electricity market data obtained through the Elexon Insights Solution API. Contains BMRS data © Elexon Limited copyright and database right 2026. See the [BMRS Data License](https://www.elexon.co.uk/bsc/data/balancing-mechanism-reporting-agent/copyright-licence-bmrs-data/).

- Open-Meteo / UK Met Office - Weather forecast data obtained through the Open-Meteo API using UK Met Office weather model data. UK Met Office data is provided under the [CC BY-SA 4.0 licence](https://creativecommons.org/licenses/by-sa/4.0/).

The underlying training datasets are not distributed with this project. Historical data used for model development is stored separately from the published source code and model. Live prediction inputs are retrieved from the respective APIs at inference time. API responses may be temporarily cached server-side to reduce repeated requests.
