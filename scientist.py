import requests
from dotenv import dotenv_values

config = dotenv_values(".env")

def start_experiment(server, number):
    response = requests.post(f"{server}/start_experiment", json={"number": number})
    return response.json()

def respond_to_client(server, name, answer):
    response = requests.get(f"{server}/experiment/{name}", json={"answer": f"Your number is {answer}"})
    return response.json()

def get_waiting_participants(server):
    response = requests.get(f"{server}/waiting_participants")
    return response.json()

def get_leaderboard(server):
    response = requests.get(f"{server}/leaderboard")
    return response.json()

def answer(server, name):
    response = requests.post(f"{server}/answer", json={"name": name})
    return response.json()

def scientists_loop(server_url):
    experiment_running = False
    while not experiment_running:
        action = input('Type "start" to start new experiment: ')
        if action == "start":
            number = int(input('Enter a number for clients to guess: '))
            start_experiment(server_url, number)
            experiment_running = True
        else:
            print("command is incorrect")

    while experiment_running:
        action = input('Type "leaderboard" to view leaderboard, "waiting" to view names of all waiting clients, "answer" to answer a client: ')
        if action == "leaderboard":
            print(get_leaderboard(server_url))
        elif action == "waiting":
            print(get_waiting_participants(server_url))
        elif action == "answer":
            name = input("Enter client's name: ")
            ans = answer(server_url, name)
            print(ans)


if __name__ == "__main__":
    print("Clever scientist, welcome to the guessing experiment!")
    server_url = config["SERVER_URL"]
    while True:
        scientists_loop(server_url)
