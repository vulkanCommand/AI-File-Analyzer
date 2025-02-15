import boto3
import json
import base64
import io
import csv
import mimetypes
import requests
import docx
import chardet
from botocore.config import Config
from pdfminer.high_level import extract_text
from PIL import Image
import pytesseract

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
    """Extracts text from PDFs, CSVs, Word docs, images, and code files."""
    try:
        if "pdf" in file_type:
            return extract_text(io.BytesIO(file_content))  # Extract from PDF

        elif "csv" in file_type:
            return extract_text_from_csv(io.BytesIO(file_content))  # Extract from CSV

        elif "plain" in file_type or "text" in file_type:
            return extract_text_from_text(file_content)  # Read TXT and Code Files

        elif "msword" in file_type or "vnd.openxmlformats-officedocument.wordprocessingml.document" in file_type:
            return extract_text_from_word(file_content)  # Extract from DOCX

        elif "image" in file_type:
            return extract_text_from_image(file_content)  # Extract text from Image (OCR)

        else:
            return "Unsupported file format"

    except Exception as e:
        return f"Error reading file: {str(e)}"


# ✅ Function to Extract Text from CSV Files
def extract_text_from_csv(csv_content):
    """Extracts text from CSV file"""
    try:
        csv_reader = csv.reader(io.StringIO(csv_content.decode("utf-8")))
        return "\n".join([" | ".join(row) for row in csv_reader])
    except Exception:
        return "Error extracting CSV content"


# ✅ Function to Extract Text from Images (OCR)
def extract_text_from_image(image_content):
    """Extracts text from an image using OCR (Tesseract)."""
    try:
        image = Image.open(io.BytesIO(image_content))
        return pytesseract.image_to_string(image)
    except Exception:
        return "Error extracting text from image"


# ✅ Function to Extract Text from Word Documents (.docx)
def extract_text_from_word(word_content):
    """Extracts text from a Word document (DOCX)."""
    try:
        doc = docx.Document(io.BytesIO(word_content))
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except Exception:
        return "Error extracting text from Word document"


# ✅ Function to Extract Text from Text & Code Files (.py, .java, .c, etc.)
def extract_text_from_text(file_content):
    """Extracts text from text-based files (TXT, Python, Java, C, etc.)."""
    try:
        detected_encoding = chardet.detect(file_content)["encoding"]
        return file_content.decode(detected_encoding, errors="ignore")  # Read Text and Code Files
    except Exception:
        return "Error extracting text from code file"
