from fastapi import FastAPI, WebSocket, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

participants = {}
current_experiment = None
leaderboard = []

class Experiment:
    def __init__(self, secret_number: int):
        self.secret_number = secret_number
        self.guesses = {}

class Participant(BaseModel):
    name: str

class NumberToGuess(BaseModel):
    number: int

class Guess(BaseModel):
    name: str
    guess_value: int

class Guess(BaseModel):
    name: str
    guess_value: int

class StartedExperimentMessage(BaseModel):
    message: str

@app.post("/register")
async def register(participant: Participant):
    if participant.name in participants:
        raise HTTPException(status_code=400, detail="Participant already registered")
    participants[participant.name] = {
        "attempts": 0,
        "history": [],
        "status": "waiting"
    }
    leaderboard.append(participant.name)
    return {"message": f"{participant.name} registered successfully"}

@app.post("/start_experiment")
async def start_experiment(number: NumberToGuess):
    global current_experiment
    secret_number = number
    current_experiment = Experiment(secret_number)
    for participant in participants:
        participants[participant]['status'] = "active"
    return {"message": "Experiment started", "secret_number": secret_number}

@app.get("/experiment_started/{name}")
async def start_experiment(name: str):
    if participants[name]['status'] == "active" or participants[name]['status'] == "posted new guess":
        return {"message": "experiment started"}
    else:
        return {"message": "experiment is not started yet"}

@app.get("/get_history/{name}")
async def start_experiment(name: str):
    if participants[name]['status'] == "active" or participants[name]['status'] == "posted new guess":
        return {"history": participants[name]["history"]}
    else:
        return {"message": "you have no history"}

@app.post("/guess")
async def guess(guess: Guess):
    name = guess.name
    guess_value = guess.guess_value
    if name not in participants:
        raise HTTPException(status_code=404, detail="Participant not found")
    if current_experiment is None:
        raise HTTPException(status_code=400, detail="No active experiment")

    participants[name]['attempts'] += 1
    participants[name]['history'].append(guess_value)
    participants[name]['status'] == "posted new guess"
    participants[name]['scientists_ans'] = ""
    return {"message": "your guess is delivered"}

@app.get("/last_guess/{name}")
async def guess(name: str):
    if name not in participants:
        raise HTTPException(status_code=404, detail="Participant not found")
    if current_experiment is None:
        raise HTTPException(status_code=400, detail="No active experiment")

    if participants[name]['status'] == "posted new guess":
        return { "message": "scientists haven't answered yet"}
    elif participants[name]['status'] == "active":
        return { "message": participants[name]['scientists_ans'] }

@app.post("/answer")
async def guess(name: Participant):
    name = name.name
    if name not in participants.keys():
        raise HTTPException(status_code=404, detail="Participant not found")
    if current_experiment is None:
        raise HTTPException(status_code=400, detail="No active experiment")

    last_guess = participants[name]['history'][-1]
    if last_guess < current_experiment.secret_number.number:
        answer = "Your number is less"
    elif last_guess > current_experiment.secret_number.number:
        answer = "Your number is more"
    else:
        answer = "Your number is correct"
    participants[name]['scientists_ans'] = answer
    participants[name]['status'] = "active"
    return { "message": "answer is delivered" }

@app.get("/waiting_participants")
async def get_participants():
    waiting = []
    for name in participants.keys():
        if participants[name]['status'] == "posted a new guess":
            waiting.append(participants[name])
    return {"participants": waiting}

@app.get("/leaderboard")
async def get_leaderboard():
    sorted_leaderboard = sorted(leaderboard, key=lambda x: participants[x]['attempts'])
    final_leaderboard = []
    for el in sorted_leaderboard:
        final_leaderboard.append([el, participants[el]['attempts']])
    return {"leaderboard": final_leaderboard}


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
