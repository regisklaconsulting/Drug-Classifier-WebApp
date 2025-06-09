# Command to start:
# (...) $ export MODEL_FILE_PATH=/tmp/model/drug-classifier-pipeline.skops && python app/drug_app.py

import logging 
logging.basicConfig(
    level=logging.DEBUG,
    format="[{asctime}] - [{levelname}] - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)

logging.info("")
logging.info(" ================== ")
logging.info(" drug_app.py")
logging.info(" ================== ")
logging.info("")

# Imports 
import os 
import gradio as gr
import skops.io as sio
import warnings
from sklearn.exceptions import InconsistentVersionWarning # type: ignore

# Suppress the version warnings
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

# Explicitly specify trusted types
trusted_types = [
    "sklearn.pipeline.Pipeline",
    "sklearn.preprocessing.OneHotEncoder",
    "sklearn.preprocessing.StandardScaler",
    "sklearn.compose.ColumnTransformer",
    "sklearn.preprocessing.OrdinalEncoder",
    "sklearn.impute.SimpleImputer",
    "sklearn.tree.DecisionTreeClassifier",
    "sklearn.ensemble.RandomForestClassifier",
    "numpy.dtype",
]

# The path of the model is available as an environment variable
MODEL_FILE_PATH = os.getenv("MODEL_FILE_PATH")
logging.info(f">> Loading the model located at [{MODEL_FILE_PATH}]")
training_pipeline = sio.load(str(MODEL_FILE_PATH), trusted=trusted_types)
logging.debug(f"\tLoaded training pipeline: {training_pipeline}")
logging.info("Done!")



def predict_drug(age, sex, blood_pressure, cholesterol, na_to_k_ratio):
    """Predict drugs based on patient features.

    Args:
        age (int): Age of patient
        sex (str): Sex of patient
        blood_pressure (str): Blood pressure level
        cholesterol (str): Cholesterol level
        na_to_k_ratio (float): Ratio of sodium to potassium in blood

    Returns:
        str: Predicted drug label
    """
    features = [age, sex, blood_pressure, cholesterol, na_to_k_ratio]
    predicted_drug = training_pipeline.predict([features])[0]

    label = f"Predicted Drug: {predicted_drug}"
    return label

inputs = [
    gr.Slider(15, 74, step=1, label="Age"),
    gr.Radio(["M", "F"], label="Sex"),
    gr.Radio(["HIGH", "LOW", "NORMAL"], label="Blood Pressure"),
    gr.Radio(["HIGH", "NORMAL"], label="Cholesterol"),
    gr.Slider(6.2, 38.2, step=0.1, label="Na_to_K"),
]
outputs = [gr.Label(num_top_classes=5)]

examples = [
    [30, "M", "HIGH", "NORMAL", 15.4],
    [35, "F", "LOW", "NORMAL", 8],
    [50, "M", "HIGH", "HIGH", 34],
]

title = "Drug Classification"
description = "Enter the details to correctly identify Drug type?"
article = "This app is a part of the **[Beginner's Guide to CI/CD for Machine Learning](https://www.datacamp.com/tutorial/ci-cd-for-machine-learning)**. It teaches how to automate training, evaluation, and deployment of models to Hugging Face using GitHub Actions."

gr.Interface(
    fn=predict_drug,
    inputs=inputs,
    outputs=outputs,
    examples=examples,
    title=title,
    description=description,
    article=article,
    theme=gr.themes.Soft(), # type: ignore
).launch()

