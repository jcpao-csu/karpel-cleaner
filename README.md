# karpel-cleaner
Automated Python data cleaner of JCPAO case data reports

## Getting Started 

### Installation

1. Clone the repository:
```
git clone
```

2. Install Python dependencies:
```
# Set up virtual environment
cd 
python -m venv <venv name>
source <venv name>/bin/activate # Activate venv on MacOS / Linux
<venv name>\Scripts\activate # Activate on Windows 
deactivate # Deactivate venv on any operating system

pip install -r requirements.txt 
```

3. Create .env file and include the following:

- KARPEL_USERNAME
- KARPEL_PASSWORD

### Usage 

1. Run the main.py script:
```
python main.py
```

## About the Karpel Cleaner

Prosecutor by Karpel (PbK) is a cloud-based case management service that serves as the main hub for criminal case entry and tracking. From four custom-made reports, we are able to evaluate the Office's performance on cases received, filed, declined, and disposed. The Karpel Cleaner (main.py) automates the downloading and initial data cleaning of the Karpel custom data reports. The resulting output is then used to feed other data products:

- Homicide Ticker
- Case Dashboard
- Violent Crime Dashboard 
- Police Report Number Search Tool
- Internal Dashboards

