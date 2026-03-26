/** @odoo-module **/

import { NavBar } from "@web/webclient/navbar/navbar";
import { patch } from "@web/core/utils/patch";
import { onMounted, useState } from "@odoo/owl";

// Patch the NavBar component
patch(NavBar.prototype, 'CustomHomeMenu', {
    setup() {
        this._super();

        // Initialize custom home menu state (Odoo 17 NavBar has no this.state)
        this.customMenuState = useState({ isOpen: false });

        // Mount the overlay and replace button after component is mounted
        onMounted(() => {
            this.renderCustomOverlay();
            this.replaceAppsMenuButton();
        });
    },

    openCustomHomeMenu() {
        this.customMenuState.isOpen = true;
        document.body.style.overflow = 'hidden';
        this.renderCustomOverlay();

        // Remove active class from any previously clicked cards
        const container = document.getElementById('custom_home_menu_overlay_container');
        if (container) {
            const cards = container.querySelectorAll('.chm-card-active');
            cards.forEach(c => c.classList.remove('chm-card-active'));
        }

        // Smooth fade-in
        requestAnimationFrame(() => {
            const container = document.getElementById('custom_home_menu_overlay_container');
            if (container) {
                const overlayBg = container.querySelector('.custom_home_menu_overlay');
                if (overlayBg) overlayBg.classList.add('chm-visible');
            }
        });
    },

    closeCustomHomeMenu() {
        const container = document.getElementById('custom_home_menu_overlay_container');
        if (container) {
            const overlayBg = container.querySelector('.custom_home_menu_overlay');
            if (overlayBg) overlayBg.classList.remove('chm-visible');
        }
        // Wait for fade out
        setTimeout(() => {
            this.customMenuState.isOpen = false;
            document.body.style.overflow = '';
        }, 250);
    },

    onAppClick(ev, app) {
        // Add visual feedback before navigating
        const card = ev.target.closest('.custom_home_menu_app_card');
        if (card) card.classList.add('chm-card-active');

        // Brief delay for the click pulse, then navigate while overlay stays visible
        setTimeout(() => {
            // Navigate FIRST — this is instant in Odoo's SPA
            this.onNavBarDropdownItemSelection(app);

            // Keep overlay visible until new app renders underneath,
            // then fade it out
            setTimeout(() => {
                this.customMenuState.isOpen = false;
                document.body.style.overflow = '';
                const container = document.getElementById('custom_home_menu_overlay_container');
                if (container) {
                    const overlayBg = container.querySelector('.custom_home_menu_overlay');
                    if (overlayBg) {
                        overlayBg.classList.remove('chm-visible');
                    }
                }
            }, 400);
        }, 300);
    },

    replaceAppsMenuButton() {
        // Find the default apps menu container
        const appsMenuContainer = document.querySelector('.o_navbar_apps_menu');

        if (appsMenuContainer && !appsMenuContainer.classList.contains('custom-replaced')) {
            // Mark as replaced to avoid re-processing
            appsMenuContainer.classList.add('custom-replaced');

            // Intercept click in capture phase BEFORE OWL Dropdown handles it.
            // This keeps the original button untouched (same size/position as default),
            // and prevents the dropdown from opening.
            appsMenuContainer.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopImmediatePropagation();
                this.openCustomHomeMenu();
            }, true); // true = capture phase
        }
    },

    renderCustomOverlay() {
        // Find or create overlay container
        let overlayContainer = document.getElementById('custom_home_menu_overlay_container');
        if (!overlayContainer) {
            overlayContainer = document.createElement('div');
            overlayContainer.id = 'custom_home_menu_overlay_container';
            document.body.appendChild(overlayContainer);
        }

        // Render overlay HTML exactly once if it's empty
        if (!overlayContainer.innerHTML.trim()) {
            const overlayHtml = this.renderOverlayHTML();
            overlayContainer.innerHTML = overlayHtml;
            this.attachOverlayEventListeners(overlayContainer);
        }
    },

    renderOverlayHTML() {
        const apps = this.menuService.getApps();
        const appCards = apps.map(app => {
            let iconHtml;
            if (app.webIconData) {
                // In Odoo 17, webIconData is raw base64 without a data URI prefix
                let src = app.webIconData;
                if (!src.startsWith("data:image")) {
                    const prefix = src.startsWith("P")
                        ? "data:image/svg+xml;base64,"
                        : "data:image/png;base64,";
                    src = prefix + src.replace(/\s/g, "");
                }
                iconHtml = `<img src="${src}" alt=""/>`;
            } else if (app.webIcon) {
                // CSS class icon (e.g. fa fa-star), with color/bg from webIcon string
                const [iconClass, color, backgroundColor] = (app.webIcon || "").split(",");
                iconHtml = `<div style="background-color:${backgroundColor || '#875a7b'};width:100%;height:100%;border-radius:8px;display:flex;align-items:center;justify-content:center;">
                    <i class="${iconClass}" style="color:${color || '#fff'};font-size:28px;"></i>
                </div>`;
            } else {
                iconHtml = `<i class="oi oi-apps"></i>`;
            }

            return `
                <a href="${this.getMenuItemHref(app)}" 
                   class="custom_home_menu_app_card"
                   data-menu-xmlid="${app.xmlid}"
                   data-section="${app.id}"
                   data-app-id="${app.id}">
                  <div class="custom_home_menu_app_icon">
                    ${iconHtml}
                  </div>
                  <div class="custom_home_menu_app_name">${app.name}</div>
                </a>
            `;
        }).join('');

        return `
            <div class="custom_home_menu_overlay">
              <div class="custom_home_menu_container">
                <div class="custom_home_menu_grid">
                  ${appCards}
                </div>
              </div>
            </div>
        `;
    },

    attachOverlayEventListeners(container) {
        // Overlay background (click outside to close)
        const overlay = container.querySelector('.custom_home_menu_overlay');
        if (overlay) {
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) {
                    this.closeCustomHomeMenu();
                }
            });
        }

        // App cards
        const appCards = container.querySelectorAll('.custom_home_menu_app_card');
        appCards.forEach(card => {
            card.addEventListener('click', (e) => {
                e.preventDefault();
                const appId = parseInt(card.dataset.appId);
                const app = this.menuService.getApps().find(a => a.id === appId);
                if (app) {
                    this.onAppClick(e, app);
                }
            });
        });
    },
});

// Patch NavBar template to add the custom button
patch(NavBar, 'CustomHomeMenuTemplate', {
    template: "web.NavBar",
});
