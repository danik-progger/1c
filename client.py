import requests
import aiohttp
import asyncio


def guess(server, name, guess_value):
    response = requests.post(f"{server}/guess", json={"name": name, "guess_value":guess_value})
    return response.json()

def get_history(name, server):
    response = requests.get(f"{server}/get_history/{name}")
    return response.json()

def register_user():
    server_address = input('Enter server address: ')
    name = input('Enter your name: ')
    response = requests.post(f"{server_address}/register", json={"name": name})
    print(response.json())
    print("When an experiment starts you will get a message")
    return server_address, name


async def send_request_to_find_if_experiment_started(url):
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(url) as response:
                data = await response.text()
                if "experiment started" in data:
                    print("Experiment started!!! 😀")
                    return True
            await asyncio.sleep(1)

async def send_request_to_get_answer_from_scientists(url):
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(url) as response:
                data = await response.text()
                if "Your number is" in data:
                    print(data)
                if "Your number is correct" in data:
                    return True
            await asyncio.sleep(1)

def client_loop(server_url, name):
    experiment_started = False
    while not experiment_started:
        experiment_started = asyncio.run(send_request_to_find_if_experiment_started(f"{server_url}/experiment_started/{name}"))

    guessed = False
    while not guessed:
        action = input("'guess' to make a guess, 'history' to view your history: ")
        if action == "guess":
            guess_value = int(input("Enter your guess: "))
            print(guess(server_url, name, guess_value))
            guessed = experiment_started = asyncio.run(send_request_to_get_answer_from_scientists(f"{server_url}/last_guess/{name}"))
        elif action == "history":
            print(get_history(name, server_url))
        else:
            print("You typed a wrong command")
    print("Congratulations, you won the game!")

if __name__ == "__main__":
    print("Dear student, welcome to the guessing experiment!")
    server_url, name = register_user()
    client_loop(server_url, name)
