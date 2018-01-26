#!/usr/bin/env python
# -*- coding: utf-8 -*-
import praw, config
import requests, os
import re


#
# def bot_login():
#     r = praw.Reddit(username = config.username,
#                 password = config.password,
#                 client_id = config.client_id,
#                 client_secret = config.client_secret,
#                 user_agent = "Text chess")
#     print("Logged in")
#     return r
#
def run_bot(r, comments_replied_to):
    print("Getting the 25 newest comments")
    for comment in r.subreddit("test").comments(limit=25):
        if "Chess challenge" in comment.body and comment.id not in comments_replied_to:
            print("\"Chess challenge\" found in comment " + comment.id)
            comment.reply(format(default))
            print("Replied to comment " + comment.id)

            # Add to comments_replied_to
            comments_replied_to.append(comment.id)
            with open("comments_replied_to.txt", "a") as f:
                f.write(comment.id + "\n")


def move(comment, comments_replied_to):
    for reply in comments.replies:
        if not "Move" in comment.body:
            comment.reply("Include \'move\' in your reply")
        if reply.id not in comments_replied_to:
            # Reply should be in the form of "Move [piece] from [start] to [destination]"
            reply = reply.split()
            piece = reply[1]
            start = reply[3]
            destination = reply[5]
            print("Trying to move ", piece, " from ", start, " to ", destination)
            comment_reply = ""
            comment.reply(comment_reply)
            print("Replied to comment " + comment.id)

        # Add to comments_replied_to
        comments_replied_to.append(comment.id)
        with open("comments_replied_to.txt", "a") as f:
            f.write(comment.id + "\n")


# Start and destination are in the form [row, column]
def isValid(board, piece, start, destination):
    # Is the piece being moved white?
    white = True if piece[0] == "w" else False
    piece = piece[1:]

    # Friendly piece on destination square
    block = (board[destination[0]][destination[1]] == "w" and white) or \
            (board[destination[0]][destination[1]] == "b" and not white)
    if board[destination[0]][destination[1]] != " " and block:
        print("One of your pieces is at your destination square")
        return False

    # Going off the board
    if destination[0] < 0 or destination[0] > 7 or destination[1] < 0 or destination[1] > 7:
        print("Invalid destination")
        return False

    # Piece attempted to move is not at start
    if board[start[0]][start[1]] != piece:
        print("There is no ", piece, " there")
        return False

    # destination = start
    if start[0] == destination[0] and start[1] == destination[1]:
        print("Please move your ", piece)
        return False

    if piece == rook:
        if start[0] != destination[0] and start[1] != destination[1]:
            print("Please move horizontally or vertically")
            return False
        if start[0] == destination[0]:
            if not all(p == " " for p in board[start[0]][start[1] + 1: destination[1]]):
                print("There is something in the row blocking your rook's movement")
                return False
        if start[1] == destination[1]:
            if not all(p == " " for p in zip * (board)[start[0]][start[1] + 1: destination[1]]):
                print("There is something in the column blocking your rook's movement")
                return False

    if piece == knight:
        possible = [
            [1, 2],
            [2, 1],
        ]
        if [abs(destination[0] - start[0]), abs(destination[1] - start[1])] in possible:
            return True
        else:
            print("Invalid knight movement")
            return False

    if piece == bishop:
        if abs(start[0] - destination[0]) != abs(start[1] - destination[1]):
            print("You must move your bishop diagonally")
            return False
        vertical = 1 if destination[0] > start[0] else -1
        horizontal = 1 if destination[1] > start[1] else -1
        row = start[0] + vertical
        column = start[1] + horizontal
        while row is not destination[0] and column is not destination[1]:
            if board[row][column] != " ":
                print("A ", board[row][column], " is blocking your bishop's move")
                return False
            row += vertical
            column += horizontal
        return True

    if piece == queen:
        if isValid(board, bishop, start, destination) or isValid(board, rook, start, destination):
            print("You must move your queen either diagonally, vertically, or horizontally")
            return False
        else:
            return True

    if piece == pawn:
        # Attempting to move one or two steps forward]
        if destination[1] == start[1]:
            if (destination[0] == start[0] - 1 and white) or (destination[0] == start[0] + 1 and not white):
                return True
            # Pawns can move an extra step if still at starting position
            jump = (destination[0] == start[0] - 2 and white) or (destination[0] == start[0] + 2 and not white)
            if jump and board[(destination[0] + start[0]) / 2][start[1]] == " " and \
                    board[destination[0]][destination[1]] == " ":
                return True

        # Eating opponent piece diagonally
        if abs(destination[1] - start[1]) == 1:
            diagonally = (white and destination[0] == start[0] - 1) or (not white and destination[0] == start[0] + 1)
            opposing = (board[destination[0]][destination[1]][0] == "b" and white) or \
                       (board[destination[0]][destination[1]][0] == "w" and not white)
            return diagonally and opposing

        return False

    if piece == king:
        return abs(start[0] - destination[0]) == 1 and abs(start[1] - destination[1] == 1)


# Converts arrays of pieces to Reddit markdown
def format(board):
    blackIcons = {
        "rook": "♖",
        "knight": "♘",
        "bishop": "♗",
        "queen": "♕",
        "king": "♔",
        "pawn": "♙"
    }
    whiteIcons = {
        "rook": "♜",
        "knight": "♞",
        "bishop": "♝",
        "queen": "♛",
        "king": "♚",
        "pawn": "♟"
    }
    reply = "|A|B|C|D|E|F|G|H|\n"
    reply += ":-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|\n"
    for line in range(0, len(board)):
        reply += str(line + 1) + "|"
        for piece in board[line]:
            if piece[0] == "w":
                reply += whiteIcons[piece[1:]]
            elif piece[0] == "b":
                reply += blackIcons[piece[1:]]
            else:
                reply += " "
            reply += "|"
        reply += "\n"
    return reply


def get_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
    else:
        with open("comments_replied_to.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
    return comments_replied_to


newGame = [["brook", "bknight", "bbishop", "bqueen", "bking", "bbishop", "bknight", "brook"],
           ["bpawn"] * 8,
           [" "] * 8,
           [" "] * 8,
           [" "] * 8,
           [" "] * 8,
           ["wpawn"] * 8,
           ["wrook", "wknight", "wbishop", "wqueen", "wking", "wbishop", "wknight", "wrook"]
           ]

whiteTurn = True  # white is True if it's white's turn else False
print(format(newGame))

# r = bot_login()
# comments_replied_to = get_saved_comments()
# run_bot(r, comments_replied_to)
