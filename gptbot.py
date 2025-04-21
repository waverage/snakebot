from openai import OpenAI
import time
import re
from dotenv import load_dotenv
import os

INITIAL_PROMPT = """
Hey, lets play text-based snake videogame. You are the player. With each message I will write you the game state. The game board is 7x7.
You must avoid walls and snake's body, because if you collide with them the snake dies and you lose. Your goal is to find food and eat it. Each time you eat food the snake becomes longer.

The game state description
The state it is a grid of cells. The size of the grid is 7 by 7. It has 7 rows and 7 columns. Cells divided by one space. Each cell described by a symbol.
Here is the explanation of all symbols:
"." - it is an empty cell.
"w" - it is a wall. When you hit that you lose.
"f" - it's food that you should "eat". 
"b" - it's snake's body, don't crush into it when you move.
"l" - it's snake's head and it also represents the direction of a snake. "l" means snake moves left.
"r" - it's snake's head that moves right.
"u" - it's snake's head that moves upwards.
"d" - it's snake's head that moves downwards.

Here is an example state of the game:
```
w w w w w w w
w . b b r . w
w . b b b . w
w . . . . . w
w . . . . . w
w . . . . . w
w w w w w w w
```
In this situation if you decide to move up, the snake will die, because there is a wall on the top. If you decide to go down, the snake will die, because there is snake's body, so the snake will colide with itself. So you have only one correct movement - to the right. The next state will be:
```
w w w w w w w
w . b b b r w
w . b b . . w
w . . . . f w
w . . . . . w
w . . . . . w
w w w w w w w
```
Remember that you cant turn right when you are moving left in one step. First you have to move down or up then right. The same when you are moving up you cant turn down. First you have to move left or right and only then down.
Now you have to move down in order to keep the snake alive and move towards the food.
You control the snake movements by saying me words: "down", "up", "left", "right". When you say me "down" it means that snake will turn down. 
Be smart think for two or three steps ahead. Think what will happen if you turn left or right or down or up. You have to consider that your tail is long and dangerous. You have to avoid your tail.
So, once again I send you the state of the game, you analyze carefully what you are going to do and reply me in the format:
```
explanation: why you decided to do that step, what you want to achieve with this turn, why you didn't choose other direction.
food_direction: food direction according to the snake's head. left, right, up or down
left: what is going to happen if you turn left
right: what is going to happen if you turn right
up: what is going to happen if you turn up
down: what is going to happen if you turn down
action: in which direction the snake should turn
```
 Lets try to play now."""

class ChatGptBot:
    def __init__(self) -> None:
        load_dotenv()
        API_KEY = os.getenv('CHATGPT_API_KEY')
        print("API_key", API_KEY)
        self.client = OpenAI(api_key=API_KEY)
        self.messages = [{"role": "developer", "content": INITIAL_PROMPT}]

    def predict(self, obs) -> int:
        nextMessage = self.getNextMessage(obs)
        self.messages.append({"role": "user", "content": nextMessage})

        time.sleep(0.4)
    
        response = self.client.responses.create(
            model="gpt-4.1",
            input=self.messages,
            store=True
        )

        print("Response: ", response.output[0].content[0].text)

        self.messages += [{"role": el.role, "content": el.content} for el in response.output]

        nextAction = self.parseReply(response.output[0].content[0].text)
        if nextAction == -1:
            print("bad action")
            exit()
        
        return nextAction
    
    def punch(self, reason) -> None:
        punchMessage = "You lost because " + reason + "! But don't worry, you can try again from the beggining."
        print(punchMessage)
        self.messages.append({"role": "user", "content": punchMessage})

    def getNextMessage(self, obs) -> str:
        print(obs)
        return "```\n" + obs + "\n```"
    
    def parseReply(self, reply) -> int:
        reply = reply.lower()

        x = re.search("action:\s(\w+)", reply)
        if x is None:
            print("Usupported reply: ", reply)
            return -1
        
        action = x.group(1)

        if action == "up":
            return 0
        elif action == "right":
            return 1
        elif action == "down":
            return 2
        elif action == "left":
            return 3
        else:
            print("Usupported reply: ", reply)
            return -1
