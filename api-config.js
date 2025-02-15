const API_BASE_URL = "https://zzdsfqe063.execute-api.us-east-1.amazonaws.com/prod";

const API_ENDPOINTS = {
    ANALYZE: `${API_BASE_URL}/analyze`
};

async function analyzeFile(file) {
    const reader = new FileReader();

    return new Promise((resolve, reject) => {
        reader.onload = async function (event) {
            const base64String = event.target.result.split(",")[1]; // Extract Base64 data
            const requestBody = {
                body: base64String,
                headers: {
                    "content-type": file.type
                }
            };

            try {
                const response = await fetch(API_ENDPOINTS.ANALYZE, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(requestBody)
                });

                const data = await response.json();
                resolve(data);
            } catch (error) {
                console.error("Error analyzing file:", error);
                reject(error);
            }
        };

        reader.readAsDataURL(file);
    });
}
