// Custom JavaScript for Fanfiction Explorer

// Utility functions
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            timeout = null;
            if (!immediate) func(...args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func(...args);
    };
}

function formatNumber(num) {
    return num ? num.toLocaleString() : 'N/A';
}

// Search functionality enhancements
document.addEventListener('DOMContentLoaded', function() {
    
    // Auto-expand collapsed search sections
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.toString().length > 0) {
        const searchForm = document.querySelector('#searchForm');
        if (searchForm) {
            const collapseElement = document.querySelector('#searchCollapse');
            if (collapseElement && !collapseElement.classList.contains('show')) {
                new bootstrap.Collapse(collapseElement).show();
            }
        }
    }
    
    // Enhanced table sorting (if needed)
    const sortableTables = document.querySelectorAll('.table-sortable');
    sortableTables.forEach(table => {
        const headers = table.querySelectorAll('th[data-sort]');
        headers.forEach(header => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => {
                sortTable(table, header.dataset.sort);
            });
        });
    });
    
    // Loading states for forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
            }
        });
    });
    
    // Tooltip initialization (if using tooltips)
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Progress bar animations
    const progressBars = document.querySelectorAll('.progress-bar');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBar = entry.target;
                const width = progressBar.style.width;
                progressBar.style.width = '0%';
                setTimeout(() => {
                    progressBar.style.width = width;
                }, 100);
            }
        });
    });
    
    progressBars.forEach(bar => observer.observe(bar));
});

// Enhanced table sorting function with better performance
function sortTable(table, column) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const headerCell = table.querySelector(`th[data-sort="${column}"]`);
    const isNumeric = headerCell.dataset.type === 'numeric';
    const isDate = headerCell.dataset.type === 'date';
    const currentOrder = headerCell.dataset.order || 'asc';
    const newOrder = currentOrder === 'asc' ? 'desc' : 'asc';
    
    // Add loading state
    table.classList.add('table-loading');
    
    // Remove existing sort indicators
    table.querySelectorAll('th.sortable').forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
        delete th.dataset.order;
    });
    
    // Add new sort indicator
    headerCell.classList.add(`sort-${newOrder}`);
    headerCell.dataset.order = newOrder;
    
    // Sort rows with improved logic
    rows.sort((a, b) => {
        const cellIndex = headerCell.cellIndex;
        let aValue = a.cells[cellIndex].textContent.trim();
        let bValue = b.cells[cellIndex].textContent.trim();
        
        let comparison = 0;
        
        if (isNumeric) {
            // Handle numeric sorting (word counts, chapters, etc.)
            const aNum = parseFloat(aValue.replace(/[^\d.-]/g, '')) || 0;
            const bNum = parseFloat(bValue.replace(/[^\d.-]/g, '')) || 0;
            comparison = aNum - bNum;
        } else if (isDate) {
            // Handle date sorting
            const aDate = new Date(aValue);
            const bDate = new Date(bValue);
            comparison = aDate - bDate;
        } else {
            // Handle text sorting (case insensitive)
            comparison = aValue.toLowerCase().localeCompare(bValue.toLowerCase());
        }
        
        return newOrder === 'asc' ? comparison : -comparison;
    });
    
    // Use requestAnimationFrame for smooth DOM updates
    requestAnimationFrame(() => {
        // Reorder DOM elements
        const fragment = document.createDocumentFragment();
        rows.forEach(row => fragment.appendChild(row));
        tbody.appendChild(fragment);
        
        // Remove loading state
        table.classList.remove('table-loading');
        
        // Add fade-in animation to sorted rows
        rows.forEach((row, index) => {
            row.style.animation = `fadeIn 0.3s ease-out ${index * 0.02}s`;
        });
    });
}

// Initialize sortable tables
function initializeSortableTables() {
    const tables = document.querySelectorAll('.table-sortable');
    
    tables.forEach(table => {
        const sortableHeaders = table.querySelectorAll('th.sortable');
        
        sortableHeaders.forEach(header => {
            header.addEventListener('click', (e) => {
                e.preventDefault();
                const column = header.dataset.sort;
                if (column) {
                    sortTable(table, column);
                }
            });
            
            // Add keyboard support
            header.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    const column = header.dataset.sort;
                    if (column) {
                        sortTable(table, column);
                    }
                }
            });
            
            // Make headers focusable
            header.setAttribute('tabindex', '0');
        });
    });
}

// Fandom filtering functionality
function initializeFandomFiltering() {
    const fandomLinks = document.querySelectorAll('.fandom-link');
    
    fandomLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const fandom = link.textContent.trim();
            
            // Create search URL with fandom filter
            const url = new URL('/search', window.location.origin);
            url.searchParams.set('category', fandom);
            
            // Add visual feedback
            link.style.transform = 'scale(0.95)';
            setTimeout(() => {
                link.style.transform = '';
            }, 150);
            
            // Navigate to filtered results
            window.location.href = url.toString();
        });
        
        // Add keyboard support
        link.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                link.click();
            }
        });
        
        // Make links focusable
        link.setAttribute('tabindex', '0');
    });
}

// Author filtering functionality (bonus feature)
function initializeAuthorFiltering() {
    const authorLinks = document.querySelectorAll('.author-link');
    
    authorLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const author = link.textContent.trim();
            
            // Create search URL with author filter
            const url = new URL('/search', window.location.origin);
            url.searchParams.set('author', author);
            
            // Add visual feedback
            link.style.transform = 'scale(0.95)';
            setTimeout(() => {
                link.style.transform = '';
            }, 150);
            
            // Navigate to filtered results
            window.location.href = url.toString();
        });
        
        // Add keyboard support
        link.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                link.click();
            }
        });
        
        // Make links focusable
        link.setAttribute('tabindex', '0');
    });
}

// Search suggestions (if implementing autocomplete)
function initializeSearchSuggestions() {
    const searchInputs = document.querySelectorAll('.search-input');
    
    searchInputs.forEach(input => {
        const suggestionsList = document.createElement('div');
        suggestionsList.className = 'suggestions-list position-absolute bg-white border rounded shadow-sm';
        suggestionsList.style.display = 'none';
        suggestionsList.style.zIndex = '1000';
        suggestionsList.style.width = '100%';
        suggestionsList.style.maxHeight = '200px';
        suggestionsList.style.overflowY = 'auto';
        
        input.parentNode.appendChild(suggestionsList);
        
        const debouncedSearch = debounce(async (query) => {
            if (query.length < 2) {
                suggestionsList.style.display = 'none';
                return;
            }
            
            try {
                const response = await fetch(`/api/suggestions?q=${encodeURIComponent(query)}&type=${input.dataset.type || 'title'}`);
                const data = await response.json();
                
                if (data.success && data.data.length > 0) {
                    displaySuggestions(suggestionsList, data.data, input);
                } else {
                    suggestionsList.style.display = 'none';
                }
            } catch (error) {
                console.error('Failed to fetch suggestions:', error);
                suggestionsList.style.display = 'none';
            }
        }, 300);
        
        input.addEventListener('input', (e) => {
            debouncedSearch(e.target.value);
        });
        
        input.addEventListener('blur', () => {
            setTimeout(() => {
                suggestionsList.style.display = 'none';
            }, 200);
        });
    });
}

function displaySuggestions(container, suggestions, input) {
    container.innerHTML = '';
    
    suggestions.forEach(suggestion => {
        const item = document.createElement('div');
        item.className = 'suggestion-item p-2 cursor-pointer';
        item.textContent = suggestion;
        
        item.addEventListener('mouseenter', () => {
            item.style.backgroundColor = '#f8f9fa';
        });
        
        item.addEventListener('mouseleave', () => {
            item.style.backgroundColor = '';
        });
        
        item.addEventListener('click', () => {
            input.value = suggestion;
            container.style.display = 'none';
        });
        
        container.appendChild(item);
    });
    
    container.style.display = 'block';
}

// Chart utilities
function createChart(canvasId, type, data, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;
    
    const ctx = canvas.getContext('2d');
    
    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: type !== 'bar'
            }
        }
    };
    
    return new Chart(ctx, {
        type: type,
        data: data,
        options: { ...defaultOptions, ...options }
    });
}

// Theme management (if implementing dark mode)
function initializeTheme() {
    const themeToggle = document.getElementById('theme-toggle');
    if (!themeToggle) return;
    
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);
    
    themeToggle.addEventListener('click', () => {
        const newTheme = document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });
}

// Performance monitoring
function initializePerformanceMonitoring() {
    if ('performance' in window && 'navigation' in performance) {
        window.addEventListener('load', () => {
            setTimeout(() => {
                const perfData = performance.getEntriesByType('navigation')[0];
                if (perfData.loadEventEnd > 0) {
                    const loadTime = perfData.loadEventEnd - perfData.navigationStart;
                    console.log(`Page load time: ${loadTime}ms`);
                    
                    // Send to analytics if configured
                    if (window.gtag) {
                        gtag('event', 'timing_complete', {
                            'name': 'page_load',
                            'value': Math.round(loadTime)
                        });
                    }
                }
            }, 0);
        });
    }
}

// Error handling
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    
    // Optional: Send error to logging service
    if (window.gtag) {
        gtag('event', 'exception', {
            'description': event.error?.message || 'Unknown error',
            'fatal': false
        });
    }
});

// Service worker registration (for PWA features)
function initializeServiceWorker() {
    if ('serviceWorker' in navigator && window.location.protocol === 'https:') {
        navigator.serviceWorker.register('/sw.js')
            .then((registration) => {
                console.log('ServiceWorker registered:', registration.scope);
            })
            .catch((error) => {
                console.log('ServiceWorker registration failed:', error);
            });
    }
}

// Initialize features based on page
function initializePage() {
    const path = window.location.pathname;
    
    // Initialize common features for all pages
    initializeSortableTables();
    initializeFandomFiltering();
    initializeAuthorFiltering();
    initializeTheme();
    initializePerformanceMonitoring();
    
    // Page-specific initializations
    if (path.includes('/search') || path.includes('/browse')) {
        initializeSearchSuggestions();
        
        // Add special handling for search results
        console.log('🔍 Search/Browse page: Enhanced sorting and filtering enabled');
    }
    
    if (path === '/' || path.includes('/dashboard')) {
        // Dashboard-specific initializations
        console.log('📊 Dashboard: Interactive charts and full-width layout enabled');
    }
    
    // initializeServiceWorker(); // Uncomment if implementing PWA
    
    console.log('⚡ Fanfiction Explorer: All features initialized');
}

// Call initialization when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializePage);
} else {
    initializePage();
}
