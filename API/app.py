import mlflow
from xmlrpc.client import Boolean
import uvicorn
import pandas as pd 
from pydantic import BaseModel
from typing import Literal, List
from fastapi import FastAPI
import json

# description will apear in the doc
description = """
Welcome to GETAROUND prediction API

GetAround is a company that allows car owners to rent their cars to customers.

To make an approximation of what can be your rental price per day if you are a car owner you just have to specify some informations about your car.

Then submit and the price is displayed in a blink of an eye!!

Enjoy

## Preview

* `/preview` here you can have a preview of the cars pricing dataset


## Predict

* `/predict` put your cars informations here and you'll get you rental price per day


For further informations please visit our github link.
"""

# tags to easily sort roots
tags_metadata = [
    {
        "name": "Preview",
        "description": "Preview of the existing data",
    },

    {
        "name": "Predict",
        "description": "Prediction made with a machine learning model"
    }
]


# initialise API object
app = FastAPI(
    title="GETAROUND API",
    description=description,
    version="1.0",
    contact={
        "name": "Ghazi-13",
        "url": "https://github.com/Ghazi-13",
    },
    openapi_tags=tags_metadata
)

# Define features used in machine learning
class PredictionFeatures(BaseModel):
    model_key: str = "Mercedes"
    mileage: int = 181672
    engine_power: int = 105
    fuel: str = "diesel"
    paint_color: str = "white"
    car_type: str = "hatchback"
    private_parking_available: bool = True
    has_gps: bool = True
    has_air_conditioning: bool = False
    automatic_car: bool = False
    has_getaround_connect: bool = True
    has_speed_regulator: bool = False
    winter_tires: bool = True


# Preview a few rows of the dataset
@app.get("/preview", tags=["Preview"])
async def exemple():
    """
    Get a sample of 5 rows from the dataset
    """
    print("/preview called")
    df = pd.read_csv("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv")

    # Select only n rows
    sample = df.sample(5).iloc[:,1:]
    return sample.to_json(orient='records')

# Predict the rental price for the given cars
@app.post("/predict", tags=["Predict"])
async def predict(predictionFeatures: PredictionFeatures):
    """
    the daily rental price prediction:

    {'prediction': values}
    
    """
    print("/predict called")
    # Read data
    dataset = pd.DataFrame(dict(predictionFeatures), index=[0])

    # Log model from mlflow
    logged_model ='runs:/235a123f1c8a4fc888a9e8eedf583899/getaround_price_estimator'
    

    # Load model as a PyFuncModel.
    loaded_model = mlflow.pyfunc.load_model(logged_model)
    prediction = loaded_model.predict(dataset)

    # Format response
    response = {"prediction": prediction.tolist()[0]}
    return response

# What to do when the script is runned as main script
if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000, debug=True, reload=True)