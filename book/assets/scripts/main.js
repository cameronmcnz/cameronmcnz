// Custom JavaScript will go here 

const brand = document.getElementById('scrumtuous-brand');
const annoyingAnimations = [
  // Shake
  () => {
    brand.classList.add('annoy-shake');
    setTimeout(() => brand.classList.remove('annoy-shake'), 700);
  },
  // Color flash
  () => {
    brand.classList.add('annoy-flash');
    setTimeout(() => brand.classList.remove('annoy-flash'), 700);
  },
  // Bounce
  () => {
    brand.classList.add('annoy-bounce');
    setTimeout(() => brand.classList.remove('annoy-bounce'), 700);
  }
];

function annoyBrand() {
  const anim = annoyingAnimations[Math.floor(Math.random() * annoyingAnimations.length)];
  anim();
  const next = 10000 + Math.random() * 5000; // 10-15 seconds
  setTimeout(annoyBrand, next);
}

if (brand) {
  setTimeout(annoyBrand, 10000 + Math.random() * 5000);
}

// Page Loader
window.addEventListener('load', function() {
  const loader = document.getElementById('page-loader');
  if (loader) {
    loader.classList.add('hidden');
    setTimeout(() => loader.remove(), 500);
  }
});

// Testimonials fly-in animation
const testimonialImgs = document.querySelectorAll('.testimonial-img');
if (testimonialImgs.length > 0) {
  const observer = new window.IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });
  testimonialImgs.forEach(img => observer.observe(img));
}

// About section image fly-in
const aboutImg = document.querySelector('.about-img');
if (aboutImg) {
  const aboutObserver = new window.IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        aboutObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });
  aboutObserver.observe(aboutImg);
}

// Stats section count-up animation
function animateCountUp(el, target, plus) {
  let start = 0;
  const duration = 1200;
  const startTime = performance.now();
  function update(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const value = Math.floor(progress * target);
    el.textContent = value + (plus && progress === 1 ? plus : '');
    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      el.textContent = target + (plus ? plus : '');
    }
  }
  requestAnimationFrame(update);
}

const statSection = document.querySelector('.stats-section');
if (statSection) {
  let statsAnimated = false;
  const statObserver = new window.IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !statsAnimated) {
        statsAnimated = true;
        document.querySelectorAll('.stat-number').forEach(el => {
          const target = parseInt(el.getAttribute('data-target'), 10);
          const plus = el.getAttribute('data-plus') || '';
          animateCountUp(el, target, plus);
        });
        statObserver.unobserve(statSection);
      }
    });
  }, { threshold: 0.3 });
  statObserver.observe(statSection);
} 