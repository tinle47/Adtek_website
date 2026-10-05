import monaCreateModuleDefault from './modules/default.js';
import monaSolutionsBtn from './modules/solutions_btn.js';
import SelectGetCities from './modules/getCities.js';
import GetRankingEcommerce from './modules/getRankingEcommerce.js';

/****************************/

function monaCf7Popup() {
    document.addEventListener('click', (event) => {
        const openButton = event.target.closest('.js-mona-cf7-popup-open');
        const closeButton = event.target.closest('[data-mona-cf7-popup-close]');

        if (openButton) {
            event.preventDefault();
            const popup = document.querySelector(openButton.dataset.popupTarget);

            if (popup) {
                document.body.appendChild(popup);
                popup.classList.add('is-open');
                popup.setAttribute('aria-hidden', 'false');
                document.body.classList.add('mona-cf7-popup-active');
            }
        }

        if (closeButton) {
            const popup = closeButton.closest('.mona-cf7-popup');

            if (popup) {
                popup.classList.remove('is-open');
                popup.setAttribute('aria-hidden', 'true');
                document.body.classList.remove('mona-cf7-popup-active');
            }
        }
    });

    document.addEventListener('keydown', (event) => {
        if (event.key !== 'Escape') {
            return;
        }

        document.querySelectorAll('.mona-cf7-popup.is-open').forEach((popup) => {
            popup.classList.remove('is-open');
            popup.setAttribute('aria-hidden', 'true');
        });
        document.body.classList.remove('mona-cf7-popup-active');
    });
}

monaCreateModuleDefault();
monaSolutionsBtn();
SelectGetCities();
GetRankingEcommerce();
monaCf7Popup();