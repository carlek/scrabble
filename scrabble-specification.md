<a name="br1"></a> 

Scrabble Project Speciﬁcation

Your assignment is to build the logic for a simpliﬁed version of Scrabble. The logic is tested via included tests, which should not be changed.

Scrabble Rules

Scrabble is played on a square grid, 15 spaces to a side. Each turn, the player will place a set of letter tiles on the board to form a new word. The tiles may be placed on the board, and the

resulting words scored, based on the following rules:

If a play is not valid for any reason, the score for that play is zero, and the letters are not left on the board.

Plays that result in invalid words are invalid.

The validity of a word should be determined by the existence of the word in the words.txt ﬁle included with the sample projects.

If you’re not using one of the built-in dictionary helpers, then you may use your own, but you must use the words from words.txt . Matches should be case insensitive (the built-in

helpers convert every word to lowercase).

The ﬁrst move of the game must include a tile on the space 7,7 (the center space).

Subsequent moves must form words by sharing at least existing tile.

You may not replace existing tiles.

You may share existing tiles by placing new tiles at the beginning or end of an existing word.

If more than one tile is placed, they must all exist within a single horizontal or vertical line.

The score for a move is the sum of the point values for each the letters making up all of the newly formed words. Note that a play can form many words by being placed against several

existing tiles. For example, in this play

the player formed the word “NOT,” but also formed the words “NO” and “OW.” All these words must be valid for the moved to be valid, and the player gains points for the total value of

all the words.

Ignored Rules

If you’re familiar with Scrabble, you know that those aren’t all the rules. However, the rules above, and as implemented in the included tests, are all the rules that you need to implement for

this project.

Letter Values

The value of each tile is as follows, based on the tile’s letter:

A: 1

B: 3

C: 3

D: 2

E: 1

F: 4

G: 2

H: 4

I: 1

J: 8

K: 5

L: 1

M: 3

N: 1

O: 1

P: 3

Q: 10

R: 1

S: 1

T: 1

U: 1

V: 4

W: 4

X: 8

Y: 4

Z: 10

Game API

Your API must conform to the following rough rules; changes for the sake of language conventions (e.g. functional languages might not have classes/instances, capitalization may be different,

etc.) are ﬁne.

You must be able to instantiate multiple separate games (e.g. no globals, etc.)

There must be a method or function playTiles that accepts an array/list of dictionaries/hashes

Each hash contains a letter , row , and col key indicating the tile’s letter value and position on the board. row and col should be 0 through 14.

The return value of playTiles should be a dictionary/hash with the keys valid and score , indicating whether or not the move was valid, and how many points it scored. Invalid

moves are worth zero points.

There must be a way to access the current running score via a function/method/property named score .

