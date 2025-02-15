# 📄 AI-Powered File Analyzer (PDF Only)

🚀 AI-Powered File Analyzer is a web application that allows users to upload PDF files and receive AI-generated summaries. 
The project is built using **Amazon Bedrock, AWS Lambda, API Gateway, S3, and JavaScript**.

---

## 🌟 Project Overview

This project uses **Amazon Bedrock**, a fully managed AI service by AWS, to analyze and summarize PDF files.\
It leverages **AWS Lambda** for serverless backend processing and **API Gateway** to expose a public API endpoint.\
The frontend is deployed on **Amazon S3**, making it accessible globally.

---

## 📌 **How It Works**

1. **User uploads a PDF file** via the web application.
2. **Frontend converts the file into Base64 format** and sends a request to the API Gateway.
3. **API Gateway triggers an AWS Lambda function**, which:
   - Decodes the PDF file.
   - Extracts text from the PDF.
   - Sends the extracted text to **Amazon Bedrock** for summarization.
4. **Amazon Bedrock generates an AI summary** using **Titan AI Model**.
5. **Lambda returns the summary to the frontend**, which is displayed to the user.

---

## 🚀 **Tech Stack**

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** AWS Lambda (Python)
- **AI Model:** Amazon Bedrock (Text Summarization)
- **Storage:** AWS S3
- **API Management:** AWS API Gateway

---

## ✅ **Project Structure**

The project follows a modular structure for maintainability and scalability:

```
AI-File-Analyzer/
│── frontend/                     # Frontend UI files
│   ├── index.html                # Main HTML file
│   ├── assets/
│   │   ├── css/
│   │   │   ├── styles.css        # Styling file
│   │   │   ├── animations.css    # UI animations
│   │   ├── js/
│   │   │   ├── main.js           # Main JavaScript logic
│   │   │   ├── api-config.js     # API configuration file
│   │   │   ├── upload.js         # Handles file uploads
│   │   │   ├── ai-analysis.js    # Handles AI analysis API calls
│   │   │   ├── effects.js        # UI effects
│── backend/                      # Backend Lambda function
│   ├── lambda_function.py        # AWS Lambda function
│── README.md                     # Project documentation
```

This structure ensures that **frontend** and **backend** components are clearly separated for better development workflow.

---

## ✅ **Amazon Bedrock & AI Model Setup**

1️⃣ **Open AWS Console → Amazon Bedrock**\
2️⃣ Enable **Amazon Bedrock Service**\
3️⃣ Select **Titan AI Model** (Amazon Titan Text Model)\
4️⃣ **Set permissions** so Lambda can call Amazon Bedrock

---
✅ Creating AWS Lambda

1️⃣ Go to AWS Lambda Console\
2️⃣ Click Create Function → Choose Author from scratch\
3️⃣ Enter a function name (e.g., ai-file-analyzer-lambda)\
4️⃣ Select Python 3.x as the runtime\
5️⃣ Choose an execution role and attach AmazonBedrockFullAccess policy\
6️⃣ Upload the Lambda function (``)\
7️⃣ Click Deploy\
8️⃣ Test the function using a sample event\

Lambda Function Code:

{lambda_function.py}

## ✅ **Configure AWS Lambda (Backend)**

1️⃣ **Create a new Lambda function** in AWS Console\
2️⃣ Select **Python 3.x** runtime\
3️⃣ Attach **IAM Role** with `AmazonBedrockFullAccess` permissions\
4️⃣ Upload the **Lambda function (********`lambda_function.py`********)**\
5️⃣ Ensure the function returns **AI-generated summaries**

✅ Creating and Configuring API Gateway

To expose the Lambda function as a REST API, follow these steps:

1️⃣ Go to AWS API Gateway Console\
2️⃣ Click Create API → Select HTTP API\
3️⃣ Click Add Integration → Select Lambda Function\
4️⃣ Choose your Lambda function (e.g., ai-file-analyzer-lambda)\
5️⃣ Click Next and configure the /analyze endpoint\
6️⃣ Enable CORS to allow requests from your frontend\
7️⃣ Click Deploy API and copy the Invoke URL\
8️⃣ Update your frontend (api-config.js) with the new API URL\

API Config Code:

{api-config.js}

✅ Now, your Lambda function is successfully connected to API Gateway


## ✅ **Installed Packages & Dependencies**

Your **AWS Lambda function** requires the following Python packages:

- `boto3` (AWS SDK)
- `pdfminer.six` (Extract text from PDFs)
- `Pillow` (Image Processing for OCR)
- `pytesseract` (OCR for Image Text Extraction)
- `requests` (Downloading files from S3)
- `docx` (Extracting text from Word documents)
- `chardet` (Detecting encoding in text files)

---

## ✅ **Installing, Configuring, and Zipping the Lambda Package**

Since AWS Lambda requires dependencies in a **ZIP format**, install them in a local folder before deployment.

### **1️⃣ Install Dependencies Locally**

```bash
mkdir lambda_package
pip install boto3 pdfminer.six pillow pytesseract requests python-docx chardet -t lambda_package/
```

### **2️⃣ Add Lambda Function to Package**

Move the `lambda_function.py` file into the **lambda\_package** directory:

```bash
cp lambda_function.py lambda_package/
```

### **3️⃣ Zip the Lambda Package for Deployment**

Change into the `lambda_package` directory and zip everything:

```bash
cd lambda_package
zip -r ../lambda_function.zip .
```

Now your **lambda\_function.zip** is ready for deployment!

### **4️⃣ Deploy to AWS Lambda**

Upload the zipped package to AWS Lambda:

```bash
aws lambda update-function-code --function-name your-lambda-function-name --zip-file fileb://lambda_function.zip
```

✅ **Now, your Lambda function is correctly configured with all required dependencies!** 🚀

---

## ✅ **Deploy Web Application on S3**

1️⃣ **Create an S3 bucket**

```bash
aws s3 mb s3://your-s3-bucket-name
```

2️⃣ **Upload your frontend files**

```bash
aws s3 sync ./frontend s3://your-s3-bucket-name --acl public-read
```

3️⃣ **Enable Static Website Hosting in S3**\
4️⃣ **Set Permissions:** Make the bucket publicly accessible

---

## 📂 **Frontend Code**

### index.html:

```html
{index.html}
```

### main.js:

```javascript
{main.js}
```

### upload.js:

```javascript
{upload.js}
```

### ai-analysis.js:

```javascript
{ai-analysis.js}
```

### effects.js:

```javascript
{effects.js}
```

### styles.css:

```css
{styles.css}
```

### animations.css:

```css
{animations.css}
```

---

## 🤝 **Contributing**

- **Fork the Repo**
- **Create a Feature Branch** (`git checkout -b feature-new`)
- **Commit Changes** (`git commit -m "Added new feature"`)
- **Push & Create PR** (`git push origin feature-new`)

---

## 📜 **License**

This project is **MIT Licensed**. You are free to use and modify it.

---

## 💡 **Future Enhancements**

- 🔹 Add support for **Word Documents, Python & Code Files**
- 🔹 Improve **UI with Tailwind CSS**
- 🔹 Secure API with **JWT Authentication**
- 🔹 Use **CloudFront for Faster Performance**

---

