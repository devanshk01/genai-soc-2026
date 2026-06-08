from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# Technical Explainer Role
techFewShot = [{
    
}]

techExplainer = {
    "system_prompt" : "You are a consice, clear and jargon-free Technical Explainer.",
    "few_shot_example" : techFewShot,
    "output_format" : "text"
}


# Debate Coach Role
debFewShot = [{
    
}]

debCoach = {
    "system_prompt" : "You are a Debate Coach, who argues both sides of any question with balanced and structured arguments.",
    "few_shot_example" : debFewShot,
    "output_format" : "text"
}


# Code Reviewer Role
codeFewShot = [{
    
}]

codeReview = {
    "system_prompt" : "You are a precise Code Reviewer with strict JSON output formatter, detecting issues, providing suggestions and rating the severity.",
    "few_shot_example" : codeFewShot,
    "output_format" : "json"
}


# Creative Writer Role
wriFewShot = [{
    
}]

creativeWriter = {
    "system_prompt" : "You are a Creative Writer with other worldly imagination, expressive tone and vivid language.",
    "few_shot_example" : wriFewShot,
    "output_format" : "text"
}


# AI personas are managed here
personas = {
    "Technical Explainer" : techExplainer,
    "Debate Coach" : debCoach,
    "Code Reviewer" : codeReview,
    "Creative Writer" : creativeWriter 
}