/**
 * Color Detector Application - Main JavaScript
 * Production-ready with advanced features
 */

class ColorDetectorApp {
    constructor() {
        this.video = document.getElementById('video');
        this.canvas = document.createElement('canvas');
        this.currentStream = null;
        this.useFrontCamera = false;
        this.isDarkMode = localStorage.getItem('darkMode') === 'true';
        this.currentScheme = 'monochromatic';
        this.init();
    }

    async init() {
        this.setupEventListeners();
        this.applyTheme();
        await this.startCamera();
        await this.loadHistory();
    }

    setupEventListeners() {
        // Camera controls
        document.getElementById('capture').addEventListener('click', () => this.captureColor());
        document.getElementById('switchCam').addEventListener('click', () => this.switchCamera());
        
        // Theme toggle
        document.getElementById('themeToggle').addEventListener('click', () => this.toggleTheme());
        
        // Scheme selector
        document.querySelectorAll('.scheme-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.changeScheme(e.target.dataset.scheme));
        });
        
        // History controls
        document.getElementById('clearHistory').addEventListener('click', () => this.clearHistory());
        
        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });
        
        // Export buttons
        document.getElementById('exportJSON').addEventListener('click', () => this.exportData('json'));
        document.getElementById('exportCSS').addEventListener('click', () => this.exportData('css'));
        document.getElementById('copyHex').addEventListener('click', () => this.copyToClipboard());
    }

    async startCamera() {
        try {
            if (this.currentStream) {
                this.currentStream.getTracks().forEach(track => track.stop());
            }

            const constraints = {
                video: {
                    facingMode: this.useFrontCamera ? "user" : "environment",
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                }
            };

            this.currentStream = await navigator.mediaDevices.getUserMedia(constraints);
            this.video.srcObject = this.currentStream;
            this.showNotification('Camera started successfully', 'success');
        } catch (err) {
            this.showNotification(`Camera error: ${err.message}`, 'error');
            console.error('Camera error:', err);
        }
    }

    async switchCamera() {
        this.useFrontCamera = !this.useFrontCamera;
        await this.startCamera();
    }

    async captureColor() {
        try {
            const btn = document.getElementById('capture');
            btn.classList.add('loading');
            btn.disabled = true;

            // Capture frame
            this.canvas.width = this.video.videoWidth;
            this.canvas.height = this.video.videoHeight;
            const ctx = this.canvas.getContext('2d');
            ctx.drawImage(this.video, 0, 0);

            const image = this.canvas.toDataURL('image/jpeg');

            // Send to backend
            const response = await fetch('/api/detect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image })
            });

            const data = await response.json();

            if (data.success) {
                this.displayColorResult(data.color, data.schemes);
                await this.loadHistory();
                this.showNotification('Color detected successfully!', 'success');
            } else {
                throw new Error(data.error || 'Detection failed');
            }
        } catch (err) {
            this.showNotification(`Detection error: ${err.message}`, 'error');
            console.error('Detection error:', err);
        } finally {
            const btn = document.getElementById('capture');
            btn.classList.remove('loading');
            btn.disabled = false;
        }
    }

    displayColorResult(color, schemes) {
        // Show result section
        document.getElementById('result').classList.remove('hidden');

        // Main color display
        const mainColor = document.getElementById('mainColor');
        mainColor.style.background = color.hex;
        
        document.getElementById('colorName').textContent = color.name;
        document.getElementById('hexValue').textContent = color.hex;

        // Color formats
        document.getElementById('rgbValue').textContent = 
            `rgb(${color.rgb.r}, ${color.rgb.g}, ${color.rgb.b})`;
        document.getElementById('hslValue').textContent = 
            `hsl(${color.hsl.h}°, ${color.hsl.s}%, ${color.hsl.l}%)`;
        document.getElementById('hsvValue').textContent = 
            `hsv(${color.hsv.h}°, ${color.hsv.s}%, ${color.hsv.v}%)`;
        document.getElementById('cmykValue').textContent = 
            `cmyk(${color.cmyk.c}%, ${color.cmyk.m}%, ${color.cmyk.y}%, ${color.cmyk.k}%)`;

        // Temperature
        document.getElementById('temperatureValue').textContent = 
            `${color.temperature.temperature} (${color.temperature.warmth_value})`;
        document.getElementById('temperatureDesc').textContent = 
            color.temperature.description;

        // Accessibility
        this.displayAccessibility(color.accessibility);

        // Store current color
        this.currentColor = color;
        this.currentSchemes = schemes;

        // Display current scheme
        this.displayScheme(this.currentScheme);
    }

    displayAccessibility(accessibility) {
        const whiteSection = document.getElementById('whiteAccessibility');
        const blackSection = document.getElementById('blackAccessibility');

        whiteSection.innerHTML = `
            <h4>On White Background</h4>
            <p>Contrast Ratio: ${accessibility.white_background.ratio}:1</p>
            <div class="wcag-badges">
                <span class="badge ${accessibility.white_background.aa_normal ? 'pass' : 'fail'}">
                    AA Normal: ${accessibility.white_background.aa_normal ? '✓' : '✗'}
                </span>
                <span class="badge ${accessibility.white_background.aa_large ? 'pass' : 'fail'}">
                    AA Large: ${accessibility.white_background.aa_large ? '✓' : '✗'}
                </span>
                <span class="badge ${accessibility.white_background.aaa_normal ? 'pass' : 'fail'}">
                    AAA Normal: ${accessibility.white_background.aaa_normal ? '✓' : '✗'}
                </span>
                <span class="badge ${accessibility.white_background.aaa_large ? 'pass' : 'fail'}">
                    AAA Large: ${accessibility.white_background.aaa_large ? '✓' : '✗'}
                </span>
            </div>
        `;

        blackSection.innerHTML = `
            <h4>On Black Background</h4>
            <p>Contrast Ratio: ${accessibility.black_background.ratio}:1</p>
            <div class="wcag-badges">
                <span class="badge ${accessibility.black_background.aa_normal ? 'pass' : 'fail'}">
                    AA Normal: ${accessibility.black_background.aa_normal ? '✓' : '✗'}
                </span>
                <span class="badge ${accessibility.black_background.aa_large ? 'pass' : 'fail'}">
                    AA Large: ${accessibility.black_background.aa_large ? '✓' : '✗'}
                </span>
                <span class="badge ${accessibility.black_background.aaa_normal ? 'pass' : 'fail'}">
                    AAA Normal: ${accessibility.black_background.aaa_normal ? '✓' : '✗'}
                </span>
                <span class="badge ${accessibility.black_background.aaa_large ? 'pass' : 'fail'}">
                    AAA Large: ${accessibility.black_background.aaa_large ? '✓' : '✗'}
                </span>
            </div>
        `;
    }

    changeScheme(scheme) {
        this.currentScheme = scheme;
        document.querySelectorAll('.scheme-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.scheme === scheme);
        });
        this.displayScheme(scheme);
    }

    displayScheme(scheme) {
        if (!this.currentSchemes || !this.currentSchemes[scheme]) return;

        const container = document.getElementById('schemeColors');
        container.innerHTML = '';

        this.currentSchemes[scheme].forEach(color => {
            const swatch = document.createElement('div');
            swatch.className = 'color-swatch';
            swatch.style.background = color.hex;
            swatch.title = `${color.name}\n${color.hex}`;
            swatch.innerHTML = `
                <span class="swatch-hex">${color.hex}</span>
            `;
            swatch.addEventListener('click', () => this.copyToClipboard(color.hex));
            container.appendChild(swatch);
        });
    }

    async loadHistory() {
        try {
            const response = await fetch('/api/history?limit=10');
            const data = await response.json();

            if (data.success) {
                this.displayHistory(data.history);
            }
        } catch (err) {
            console.error('Error loading history:', err);
        }
    }

    displayHistory(history) {
        const container = document.getElementById('historyList');
        if (history.length === 0) {
            container.innerHTML = '<p class="empty-state">No color history yet</p>';
            return;
        }

        container.innerHTML = history.map(item => `
            <div class="history-item" data-id="${item.id}">
                <div class="history-color" style="background: ${item.hex_code}"></div>
                <div class="history-info">
                    <strong>${item.color_name}</strong>
                    <span>${item.hex_code}</span>
                    <span class="history-date">${new Date(item.created_at).toLocaleString()}</span>
                </div>
                <button class="delete-btn" onclick="app.deleteHistoryItem(${item.id})">×</button>
            </div>
        `).join('');
    }

    async deleteHistoryItem(id) {
        try {
            const response = await fetch(`/api/history/${id}`, { method: 'DELETE' });
            const data = await response.json();

            if (data.success) {
                await this.loadHistory();
                this.showNotification('History item deleted', 'success');
            }
        } catch (err) {
            this.showNotification('Failed to delete item', 'error');
        }
    }

    async clearHistory() {
        if (!confirm('Are you sure you want to clear all history?')) return;

        try {
            const response = await fetch('/api/history/clear', { method: 'DELETE' });
            const data = await response.json();

            if (data.success) {
                await this.loadHistory();
                this.showNotification('History cleared', 'success');
            }
        } catch (err) {
            this.showNotification('Failed to clear history', 'error');
        }
    }

    toggleTheme() {
        this.isDarkMode = !this.isDarkMode;
        localStorage.setItem('darkMode', this.isDarkMode);
        this.applyTheme();
    }

    applyTheme() {
        document.body.classList.toggle('dark-mode', this.isDarkMode);
        const icon = document.querySelector('#themeToggle i');
        icon.className = this.isDarkMode ? 'fas fa-sun' : 'fas fa-moon';
    }

    switchTab(tab) {
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tab);
        });
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.toggle('active', content.id === `${tab}Tab`);
        });
    }

    copyToClipboard(text) {
        const toCopy = text || this.currentColor?.hex;
        if (!toCopy) return;

        navigator.clipboard.writeText(toCopy).then(() => {
            this.showNotification(`Copied ${toCopy} to clipboard!`, 'success');
        }).catch(() => {
            this.showNotification('Failed to copy', 'error');
        });
    }

    exportData(format) {
        if (!this.currentColor) {
            this.showNotification('No color to export', 'error');
            return;
        }

        let content, filename, mimeType;

        if (format === 'json') {
            content = JSON.stringify({
                color: this.currentColor,
                schemes: this.currentSchemes
            }, null, 2);
            filename = 'color-data.json';
            mimeType = 'application/json';
        } else if (format === 'css') {
            content = this.generateCSS();
            filename = 'colors.css';
            mimeType = 'text/css';
        }

        this.downloadFile(content, filename, mimeType);
        this.showNotification(`Exported as ${format.toUpperCase()}`, 'success');
    }

    generateCSS() {
        const c = this.currentColor;
        let css = `/* Color Palette */\n:root {\n`;
        css += `  --primary-color: ${c.hex};\n`;
        css += `  --primary-rgb: ${c.rgb.r}, ${c.rgb.g}, ${c.rgb.b};\n`;
        css += `  --primary-hsl: ${c.hsl.h}, ${c.hsl.s}%, ${c.hsl.l}%;\n\n`;

        const scheme = this.currentSchemes[this.currentScheme];
        scheme.forEach((color, i) => {
            css += `  --color-${i + 1}: ${color.hex};\n`;
        });

        css += `}\n`;
        return css;
    }

    downloadFile(content, filename, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        URL.revokeObjectURL(url);
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.classList.add('show');
        }, 10);

        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
}

// Initialize app when DOM is loaded
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new ColorDetectorApp();
});
