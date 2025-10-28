const form = document.getElementById('contactForm');
const responseDiv = document.getElementById('formResponse');

form.addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent default form submission

    const formData = {
        name: form.name.value,
        email: form.email.value,
        subject: form.subject.value,
        message: form.message.value
    };

    fetch('/submit_contact', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(res => res.json())
    .then(data => {
        responseDiv.style.display = 'block';
        if(data.status === 'success') {
            responseDiv.className = 'form-response success';
            responseDiv.textContent = data.message;
            form.reset();
        } else {
            responseDiv.className = 'form-response error';
            responseDiv.textContent = data.message;
        }
    })
    .catch(err => {
        responseDiv.style.display = 'block';
        responseDiv.className = 'form-response error';
        responseDiv.textContent = 'Something went wrong!';
        console.error(err);
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Mobile navigation toggle
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');   // Likhta menu slide kare
            navToggle.classList.toggle('active'); // Hamburger bars animation ke liye (CSS me hai)
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            }
        });

        // ✅ Close mobile menu when clicking on any nav link
        const navLinks = navMenu.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            });
        });
    }

        // ✅ Progress Bar Animation
    const progressBars = document.querySelectorAll('.skill-progress');
    const skillsSection = document.querySelector('.skills-section');

    if (skillsSection && progressBars.length > 0) {
        const showProgress = () => {
            progressBars.forEach(bar => {
                const width = bar.getAttribute('data-width');
                bar.style.width = width;
            });
        };

        // Animate only when section comes into view
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    showProgress();
                    observer.unobserve(skillsSection); // Run only once
                }
            });
        }, { threshold: 0.4 });

        observer.observe(skillsSection);
    }
});
