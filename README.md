# Named Entity Recognition Web Application

Here's a project on exploring and testing out the NER model. We are given words with label (it's a person name or not) for the training process. Then after we have our model, we can use a Python Web Server to output to prediction of the inputed words on the website.

<img width="1420" alt="Screenshot 2023-04-14 at 1 49 32 AM" src="https://user-images.githubusercontent.com/82365010/231842664-fd2ef01e-d60e-471c-888b-d7dba87c0e85.png">

## Keywords

- Named Entity Recognition
- NLTK Maxent Classifier
- names_dataset
- Flask

## Installation

For the purpose of running the project, you have to install all the needed modules. I prefer using the virtual environment in Python in a way that all modules are independent for this project.

Install the virtualenv module:

```bash
python3 -m pip install --user virtualenv
```

Creating a virtual environemnt inside the project:

```bash
cd ./project-name
python3 -m venv venv
```

Activating the venv:

```bash
source venv/bin/activate
```

At this stage, you have a seperated environment for accessing the modules for this project. You might want to install the required modules altogether, so run the following command to install all of them:

```bash
pip install -r requirements.txt
```


To leave the venv if you no longer needed it:

```bash
deactivate
```

> My environment is on MacOS, it would be slightly different if you're on Windows. Just google it.

## To run the NER Model

The entry of the py script for the model is this file `src/scripts/run.py`. It requires a argument to work:

```bash
python src/scripts/run.py -t | -d | -s | -p

// --train, --dev, --show, --predict
```

In order to do prediction, you have to train the model first. Then since the customed sentence is hard coded so far, you will need to change it in the code if you want. Otherwise, I suggest adding an extra agrument for the sentence if CLI needed.

## To run the Web Server

We're using Flask for the Web Server. To boot the web server, you will need to execute the entry file which is located in here `src/app.py`.

```bash
python ./src/app.py
```

It will take a bit time for the server run, because it will need to load the model first for the futher usage.
