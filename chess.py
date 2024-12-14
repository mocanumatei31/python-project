import pygame
import pieces

colours = dict()
colours['white'] = (255, 255, 255)
colours['blue'] = (150, 190, 210)


class GameInstance:
    def __init__(self, screen_width):
        """
        Initializes a Game Instance object

        Args:
            screen_width (int): The size of the screen (height is assumed equal to width due to square board)
        """
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_width
        self.square_size = screen_width / 8
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.board_state = [[None] * 9 for _ in range(9)]
        self.generate_initial_board()
        self.draw_chessboard()
        pygame.display.set_caption("Chess Game")

    def draw_square(self, x, y, size, color):
        """
        Draws a filled square
        :param x: coordinate on the X-Axis for the upper-left corner of the square
        :param y: coordinate on the Y-Axis for the upper-left corner of the square
        :param size: length of square
        :param color: filling color of square
        """
        pygame.draw.rect(self.screen, color, (x, y, size, size))

    def generate_initial_board(self):
        """
        Generates the board state according to initial configuration of a chess game
        """
        for row in range(9):
            for col in range(9):
                if 0 < row <= 2:
                    color = 'black'
                    image_path = 'b'
                elif row > 6:
                    color = 'white'
                    image_path = 'w'
                else:
                    color = None
                if row == 1 or row == 8:
                    if col == 1 or col == 8:
                        self.board_state[row][col] = pieces.Rook(color, f"assets/{image_path}r.png", (row, col))
                    elif col == 2 or col == 7:
                        self.board_state[row][col] = pieces.Knight(color, f"assets/{image_path}n.png", (row, col))
                    elif col == 3 or col == 6:
                        self.board_state[row][col] = pieces.Bishop(color, f"assets/{image_path}b.png", (row, col))
                    elif col == 4:
                        self.board_state[row][col] = pieces.Queen(color, f"assets/{image_path}q.png", (row, col))
                    else:
                        self.board_state[row][col] = pieces.King(color, f"assets/{image_path}k.png", (row, col))
                elif row == 2 or row == 7:
                    self.board_state[row][col] = pieces.Pawn(color, f"assets/{image_path}p.png", (row, col))

    def draw_chessboard(self):
        """
        Draws the chessboard in accordance with the current configuration of the board
        """
        self.screen.fill(colours['white'])
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 != 0:
                    self.draw_square(col * self.square_size, row * self.square_size, self.square_size, colours['blue'])
        for row in range(1, 9):
            for col in range(1, 9):
                piece = self.board_state[row][col]
                if piece is not None:
                    image = pygame.image.load(piece.image)
                    image = pygame.transform.scale(image, (120, 120))
                    self.screen.blit(image, ((col - 1) * self.square_size, (row - 1) * self.square_size))
        pygame.display.flip()

    def check_piece_click(self, x, y):
        """
        Checks if the clicked square corresponds to a piece or not
        :param x: coordinate on the X-Axis for the clicked point
        :param y: coordinate on the Y-Axis for the clicked point
        :return: Piece on clicked position if it exists, None otherwise
        """
        row = int(y // self.square_size)
        col = int(x // self.square_size)
        return self.board_state[row + 1][col + 1]

    def draw_possible_moves(self, possible_moves, color=(0, 0, 255, 128)):
        """
        Marks any possible moves a clicked piece may have on the chessboard
        :param possible_moves: array of possible moves for the piece
        :param color: color of the circles, defaults to light blue
        """
        circle_surface = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
        pygame.draw.circle(circle_surface, color, (self.square_size // 2, self.square_size // 2), self.square_size // 8)
        for y, x in possible_moves:
            x -= 1
            y -= 1
            self.screen.blit(circle_surface, (x * self.square_size, y * self.square_size))
        pygame.display.flip()

    def handle_click(self, coordinates, clicked_piece=None):
        """
        Handles the input on click
        :param coordinates: the coordinates of the point that was clicked
        :param clicked_piece: previous clicked piece, if it exists, otherwise it is None
        :return: the piece at the coordinates if it exists, otherwise None
        """
        mouse_x, mouse_y = coordinates
        print(clicked_piece)
        current_clicked_piece = self.check_piece_click(mouse_x, mouse_y)
        if current_clicked_piece:
            if (clicked_piece and clicked_piece.color == current_clicked_piece.color) or not clicked_piece:
                self.screen.fill((colours['white']))
                self.draw_chessboard()
        else:
            if clicked_piece:
                possible_moves = clicked_piece.get_possible_moves(self.board_state)
                row = int(mouse_y // self.square_size) + 1
                col = int(mouse_x // self.square_size) + 1
                print(row, col)
                print(possible_moves)
                for x, y in possible_moves:
                    if row == x and col == y:
                        px, py = clicked_piece.board_position
                        self.board_state[row][col] = clicked_piece
                        self.board_state[px][py] = None
                        clicked_piece.board_position = (row, col)
                        self.screen.fill((colours['white']))
                        self.draw_chessboard()
                        return None
        clicked_piece = self.check_piece_click(mouse_x, mouse_y)
        if clicked_piece:
            self.draw_possible_moves(clicked_piece.get_possible_moves(self.board_state))
        return clicked_piece

    def run_game(self):
        """
        Main Loop of the Game
        """
        running = True
        clicked_piece = None
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_piece = self.handle_click(pygame.mouse.get_pos(), clicked_piece)
        pygame.quit()


if __name__ == '__main__':
    game_instance = GameInstance(960)
    game_instance.run_game()
