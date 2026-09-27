# UK Electricity Demand Forecasting

This project develops and deploys a machine learning application for forecasting Great Britain’s electricity demand over the next 24 hours at half-hourly intervals.

The project covers data collection, PostgreSQL storage, feature engineering, model training and evaluation, live inference through a FastAPI backend, and an interactive Streamlit application. 

The forecasting pipeline combines historical electricity demand, historical electricity generation, and weather forecasts to generate 48 future demand predictions. Several machine learning models were evaluated, with XGBoost selected as the final deployed model.

## Project Links

**Deployment Notice:** *The application is hosted on Render, which uses shared IP addresses. Open-Meteo applies rate limits to its free API by IP address, so usage from other services sharing the same Render IP can cause the daily limit to be reached. When this occurs, the Streamlit application cannot retrieve the required weather data and will display an error until the API becomes available again. The application and API function normally when run locally, unless the external data providers are unavailable.*

- Live Application: [Streamlit App](https://uk-electricity-demand-forecasting-eypjsess6mtpzorjkmwdxy.streamlit.app/)
- Electricity Data: [Elexon Insights Solution API](https://developer.data.elexon.co.uk/api-details#api=prod-insol-insights-api&operation=get-generation-availability-summary-14d)
- Weather Data: [Open-Meteo](https://open-meteo.com/en/docs/ukmo-api)

## Application

![Application screenshot](https://github.com/user-attachments/assets/f696c69c-5933-4a6b-84d4-ef697e6a7b48)

The app uses a Streamlit frontend with a FastAPI backend deployed on Render. The backend retrieves electricity and weather data, prepares the model input data, generates forecasts, and returns the results to the Streamlit interface.

### Model Performance

![Model performance](https://github.com/user-attachments/assets/292b457b-e1b6-433d-9c26-1e88f76bb8de)

The application displays the deployed model alongside its test performance metrics, including MAE and RMSE. This provides context for the expected forecasting accuracy of the model. 

Currently, these metrics are static. Ideally, the models would be periodically evaluated against new data, with the performance metrics automatically updated to reflect their latest performance.  

### Live Forecast

![Live forecast](https://github.com/user-attachments/assets/aec0cebc-8825-4f4b-91e3-a0aec6f34a40)

The Streamlit dashboard displays the latest 24-hour electricity demand forecast across 48 horizons using a line chart. Below the line chart, a summary panel shows the minimum, average, and maximum demand for the forecast period. 

### Prediction Explanations

![Prediction explanations](https://github.com/user-attachments/assets/51c8418f-d625-4f18-98f5-cf27919b21ec)

Under the live forecast, a dropdown provides all 48 forecast horizons. These can be selected to see a SHAP-based explanation of the prediction. The application shows the predicted demand along with the model baseline and, on the right, a bar chart showing the top 10 features ranked by absolute influence, with their actual positive or negative SHAP values displayed.

### Live Data and Refresh Behaviour

As the application uses live data that is not stored, both the API and Streamlit use caching to reduce repeated API calls and recomputation. Both caches refresh every 15 minutes. 

## Development

### Data Collection

Historical electricity market data was collected from the Elexon Insights Solution API, including electricity demand, generation by fuel type (including interconnectors and generation fuels), and published demand forecasts. Weather forecast data was collected from Open-Meteo using the UK Met Office forecast model across eight locations (Manchester, Plymouth, Norwich, Edinburgh, Cardiff, London, Inverness, and Newcastle) in Great Britain.

The data was stored in PostgreSQL, with separate tables used for demand, generation, forecasts, and weather. An additional locations table was used to provide location keys for the weather data. The database was then used to create the modelling dataset, while also making it easier to explore and analyse the data using SQL.

### Feature Engineering

Raw demand, generation, and weather data were turned into features that were more useful for forecasting. Temporal data was separated into features such as time of day, season, and weekend indicators. Historical demand and generation values were also transformed into lagged and rolling features so the models could capture recent trends and recurring patterns. 

Each time was expanded into 48 forecast horizons, representing half hourly demand predictions across 24 hours. The horizon was included as a model feature, allowing a single model to learn across all forecast lead times rather than training a separate model for each horizon.

The features were checked to see whether they were useful and whether any were too similar or unnecessary. For example, temperature forecasts across the UK were highly correlated, so these were combined into aggregate temperature features instead of keeping each location separate.

The final feature set contains historical demand, generation, weather conditions, and calendar information. With approximately 52,000 half-hourly observations across three years, expanding each observation across 48 forecast horizons produced roughly 2.5 million rows in the final modelling dataset.

### Model Training

The modelling dataset was split chronologically into 70% training, 15% validation and 15% test data. This preserved the time ordering of the observations and ensured that models were trained only on data occurring before the validation and test periods.

Simple forecasting baselines were created first, using recent historical demand values such as demand from 30 minutes earlier and demand from the same period one week earlier. These provided a reference point for assessing whether the machine learning models offered a meaningful improvement.

Three machine learning models were trained and compared: Ridge Regression, Random Forest and XGBoost. Ridge Regression was used as a regularised linear model, providing a ML benchmark while being less affected by correlated input features than linear regression. Random Forest and XGBoost were then used to capture more complex non-linear relationships between electricity demand and the engineered features. Hyperparameter tuning was done using randomised search. A small set of hyperparameters was explored to reduce training time for the tree-based models.

### Model Evaluation

Models were evaluated using the test split, with performance being assessed using MAE and RMSE. Results were also compared against the simple forecasting baselines created during model training. Model performance was also analysed across different forecast horizons, seasons, times of day and electricity demand levels, including lower demand periods below 20,000 MW and higher demand periods above 35,000 MW.

All three machine learning models were also compared against Elexon's published demand forecasts. Elexon's forecasts performed better overall, providing a useful benchmark for the project. The best-performing model was not too far behind Elexon's forecasts.

XGBoost achieved the strongest overall performance and was selected as the final deployed model, with a test MAE of approximately 1,280 MW and RMSE of approximately 1,721 MW.

Feature importance and SHAP analysis were then performed on the final XGBoost model. Historical demand features, particularly demand from 24 hours and seven days prior, were by far the most influential predictors. SHAP values showed that individual features could have substantial effects on specific predictions, in some cases changing the predicted demand by more than 1,000 MW.

## Repository Structure

uk-electricity-demand-forecasting/
├── data/             # Modelling datasets, API response samples, and results
├── models/           # Trained models
├── notebooks/        # EDA, modelling, and evaluation notebooks
├── requirements/     # Project and API dependencies
├── sql/              # SQL queries
├── src/              # All project code for data collection, model training, API, Streamlit Etc.
├── tests/            # Small test examples for data parsers
├── Dockerfile        # Docker configuration for the API
├── .dockerignore
├── .gitignore
└── README.md

## Requirements and Local Setup

The project has three dependency files for development, FastAPI, and Streamlit. 

For the development setup:
```pip install -r requirements/project.txt```

### Running the API

For the API setup:
```pip install -r requirements/api.txt```

To start the API:
```uvicorn src.deployment.api.main:app --reload```

The API is then run locally at:
```http://localhost:8000```

### Running the Streamlit App

For the Streamlit setup:
```pip install -r src/deployment/app/requirements.txt```

To start the Streamlit app:
```streamlit run src/deployment/app/streamlit_app.py```

The Streamlit app will connect to the FastAPI backend and display the live electricity demand forecast. To run the app locally, change the ```api_url``` to the local API address.

### Docker

The FastAPI backend can also be run using Docker.

Build the image from the project root:
```docker build -t uk-electricity-demand-forecasting .```

Then run the container:
```docker run -p 8000:8000 uk-electricity-demand-forecasting```

This starts the API inside a container using the configuration defined in the Dockerfile.

## Limitations and Future Improvements

Several areas could be looked into to improve forecasting performance further: 
- Additional features and feature engineering: New demand, generation or weather features could be introduced, alongside further transformations or combinations of existing features such as regional weather weighting or population weighed weather features. 
- Target transformation: The target could be transformed, for example using log demand, which may reduce the effect of changing variance for different demand levels and improve performance across low or high demand. 
- Model tuning: A wider hyperparameter search or additional forecasting models could be tested to explore whether further improvements in predictive performance are possible.

## Data Sources & Attribution

This project uses electricity market and weather data from the following sources:

- Elexon Limited - Electricity market data obtained through the Elexon Insights Solution API. Contains BMRS data © Elexon Limited copyright and database right 2026. See the [BMRS Data License](https://www.elexon.co.uk/bsc/data/balancing-mechanism-reporting-agent/copyright-licence-bmrs-data/).

- Open-Meteo / UK Met Office - Weather forecast data obtained through the Open-Meteo API using UK Met Office weather model data. UK Met Office data is provided under the [CC BY-SA 4.0 licence](https://creativecommons.org/licenses/by-sa/4.0/).

The underlying training datasets are not distributed with this project. Historical data used for model development is stored separately from the published source code and model. Live prediction inputs are retrieved from the respective APIs at inference time. API responses may be temporarily cached server-side to reduce repeated requests.
