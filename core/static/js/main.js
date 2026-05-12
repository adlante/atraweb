// ==========================================================================
// کدهای اصلی سایت (کاملا ایمن‌سازی شده با بررسی وجود المان‌ها)
// ==========================================================================
document.addEventListener('DOMContentLoaded', () => {

    // ---------------------------------------------------------
    // 1. منطق سوالات متداول (FAQ)
    // ---------------------------------------------------------
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const questionBtn = item.querySelector('.faq-question');
        if (questionBtn) {
            questionBtn.addEventListener('click', () => {
                item.classList.toggle('active');
            });
        }
    });

    // ---------------------------------------------------------
    // 2. منطق دکمه بازگشت به بالا (Scroll to Top)
    // ---------------------------------------------------------
    const scrollTopBtn = document.getElementById("glass-scroll-top");
    if (scrollTopBtn) {
        window.addEventListener("scroll", function() {
            if (window.scrollY > 300) {
                scrollTopBtn.classList.add("show");
            } else {
                scrollTopBtn.classList.remove("show");
            }
        });

        scrollTopBtn.addEventListener("click", function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        });
    }

    // ---------------------------------------------------------
    // 3. منطق دکمه شناور فروش (Sales Floating Button)
    // ---------------------------------------------------------
    const floatingBtn = document.getElementById('sales-btn');
    if (floatingBtn) {
        const banner = document.getElementById('main-hero');
        const footer = document.querySelector('footer');
        const bottomOffset = 50;

        window.addEventListener('scroll', function() {
            let scrollY = window.scrollY;
            let windowHeight = window.innerHeight;
            let showThreshold = banner ? banner.offsetHeight : 500;
            let hideThreshold = document.body.scrollHeight;

            if (footer) {
                hideThreshold = footer.offsetTop - windowHeight + bottomOffset;
            }

            if (scrollY > showThreshold && scrollY < hideThreshold) {
                floatingBtn.classList.add('is-visible');
            } else {
                floatingBtn.classList.remove('is-visible');
            }
        });
    }

    // ---------------------------------------------------------
    // 4. منطق هدر چسبان (Sticky Header)
    // ---------------------------------------------------------
    const bottomBar = document.querySelector('.bottom-bar');
    if (bottomBar) {
        const stickyOffset = bottomBar.offsetTop;

        window.addEventListener('scroll', function() {
            if (window.innerWidth >= 992) {
                if (window.scrollY > stickyOffset) {
                    bottomBar.classList.add('is-sticky');
                    document.body.classList.add('has-sticky-menu');
                } else {
                    bottomBar.classList.remove('is-sticky');
                    document.body.classList.remove('has-sticky-menu');
                }
            } else {
                bottomBar.classList.remove('is-sticky');
                document.body.classList.remove('has-sticky-menu');
            }
        });

        window.addEventListener('resize', function() {
            if (window.innerWidth < 992) {
                bottomBar.classList.remove('is-sticky');
                document.body.classList.remove('has-sticky-menu');
            }
        });
    }

    // ---------------------------------------------------------
    // 5. منطق منوی موبایل و زیرمنوها (Mobile Menu & Overlay)
    // ---------------------------------------------------------
    const menuToggleBtn = document.getElementById("atraMenuToggle");
    // از آنجایی که bottomBar را در بخش هدر چسبان تعریف کردیم، اینجا فقط از آن استفاده می‌کنیم
    if (menuToggleBtn && bottomBar) {
        const overlay = document.createElement('div');
        overlay.className = 'atra-mobile-overlay-inline';
        document.body.appendChild(overlay);

        function toggleMobileMenu() {
            menuToggleBtn.classList.toggle("active");
            bottomBar.classList.toggle("active");
            overlay.classList.toggle("active");

            if (bottomBar.classList.contains("active")) {
                document.body.style.overflow = "hidden";
            } else {
                document.body.style.overflow = "";
            }
        }

        menuToggleBtn.addEventListener("click", toggleMobileMenu);
        overlay.addEventListener("click", toggleMobileMenu);

        const dropdowns = document.querySelectorAll('.bottom-nav .dropdown');
        dropdowns.forEach(dropdown => {
            const link = dropdown.querySelector('a');
            if (link) {
                link.addEventListener('click', function(e) {
                    if (window.innerWidth <= 992) {
                        e.preventDefault();
                        dropdowns.forEach(d => {
                            if (d !== dropdown) d.classList.remove('open');
                        });
                        dropdown.classList.toggle('open');
                    }
                });
            }
        });
    }

    // ---------------------------------------------------------
    // 6. منطق پاپ‌آپ ویدیو (Video Popup Player)
    // ---------------------------------------------------------
    const popupOverlay = document.getElementById('customVideoPopup');
    const videoPlayer = document.getElementById('popupVideoPlayer');
    const closePopupBtn = document.querySelector('.close-popup-btn');
    const openVideoButtons = document.querySelectorAll('.open-video-popup');

    if (popupOverlay && videoPlayer && closePopupBtn) {
        openVideoButtons.forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                const videoSrc = this.getAttribute('data-src');

                if (videoSrc && videoSrc.trim() !== '') {
                    videoPlayer.src = videoSrc;
                    popupOverlay.classList.add('active');
                    videoPlayer.play();
                } else {
                    alert('ویدیویی برای این بخش آپلود نشده است.');
                }
            });
        });

        const closePopup = () => {
            popupOverlay.classList.remove('active');
            videoPlayer.pause();
            setTimeout(() => {
                videoPlayer.src = '';
            }, 400);
        };

        closePopupBtn.addEventListener('click', closePopup);
        popupOverlay.addEventListener('click', function(e) {
            if (e.target === popupOverlay) {
                closePopup();
            }
        });
    }

    // ---------------------------------------------------------
    // 7. منطق ارسال فرم خبرنامه (Newsletter Ajax Form)
    // ---------------------------------------------------------
    const newsletterForm = document.getElementById('newsletterForm');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const form = this;
            const url = form.getAttribute('data-url');
            const emailInput = document.getElementById('newsletterEmail');
            const messageBox = document.getElementById('newsletterMessage');
            const csrfTokenInput = form.querySelector('[name=csrfmiddlewaretoken]');
            const csrfToken = csrfTokenInput ? csrfTokenInput.value : '';
            const submitBtn = form.querySelector('button[type="submit"]');

            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.style.opacity = '0.5';
            }

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ email: emailInput ? emailInput.value : '' })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('مشکلی در سمت سرور یا آدرس‌دهی وجود دارد (کد ' + response.status + ')');
                }
                return response.json();
            })
            .then(data => {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.style.opacity = '1';
                }

                if (messageBox) {
                    messageBox.style.display = 'block';
                    messageBox.innerText = data.message;

                    if (data.status === 'success') {
                        messageBox.style.color = '#10b981';
                        if (emailInput) emailInput.value = '';
                    } else {
                        messageBox.style.color = '#ef4444';
                    }

                    setTimeout(() => {
                        messageBox.style.display = 'none';
                    }, 5000);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.style.opacity = '1';
                }
                if (messageBox) {
                    messageBox.style.display = 'block';
                    messageBox.style.color = '#ef4444';
                    messageBox.innerText = "خطایی در ارتباط با سرور رخ داد.";
                }
            });
        });
    }

}); // پایان بلاک DOMContentLoaded
