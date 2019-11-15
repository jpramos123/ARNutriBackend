# ARNutri API

This API aim to centralize the requests of the ARNutri platform.

Request that are made throw this API are:

- Account Creation
- Individual Diabetes classification
- Menu Generation



OBS: You docker instance needs to have almost 4GB of memory to run.

Get the sql server docker image:

docker pull microsoft/mssql-server-linux

And run the image with the following command:

docker run -d --name sql_server_arnutri -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=ARNutri123!@#' -p 1433:1433 microsoft/mssql-server-linux

Set the environment variables:

export FLASK_APP=flaskr.py
export FLASK_ENV=development

To run the application (need to be at the root directory of the application):

flask run

