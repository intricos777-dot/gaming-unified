/* =========================================================
   Joshua Allen Cole Scott - Professional Gaming Portfolio
   Main JavaScript
   ========================================================= */

'use strict';

/* =========================================================
   DOM Ready
   ========================================================= */
document.addEventListener('DOMContentLoaded', () => {
    initHeaderScroll();
    initMobileNav();
    initSmoothScroll();
    initFadeToggle();
    initVideoModals();
    initCounterAnimation();
    initActiveNavLink();
});

/* =========================================================
   Header Scroll Effect
   ========================================================= */
function initHeaderScroll() {
    const header = document.getElementById('siteHeader');
    if (!header) return;

    const onScroll = () => {
        header.classList.toggle('scrolled', window.scrollY > 50);
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
}

/* =========================================================
   Mobile Navigation
   ========================================================= */
function initMobileNav() {
    const toggle = document.querySelector('.nav-toggle');
    const menu = document.getElementById('navMenu');
    if (!toggle || !menu) return;

    const closeMenu = () => {
        menu.classList.remove('open');
        toggle.classList.remove('active');
        toggle.setAttribute('aria-expanded', 'false');
    };

    toggle.addEventListener('click', (e) => {
        e.stopPropagation();
        menu.classList.toggle('open');
        toggle.classList.toggle('active');
        const isOpen = menu.classList.contains('open');
        toggle.setAttribute('aria-expanded', String(isOpen));
    });

    menu.querySelectorAll('.nav-link').forEach((link) => {
        link.addEventListener('click', closeMenu);
    });

    document.addEventListener('click', (e) => {
        if (menu.classList.contains('open') && !menu.contains(e.target) && !toggle.contains(e.target)) {
            closeMenu();
        }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && menu.classList.contains('open')) {
            closeMenu();
        }
    });
}

/* =========================================================
   Smooth Scroll for Anchor Links
   ========================================================= */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener('click', (e) => {
            const targetId = anchor.getAttribute('href');
            if (targetId === '#' || targetId.length < 2) return;
            const target = document.querySelector(targetId);
            if (!target) return;
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    });
}

/* =========================================================
   Fade Toggle - Core Feature
   ========================================================= */
function initFadeToggle() {
    const fadeBtn = document.getElementById('fadeToggle');
    const fadeContainer = document.getElementById('fadeContainer');
    if (!fadeBtn || !fadeContainer) return;

    let isFaded = false;

    const updateButton = () => {
        fadeBtn.classList.toggle('active', isFaded);
        fadeBtn.setAttribute('aria-pressed', String(isFaded));
        const fadeText = fadeBtn.querySelector('.fade-text');
        if (fadeText) {
            fadeText.textContent = isFaded ? 'Showcase Hidden - Click to Restore' : 'Fade Showcase for Full Site Clarity';
        }
    };

    fadeBtn.addEventListener('click', () => {
        isFaded = !isFaded;
        fadeContainer.classList.toggle('faded', isFaded);
        updateButton();
    });

    // Initialize button state
    updateButton();
}

/* =========================================================
   Video Modals
   ========================================================= */
const videoData = {
    'eldon-ring-victory': {
        id: '8E7qF3dQ5Q0',
        title: 'Elden Ring - Legendary Victory vs letmesoloher',
        youtubeUrl: 'https://www.youtube.com/@letmesoloher',
        channel: 'letmesoloher'
    },
    'tournament-highlights': {
        id: 'dQw4w9WgXcQ',
        title: 'Elite Tournament Performance',
        youtubeUrl: 'https://www.youtube.com/@Living_Sin',
        channel: 'Living_Sin'
    },
    'cross-platform': {
        id: 'pQ9J7K8cR3E',
        title: 'Cross-Platform Mastery',
        youtubeUrl: 'https://www.youtube.com/@Living_Sin',
        channel: 'Living_Sin'
    },
    'competitive': {
        id: 'f2Z4cJkR9T0',
        title: 'Competitive Gaming Highlights',
        youtubeUrl: 'https://www.youtube.com/@letmesoloher',
        channel: 'letmesoloher'
    }
};

function initVideoModals() {
    const modal = document.getElementById('videoModal');
    const modalVideo = document.getElementById('modalVideo');
    const modalTitle = document.getElementById('modalTitle');
    const modalClose = modal.querySelector('.modal-close');
    const modalOverlay = modal.querySelector('.modal-overlay');

    if (!modal || !modalVideo || !modalTitle) return;

    let currentVideoId = null;

    const openModal = (videoKey) => {
        const video = videoData[videoKey];
        if (!video) return;

        currentVideoId = video.id;

        // Embed video with autoplay
        modalVideo.innerHTML = `
            <iframe
                src="https://www.youtube.com/embed/${video.id}?autoplay=1&rel=0"
                title="${video.title}"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
            ></iframe>
        `;
        modalTitle.textContent = video.title;

        modal.hidden = false;
        document.body.style.overflow = 'hidden';

        modalClose.focus();

        // Add video source link
        const sourceLink = document.createElement('a');
        sourceLink.href = video.youtubeUrl;
        sourceLink.target = '_blank';
        sourceLink.rel = 'noopener noreferrer';
        sourceLink.className = 'btn btn-sm btn-outline';
        sourceLink.style.marginTop = '10px';
        sourceLink.textContent = `View on ${video.channel}'s YouTube`;
        modalTitle.after(sourceLink);
    };

    const closeModal = () => {
        modal.hidden = true;
        modalVideo.innerHTML = '';
        document.body.style.overflow = '';
        currentVideoId = null;
        modalTitle.after().remove?.();
    };

    modalClose.addEventListener('click', closeModal);
    modalOverlay.addEventListener('click', closeModal);

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !modal.hidden) {
            closeModal();
        }
    });

    // Trigger modals from thumbnails
    document.querySelectorAll('.video-thumbnail').forEach((thumbnail) => {
        const card = thumbnail.closest('.showcase-card');
        if (!card) return;
        const videoKey = card.dataset.video;
        if (!videoData[videoKey]) return;

        thumbnail.addEventListener('click', () => openModal(videoKey));

        // Keyboard accessibility
        thumbnail.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                openModal(videoKey);
            }
        });
    });
}

/* =========================================================
   Counter Animation
   ========================================================= */
function initCounterAnimation() {
    const counters = document.querySelectorAll('.stat-number[data-target]');

    if (!counters.length) return;

    const formatNumber = (num) => {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1).replace(/\.0$/, '') + 'M';
        }
        if (num >= 1000) {
            return (num / 1000).toFixed(1).replace(/\.0$/, '') + 'K';
        }
        return num.toLocaleString();
    };

    const animateCounter = (counter) => {
        const target = parseInt(counter.dataset.target, 10);
        const duration = 2000;
        const startTime = performance.now();

        const updateValue = (currentTime) => {
            const progress = Math.min((currentTime - startTime) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(target * eased);
            counter.textContent = formatNumber(current);

            if (progress < 1) {
                requestAnimationFrame(updateValue);
            } else {
                counter.textContent = formatNumber(target);
            }
        };

        requestAnimationFrame(updateValue);
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach((counter) => observer.observe(counter));
}

/* =========================================================
   Active Nav Link Highlight
   ========================================================= */
function initActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    if (!sections.length || !navLinks.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                navLinks.forEach((link) => {
                    link.classList.toggle(
                        'active',
                        link.getAttribute('href') === `#${entry.target.id}`
                    );
                });
            }
        });
    }, { rootMargin: '-45% 0px -45% 0px' });

    sections.forEach((section) => observer.observe(section));
}

/* =========================================================
   Contact Form Handling
   ========================================================= */
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('contactForm');
    if (!form) return;

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;

        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending...';

        const formData = new FormData(form);
        const formDataObject = Object.fromEntries(formData.entries());

        fetch(form.action, {
            method: 'POST',
            body: new URLSearchParams(formData),
            headers: {
                'Accept': 'application/json'
            }
        })
        .then((response) => {
            if (response.ok) {
                form.reset();
                showFormMessage('Message sent successfully! I\'ll get back to you within 24-48 hours.', 'success');
            } else {
                throw new Error('Form submission failed');
            }
        })
        .catch(() => {
            showFormMessage('Failed to send message. Please try again or email me directly.', 'error');
        })
        .finally(() => {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        });
    });

    function showFormMessage(message, type) {
        const existing = form.querySelector('.form-message');
        if (existing) existing.remove();

        const msg = document.createElement('p');
        msg.className = `form-message form-message-${type}`;
        msg.textContent = message;
        msg.style.textAlign = 'center';
        msg.style.marginTop = '12px';
        msg.style.padding = '10px';
        msg.style.borderRadius = '4px';
        msg.style.fontSize = '0.875rem';

        if (type === 'success') {
            msg.style.color = '#2ECC71';
            msg.style.border = '1px solid #2ECC71';
            msg.style.background = 'rgba(46, 204, 113, 0.1)';
        } else {
            msg.style.color = '#E74C3C';
            msg.style.border = '1px solid #E74C3C';
            msg.style.background = 'rgba(231, 76, 60, 0.1)';
        }

        form.appendChild(msg);

        setTimeout(() => msg.remove(), 6000);
    }
});