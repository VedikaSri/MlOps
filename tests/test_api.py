# import TestClient so we can send simulated HTTP requests
from fastapi.testclient import TestClient

# import the application object defined in main.py
from main import app

# create a reusable test client for all test functins
client=TestClient(app)

def test_health_endpoint():
    """
    Verify that the application is running and can repond to a health-check request
    """
    response = client.get("/health")

    assert response.status_code == 200

    # Now check reponse body
    assert response.json() == {"status": "healthy"}

def test_valid_iris_prediction():
    """
    Verify that valid flower measurements produce a prediction
    """
    payload= {
    "sepal_length":5.1,
    "sepal_width":3.5,
    "petal_length":1.6,
    "petal_width":0.5
    }

    # send a simulated https post request with json input
    response = client.post("/predict",json=payload)
    assert response.status_code == 200
    # convert the json response into a Python dictionary
    result= response.json()

    # check the response contract: both fields must exists
    assert "prediction" in result
    assert "class_name" in result

    # the predicte class must be one of the three Iris classes
    assert result["class_name"] in ["setosa","versicolor","virginica"]
    # the predicted integer must be 0,1,2
    assert result["prediction"] in [0,1,2]

def test_invalid_iris_input():
    """
    Verify that invalid inputs are rejected by FastAPI
    """
    payload= {
        "sepal_length":5.1,
        "sepal_width":3.5,
        "petal_length":1.6,
    }
    
    # send a simulated https post request with json input
    response = client.post("/predict",json=payload)
    # FastAPI normally returns HTTP 422 for validation error
    assert response.status_code == 422
