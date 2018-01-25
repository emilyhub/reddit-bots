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
# def run_bot(r, comments_replied_to):
#     print("Getting the 25 newest comments")
#     for comment in r.subreddit("test").comments(limit=25):
#         if "Chess challenge" in comment.body and comment.id not in comments_replied_to:
#             print("\"Chess challenge\" found in comment " + comment.id)
#             comment_reply = "|A|B|C|D|E|F|G|H|\n
#                             :-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|\n
#                             1|♖|♘|♗|♕|♔|♗|♘|♖|\n
#                             2|♙|♙|♙|♙|♙|♙|♙|♙|\n
#                             3|||||||||\n
#                             4|||||||||\n
#                             5|||||||||\n
#                             6|||||||||\n
#                             7|♟|♟|♟|♟|♟|♟|♟|♟|\n
#                             8|♜|♞|♝|♛|♚|♝|♞|♜​|\n"
#             comment.reply(comment_reply)
#             print("Replied to comment " + comment.id)
#         elif
#
#             comments_replied_to.append(comment.id)
#             with open("comments_replied_to.txt", "a") as f:
#                 f.write(comment.id + "\n")

# def move(comment, comments_replied_to):
#     for reply in comments.replies:
#         if not "Move" in comment.body:
#             comment.reply("Include \'move\' in your reply")
#         if reply.id not in comments_replied_to:
#             # Reply should be in the form of "Move [piece] from [start] to [destination]"
#             reply = reply.split()
#             piece = reply[1]
#             start = reply[3]
#             destination = reply[5]
#             print("Trying to move ", piece, " from ", start, " to ", destination)
#             comment_reply = "
#                             1|♖|♘|♗|♕|♔|♗|♘|♖|\n
#                             2|♙|♙|♙|♙|♙|♙|♙|♙|\n
#                             3|||||||||\n
#                             4|||||||||\n
#                             5|||||||||\n
#                             6|||||||||\n
#                             7|♟|♟|♟|♟|♟|♟|♟|♟|\n
#                             8|♜|♞|♝|♛|♚|♝|♞|♜​|\n"
#             comment.reply(comment_reply)
#             print("Replied to comment " + comment.id)
#         comments_replied_to.append(comment.id)
#         with open("comments_replied_to.txt", "a") as f:
#             f.write(comment.id + "\n")

# Converts arrays of pieces to Reddit markdown
def printBoard(board):
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

array = [["brook", "bknight", "bbishop", "bqueen", "bking", "bbishop", "bknight", "brook"],
         ["bpawn"]*8,
         [" "]*8,
         [" "]*8,
         [" "]*8,
         [" "]*8,
         ["wpawn"]*8,
         ["wrook", "wknight", "wbishop", "wqueen", "wking", "wbishop", "wknight", "wrook"]
         ]
print(printBoard(array))


# r = bot_login()
# comments_replied_to = get_saved_comments()
# run_bot(r, comments_replied_to)