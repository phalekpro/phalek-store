// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    // Loader
    setTimeout(() => {
        document.getElementById('loader').classList.add('hidden');
    }, 2000);

    // Effet de particules
    createParticles();
    
    // Animation de frappe
    startTypewriter();
    
    // Scroll events
    window.addEventListener('scroll', handleScroll);
    
    // Formulaire de contact
    document.getElementById('contact-form').addEventListener('submit', handleFormSubmit);
    
    // Animations au scroll
    initScrollAnimations();
});

// Effet de particules
function createParticles() {
    const container = document.getElementById('particles');
    const particleCount = 15;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        
        // Position aléatoire
        const size = Math.random() * 100 + 50;
        const posX = Math.random() * 100;
        const posY = Math.random() * 100;
        const delay = Math.random() * 5;
        
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.left = `${posX}%`;
        particle.style.top = `${posY}%`;
        particle.style.animationDelay = `${delay}s`;
        particle.style.opacity = Math.random() * 0.1 + 0.05;
        
        container.appendChild(particle);
    }
}

// Animation de frappe
function startTypewriter() {
    const text = "Yapo Atsé Phalek Ariel";
    const element = document.getElementById('typewriter');
    let index = 0;
    
    function type() {
        if (index < text.length) {
            element.innerHTML += text.charAt(index);
            index++;
            setTimeout(type, 100);
        }
    }
    
    setTimeout(type, 1000);
}

// Gestion du scroll
function handleScroll() {
    const header = document.getElementById('header');
    if (window.scrollY > 100) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
    
    // Animation des éléments au scroll
    animateOnScroll();
}

// Animation au scroll
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observer les éléments à animer
    document.querySelectorAll('.project-card, .about-content, .contact-form').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

function animateOnScroll() {
    const elements = document.querySelectorAll('.project-card, .about-content, .contact-form');
    const windowHeight = window.innerHeight;
    
    elements.forEach(element => {
        const position = element.getBoundingClientRect().top;
        
        if (position < windowHeight - 100) {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }
    });
}

// Gestion du formulaire
function handleFormSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const successMessage = document.getElementById('contact-success');
    
    // Simulation d'envoi
    form.style.display = 'none';
    successMessage.style.display = 'block';
    
    // Réinitialiser après 5 secondes
    setTimeout(() => {
        form.style.display = 'block';
        successMessage.style.display = 'none';
        form.reset();
    }, 5000);
}

// Scroll vers une section
function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    const headerHeight = document.getElementById('header').offsetHeight;
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - headerHeight;

    window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
    });
}

// Effet de rebond pour le bouton CTA
document.querySelector('.cta-button').addEventListener('click', function() {
    this.style.transform = 'scale(0.95)';
    setTimeout(() => {
        this.style.transform = '';
    }, 150);
});
// Navigation entre les pages
function navigateTo(page) {
    window.location.href = page;
}

// Gestion des liens dans les pages de projet
document.addEventListener('DOMContentLoaded', function() {
    // S'assurer que tous les liens internes fonctionnent
    document.querySelectorAll('a[href^="/"]').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = this.getAttribute('href');
        });
    });
});