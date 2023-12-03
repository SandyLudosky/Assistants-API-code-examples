## Project : Build a AI-powered chatbot application

....

## **Install Python** ![Python](img/python_65.png)

A [Quick Guide for Installing](https://github.com/PackeTsar/Install-Python/blob/master/README.md#install-python-) Python on Common Operating Systems

....

**openai** : [OpenAI](https://openai.com/) is an artificial intelligence research laboratory consisting of the for-profit corporation OpenAI LP and its parent company, the non-profit OpenAI Inc. The company, considered a competitor to DeepMind, conducts research in the field of artificial intelligence (AI) with the stated aim to promote and develop friendly AI in such a way as to benefit humanity as a whole.

**python-dotenv** : [python-dotenv](https://pypi.org/project/python-dotenv/) reads key-value pairs from a .env file and can set them as environment variables. It is great for managing app settings during development and in production using 12-factor principles.

**colorama** : [colorama](https://pypi.org/project/colorama/) makes ANSI escape character sequences (for producing colored terminal text and cursor positioning) work under MS Windows.

## Create a virtual environment :

**MacOS/Linux**:

```
python3 -m venv env
```

**Windows**:

```
python -m venv env
```

## Activate the virtual environment :

```
source env/bin/activate
```

## Installation:

**MacOS/Linux**:

```
pip3 install -r requirements.txt
```

**Windows**:

```
pip install -r requirements.txt
```

## [Get an API key](https://platform.openai.com/account/api-keys)

### Set the key as an environment variable:

`export OPENAI_API_KEY='sk-brHeh...A39v5iXsM2'`

.env file:

```
OPENAI_API_KEY=sk-brHeh...A39v5iXsM2
```

## Run the script:

**MacOS/Linux**:

```
python3 main.py
```

**Windows**:

```
python main.py
```

## start Streamlit app

```
streamlit run main.py
```
