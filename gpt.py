import os
import requests
import markdownify

from openai import OpenAI
from typing import List
from pydantic import BaseModel
from bs4 import BeautifulSoup

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class Violate(BaseModel):
    violation_text: str  
    policy_violated: str
    explanation: str 
    suggestion: str

class Violates(BaseModel):
    violations: List[Violate]

def get_gpt_response(webpage_content, compliance_terms):
    user_prompt = get_user_prompt(webpage_content, compliance_terms)
    try:
        response = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a financial compliance expert that analyzes webpages against compliance policies."},
                {"role": "user", "content":user_prompt}
            ],
            response_format=Violates
        )
        
        try:
            result = response.choices[0].message.content
            return result
        except Exception as e:
            raise {"error": f"Failed to parse LLM response: {str(e)}"}
            
    except Exception as e:
        raise {"error": f"LLM processing error: {str(e)}"}
    
def get_user_prompt(webpage_content, compliance_terms):
    try:
        with open("./prompts/user_prompt.txt", "r", encoding="utf-8") as file:
            prompt = file.read()
        
        prompt = prompt.format(webpage_content=webpage_content, compliance_terms=compliance_terms)
        return prompt
    except Exception as e:
        raise f"An unexpected error occurred: {str(e)}"


def extract_text_from_webpage(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch webpage: {response.status_code}")
        
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup.find_all(['a', 'img']):
            tag.insert_before(' ')
            tag.decompose()
        
        markdown_text = markdownify.markdownify(str(soup), heading_style="ATX")
        
        return markdown_text
    except Exception as e:
        raise Exception(f"Error extracting content from URL: {str(e)}")