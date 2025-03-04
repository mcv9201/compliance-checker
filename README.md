# **Web Compliance Checker**

## **Overview**
This project is a **Web Compliance Checker** that analyzes webpage content against Stripe's public compliance policy https://stripe.com/docs/treasury/marketing-treasury using **GPT-4o**. The system extracts text from a given URL, processes it through a structured prompt, and returns violations in a structured JSON format.

## **Key Features**
- **Structured Output with Pydantic:** Ensures predictable and validated responses from the model.
- **Prompt Caching:** OpenAI's caching mechanism is leveraged, as the initial prompt remains the same while only the webpage content changes, reducing redundant token consumption and improving response efficiency.
- **Markdown Extraction:** Converts webpage content into markdown for improved readability.

---

## **Tech Stack**
- **Python** (Flask for API, Requests for HTTP requests, BeautifulSoup for parsing)
- **OpenAI GPT-4o** (For compliance checking)
- **Pydantic** (For structured responses)
- **Markdownify** (For converting HTML to Markdown)

---

## **Installation & Setup**
### **1. Clone the repository:**
```bash
 git clone <repo-url>
 cd compliance-checker
```

### **2. Create a virtual environment & install dependencies:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
pip install -r requirements.txt
```

### **3. Set environment variables:**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### **4. Run the Flask application:**
```bash
python app.py
```

The app will be available at `http://127.0.0.1:5000/`

---

## **How It Works**

### **1. Extracting Web Content**
- The function `extract_text_from_webpage(url)` fetches webpage content using `requests`.
- It uses `BeautifulSoup` to strip unnecessary tags (e.g., links, images).
- The content is converted to markdown using `markdownify` for better readability.

### **2. Structured Prompting & Caching**
- The prompt is pre-defined in `prompts/user_prompt.txt`.
- The function `get_user_prompt()` dynamically fills in `{webpage_content}` and `{compliance_terms}`.

### **3. Structured Output Handling**
- The model's response is structured using **Pydantic**.
- `Violation` and `Violations` classes enforce type validation:
  ```python
  class Violation(BaseModel):
      violation_text: str  
      policy_violated: str
      explanation: str
      suggestion: str

  class Violations(BaseModel):
      violations: List[Violation]
  ```
- This ensures that the output is always **structured** and can be easily parsed.

### **4. API Endpoint**
- **POST `/check-compliance`**:
  - Accepts `{ "url": "<webpage_url>" }` in JSON format.
  - Extracts content, formats the prompt, and sends it to GPT-4o.
  - Returns structured JSON with compliance violations.

Example Response:
```json
{
    "violations": [
        {
            "policy_violated": "Cash back compliance marketing guidance",
            "violation_text": "Earn up to 4.50% yield on your idle cash with portfolios powered by J.P. Morgan and Morgan Stanley"
            "explanation": "The term 'yield' implies interest, which contradicts the cash back compliance guidelines that explicitly state not to refer to cash back as 'interest' or 'yield'.",
            "suggestion": "Rephrase as 'Earn up to 4.50% cash back on your idle cash with portfolios powered by J.P. Morgan and Morgan Stanley' to comply with guidelines.",  
        }
    ]
}
```
