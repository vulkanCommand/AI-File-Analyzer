async function analyzeFile(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch('/analyze', {
        method: 'POST',
        body: formData
    });

    return await response.json();
}
