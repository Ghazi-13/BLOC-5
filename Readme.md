# Getaround
GetAround is a company that allows car owners to rent their cars to customers. Sometimes a customer might be late to checkout and the next customer might have to wait to checkin. It leads to cancellations, have a negative impact on the company revenues and image. The goal of this project is to be able to anticipate late checkouts, and evaluate the impact of some measures on car owners revenues.

The project goals:
* Web dashbord acessible anywhere
* Web MLFlow server to exchange with peer data scientists
* Web API exposing a machine learning prediction route 

## Details for certification purpose

* email adress: ghazibouchnak@gmail.com
* video link: https://share.vidyard.com/watch/CQV9RLndkXhxMiFTbrt6j1?


## Links:

* MLFLOW: https://getaround-mlflow-app.herokuapp.com/#/experiments/1
* API: https://getaround-price-pred-api.herokuapp.com/docs
* STREAMLIT: https://getaround-streamlit.herokuapp.com/

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 
Don't forget to replace your access informations.

### Data

The data are composed of 2 dataset:
Delay Analysis -> for delay analysis purpose (dashboard)
Pricing Optimization: for pricing prediction (machine learning + API)

### Prerequisites

* The source code is written in Python 3
* The python packages can be installed with pip : pip3 install or !pip install if in jupyter notebook
* Check packages that need to be imported or installed in the requirements.txt file


## Deployment
* Dashboard:
Build the docker image then run the docker container based on the image, create a heroku app then push your container on it and release the app.

MLFlow
Use your aws secret informations to create a S3 bucket and a posgres database. Build the docker image and run the docker container based on the image for local test. Then create a heroku app and push your container to the app then release the app. Once your MLFlow server is set up, use train.py to train your Machine Learning algorithm and get all the logs online.

API
You must have a MLFlow server and its URI ready at this point. All previous credentials and the server URI must be available in env vars.Build the docker image then run the docker container based on the image, create a heroku app then push your container on it and release the app.

* Build DOCKER IMAGE:  
docker build . -t YOUR_IMAGE_NAME  

* Run MLFLOW:  
docker run -it -v "$(pwd):/home/app" -e AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY" -e AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_ACCESS_KEY" -e BACKEND_STORE_URI="YOUR_BACKEND_STORE_URI" -e ARTIFACT_ROOT="YOUR_S3_BUCKET" -e MLFLOW_TRACKING_URI="YOUR_MLFLOW_HEROKU_SERVER_URI" YOUR_IMAGE_NAME python train.py  

* Run API:  
docker run -it -v "$(pwd):/home/app" -e AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY" -e AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_ACCESS_KEY" -e BACKEND_STORE_URI="YOUR_BACKEND_STORE_URI" -e ARTIFACT_ROOT="YOUR_S3_BUCKET" -e MLFLOW_TRACKING_URI="YOUR_MLFLOW_HEROKU_SERVER_URI" YOUR_IMAGE_NAME python app.py  

* Run STREAMLIT:  
docker run -it -v "$(pwd):/home/app" -e PORT=80 -e AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY" -e AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_ACCESS_KEY" -e BACKEND_STORE_URI="YOUR_BACKEND_STORE_URI" -e ARTIFACT_ROOT="YOUR_S3_BUCKET" YOUR_IMAGE_NAME python app.py  

* Create your app and deploy it on HEROKU  
  1-heroku container:login  
  2-heroku create YOUR_APP_NAME  
  3-heroku container:push web -a YOUR_APP_NAME  
  4-heroku container:release web -a YOUR_APP_NAME  
  5-heroku open -a YOUR_APP_NAME  

-> Don't forget to use your credentials in CLI (command line interface)


## Authors

**Ghazi BOUCHNAK** - [Ghazi-13](https://github.com/Ghazi-13)


