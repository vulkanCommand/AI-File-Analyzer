document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("fileInput");
    const uploadBtn = document.getElementById("uploadBtn");

    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            uploadBtn.textContent = "Analyze File";
            uploadBtn.classList.add("animate-btn");
        } else {
            uploadBtn.textContent = "Upload & Analyze";
            uploadBtn.classList.remove("animate-btn");
        }
    });

    uploadBtn.addEventListener("click", function () {
        if (!fileInput.files.length) {
            alert("Please select a file first.");
            return;
        }

        uploadBtn.textContent = "Analyzing...";
        uploadBtn.disabled = true;

        setTimeout(() => {
            uploadBtn.textContent = "Upload & Analyze";
            uploadBtn.disabled = false;
        }, 5000);
    });
});
