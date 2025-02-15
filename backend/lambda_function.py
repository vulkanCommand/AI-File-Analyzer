import boto3
import json
import base64
import io
import csv
import mimetypes
import requests
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
        file_content = None
        file_type = None

        # ✅ Determine whether request contains a file URL or Base64-encoded file
        body = json.loads(event["body"]) if "body" in event else event

        if "fileUrl" in body:
            # ✅ Handle S3 File URL
            file_url = body["fileUrl"]
            file_content, file_type = download_file_from_s3(file_url)

            if not file_content:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "Failed to download file from S3."})
                }

        elif "body" in body:
            # ✅ Handle Direct Base64 Upload
            try:
                file_content = base64.b64decode(body["body"])
            except Exception:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "Invalid Base64 encoding."})
                }

            # Detect file type from headers
            file_type = event.get("headers", {}).get("content-type", "unknown")

            # If Content-Type is missing or incorrect, assume PDF
            if file_type in ["binary/octet-stream", "application/json", "unknown"]:
                file_type = mimetypes.guess_type("file.pdf")[0]  # Default to PDF

        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No file uploaded or URL provided."})
            }

        # ✅ Extract text from the file
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
    "headers": {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    },
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


# ✅ Function to Download File from S3
def download_file_from_s3(file_url):
    """Downloads file from S3 and returns content and file type"""
    try:
        response = requests.get(file_url)
        if response.status_code == 200:
            file_content = response.content
            file_type = response.headers.get("Content-Type", "unknown")

            # 🛠 If Content-Type is unknown, try inferring from URL extension
            if file_type in ["binary/octet-stream", "unknown"]:
                file_type = mimetypes.guess_type(file_url)[0] or "application/pdf"

            return file_content, file_type
        else:
            return None, None
    except Exception as e:
        return None, None


# ✅ Function to Extract Text from Different File Types
def extract_text_from_file(file_content, file_type):
    """Extracts text from various file formats, handling unknown file types."""
    try:
        if "pdf" in file_type:
            try:
                return extract_text(io.BytesIO(file_content))  # Extract from PDF
            except Exception:
                return "Error: Unable to extract text from PDF, possibly corrupted."
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
