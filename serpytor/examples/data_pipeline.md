# Pipeline data collection and analysis

In this example, we will be building a simple data collection and analysis pipeline using **SerPyTor**.

Features:

- Custom pipeline measuring execution times
- Event captures for logging warnings and errors.
- Logging DB
  
```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from functools import wraps
from serpytor.components.automl import get_best_model
from serpytor.components.pipelines import Pipeline
from serpytor.components.events.event_capture import EventCapture
from serpytor.components.analytics.decorators import get_execution_time

DB_PATH = "./db.json"  # Path to the database

class CustomEventCapture(EventCapture):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @get_execution_time
    def capture_event(self, function: Callable) -> None:
        @wraps(function)
        def wrapper(*args, **kwargs):
            print("Passint through the event capture function")
            output = self.logger.log(function, *args, **kwargs)
            return output

        return wrapper

EVENT_CAPTURE_COMPONENT = CustomEventCapture(db_url=DB_PATH, event_name="Sample Event Capture")

class CustomPipeline(Pipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @EVENT_CAPTURE_COMPONENT.capture_event
    def execution_pipeline(self, *args, **kwargs):
        super().execution_pipeline(*args, **kwargs)


def get_data(*args, **kwargs):
    '''Return the Iris Datasets
    '''
    return load_iris()

def consumer1(data, *args, **kwargs):
    '''Convert received data into training and testing portions
    '''
    features = data.data
    labels = data.target
    
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.25)
    
    return [X_train, X_test, y_train, y_test]

def consumer2(data, *args, **kwargs):
    '''Returns best model available through the AutoML component
    '''
    X_train, X_test, y_train, y_test = data
    return [get_best_model(X_train, y_train), (X_test, y_test)]

def pipeline_work(data, *args, **kwargs):
    pipe = CustomPipeline(pipeline=[(get_data, [], {}), (consumer1, [], {}), (consumer2, [], {})])
    results = pipe.execute_pipeline()
    print(results)

pipeline_work()  # Returns a list containing 2 elements - the best model found for the Iris dataset, and a tuple containing the testing data. 
```

## Step-by-step explanation
