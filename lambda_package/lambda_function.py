import boto3
import json
import base64
import io
import csv
from botocore.config import Config
from pdfminer.high_level import extract_text

# Initialize Amazon Bedrock client
client = boto3.client(
    "bedrock-runtime",
    config=Config(connect_timeout=10, read_timeout=30)
)

MODEL_ID = "amazon.titan-tg1-large"

def lambda_handler(event, context):
    try:
        # ✅ Ensure file content exists
        if "body" not in event:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No file uploaded."})
            }

        # ✅ Decode Base64 file content
        file_content = base64.b64decode(event["body"])

        # ✅ Detect file type
        file_type = event.get("headers", {}).get("content-type", "unknown")

        # ✅ Extract text from different file types
        extracted_text = extract_text_from_file(file_content, file_type)

        if not extracted_text.strip():
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Uploaded file is empty or unreadable."})
            }

        # ✅ AI Prompt for summarization
        payload = {
            "inputText": f"Summarize this content in a concise, human-readable way:\n\n{extracted_text}",
            "textGenerationConfig": {
                "maxTokenCount": 200,
                "temperature": 0.5
            }
        }

        response = client.invoke_model(
            modelId=MODEL_ID,
            accept="application/json",
            contentType="application/json",
            body=json.dumps(payload)
        )

        # ✅ Read and parse AI response
        response_body = json.loads(response["body"].read().decode("utf-8"))
        ai_output = response_body.get("results", [{}])[0].get("outputText", "No summary available").strip()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "fileType": file_type,
                "summary": ai_output
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


# ✅ Function to Extract Text from Different File Types
def extract_text_from_file(file_content, file_type):
    """Extracts text from various file formats"""
    try:
        if "pdf" in file_type:
            return extract_text(io.BytesIO(file_content))  # Extract from PDF
        elif "csv" in file_type:
            return extract_text_from_csv(io.BytesIO(file_content))  # Extract from CSV
        elif "plain" in file_type or "text" in file_type:
            return file_content.decode("utf-8", errors="ignore")  # Read TXT
        else:
            return "Unsupported file format"
    except Exception as e:
        return f"Error reading file: {str(e)}"


# ✅ Function to Extract Text from CSV Files
def extract_text_from_csv(csv_content):
    """Extracts text from CSV file"""
    try:
        csv_reader = csv.reader(io.StringIO(csv_content.decode("utf-8")))
        text_output = "\n".join([" | ".join(row) for row in csv_reader])
        return text_output
    except Exception:
        return "Error extracting CSV content"
