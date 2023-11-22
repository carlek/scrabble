from dictionary import dictionary
from collections import OrderedDict

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
           'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
scores = [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1,
          3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10]
scores_by_letter = dict(zip(letters, scores))  # { 'a': 1, 'b': 3, ... }


class ScrabbleGame(object):
    def __init__(self):
        self.score = 0
        self.first_move = True
        # initialize board
        # board is 15x15 ordered dict of letters indexed by key of(row,col)
        # [((0, 1), ''), ((0, 1), ''), ..., ((14, 13), ''), ((14, 14), '')])
        self.board = OrderedDict()
        for i in xrange(15):
            for j in xrange(15):
                self.board[(i, j)] = ''
        self.current_move_dimension = ''  # if vertical:'col' else 'row' (1 character is 'row')
        self.current_move_start_position = None
        # played words is list of words with starting position and dimension
        self.played_words = []

    def move_valid(self, tiles):
        # check if all squares are available on a 15x15 zeroindexed board
        for t in tiles:
            if not 0 < t['row'] < 15:
                return False
            if not 0 < t['col'] < 15:
                return False
            if self.board[(t['row'], t['col'])] != '':
                return False

        # 7,7 must be in first move
        if self.first_move:
            if (7, 7) not in [(t['row'], t['col']) for t in tiles]:
                return False

        # checks for adjacent tile(s) if not first move
        good = True
        if not self.first_move:
            good = False
            for t in tiles:
                pos = (t['row'], t['col'])
                for i in range(pos[0]-1, pos[1]+2):
                    for j in range(pos[0]-1, pos[1]+2):
                        if (i,j) != pos and self.board[(i,j)] != '':
                            good = True
        if not good:
            return False

        # checks if tiles are all in one line
        min_row = min(t['row'] for t in tiles)
        min_col = min(t['col'] for t in tiles)
        self.current_move_start_position = (min_row, min_col)
        # the word is either horizonatal or vertical
        if max(t['row'] for t in tiles) == min_row:
            self.current_move_direction = 'row'
            cols = [t['col'] for t in tiles]
            # check if played tiles make up line
            cols_not_played = list(set(range(min(cols), max(cols)+1)) - set(cols))
            if not cols_not_played: # all in a line
                return True
            for c in cols_not_played:  # check if board tiles complete word
                if self.board[(min_row, c)] != '':
                    return True
        if max(t['col'] for t in tiles) == min_col:
            self.current_move_direction = 'col'
            rows = [t['row'] for t in tiles]
            # check if played tiles make up line
            rows_not_played = list(set(range(min(rows), max(rows)+1)) - set(rows))
            if not rows_not_played: # all in a line
                return True
            for r in rows_not_played:  # check if board tiles complete
                if self.board[(r, min_col)] != '':
                    return True

        # all other cases are invalid
        return False

    def add_tiles_to_board(self, tiles):
        for t in tiles:
            self.board[(t['row'], t['col'])] = t['letter']

    def all_words_in_move(self, tiles):
        # get all words in move
        # words is a list of tuples: (word, rol, col, 'row'|'col')
        # where 'row'|'col' indicates horizontal word, or vertical word
        words = []
        # set the starting position and determine horiz or vertical
        (i,j) = self.current_move_start_position
        if self.current_move_direction == 'row':  # horizontal placement
            # get horizontal word and all subsequent vertical words
            word_tuple = self.get_horizontal_word((i,j))
            if word_tuple:
                word, row, col = word_tuple
                words.append((word, row, col, 'row'))
            c = j
            while self.board[(i,c)] != '':
                word_tuple = self.get_vertical_word((i,c))
                if word_tuple:
                    word, row, col = word_tuple
                    words.append((word, row, col, 'col'))
                c += 1
        if self.current_move_direction == 'col':  # vertical placement
            # get vertical word and all subsequent horizontal words
            word_tuple = self.get_vertical_word((i,j))
            if word_tuple:
                word, row, col = word_tuple
                words.append((word, row, col, 'col'))
            r = i
            while self.board[(r,j)] != '':
                word_tuple = self.get_horizontal_word((r,j))
                if word_tuple:
                    word, row, col = word_tuple
                    words.append((word, row, col, 'row'))
                r += 1
        return words

    def get_vertical_word(self, pos):
        # get vertical word at position
        # return word and starting position tuple (word, row, col)
        (r,c) = pos
        # single letter
        if 0 < r < 15 and self.board[(r-1, c)] == '' and self.board[(r+1, c)] == '':
            return None
        word = ''
        i = r
        while i > 0 and self.board[(i,c)] != '':
            word = self.board[(i,c)] + word
            i -= 1
        start_row = i+1
        i = r+1
        while i < 15 and self.board[(i,c)] != '':
            word = word + self.board[(i,c)]
            i += 1
        return word, start_row, c

    def get_horizontal_word(self, pos):
        # get horizontal word at position
        # return word and starting position tuple (word, row, col)
        (r, c) = pos
        # single letter
        if 0 < c < 15 and self.board[(r, c-1)] == '' and self.board[(r, c+1)] == '':
            return None
        word = ''
        j = c
        while j > 0 and self.board[(r, j)] != '':
            word = self.board[(r,j)] + word
            j -= 1
        start_col = j+1
        j = c + 1
        while j < 15 and self.board[(r, j)] != '':
            word = word + self.board[(r, j)]
            j += 1
        return word, r, start_col

    def are_words_in_dictionary(self, words):
        for (w, r, c, d) in words:
            if not dictionary.contains(w):
                return False
        return True

    def remove_tiles_from_board(self, tiles):
        for t in tiles:
            self.board[(t['row'], t['col'])] = ''

    # tiles - List<{ 'letter': String, 'row': Int, 'col': Int }>
    #
    #  an array of objects; each object contains a `letter` (the letter
    #  of the tile to play), a `row` (the row to play the tile in) and
    #  a `col` (the column to play the tile in).
    #
    # score - { 'valid': Boolean, 'score': Int }
    #
    #  `valid` is whether or not the set of tiles represent a valid game
    #  move. If so, `score` is the value of the play to be added to the
    #  score, and if not, `score` is 0.
    #
    def play_tiles(self, tiles):
        # initialize default
        play = {'valid': False, 'score': 0}

        # invalid tile placement
        if not self.move_valid(tiles):
            return play

        # add tiles to board
        # if not all words formed are in dictionary remove them and return
        self.add_tiles_to_board(tiles)
        words = self.all_words_in_move(tiles)
        if not self.are_words_in_dictionary(words):
            self.remove_tiles_from_board(tiles)
            return play

        # words are valid
        play['valid'] = True

        # score all words not already played
        for word_tuple in words:
            if word_tuple not in self.played_words:
                self.played_words.append(word_tuple)
                word, row, col, dir = word_tuple
                for c in word:
                    play['score'] += scores_by_letter[c]

        # total score
        self.score += play['score']

        if self.first_move:
            self.first_move = False
        return play
