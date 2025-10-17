document.getElementById("aboutBtn").addEventListener("click", () => {
    document.getElementById("content").innerHTML = `
    <h2>About Us</h2>
    <p>We’re a small team passionate about clean design and great experiences.</p>
  `;
});

document.getElementById("contactBtn").addEventListener("click", () => {
    document.getElementById("content").innerHTML = `
    <h2>Contact</h2>
    <p>Email us at <a href="mailto:info@example.com">info@example.com</a></p>
      `});