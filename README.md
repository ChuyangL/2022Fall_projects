# 2022Fall_projects: Connect Three

Group Member: Maggie Zhang, Chuyang Li

Project Type Choice: Option 3

## Intention:
Our goal is to develop the game of Connect Three with certain strategy. Connect Three is a simplified game derived from traditional Connect Four game, which is a two-player connection board game which is first solve in 1988. It requires each player take turns to drop tokens into a vertically suspended grid, which occupies the lowest available space within the column. The condition of winning is to be the first to form a horizontal, vertical or diagonal line in three tokens of one player. The size of grid of our choice is 5 * 5 grid, which is smaller than Connect Four board. This size of board now proved to be strongly solved. However, as the standard Connect Four (7 * 6 grid) is solved, there are certain strategy we can refer to when we implement the game. Based on existing program of standard Connect Four games, we are going to develop our own 5 * 5 Connect Three game with reasonable time complexity, proven mathematical strategy and visible output of game process.

## Originality:
Instead of solved 7 * 6 standard Connect Four game, we choose 5 * 5 Connect Three game, which is strongly solved with smaller game space. To implement the game, we will first analyze the game with a standard board 7-column-wide, 6-row-high grid. Then we would try strategy on 5 * 5 Connect Three game to see if certain strategies applied in solving 7 * 6 games is also suitable. Therefore, we can validate this claim through our own analysis through the final outcome and performance of our program.  

## Program files:
Connect_three.py contains all code need for the game.

## Algorithm:
The algorithm we are using in this game is minimax with Alpha-Beta pruning. An example of minimax searching tree for Connect Four (7 * 6) game is shown below:
<img width="206" alt="image" src="https://user-images.githubusercontent.com/89555523/206934053-788d19ea-1a23-4501-b661-d029154b2bf3.png">
Its strategy is to search within given depth (n steps forward) for every possible position, returning score for the result. The score is given by following rules (using maximize player as example):
  •	Occupation of middle columns will achieve higher score
  •	For each evaluation window, more occupied window gets higher score
  •	If the window is occupied by the opponent, the score of the window is negative
  •	The iteration stops when alpha is greater than beta (alpha cut-off)
According to this, we have following pseudo code:
<img width="407" alt="image" src="https://user-images.githubusercontent.com/89555523/206934085-37318a97-c894-4440-a480-94ffeb1d6124.png">

## Targeted Algorithm Analysis:
As we are using minimax algorithm, the heuristic evaluation function of our program is the minimax method (in Board class). The minimax will recursively call itself to evaluate the next step based on given status of the board. Therefore, the big-O of the minimax function is the linear function of the depth multiplies the number of columns (O(d * n)), and the big-Omega will be constant (O(1)).
Also, the minimax function may call is_winning() method in each time of iteration to see if this is a terminating step. The brute-force implement of the is_winning() function is to search the horizontal, vertical and diagonal windows based on each node of the board, which makes the big-O to be O(n * n). To make an improvement on this function, we encoded our board into the form of bits according to Dominikus Herzberg’s implement of Connect Four game, which allows bit shifting and combining bits that make it a parallel computation for all positions on the board. Therefore, the big-O of this method is constant. An example of encoding is attached below:
<img width="468" alt="image" src="https://user-images.githubusercontent.com/89555523/206934108-f4807cf4-8d4d-41e8-9413-a77a26b6e32e.png">
At the last iteration of minimax, a function to call score_position to evaluate score of the final status. The big-O of this method is O(n * n), as it search windows based on every node on the board. Therefore, the final time complexity of the minimax method is O(n^3).

## Performance Measurement:
To test the game, we set one as human and another player as automated player. Player 1 is allowed to make moves through pygame interface. A picture of the surface is attached below:
<img width="183" alt="image" src="https://user-images.githubusercontent.com/89555523/206934132-8ada7308-049c-4814-8062-de4341872892.png">
As the Connect Three game is a solved game, which means that if there are no mistakes made during the game (the player always picks the optimized move for each step), the first player will always win. Therefore, we let the automated player to move first to test at what search depth will this player win the game. Through testing, we can see that starting from depth of 4, the automated player has a significant higher winning rate than depth of three and below. The depth of 5 has the best performance.
However, during playing we can still see some flaws in the strategy of the minimax function, especially for the score_position method. For example, sometimes the automated player cannot take steps for immediate winning, and increasing depth or changing score does not help with this situation.
As the Connect Three game is a solved game, which means that if there are no mistakes made during the game (the player always picks the optimized move for each step), the first player will always win. Therefore, we let the automated player to move first to test at what search depth will this player win the game. Through testing, we can see that starting from depth of 4, the automated player has a significant higher winning rate than depth of three and below. The depth of 5 has the best performance.
However, during playing we can still see some flaws in the strategy of the minimax function, especially for the score_position method. For example, sometimes the automated player cannot take steps for immediate winning, and increasing depth or changing score does not help with this situation.
<img width="282" alt="image" src="https://user-images.githubusercontent.com/89555523/206934146-1f162eb3-56ab-4da1-95f0-fc992e079c0e.png">

## Contribution:
Chuyang Li: Implementation of the automated player, analysis and presentation.
Maggie Zhang: Implementation of is_winning and make_move method, analysis.

## Reference:
1.	7 * 6 standard Connect Four Game (From scratch)
https://cpb-us-w2.wpmucdn.com/u.osu.edu/dist/b/69689/files/2018/12/Connect-Four-Main-Code-2dct7ox.pdf Links to an external site.

2.	7 * 6 standard Connect Four Game using pygame library
https://www.askpython.com/python/examples/connect-four-game Links to an external site.

3.	John's Connect Four Playground (Strategy for Connect Four)
https://tromp.github.io/c4/c4.html Links to an external site.

4.	Wikipedia – Connect Four
https://en.wikipedia.org/wiki/Connect_Four

5.	Dominikus Herzberg’s detailed explanation of Connect Four Game
https://github.com/denkspuren/BitboardC4/blob/master/BitboardDesign.md

6.	Jonathan C.T. Kuo – AI Connect Four Using Minimax
https://medium.com/analytics-vidhya/artificial-intelligence-at-play-connect-four-minimax-algorithm-explained-3b5fc32e4a4f
