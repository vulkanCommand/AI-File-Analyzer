// ✅ Function to Convert File to Base64
function getBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = (error) => reject(error);
    });
}

// ✅ Ensure Button Click Works
document.getElementById('uploadBtn').addEventListener('click', async function () {
    console.log("✅ Analyze button clicked!");

    const fileInput = document.getElementById('fileInput');
    if (!fileInput.files.length) {
        console.error("🚨 No file selected.");
        alert("Please select a file to upload.");
        return;
    }

    const file = fileInput.files[0];
    console.log(`📂 Selected file: ${file.name}, Type: ${file.type}`);

    document.getElementById('result').classList.add('hidden');
    document.getElementById('uploadBtn').textContent = "Analyzing...";
    document.getElementById('uploadBtn').disabled = true;

    try {
        console.time("🔄 Encoding file to Base64");
        const base64Data = await getBase64(file); // ✅ Using defined function
        console.timeEnd("🔄 Encoding file to Base64");

        const requestBody = {
            body: base64Data.split(",")[1], // Remove Base64 header
            headers: {
                "content-type": file.type
            }
        };

        console.log("🚀 Sending request to API...", API_ENDPOINTS.ANALYZE, requestBody);

        console.time("🔄 API Request Time");
        const response = await fetch(API_ENDPOINTS.ANALYZE, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(requestBody)
        });
        console.timeEnd("🔄 API Request Time");

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("✅ API Response:", data);

        if (data.error) {
            throw new Error(data.error);
        }

        document.getElementById('fileType').textContent = `File Type: ${data.fileType}`;
        document.getElementById('summary').textContent = `Summary: ${data.summary}`;
        document.getElementById('result').classList.remove('hidden');

    } catch (error) {
        console.error("🚨 Error analyzing file:", error);
        alert(`Error analyzing file: ${error.message}`);
    }

    document.getElementById('uploadBtn').textContent = "Upload & Analyze";
    document.getElementById('uploadBtn').disabled = false;
});
