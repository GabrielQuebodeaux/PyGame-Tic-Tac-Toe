import random
import numpy as np


#Returns a list of all open spaces on the board
def get_open_spaces(board: list) -> list:
  open_spaces = []
  for row in range(3):
    for col in range(3):
      if board[row][col] == "-":
        open_spaces.append((row, col))
  return open_spaces


#Returns a list of winning spaces
def get_win(board: list, piece: str) -> list:
  win = set()

  #Checks if there is a potential win in any row
  for row in range(3):
    row_array = np.array(board[row])
    piece_only_row_array = [piece for i in board[row] if i == piece]
    if any(row_array == "-") and not all(
        row_array == "-") and len(piece_only_row_array) == 2:
      if board[row][0] == board[row][2]:
        win.add((row, 1))
      elif board[row][0] == board[row][1]:
        win.add((row, 2))
      else:
        win.add((row, 0))
  #Checks if there is a potential win in any column
  for col in range(3):
    col_list = [board[0][col], board[1][col], board[2][col]]
    col_array = np.array([col_list[0], col_list[1], col_list[2]])
    piece_only_col_array = [piece for i in col_list if i == piece]
    if any(col_array == "-") and not all(
        col_array == "-") and len(piece_only_col_array) == 2:
      if col_list[1] == col_list[2]:
        win.add((0, col))
      elif col_list[0] == col_list[2]:
        win.add((1, col))
      else:
        win.add((2, col))

  #Checks if there is a potential win each diagonal
  descend_diag_list = [board[0][0], board[1][1], board[2][2]]
  descend_diag_array = np.array(descend_diag_list)
  piece_only_des_diag_array = [piece for i in descend_diag_list if i == piece]
  if any(descend_diag_array == "-") and not all(
      descend_diag_array == "-") and len(piece_only_des_diag_array) == 2:
    if descend_diag_list[1] == descend_diag_list[2]:
      win.add((0, 0))
    elif descend_diag_list[0] == descend_diag_list[2]:
      win.add((1, 1))
    else:
      win.add((2, 2))

  ascend_diag_list = [board[0][2], board[1][1], board[2][0]]
  ascend_diag_array = np.array(ascend_diag_list)
  piece_only_asc_diag_array = [piece for i in ascend_diag_list if i == piece]
  if any(ascend_diag_array == "-") and not all(
      ascend_diag_array == "-") and len(piece_only_asc_diag_array) == 2:
    if ascend_diag_list[1] == ascend_diag_list[2]:
      win.add((0, 2))
    elif ascend_diag_list[0] == ascend_diag_list[2]:
      win.add((1, 1))
    else:
      win.add((2, 0))

  return list(win)


#Creates a copy of the board to test win outcomes
def get_temp_board(board: list) -> list:
  temp_board = [[], [], []]
  for i in range(3):
    for k in range(3):
      temp_board[i].append(str(board[i][k]))
  return temp_board


#Returns a list of spaces that would cause a forced win
def get_force(board: list, piece: str, type: int = 2) -> list:
  force = set()
  for row in range(3):
    for col in range(3):
      temp_board = get_temp_board(board)
      if temp_board[row][col] == "-":
        temp_board[row][col] = piece
        if len(get_win(temp_board, piece)) >= type:
          force.add((row, col))
  force = list(force)
  if type == 1:
    force_loss = get_force(board, "x" if piece == "o" else "o")
    for i in force_loss:
      if i in force:
        force.remove(i)
  return force


#Returns the move of the easy difficulty bot
def get_lvl1_move(board: list, turn, move_list: list, piece: str) -> list:
  win = get_win(board, piece)
  loss = get_win(board, "x" if piece == "o" else "x")
  available = get_open_spaces(board)
  force_win = get_force(board, piece)
  force_loss = get_force(board, "x" if piece == "o" else "o")

  
  for i in win:
    if i in available:
      available.remove(i)
  for i in loss:
    if i in available:
      available.remove(i)
  for i in force_win:
    if i in available:
      available.remove(i)
  for i in force_loss:
    if i in available:
      available.remove(i)

  if len(available) == 0:
    if win == loss or len(loss) == 0:
      return random.choice(win)
    else:
      if len(win) == 0:
        if len(force_loss) != 0:
          for i in get_open_spaces(board):
            if not i in loss and not i in force_win:
              available.append(i)
        else:
          return random.choice(loss)
  return random.choice(available)

#Returns the move of the medium difficulty bot
def get_lvl2_move(board: list, turn, move_list: list, piece: str) -> list:
  if turn % 2 != 0:
    if turn == 1:
      return random.choice(get_open_spaces(board))
  else:
    if turn == 2:
      if move_list[0] == [1, 1]:
        return random.choice(([0, 1], [1, 0], [1, 2], [2, 1]))
      else:
        return random.choice(get_open_spaces(board))
  return get_lvl3_move(board, turn, move_list, piece)

#Returns the move of the hard difficulty bot
def get_lvl3_move(board: list, turn: int, move_list: list, piece: str) -> list:
  
  win = get_win(board, piece)
  loss = get_win(board, "x" if piece == "o" else "o")
  force_win = get_force(board, piece)
  force_loss = get_force(board, "x" if piece == "o" else "o")
  force_block = get_force(board, piece, 1)

  if len(win) != 0:
    return random.choice(win)
  elif len(loss) != 0:
    return random.choice(loss)
  elif len(force_win) != 0:
    return random.choice(force_win)
  elif len(force_loss) > 1:
    if len(force_block) == 0:
      return random.choice(force_loss)
    else:
      return random.choice(force_block)
  elif len(force_loss) == 1:
    return force_loss[0]

  if turn % 2 != 0:
    if turn == 1:
      return random.choice(get_open_spaces(board))
    else:
      if len(force_block) != 0:
        return random.choice(force_block)
      else:
        return random.choice(get_open_spaces(board))
  else:
    if turn == 2:
      if move_list[0] == [1, 1]:
        return random.choice(([0, 0], [0, 2], [2, 0], [2, 2]))
      else:
        return [1, 1]

    else:
      return random.choice(get_open_spaces(board))

  
  