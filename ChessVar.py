# GitHub username: schectma
# Date: 06/09/2024
# Description: Plays a game of atomic chess in which captures result
#               in the destruction of all adjacent pieces (while otherwise
#               functioning identically to standard chess). Comprised of two
#               classes: one to embody the game and its rules; one to embody
#               its pieces and their variants.

class ChessVar:
    """
    Represents a game of chess, its rules, and its top-level properties.
    """
    def __init__(self):
        """
        Initializes all starting values for the game.
        """
        self._game_state = "UNFINISHED"
        self._grid_size = 8
        # self._grid = [[0] * self._grid_size for col in range(self._grid_size)]
        self._col_ref = {}
        self._board = {}
        self._start_chr = 97
        self._total_turns = 0
        self._turn = True
        self._active_piece = None
        self._pawns = {}
        self._blast_radius = (abs(1), abs(1))
        self._victims = []
        # Generate board and pieces upon init
        self.make_board()
        self.generate_pieces()

    def set_active_piece(self, piece):
        """
        Sets the currently-picked piece.
        :param piece: object instance.
        :return: N/A
        """
        self._active_piece = piece

    # def test_cell(self, cell):
    #     if cell[0] in self._col_ref and int(cell[1:]) <= 8:
    #         x = self._col_ref[cell[0]]
    #         y = int(cell[1]) - 1
    #         print(x, y)
    #     else:
    #         print("cell out of range")

    def turn_toggle(self):
        """
        Changes the current turn.
        :return: N/A
        """
        if self._turn is False:
            self._turn = True
            return
        if self._turn is True:
            self._turn = False
            return

    def get_turn(self):
        """
        Gets the current turn.
        :return: bool
        """
        return self._turn

    def get_board(self):
        """
        Gets the game board.
        :return: dict
        """
        return self._board

    def make_board(self):
        """
        Generates board (grid) with spaces (cells).
        Each cell has two properties: its xy coordinate and its occupant piece.
        :return: N/A
        """
        letter = self._start_chr
        number = self._grid_size
        for row in range(self._grid_size):
            for col in range(self._grid_size):
                # Each cell/key will contain a symbol and coordinates.
                self._board[chr(letter + col) + str(number - row)] = {
                    "xy": (col, number - row - 1),
                    "piece": None
                }

    def get_space_xy(self, space):
        """
        Gets a board space's xy coordinates.
        :param space:
        :return: tuple
        """
        return self._board[space]["xy"]

    def print_board(self):
        """
        Prints board to console.
        :return: N/A
        """

        letter = self._start_chr
        number = self._grid_size

        print("\n")

        # Column letters
        print("   ", end="")
        for col in range(97, 97 + self._grid_size):
            print(chr(col), " ", end="")
        print("\r")

        for row in range(self._grid_size):
            # Row number
            print(self._grid_size - row, end="  ")

            # Cells/values
            for col in range(self._grid_size):
                # print(self._board[chr(letter + col) + str(number - row)]["sym"], end="  ")
                if self._board[chr(letter + col) + str(number - row)]["piece"]:
                    print(self._board[chr(letter + col) + str(number - row)]["piece"].get_symbol(), end="  ")
                else:
                    print("\u25A1", end="  ")

            # Row number
            print(self._grid_size - row, end="  ")
            print("\r")

        # Column letters
        print("   ", end="")
        for col in range(97, 97 + self._grid_size):
            print(chr(col), " ", end="")
        print("\r")

    def get_game_state(self):
        """
        Returns victory status of game.
        :return: string
        """
        return self._game_state

    def set_game_state(self):
        """
        Changes state of game from default.
        :return: N/A
        """
        if self._active_piece.get_color() == 0:
            self._game_state = "BLACK_WON"
        if self._active_piece.get_color() == 1:
            self._game_state = "WHITE_WON"

    def get_occupant(self, coord):
        """
        Gets the piece occupying a specified square.
        :param coord: string
        :return: object
        """
        return self._board[coord]["piece"]

    def generate_pieces(self):
        """
        Generates instances of pieces at board locations specified.
        :return: N/A
        """
        # Pawns:
        color = "white"
        for unit in range(8):
            current_space = chr(self._start_chr + unit) + str(2)
            current_piece = self._pawns[color + "Pawn" + str(unit)] = Pawn(current_space, 1)
            self.place_piece(current_piece, current_space)

        color = "black"
        for unit in range(8):
            current_space = chr(self._start_chr + unit) + str(7)
            current_piece = self._pawns[color + "Pawn" + str(unit)] = Pawn(current_space, 0)
            self.place_piece(current_piece, current_space)

        whiteBishop1 = Bishop("c1", 1)
        self.place_piece(whiteBishop1, "c1")
        whiteBishop2 = Bishop("f1", 1)
        self.place_piece(whiteBishop2, "f1")
        blackBishop1 = Bishop("c8", 0)
        self.place_piece(blackBishop1, "c8")
        blackBishop2 = Bishop("f8", 0)
        self.place_piece(blackBishop2, "f8")

        # Knights
        whiteKnight1 = Knight("b1", 1)
        self.place_piece(whiteKnight1, "b1")
        whiteKnight2 = Knight("g1", 1)
        self.place_piece(whiteKnight2, "g1")
        blackKnight1 = Knight("b8", 0)
        self.place_piece(blackKnight1, "b8")
        blackKnight2 = Knight("g8", 0)
        self.place_piece(blackKnight2, "g8")

        # Rooks
        whiteRook1 = Rook("a1", 1)
        self.place_piece(whiteRook1, "a1")
        whiteRook2 = Rook("h1", 1)
        self.place_piece(whiteRook2, "h1")
        blackRook1 = Rook("a8", 0)
        self.place_piece(blackRook1, "a8")
        blackRook2 = Rook("h8", 0)
        self.place_piece(blackRook2, "h8")

        # Queens
        whiteQueen = Queen("d1", 1)
        self.place_piece(whiteQueen, "d1")
        blackQueen = Queen("d8", 0)
        self.place_piece(blackQueen, "d8")

        # Kings
        whiteKing = King("e1", 1)
        self.place_piece(whiteKing, "e1")
        blackKing = King("e8", 0)
        self.place_piece(blackKing, "e8")

    def make_move(self, origin, destination):
        """
        Moves a piece from specified origin to specified destination.
        :param origin: string
        :param destination: string
        :return: bool
        """
        # Confirm game state
        if self._game_state == "WHITE_WON" or self._game_state == "BLACK_WON":
            # Game is already over.
            return False

        # Confirm origin contains piece.
        if not self._board[origin]["piece"]:
            return False

        # Set active piece to occupant of origin.
        self.set_active_piece(self.get_board()[origin]["piece"])

        if self._active_piece.get_turn_affinity() != self._turn:
            print("wrong player")
            return False

        # Verify destination in range of origin piece
        if not self.verify_range(destination):
            print("destination out of range")
            return False

        if self.check_path(origin, destination) is False:
            print("friendly piece in path")
            return False

        # Check for piece in destination.
        target = self.get_occupant(destination)
        if target:

            # Prevent king from making capture.
            if self._active_piece.get_symbol().lower() == "k":
                return False

            # Confirm if target is friendly.
            if target.get_color() == self._active_piece.get_color():
                return False

            # Confirm if target piece is a king (can assume opposition)
            if target.get_symbol().lower() == "k":
                self.set_game_state()

            self.remove_piece(target, destination)
            self.remove_piece(self._active_piece, origin)
            self.place_piece(self._active_piece, destination)
            self.victimize(destination)
            self.detonate()
            self.remove_piece(self._active_piece, destination)

        else:
            self.remove_piece(self._active_piece, origin)
            self.place_piece(self._active_piece, destination)

            self._active_piece.increment_move_count()

        self.turn_toggle()

        return True

    def check_cell(self, tup, color):
        """
        Verifies occupant of specified cell has specific color.
        :param tup: tuple
        :param color: int
        :return: bool - True if cell is empty or contains enemy piece, False if contains friendly piece
        """
        for cell in self._board:
            if self._board[cell]["xy"] == tup:
                occupant = self._board[cell]["piece"]
                # If cell is empty, it's valid (no friendly piece blocking)
                if occupant is None:
                    return True
                # If occupant is same color -> blocked by friendly
                if occupant.get_color() == color:
                    return False
                # Occupant is enemy -> not blocked (capture eligibility handled elsewhere)
                return True
        # If cell coordinate not found, treat as blocked/invalid
        return False

    def check_path(self, origin, destination):
        """
        Checks all cells for friendly pieces in path from origin to destination.
        :param origin: string
        :param destination: string
        :return: bool
        """
        origin_xy = self._board[self._active_piece.get_pos()]["xy"]
        dest_xy = self._board[destination]["xy"]
        x_delta, y_delta = self.get_trajectory(destination)
        active_color = self._active_piece.get_color()
        active_symbol = self._active_piece.get_symbol().lower()

        current_cell = [origin_xy[0], origin_xy[1]]
        final_cell = [dest_xy[0], dest_xy[1]]

        # Pawn -- if diagonal does NOT contain opposition piece, return false
        if active_symbol == "p":
            # check for diagonal move
            if abs(x_delta) == abs(y_delta):
                current_cell = [current_cell[0] + x_delta, current_cell[1] + y_delta]
                current_tuple = (current_cell[0], current_cell[1])
                # if diag. dest. is none or contains friendly
                for cell in self._board:
                    if self._board[cell]["xy"] == current_tuple:
                        if self._board[cell]["piece"] is None:
                            return False
                return self.check_cell(current_tuple, active_color)

        # Bishop
        if active_symbol == "b":
            while current_cell != final_cell:
                current_cell = [current_cell[0] + 1, current_cell[1] + 1]
                current_tuple = (current_cell[0], current_cell[1])
                return self.check_cell(current_tuple, active_color)

        # Rook
        if active_symbol == "r":
            while current_cell != final_cell:
                if x_delta == 0:
                    if y_delta < 0:
                        current_cell = [current_cell[0], current_cell[1] - 1]
                    if y_delta > 0:
                        current_cell = [current_cell[0], current_cell[1] + 1]
                if y_delta == 0:
                    if x_delta < 0:
                        current_cell = [current_cell[0] - 1, current_cell[1]]
                    if x_delta > 0:
                        current_cell = [current_cell[0] + 1, current_cell[1]]

                current_tuple = (current_cell[0], current_cell[1])
                return self.check_cell(current_tuple, active_color)

        # Queen
        if active_symbol == "q":
            while current_cell != final_cell:
                # N/S
                if x_delta == 0:
                    if y_delta < 0:
                        current_cell = [current_cell[0], current_cell[1] - 1]
                    if y_delta > 0:
                        current_cell = [current_cell[0], current_cell[1] + 1]

                # E/W
                if y_delta == 0:
                    if x_delta < 0:
                        current_cell = [current_cell[0] - 1, current_cell[1]]
                    if x_delta > 0:
                        current_cell = [current_cell[0] + 1, current_cell[1]]

                # Diagonal
                if abs(x_delta) == abs(y_delta):
                    # NE
                    if x_delta > 0 and y_delta > 0:
                        current_cell = [current_cell[0] + 1, current_cell[1] + 1]
                    # SE
                    if x_delta > 0 > y_delta:
                        current_cell = [current_cell[0] + 1, current_cell[1] - 1]
                    # SW
                    if x_delta < 0 and y_delta < 0:
                        current_cell = [current_cell[0] - 1, current_cell[1] - 1]
                    # NW
                    if x_delta < 0 < y_delta:
                        current_cell = [current_cell[0] - 1, current_cell[1] + 1]

                current_tuple = (current_cell[0], current_cell[1])
                return self.check_cell(current_tuple, active_color)

        # Knight bypasses all pieces in path. King's radius is 1,
        # so destination occupant check in parent method will detect friendly.
        # Pawns will be handled similarly.
        else:
            return True

    def get_trajectory(self, destination):
        """
        Calculates the slope/direction of a piece in motion.
        :param destination: string
        :return: ints
        """
        dest_xy = self._board[destination]["xy"]
        origin_xy = self._board[self._active_piece.get_pos()]["xy"]
        picked_range = self._active_piece.get_range()

        piece_type = self._active_piece.get_symbol()

        # for range_tuple in picked_range:
        x_1 = origin_xy[0]
        y_1 = origin_xy[1]
        x_2 = dest_xy[0]
        y_2 = dest_xy[1]
        x_delta = x_2 - x_1
        y_delta = y_2 - y_1

        return x_delta, y_delta

    def verify_range(self, destination):
        """
        Confirms destination cell is in range of active/origin piece.
        :param destination: string
        :return: bool
        """
        dest_xy = self._board[destination]["xy"]
        origin_xy = self._board[self._active_piece.get_pos()]["xy"]

        piece_type = self._active_piece.get_symbol()

        x_delta, y_delta = self.get_trajectory(destination)

        # Pawn
        if piece_type.lower() == "p":
            # Prevent lateral movement.
            if y_delta == 0:
                return False
            # Prevent forward capture.
            if x_delta == 0 and self._board[destination]["piece"] is not None:
                return False

            # Set threshold based on turn count.
            y_thresh = 1
            if self._active_piece.get_move_count() == 0:
                y_thresh = 2

            # Prevent backwards movement.
            if ((piece_type == "P") and (y_delta > 0)) or ((piece_type == "p") and (y_delta < 0)):
                return False

            if abs(y_delta) <= y_thresh:
                return True

            # Bishop
        if piece_type.lower() == "b":
            if abs(x_delta) == abs(y_delta):
                return True

        # Knight
        if piece_type.lower() == "n":
            if (abs(x_delta) == 1 and abs(y_delta) == 2) or (abs(x_delta) == 2 and abs(y_delta) == 1):
                return True

        # Rook
        if piece_type.lower() == "r":
            if (abs(x_delta) > 0 and y_delta == 0) or (x_delta == 0 and abs(y_delta) > 0):
                return True
        # Queen
        if piece_type.lower() == "q":
            if (abs(x_delta) > 0 and y_delta == 0) or (x_delta == 0 and abs(y_delta) > 0) or (
                    abs(x_delta) == abs(y_delta)):
                return True
        # King
        if piece_type.lower() == "k":
            if (abs(x_delta) == 1 and abs(y_delta == 1)) or (x_delta == 0 and abs(y_delta) == 1) or (
                    abs(x_delta) == 1 and y_delta == 0):
                return True

        return False

    def place_piece(self, piece, coord):
        """
        Occupies specified cell with piece.
        :param piece: object
        :param coord: string
        :return: N/A
        """
        # Transmit cell coordinates to piece object's position.
        piece.set_pos(coord)
        # Set cell "piece" subkey to piece object itself.
        self._board[coord]["piece"] = piece

    def remove_piece(self, piece, coord):
        """
        Removes piece from specified cell.
        :param piece: object
        :param coord: string
        :return: N/A
        """
        piece.set_pos(None)
        self._board[coord]["piece"] = None

    def victimize(self, destination):
        """
        Gathers coordinates of all cells in blast radius of capture.
        :param destination: string
        :return: N/A
        """
        center = self._board[destination]["xy"]
        for cell in self._board:
            cell_xy = self._board[cell]["xy"]
            x_delta = abs(cell_xy[0] - center[0])
            y_delta = abs(cell_xy[1] - center[1])
            if x_delta <= self._blast_radius[0] and y_delta <= self._blast_radius[1]:
                # Don't add cell if empty.
                if not self._board[cell]["piece"]:
                    continue
                else:
                    if cell != destination and self._board[cell]["piece"].get_symbol().lower() != "p":
                        self._victims.append(cell)

    def detonate(self):
        """
        Removes all pieces from the list of victims.
        :return: N/A
        """
        for cell in self._victims:
            if self._board[cell]["piece"] is not None and self._board[cell]["piece"].get_symbol().lower() == "k":
                self.set_game_state()
            self.remove_piece(self._board[cell]["piece"], cell)


class Piece:
    """
    Represents a generic chess piece, with properties common amongst all.
    """
    def __init__(self, pos, color):
        self._symbol = None
        self._pos = pos
        self._color = color
        self._range = None
        self._move_count = 0

        # Black
        if self._color == 0:
            self._turn_affinity = False
            # White
        if self._color == 1:
            self._turn_affinity = True

    def get_pos(self):
        """
        Gets position of piece.
        :return: tuple
        """
        return self._pos

    def set_pos(self, coord):
        """
        Sets position of piece.
        :param coord: string
        :return: N/A
        """
        self._pos = coord

    def get_color(self):
        """
        Gets color of piece.
        :return: int
        """
        return self._color

    def get_symbol(self):
        """
        Returns symbol of piece.
        :return: string
        """
        return self._symbol

    def increment_move_count(self):
        """
        Increases move count by 1.
        :return: N/A
        """
        self._move_count += 1

    def get_range(self):
        """
        Gets range of piece.
        :return: tuple
        """
        return self._range

    def get_turn_affinity(self):
        """
        Gets which turn on which the piece can move
        :return:
        """
        return self._turn_affinity

    def get_move_count(self):
        """
        Gets how many moves a piece has made.
        :return: int
        """
        return self._move_count


class Pawn(Piece):
    """
    Represents a pawn variant.
    """
    def __init__(self, pos, color):
        """
        Initializes values specific to the subclass.
        :param pos: string
        :param color: int
        """

        super().__init__(pos, color)

        self._start_pos = []

        if self._color == 0:  # black

            self._symbol = "P"
            if self._move_count == 0:
                self._range = [(1, -1), (-1, -1), (0, -2)]
            else:
                self._range = [(1, -1), (-1, -1)]

            for unit in range(8):
                self._start_pos.append(chr(97 + unit) + str(7))

        if self._color == 1:  # white
            self._symbol = "p"
            if self._move_count == 0:
                self._range = [(1, 1), (-1, 1), (0, 2)]
            else:
                self._range = [(1, 1), (-1, 1)]

            for unit in range(8):
                self._start_pos.append(chr(97 + unit) + str(2))


class Bishop(Piece):
    """
    Represents a bishop variant.
    """
    def __init__(self, pos, color):
        """
        Initializes values specific to the subclass.
        :param pos: string
        :param color: int
        """
        super().__init__(pos, color)
        if self._color == 0:
            self._symbol = "B"
            self._start_pos = ["c8", "f8"]
        if self._color == 1:
            self._symbol = "b"
            self._start_pos = ["c1", "f1"]

        self._range = [(8, 8)]


class Knight(Piece):
    """
    Represents a knight variant.
    """
    def __init__(self, pos, color):
        """
        Initializes values specific to the subclass.
        :param pos: string
        :param color: int
        """
        super().__init__(pos, color)
        if self._color == 0:
            self._symbol = "N"
            self._start_pos = ["b8", "g8"]
        if self._color == 1:
            self._symbol = "n"
            self._start_pos = ["b1", "g1"]
        self._range = [
            (1, 2), (-1, 2), (1, -2), (-1, -2),
            (2, 1), (-2, 1), (2, -1), (-2, -1)]

class Rook(Piece):
    """
    Represents a rook variant.
    """
    def __init__(self, pos, color):
        """
        Initializes values specific to the subclass.
        :param pos: string
        :param color: int
        """
        super().__init__(pos, color)
        if self._color == 0:
            self._symbol = "R"
            self._start_pos = ["a8", "h8"]
        if self._color == 1:
            self._symbol = "r"
            self._start_pos = ["a1", "b1"]
        self._range = [(8, 0), (-8, 0), (0, 8), (0, -8)]


class Queen(Piece):
    """
    Represents a queen variant.
    """
    def __init__(self, pos, color):
        """
        Initializes values specific to the subclass.
        :param pos: string
        :param color: int
        """
        super().__init__(pos, color)
        if self._color == 0:
            self._symbol = "Q"
            self._start_pos = ["e8"]
        if self._color == 1:
            self._symbol = "q"
            self._start_pos = ["e1"]
        self._range = [
            (8, 8), (8, -8), (-8, -8), (-8, 8),
            (8, 0), (-8, 0), (0, 8), (0, -8)
        ]


class King(Piece):
    """
    Represents a king variant.
    """
    def __init__(self, pos, color):
        """
        Initializes values specific to the subclass.
        :param pos: string
        :param color: int
        """
        super().__init__(pos, color)
        if self._color == 0:
            self._symbol = "K"
            self._start_pos = ["d8"]
        if self._color == 1:
            self._symbol = "k"
            self._start_pos = ["d1"]
        self._range = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
