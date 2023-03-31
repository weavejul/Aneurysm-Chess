# Aneurysm-Chess
----OVERVIEW----
Is GPT-4 even remotely good at playing chess? After extensive testing over the course of a night using terrible, uncommented code I wrote in ninth grade and a fresh new GPT-4 API token, I can conclusively say that GPT-4 is terrible at chess. Steady your mind and take some nimodipine, because what GPT-4 does to this chess board WILL give you an aneurysm.

So what exactly is happening here? Your responses are sent as chess notation to GPT-4, and GPT-4 sends its chess notation back, which is converted into a move. GPT-4 is also given the entire chessboard in text form every move to try and keep it from being too crazy. Despite this, GPT-4 will try to play nonexistent moves, and whenever it does so, it has an "aneurysm" as is shown prominently on the screen. 
What will happen to the board after this aneurysm? WHO KNOWS! That's the fun of the the game. Will a piece disappear? Will you all of a sudden be in check? Will GPT-4 completely fail to realize that IT'S in check? These questions and more will induce your afformentioned aneurysm.

----REQUIREMENTS----
The game requires the python packages found in requirements.txt. Install these with pip install -r requirements.txt.

----API KEY----
This game requires your own GPT-4 API key. $0.03/1k tokens is a lot of money for a youth in the year of our lord 2023. Place your API key in the .env file creatively named .env.env. 

----HOW TO PLAY----
Run the python file named game.py to play the game. An artesanal, hand-crafted GUI will apear, courtesy of myself and pygame. Click and drag the pieces to move. Cells will highlight to show you the legal moves you can make. Be warned, GPT-4 does not particularly care about what is and isnt a 'legal move.' 
Alignment researchers clearly still have to work on AI chess ethics.
