import pygame, sys
from pygame.locals import QUIT
import numpy as np
import bot

pygame.init()

#Variables
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Tic-Tac-Toe')

#Game Variables (Defaulted to being in single player on medium difficulty with the X piece)
board = [["-" for i in range(3)], ["-" for i in range(3)], ["-" for i in range(3)]]
move_list = list()
turn = 1
mode = 1
player = 1
difficulty = 2
x_wins, o_wins = 0, 0

#Fonts
title_font = pygame.font.Font("Pixel_Font.ttf", 35)
large_font = pygame.font.Font("Pixel_Font.ttf", 50)
large_font_alt = pygame.font.Font("Pixel_Font.ttf", 51)
font = pygame.font.Font("Pixel_Font.ttf", 20)
font_alt = pygame.font.Font("Pixel_Font.ttf", 21)

#Text Images
restart_txt_img = font.render("Restart Game", True, "blue")
restart_txt_img_alt = font_alt.render("Restart Game", True, "blue")

back_txt_img = font.render("<< Back", True, "blue")
back_txt_img_alt = font_alt.render("<< Back", True, "blue")

options_txt_img = font.render("Options", True, "blue")
options_txt_img_alt = font_alt.render("Options", True, "blue")

title_txt_img = title_font.render("Tic-Tac-Toe", True, "white")

play_txt_img = large_font.render("Play", True, "blue")
play_txt_img_alt = large_font_alt.render("Play", True, "blue")

options_title_txt_img = title_font.render("Options", True, "white")

player_one_txt_img = title_font.render("1P", True, "white")
player_two_txt_img = title_font.render("2P", True, "white")

x_option_txt_img = title_font.render("X", True, "white")
o_option_txt_img = title_font.render("O", True, "white")

easy_difficulty_txt_img = font.render("Easy", True, "white")
medium_difficulty_txt_img = font.render("Medium", True, "white")
hard_difficulty_txt_img = font.render("Hard", True, "white")

x_text_img = font.render("X: ", True, "white")
o_text_img = font.render("O: ", True, "white")

#Draws the lines of the board as well as the pieces that have been placed
def draw_board() -> None:
  #Draws Board
  pygame.draw.line(window, "black", (100, 200), (400, 200), 8)
  pygame.draw.line(window, "black", (100, 300), (400, 300), 8)
  pygame.draw.line(window, "black", (200, 100), (200, 400), 8)
  pygame.draw.line(window, "black", (300, 100), (300, 400), 8)

  #Creates Win Display
  window.blit(x_text_img, [215, 25])
  window.blit(font.render(str(x_wins), True, "white"), [265, 25])
  window.blit(o_text_img, [215, 60])
  window.blit(font.render(str(o_wins), True, "white"), [265, 60])

  
  for i in range(3):
    for k in range(3):
      if board[i][k] != "-":
        draw_piece(i, k, board[i][k])

#Creates a button with a border, fill, and text with default boarder being black and default fill being sky blue
def draw_button(txt, coords: list, border: str = "black", fill: str = "sky blue") -> None:
  pygame.draw.rect(window, border, coords)
  pygame.draw.rect(window, fill, (coords[0] + 5, coords[1] + 5, coords[2] - 10, coords[3] - 10))
  window.blit(txt, (coords[0] + 7, coords[1] + (coords[3] / 2) - coords[3] / 5))

#Returns a list that represents the quadrant of the mouse click (row, column)
def determine_quadrant() -> list:
  mouse_position_x = pygame.mouse.get_pos()[0]
  mouse_position_y = pygame.mouse.get_pos()[1]

  if mouse_position_x < 100 or mouse_position_x > 400:
    column = None
  elif mouse_position_x < 200:
    column = 0
  elif mouse_position_x < 300:
    column = 1
  elif mouse_position_x < 400:
    column = 2


  if mouse_position_y < 100 or mouse_position_y > 400:
    row = None
  elif mouse_position_y < 200:
    row = 0
  elif mouse_position_y < 300:
    row = 1
  elif mouse_position_y < 400:
    row = 2
  else:
    row = None
  return (row, column)

#Draws the piece onto the board and choses which piece to draw based on whose turn it is
def draw_piece(row: int, column: int, piece: str, color = "black") -> None:
  if piece == "x":
    top_left_corner = (column * 100 + 115, row * 100 + 115)
    top_right_corner = (column * 100 + 185, row * 100 + 115)
    bottom_left_corner = (column * 100 + 115, row * 100 + 185)
    bottom_right_corner = (column * 100 + 185, row * 100 + 185)
    
    pygame.draw.line(window, color, top_left_corner, bottom_right_corner, 10)
    pygame.draw.line(window, color, top_right_corner, bottom_left_corner, 10)
  elif piece == "o":
    pygame.draw.circle(window, "white" if color == "black" else color, (column * 100 + 150, row * 100 + 150), 40, 8)


#Indirectly makes the move by altering the board list so that the piece is drawn the next time draw_board() is called
def make_move(location: list) -> None:
  global turn
  row = location[0]
  column = location[1]
  piece = "x" if turn % 2 != 0 else "o"
  
  if board[row][column] == "-":
    board[row][column] = piece
    move_list.append([row, column])
    turn += 1

#Returns a list that represent the type of win (type, location, piece)
def check_win() -> list:
  #Checks Rows
  for i in range(3):
    row_np_arr = np.array(board[i])
    if all(row_np_arr == "x") or all(row_np_arr == "o"):
      return("row", i, board[i][0])
  #Checks Columns
  for i in range(3):
    col_np_arr = np.array((board[0][i], board[1][i], board[2][i]))
    if all(col_np_arr == "x") or all(col_np_arr == "o"):
      return("column", i, board[0][i])
  #Checks Diagonals
  if board[1][1] != "-":
    if board[0][0] == board[1][1] == board[2][2]:
      return("diagonal", 0, board[1][1])
    elif board[0][2] == board[1][1] == board[2][0]:
      return("diagonal", 2, board[1][1])


#Turns the winning three pieces blue
def show_win(win_type: str, location: int, piece: str) -> None:
  if win_type == "row":
    for i in range(3):
      draw_piece(location, i, piece, "blue")
  elif win_type == "column":
    for i in range(3):
      draw_piece(i, location, piece, "blue")
  elif win_type == "diagonal":
    draw_piece(0, location, piece, "blue")
    draw_piece(1, 1, piece, "blue")
    draw_piece(2, 2 - location, piece, "blue")

#Turns every piece gray in event of a tie
def show_tie():
  for i in range(3):
    for k in range(3):
      draw_piece(i, k, board[i][k], (66, 66, 66))

#Resets the game and all game variables
def reset() -> None:
  global turn
  global move_list
  
  for i in range(3):
    for k in range(3):
      board[i][k] = "-"
      turn = 1
  move_list = []

def hard_reset() -> None:
  global x_wins
  global o_wins

  reset()
  x_wins = 0
  o_wins = 0
      
#Main Menu which includes title and play button
def main_menu():
  while True:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()

      #Has play button been pressed, sends to game
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if mouse[0] > 145 and mouse[0] < 355 and mouse[1] > 250 and mouse[1] < 460:
          game_loop()

    window.fill("sky blue")
    window.blit(title_txt_img, (53, 100))
    if mouse[0] > 145 and mouse[0] < 355 and mouse[1] > 250 and mouse[1] < 460:
      draw_button(play_txt_img_alt, [140, 245, 220, 110])
    else:
      draw_button(play_txt_img, [145, 250, 210, 100], "black", "white")
    pygame.display.update()

#Menu that includes player mode, piece selection, and difficulty delection
def options_menu():
  global mode
  global player
  global difficulty
  
  while True:
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          if mouse[0] > 175 and mouse[0] < 327 and mouse[1] > 400 and mouse[1] < 450:
            game_loop()
          
          if mouse[0] > 130 and mouse[0] < 210 and mouse[1] > 125 and mouse[1] < 185:
            mode = 1
          elif mouse[0] > 270 and mouse[0] < 350 and mouse[1] > 80 and mouse[1] < 185:
            mode = 2
          elif mouse[0] > 140 and mouse[0] < 190 and mouse[1] > 225 and mouse[1] < 285:
            player = 1
          elif mouse[0] > 280 and mouse[0] < 330 and mouse[1] > 225 and mouse[1] < 285:
            player = 2
          elif mouse[0] > 25 and mouse[0] < 125 and mouse[1] > 325 and mouse[1] < 365:
            difficulty = 1
          elif mouse[0] > 180 and mouse[0] < 280 and mouse[1] > 325 and mouse[1] < 365:
            difficulty = 2
          elif mouse[0] > 375 and mouse[0] < 475 and mouse[1] > 325 and mouse[1] < 365:
            difficulty = 3
    
    window.fill("sky blue")
    window.blit(options_title_txt_img, (125, 50))
    if mode == 1:
      draw_button(player_one_txt_img, [130, 125, 80, 60])
      draw_button(player_two_txt_img, [270, 125, 80, 60], "sky blue", "sky blue")
      if player == 1:
        draw_button(x_option_txt_img, [140, 225, 50, 60])
        draw_button(o_option_txt_img, [280, 225, 50, 60], "sky blue", "sky blue")
      else:
        draw_button(x_option_txt_img, [140, 225, 50, 60], "sky blue", "sky blue")
        draw_button(o_option_txt_img, [280, 225, 50, 60])

      if difficulty == 1:
        draw_button(easy_difficulty_txt_img, [25, 325, 90, 40])
        draw_button(medium_difficulty_txt_img, [180, 325, 130, 40], "sky blue", "sky blue")
        draw_button(hard_difficulty_txt_img, [375, 325, 90, 40], "sky blue", "sky blue")
      elif difficulty == 2:
        draw_button(easy_difficulty_txt_img, [25, 325, 90, 40], "sky blue", "sky blue")
        draw_button(medium_difficulty_txt_img, [180, 325, 130, 40])
        draw_button(hard_difficulty_txt_img, [375, 325, 90, 40], "sky blue", "sky blue")
      else:
        draw_button(easy_difficulty_txt_img, [25, 325, 90, 40], "sky blue", "sky blue")
        draw_button(medium_difficulty_txt_img, [180, 325, 130, 40], "sky blue", "sky blue")
        draw_button(hard_difficulty_txt_img, [375, 325, 90, 40])
      
    elif mode == 2:
      draw_button(player_one_txt_img, [130, 125, 80, 60], "sky blue", "sky blue")
      draw_button(player_two_txt_img, [270, 125, 80, 60])
    if mouse[0] > 175 and mouse[0] < 327 and mouse[1] > 400 and mouse[1] < 450:
      draw_button(back_txt_img_alt, [170, 395, 162, 60])
    else:
      draw_button(back_txt_img, [175, 400, 152, 50], "black", "white")
    pygame.display.update()

#Game loop which has the board
def game_loop():
  new_game = True
  while True:
    global mode
    global difficulty
    global x_wins
    global o_wins
    win = check_win()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
          
        #Has there been a click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

          #Checks if there has been input on the board and makes a move based on which area it is in
          if win == None:
            location = determine_quadrant()
            temp = np.array(location)
            if all(temp != None):
              make_move(location)
            
          #Mouse position
          mouse = pygame.mouse.get_pos()

          #Has the rest button been pressed
          if mouse[0] > 125 and mouse[0] < 375 and mouse[1] > 420 and mouse[1] < 470:
            reset()
            new_game = True
            win = None
          #Has the back button been pressed
          elif mouse[0] > 25 and mouse[0] < 177 and mouse[1] > 25 and mouse[1] < 75:
            hard_reset()
            main_menu()
          #Has the options button been pressed
          elif mouse[0] > 323 and mouse[0] < 475 and mouse[1] > 25 and mouse[1] < 75:
            hard_reset()
            options_menu()

    if win != None and new_game == True:
      new_game = False
      if win[2] == "x":
        x_wins += 1
      elif win[2] == "o":
        o_wins += 1
    
    window.fill("Sky blue")
    draw_board()

    #Mouse position
    mouse = pygame.mouse.get_pos()

    #Is the mouse hovering over the reset button
    if mouse[0] > 125 and mouse[0] < 375 and mouse[1] > 420 and mouse[1] < 470:
      draw_button(restart_txt_img_alt, [120, 415, 260, 60])
    else:
      draw_button(restart_txt_img, [125, 420, 250, 50], "black", "white")

    #Is the mouse hovering over the back button
    if mouse[0] > 25 and mouse[0] < 177 and mouse[1] > 25 and mouse[1] < 75:
      draw_button(back_txt_img_alt, [20, 20, 162, 60])
    else:
      draw_button(back_txt_img, [25, 25, 152, 50], "black", "white")

    #Is the mouse hovering over the options button
    if mouse[0] > 323 and mouse[0] < 475 and mouse[1] > 25 and mouse[1] < 75:
      draw_button(options_txt_img_alt, [318, 20, 162, 60])
    else:
      draw_button(options_txt_img, [323, 25, 152, 50], "black", "white")

    
    win = check_win()
    if win != None:
      show_win(win[0], win[1], win[2])
    elif turn == 10:
      show_tie()
    pygame.display.update()
    

    if player == 1:
      ready = turn % 2 == 0
    else:
      ready = turn % 2 != 0

    
    #Makes bot move based on who goes first and difficulty
    if ready and win == None and mode == 1 and turn < 10:
      piece = "o" if player == 1 else "x"
      pygame.time.wait(250)
      if difficulty == 1:
        make_move(bot.get_lvl1_move(board, turn, move_list, piece))
      elif difficulty == 2:
        make_move(bot.get_lvl2_move(board, turn, move_list, piece))
      elif difficulty == 3:
        make_move(bot.get_lvl3_move(board, turn, move_list, piece))

main_menu()