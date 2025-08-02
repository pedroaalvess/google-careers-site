// DOM Elements
const candidatureForm = document.getElementById('candidatureForm');
const submitBtn = document.getElementById('submitBtn');
const messageContainer = document.getElementById('messageContainer');
const faqItems = document.querySelectorAll('.faq-item');
const fileInputs = document.querySelectorAll('.file-input');
const jobsGrid = document.getElementById('jobsGrid');
const carouselIndicators = document.getElementById('carouselIndicators');

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initializeFileUploads();
    initializeFAQ();
    initializeFormValidation();
    initializeSmoothScrolling();
    initializeJobsCarousel();
});

// Jobs Carousel Functionality
function initializeJobsCarousel() {
    if (!jobsGrid || !carouselIndicators) return;
    
    const indicators = carouselIndicators.querySelectorAll('.indicator');
    const jobCards = jobsGrid.querySelectorAll('.job-card');
    
    // Handle indicator clicks
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => {
            scrollToJob(index);
        });
    });
    
    // Handle scroll events to update active indicator
    let scrollTimeout;
    jobsGrid.addEventListener('scroll', () => {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            updateActiveIndicator();
        }, 100);
    });
    
    // Hide swipe hint after first interaction
    let hasInteracted = false;
    jobsGrid.addEventListener('scroll', () => {
        if (!hasInteracted) {
            hasInteracted = true;
            const swipeHint = document.querySelector('.swipe-hint');
            if (swipeHint) {
                swipeHint.style.animation = 'fadeOut 0.5s ease-out forwards';
                setTimeout(() => {
                    swipeHint.style.display = 'none';
                }, 500);
            }
        }
    });
}

function scrollToJob(index) {
    if (!jobsGrid) return;
    
    const jobCards = jobsGrid.querySelectorAll('.job-card');
    if (jobCards[index]) {
        const cardWidth = 320; // Nova largura fixa para mobile
        const gap = 15; // Gap atualizado
        const scrollLeft = index * (cardWidth + gap);
        
        jobsGrid.scrollTo({
            left: scrollLeft,
            behavior: 'smooth'
        });
    }
}

function updateActiveIndicator() {
    if (!jobsGrid || !carouselIndicators) return;
    
    const indicators = carouselIndicators.querySelectorAll('.indicator');
    const jobCards = jobsGrid.querySelectorAll('.job-card');
    
    if (jobCards.length === 0) return;
    
    const scrollLeft = jobsGrid.scrollLeft;
    const cardWidth = 320; // Nova largura fixa para mobile
    const gap = 15; // Gap atualizado
    const activeIndex = Math.round(scrollLeft / (cardWidth + gap));
    
    // Update active indicator
    indicators.forEach((indicator, index) => {
        if (index === activeIndex) {
            indicator.classList.add('active');
        } else {
            indicator.classList.remove('active');
        }
    });
}

// File Upload Handling
function initializeFileUploads() {
    fileInputs.forEach(input => {
        const uploadArea = input.nextElementSibling;
        
        // Click to select file
        uploadArea.addEventListener('click', () => {
            input.click();
        });
        
        // Drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = '#1a73e8';
            uploadArea.style.background = '#f8f9ff';
        });
        
        uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = '#e0e0e0';
            uploadArea.style.background = 'white';
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = '#e0e0e0';
            uploadArea.style.background = 'white';
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                input.files = files;
                updateFileDisplay(input, uploadArea);
            }
        });
        
        // File selection change
        input.addEventListener('change', () => {
            updateFileDisplay(input, uploadArea);
        });
    });
}

function updateFileDisplay(input, uploadArea) {
    const file = input.files[0];
    if (file) {
        const fileName = file.name;
        const fileSize = (file.size / 1024 / 1024).toFixed(2) + ' MB';
        
        uploadArea.innerHTML = `
            <i class="fas fa-check-circle" style="color: #34a853;"></i>
            <span style="color: #34a853; font-weight: 600;">${fileName}</span>
            <small style="color: #5f6368;">${fileSize}</small>
        `;
        
        // Validate file
        if (!validateFile(file)) {
            showMessage('Fichier invalide. Veuillez sélectionner un fichier PNG, JPEG ou PDF de moins de 16MB.', 'error');
            input.value = '';
            resetFileDisplay(uploadArea);
        }
    }
}

function resetFileDisplay(uploadArea) {
    uploadArea.innerHTML = `
        <i class="fas fa-cloud-upload-alt"></i>
        <span>Cliquez pour sélectionner ou glissez votre fichier</span>
        <small>PNG, JPEG ou PDF - Max 16MB</small>
    `;
}

function validateFile(file) {
    const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'application/pdf'];
    const maxSize = 16 * 1024 * 1024; // 16MB
    
    return allowedTypes.includes(file.type) && file.size <= maxSize;
}

// FAQ Functionality
function initializeFAQ() {
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        
        question.addEventListener('click', () => {
            const isActive = item.classList.contains('active');
            
            // Close all FAQ items
            faqItems.forEach(faqItem => {
                faqItem.classList.remove('active');
            });
            
            // Open clicked item if it wasn't active
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });
}

// Form Validation
function initializeFormValidation() {
    const requiredFields = candidatureForm.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        field.addEventListener('blur', () => {
            validateField(field);
        });
        
        field.addEventListener('input', () => {
            if (field.classList.contains('error')) {
                validateField(field);
            }
        });
    });
}

function validateField(field) {
    const isValid = field.checkValidity();
    
    if (isValid) {
        field.classList.remove('error');
        field.style.borderColor = '#34a853';
    } else {
        field.classList.add('error');
        field.style.borderColor = '#ea4335';
    }
    
    return isValid;
}

function validateForm() {
    let isValid = true;
    const requiredFields = candidatureForm.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });
    
    // Validate file uploads
    const fileInputs = candidatureForm.querySelectorAll('.file-input[required]');
    fileInputs.forEach(input => {
        if (!input.files || input.files.length === 0) {
            isValid = false;
            input.style.borderColor = '#ea4335';
        }
    });
    
    // Validate checkboxes
    const checkboxes = candidatureForm.querySelectorAll('.form-checkbox[required]');
    checkboxes.forEach(checkbox => {
        if (!checkbox.checked) {
            isValid = false;
            checkbox.parentElement.style.background = '#fce8e6';
        } else {
            checkbox.parentElement.style.background = 'transparent';
        }
    });
    
    return isValid;
}

// Form Submission
candidatureForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
        showMessage('Veuillez remplir tous les champs requis et accepter les conditions.', 'error');
        return;
    }
    
    // Show loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = `
        <span class="button-text">Envoi en cours...</span>
        <i class="fas fa-spinner fa-spin button-icon"></i>
    `;
    
    try {
        const formData = new FormData(candidatureForm);
        
        const response = await fetch('/api/candidatures', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showMessage('Candidature soumise avec succès! Nous vous contacterons bientôt.', 'success');
            candidatureForm.reset();
            resetAllFileDisplays();
            
            // Scroll to top
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
            throw new Error(result.error || 'Erreur lors de la soumission');
        }
    } catch (error) {
        console.error('Erreur:', error);
        showMessage(error.message || 'Une erreur est survenue. Veuillez réessayer.', 'error');
    } finally {
        // Reset button state
        submitBtn.disabled = false;
        submitBtn.innerHTML = `
            <span class="button-text">Envoyer ma candidature</span>
            <i class="fas fa-paper-plane button-icon"></i>
        `;
    }
});

function resetAllFileDisplays() {
    const uploadAreas = document.querySelectorAll('.file-upload-area');
    uploadAreas.forEach(resetFileDisplay);
}

// Message System
function showMessage(text, type = 'info') {
    const message = document.createElement('div');
    message.className = `message ${type}`;
    message.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px;">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
            <span>${text}</span>
        </div>
    `;
    
    messageContainer.appendChild(message);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (message.parentNode) {
            message.style.animation = 'slideOutRight 0.3s ease-out forwards';
            setTimeout(() => {
                message.remove();
            }, 300);
        }
    }, 5000);
    
    // Click to close
    message.addEventListener('click', () => {
        message.style.animation = 'slideOutRight 0.3s ease-out forwards';
        setTimeout(() => {
            message.remove();
        }, 300);
    });
}

// Smooth Scrolling
function initializeSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            const targetId = link.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = targetElement.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Header Scroll Effect
window.addEventListener('scroll', () => {
    const header = document.querySelector('.header');
    const scrollY = window.scrollY;
    
    if (scrollY > 100) {
        header.style.background = 'rgba(255, 255, 255, 0.98)';
        header.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
    } else {
        header.style.background = 'rgba(255, 255, 255, 0.95)';
        header.style.boxShadow = 'none';
    }
});

// Intersection Observer for Animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.6s ease-out forwards';
        }
    });
}, observerOptions);

// Observe elements for animation
document.addEventListener('DOMContentLoaded', () => {
    const animateElements = document.querySelectorAll('.job-card, .gallery-item, .faq-item');
    animateElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        observer.observe(el);
    });
});

// Add slideOutRight animation to CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
`;
document.head.appendChild(style);

