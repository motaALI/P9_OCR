

// var SetRatingStar = function() {
//   return $star_rating.each(function() {
//     if (parseInt($star_rating.siblings('input.rating-value').val()) >= parseInt($(this).data('rating'))) {
//       return $(this).removeClass('fa-star-o').addClass('fa-star');
//     } else {
//       return $(this).removeClass('fa-star').addClass('fa-star-o');
//     }
//   });
// };

// $star_rating.on('click', function() {
//   $star_rating.siblings('input.rating-value').val($(this).data('rating'));
//   return SetRatingStar();
// });

// SetRatingStar();

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