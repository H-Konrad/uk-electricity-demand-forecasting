# UK Electricity Demand Forecasting








### Data Sources & Attribution

This project uses electricity market and weather data from the following sources:

- Elexon Limited - Electricity market data obtained through the Elexon Insights Solution API. Contains BMRS data © Elexon Limited copyright and database right 2026. [BMRS Data License](https://www.elexon.co.uk/bsc/data/balancing-mechanism-reporting-agent/copyright-licence-bmrs-data/)

- Open-Meteo / UK Met Office - Weather forecast data obtained through the Open-Meteo API using UK Met Office weather model data. UK Met Office data is provided under the CC BY-SA 4.0 licence. [CC BY-SA 4.0 licence](https://creativecommons.org/licenses/by-sa/4.0/)

The underlying training datasets are not distributed with this project. Historical data used for model development is stored separately from the published source code and model. Live prediction inputs are retrieved from the respective APIs at inference time. API responses may be temporarily cached server-side to reduce repeated requests.
