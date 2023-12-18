function generateContent() {
    const promptInput = document.getElementById('promptInput').value;
    const fileInput = document.getElementById('fileInput').files[0];

    const formData = new FormData();
    formData.append('prompt', promptInput);
    formData.append('image', fileInput);

    fetch('/generate_content', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('output').innerHTML = `<pre>${data.generated_text}</pre>`;
    })
    .catch(error => console.error('Error:', error));
}
