from flask import Flask, render_template, request, jsonify
from model import comment_analysis
from scrapper import get_reviews, get_name
from yt_search import search_videos