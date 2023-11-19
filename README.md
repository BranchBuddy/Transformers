# Backend of BranchBuddy

## Run
First, make sure you hava an OpenAI API key. Place it in the `.env` file under the project root in the following format:

```
OPENAI_KEY=sk-************************************************
```

Then run the following command to install dependencies and start the server:

```bash
pip install -r requirements.txt
python app.py
```

To run the backend in a container, run the following command:

```bash
docker build -t branchbuddy-backend .
docker run -p 5000:5000 branchbuddy-backend
```

## Funtionalities

### Return a summary of remote changes before a pull

- POST `/summarize-assistant`

### Return suggestions of local changes before a commit

- POST `/comment`

### Compare between branches, finding out similar (duplicated) implementations of a same funtionality.

- POST `/compare-functions-between-branches`

### Return a daily/weekly/monthly digest of the advances of the project

- POST `/digest`
