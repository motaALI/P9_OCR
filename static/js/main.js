
document.ready(function(){
  setTimeout(function() {
      $('#my-alert').fadeOut('slow');
  }, 3000); // <-- time in milliseconds
});

function truncateText(text, maxLength=50) {
  if (text.length > maxLength) {
    const shortText = text.slice(0, maxLength) + "...";
    const readMoreButton = "<a href='#'>Read More</a>";
    const fullText = shortText + readMoreButton;
    return fullText;
  } else {
    return text;
  }
}

function myFunction() {
  alert("Hello from a static file!");
}

document.querySelectorAll('.read-more').forEach(function(button) {
  button.addEventListener('click', function() {
    var fullText = this.parentElement.querySelector('.full-text');
    if (fullText.style.display === 'none') {
      fullText.style.display = 'inline';
      this.innerText = 'Read Less';
    } else {
      fullText.style.display = 'none';
      this.innerText = 'Read More';
    }
  });
});