/**
 * Analytics Data Collector - Embeddable Script
 * Include this script in any website to collect analytics data
 * 
 * Usage:
 * <script src="https://yourserver.com/static/embed.js"></script>
 * <script>
 *   AnalyticsCollector.init({
 *     server: 'https://yourserver.com',
 *     auto: true,
 *     interval: 30000
 *   });
 * </script>
 */

(function(window, document) {
    'use strict';

    // Default configuration
    const defaultConfig = {
        server: 'http://localhost:5000',
        auto: true,
        interval: 0,
        debug: false,
        endpoint: '/collect'
    };

    let config = {...defaultConfig};
    let isInitialized = false;
    let intervalId = null;

    const AnalyticsCollector = {
        init: function(userConfig) {
            if (isInitialized) {
                this.log('Analytics Collector already initialized');
                return;
            }

            config = {...defaultConfig, ...userConfig};
            isInitialized = true;
            
            this.log('Analytics Collector initialized', config);

            if (config.auto) {
                this.collect();
                
                if (config.interval > 0) {
                    intervalId = setInterval(() => {
                        this.collect();
                    }, config.interval);
                }
            }
        },

        collect: function(additionalData = {}) {
            if (!isInitialized) {
                this.log('Analytics Collector not initialized. Call init() first.');
                return;
            }

            const data = {
                ...this.gatherSystemData(),
                ...additionalData,
                timestamp: new Date().toISOString(),
                collector_type: 'embed_script'
            };

            this.send(data);
        },

        gatherSystemData: function() {
            return {
                // Browser information
                browser: this.getBrowserInfo(),
                user_agent: navigator.userAgent,
                
                // System information
                os: this.getOperatingSystem(),
                platform: navigator.platform,
                
                // Display information
                screen_resolution: `${screen.width}x${screen.height}`,
                viewport: `${window.innerWidth}x${window.innerHeight}`,
                color_depth: screen.colorDepth,
                pixel_ratio: window.devicePixelRatio,
                
                // Locale and time
                timezone: this.getTimezone(),
                language: navigator.language,
                languages: navigator.languages,
                
                // Browser capabilities
                cookies_enabled: navigator.cookieEnabled,
                do_not_track: navigator.doNotTrack,
                java_enabled: navigator.javaEnabled ? navigator.javaEnabled() : false,
                
                // Hardware information
                hardware_concurrency: navigator.hardwareConcurrency,
                memory: navigator.deviceMemory,
                
                // Network information (if available)
                connection: this.getConnectionInfo(),
                
                // Fingerprinting data
                fingerprint: this.generateFingerprint(),
                canvas_fingerprint: this.getCanvasFingerprint(),
                webgl_fingerprint: this.getWebGLFingerprint(),
                
                // Page information
                url: window.location.href,
                referrer: document.referrer,
                title: document.title,
                
                // Performance data
                performance: this.getPerformanceData(),
                
                // Mouse and interaction data
                mouse_position: this.getMousePosition(),
                scroll_position: this.getScrollPosition(),
                
                // Additional browser features
                webrtc_support: this.hasWebRTC(),
                websocket_support: this.hasWebSocket(),
                local_storage: this.hasLocalStorage(),
                session_storage: this.hasSessionStorage()
            };
        },

        send: function(data) {
            const url = config.server.replace(/\/$/, '') + config.endpoint;
            
            // Try to use fetch first, fallback to XMLHttpRequest
            if (window.fetch) {
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                    mode: 'cors'
                })
                .then(response => response.json())
                .then(result => {
                    this.log('Data sent successfully:', result);
                })
                .catch(error => {
                    this.log('Error sending data:', error);
                });
            } else {
                // Fallback for older browsers
                const xhr = new XMLHttpRequest();
                xhr.open('POST', url);
                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.onreadystatechange = () => {
                    if (xhr.readyState === 4) {
                        if (xhr.status === 200) {
                            this.log('Data sent successfully:', JSON.parse(xhr.responseText));
                        } else {
                            this.log('Error sending data:', xhr.status);
                        }
                    }
                };
                xhr.send(JSON.stringify(data));
            }
        },

        // Utility functions
        getBrowserInfo: function() {
            const ua = navigator.userAgent;
            if (ua.includes('Chrome') && !ua.includes('Edge')) return 'Chrome';
            if (ua.includes('Firefox')) return 'Firefox';
            if (ua.includes('Safari') && !ua.includes('Chrome')) return 'Safari';
            if (ua.includes('Edge')) return 'Edge';
            if (ua.includes('Opera')) return 'Opera';
            if (ua.includes('MSIE') || ua.includes('Trident')) return 'Internet Explorer';
            return 'Unknown';
        },

        getOperatingSystem: function() {
            const platform = navigator.platform.toLowerCase();
            const ua = navigator.userAgent.toLowerCase();
            
            if (platform.includes('win')) return 'Windows';
            if (platform.includes('mac')) return 'macOS';
            if (platform.includes('linux')) return 'Linux';
            if (ua.includes('android')) return 'Android';
            if (ua.includes('iphone') || ua.includes('ipad')) return 'iOS';
            return 'Unknown';
        },

        getTimezone: function() {
            try {
                return Intl.DateTimeFormat().resolvedOptions().timeZone;
            } catch (e) {
                return 'Unknown';
            }
        },

        getConnectionInfo: function() {
            if (navigator.connection) {
                return {
                    effective_type: navigator.connection.effectiveType,
                    downlink: navigator.connection.downlink,
                    rtt: navigator.connection.rtt,
                    save_data: navigator.connection.saveData
                };
            }
            return null;
        },

        generateFingerprint: function() {
            const components = [
                navigator.userAgent,
                navigator.language,
                screen.width + 'x' + screen.height,
                new Date().getTimezoneOffset(),
                navigator.platform,
                navigator.cookieEnabled,
                navigator.doNotTrack
            ];
            
            try {
                return btoa(components.join('|')).slice(0, 32);
            } catch (e) {
                return 'unavailable';
            }
        },

        getCanvasFingerprint: function() {
            try {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                ctx.textBaseline = 'top';
                ctx.font = '14px Arial';
                ctx.fillText('Canvas fingerprint test 🎨', 2, 2);
                return canvas.toDataURL().slice(-32);
            } catch (e) {
                return 'unavailable';
            }
        },

        getWebGLFingerprint: function() {
            try {
                const canvas = document.createElement('canvas');
                const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
                if (!gl) return 'unavailable';
                
                const vendor = gl.getParameter(gl.VENDOR);
                const renderer = gl.getParameter(gl.RENDERER);
                return btoa(vendor + '|' + renderer).slice(-32);
            } catch (e) {
                return 'unavailable';
            }
        },

        getPerformanceData: function() {
            if (!window.performance) return null;
            
            return {
                navigation_type: performance.navigation ? performance.navigation.type : null,
                redirect_count: performance.navigation ? performance.navigation.redirectCount : null,
                timing: performance.timing ? {
                    load_time: performance.timing.loadEventEnd - performance.timing.navigationStart,
                    dom_ready: performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart
                } : null
            };
        },

        getMousePosition: function() {
            // Return last known mouse position if available
            if (window._lastMousePos) {
                return window._lastMousePos;
            }
            return { x: 0, y: 0 };
        },

        getScrollPosition: function() {
            return {
                x: window.pageXOffset || document.documentElement.scrollLeft || document.body.scrollLeft || 0,
                y: window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0
            };
        },

        hasWebRTC: function() {
            return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) ||
                   !!(navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia);
        },

        hasWebSocket: function() {
            return 'WebSocket' in window;
        },

        hasLocalStorage: function() {
            try {
                return 'localStorage' in window && window.localStorage !== null;
            } catch (e) {
                return false;
            }
        },

        hasSessionStorage: function() {
            try {
                return 'sessionStorage' in window && window.sessionStorage !== null;
            } catch (e) {
                return false;
            }
        },

        log: function(message, data) {
            if (config.debug) {
                console.log('[Analytics Collector]', message, data);
            }
        },

        stop: function() {
            if (intervalId) {
                clearInterval(intervalId);
                intervalId = null;
            }
            this.log('Analytics Collector stopped');
        },

        restart: function() {
            this.stop();
            if (config.interval > 0) {
                intervalId = setInterval(() => {
                    this.collect();
                }, config.interval);
            }
            this.log('Analytics Collector restarted');
        }
    };

    // Track mouse position
    document.addEventListener('mousemove', function(e) {
        window._lastMousePos = { x: e.clientX, y: e.clientY };
    });

    // Make AnalyticsCollector available globally
    window.AnalyticsCollector = AnalyticsCollector;

    // Auto-initialize if config is present
    if (window.AnalyticsConfig) {
        AnalyticsCollector.init(window.AnalyticsConfig);
    }

})(window, document);