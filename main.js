const loginBtn = document.querySelector('.login');
const loginModal = document.querySelector('.login-wrapper');

loginBtn.addEventListener('click', e => {
    e.preventDefault();
    loginModal.style.display = 'flex';
});

loginModal.addEventListener('click', e => {
    if (e.target == loginModal) {
      loginModal.style.display = 'none';
    }
});

const regBtn = document.querySelector('.register');
const regModal = document.querySelector('.register-wrapper');

regBtn.addEventListener('click', e => {
    e.preventDefault();
    regModal.style.display = 'flex';
});

regModal.addEventListener('click', e => {
    if (e.target == regModal) {
      regModal.style.display = 'none';
    }
});

const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');

let slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  if (n > slides.length) slideIndex = 1;
  if (n < 1) slideIndex = slides.length;
  for (let i of slides) {
    i.style.display = 'none';
  }
  for (let i of dots) {
    i.classList.remove('active');
  }
  slides[slideIndex-1].style.display = 'block';
  dots[slideIndex-1].classList.add('active');
}
