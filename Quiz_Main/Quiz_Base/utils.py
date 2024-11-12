# utils.py
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re 
from django.utils.html import format_html

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

# Load environment variables from .env file
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")  # Retrieve the API key for Groq

# Set up the Groq model for generating MCQs
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-8b-8192")


import json
import re

def generate_mcqs_with_groq(pdf_text, output_filename='generated_mcqs.json'):
    # Split text into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(pdf_text)
    mcqs = []

    # Define the prompt template
    prompt_template = """
    You are an AI designed to create multiple-choice questions. Based on the provided text, generate an insightful MCQ with one correct answer and three distractors.

    Text:
    {chunk}

    Instructions:
    - Create exactly one multiple-choice question.
    - Include four answer options, clearly identifying the correct one.
    """

    for i, chunk in enumerate(chunks):
        # Format the prompt with the current text chunk
        prompt = prompt_template.format(chunk=chunk)
        
        # Generate the response
        response = llm.invoke(prompt)
        
        # Debug: Print the response to see if it's generating content
        print(f"Chunk {i+1} response:", response)

        # Ensure the response is valid and contains a valid MCQ format
        if response:
            # Extract the text content from the response (if it is an AIMessage or similar object)
            if hasattr(response, 'content'):
                response_text = response.content
            else:
                response_text = str(response)

            # Debug: Print the raw response text for troubleshooting
            print(f"Raw response text for chunk {i+1}: {response_text}")

            # Clean up the response and extract the MCQ text using regex
            match = re.search(r'(?:Question[:\s]+)(.*?)(?:\n.*?[A-D]\))', response_text, re.DOTALL)
            if match:
                mcq = match.group(1).strip()
                mcqs.append(mcq)
            else:
                mcqs.append(f"Unexpected MCQ format in chunk {i+1}: {response_text}")
        else:
            mcqs.append(f"No valid MCQ generated for chunk {i+1}. Response was empty.")

    # Save the MCQs to a JSON file
    with open(output_filename, 'w') as json_file:
        json.dump(mcqs, json_file, indent=4)

    print(f"MCQs saved to {output_filename}")
    return mcqs

    
import re

def parse_mcqs(mcq_text):
    parsed_mcqs = []
    for chunk in mcq_text:
        try:
            # Extract the question
            question_match = re.search(r"(?:Question \d+:|Here(?:'s| is) .*?:)\s*(.*?)(?=\n[A-D]\))", chunk, re.DOTALL | re.IGNORECASE)
            
            # Extract options
            options_match = re.findall(r"([A-D])\)(.*?)(?=(?:\n[A-D]\)|\nCorrect answer:|\Z))", chunk, re.DOTALL)
            
            # Extract correct answer
            correct_answer_match = re.search(r"Correct answer:\s*([A-D])", chunk)

            if question_match and options_match and correct_answer_match:
                question = question_match.group(1).strip()
                options = {opt[0]: opt[1].strip() for opt in options_match}
                correct_answer = correct_answer_match.group(1)

                parsed_mcqs.append({
                    'question': question,
                    'options': options,
                    'correct_answer': correct_answer
                })
            else:
                print(f"Failed to parse MCQ: {chunk}")

        except Exception as e:
            print(f"Error parsing chunk: {chunk}, error: {e}")

    return parsed_mcqs

def generate_html_for_quiz(mcq_list):
    html_output = ''
    for idx, mcq in enumerate(mcq_list):
        # If the MCQ has an unexpected format (like missing options), handle it
        if 'A)' not in mcq:
            html_output += format_html('<p>{}</p>', mcq)  # Just display as text
        else:
            # Extract the question and options
            question_part = mcq.split("\n")[0].strip()
            options_part = mcq.split("\n")[1:]
            options = [opt.split(")")[1].strip() for opt in options_part if ")" in opt]
            
            # Format the question with radio buttons for options
            html_output += format_html('<div class="question"><p><strong>{}</strong></p>', question_part)
            for i, option in enumerate(options):
                html_output += format_html('<label><input type="radio" name="q{0}" value="option{1}">{2}</label><br>', idx, i, option)
            html_output += '</div>'
    return html_output
