/*
 * ===================================================================
 * LIBRARY MANAGEMENT DASHBOARD - JAVASCRIPT
 * ===================================================================
 * Handles chart initialization, data visualization, and interactions
 * ===================================================================
 */

// Global chart instances
let statusChart, trendChart, topBooksChart, categoryChart;

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
    console.log('Dashboard initialized');
    
    // Animate counter numbers
    animateCounters();
    
    // Initialize all charts
    initializeCharts();
    
    // Setup interactions
    setupInteractions();
});

/**
 * Animate counter numbers on statistics cards
 */
function animateCounters() {
    const counterElements = document.querySelectorAll('.stat-number');
    
    counterElements.forEach(element => {
        const finalCount = parseInt(element.getAttribute('data-count'), 10);
        let currentCount = 0;
        
        // Calculate increment based on final value
        const increment = Math.max(1, Math.ceil(finalCount / 50));
        const duration = 1000; // 1 second
        const steps = finalCount / increment;
        const stepDuration = duration / steps;
        
        const counter = setInterval(() => {
            currentCount += increment;
            
            if (currentCount >= finalCount) {
                currentCount = finalCount;
                clearInterval(counter);
            }
            
            element.textContent = currentCount.toLocaleString();
        }, stepDuration);
    });
}

/**
 * Initialize all chart instances
 */
function initializeCharts() {
    // Status Chart - Pie/Doughnut
    initializeStatusChart();
    
    // Trend Chart - Line Chart
    initializeTrendChart();
    
    // Top Books Chart - Bar Chart
    initializeTopBooksChart();
    
    // Category Chart - Pie Chart
    initializeCategoryChart();
}

/**
 * Initialize Books Status Distribution Chart
 */
function initializeStatusChart() {
    const ctx = document.getElementById('statusChart');
    
    if (!ctx) {
        console.warn('Status chart canvas not found');
        return;
    }
    
    // Colors matching the theme
    const colors = [
        '#27ae60', // Available - Green
        '#f39c12', // Issued - Orange
        '#e74c3c'  // Overdue - Red
    ];
    
    statusChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Available', 'Issued', 'Overdue'],
            datasets: [{
                data: [
                    dashboardData.available,
                    dashboardData.issued,
                    dashboardData.overdue
                ],
                backgroundColor: colors,
                borderColor: '#ffffff',
                borderWidth: 3,
                hoverOffset: 10,
                borderRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: {
                            family: "'Poppins', sans-serif",
                            size: 12,
                            weight: '600'
                        },
                        padding: 20,
                        color: '#2c2c2c',
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        family: "'Poppins', sans-serif",
                        size: 13,
                        weight: '700'
                    },
                    bodyFont: {
                        family: "'Poppins', sans-serif",
                        size: 12
                    },
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                    borderWidth: 1,
                    displayColors: true,
                    callbacks: {
                        label: function (context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((context.parsed / total) * 100).toFixed(1);
                            return `${context.label}: ${context.parsed} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Initialize Monthly Trend Line Chart
 */
function initializeTrendChart() {
    const ctx = document.getElementById('trendChart');
    
    if (!ctx) {
        console.warn('Trend chart canvas not found');
        return;
    }
    
    trendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dashboardData.months,
            datasets: [
                {
                    label: 'Books Issued',
                    data: dashboardData.issuedTrend,
                    borderColor: '#4b7bec',
                    backgroundColor: 'rgba(75, 123, 236, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#4b7bec',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    pointHoverBackgroundColor: '#4b7bec'
                },
                {
                    label: 'Books Returned',
                    data: dashboardData.returnedTrend,
                    borderColor: '#27ae60',
                    backgroundColor: 'rgba(39, 174, 96, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#27ae60',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    pointHoverBackgroundColor: '#27ae60'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        font: {
                            family: "'Poppins', sans-serif",
                            size: 12,
                            weight: '600'
                        },
                        padding: 20,
                        color: '#2c2c2c',
                        usePointStyle: true
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        family: "'Poppins', sans-serif",
                        size: 13,
                        weight: '700'
                    },
                    bodyFont: {
                        family: "'Poppins', sans-serif",
                        size: 12
                    },
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                    borderWidth: 1,
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(200, 200, 200, 0.1)',
                        drawBorder: false
                    },
                    ticks: {
                        font: {
                            family: "'Poppins', sans-serif",
                            size: 11
                        },
                        color: '#7f8c8d'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            family: "'Poppins', sans-serif",
                            size: 11
                        },
                        color: '#7f8c8d'
                    }
                }
            }
        }
    });
}

/**
 * Initialize Top 5 Books Bar Chart
 */
function initializeTopBooksChart() {
    const ctx = document.getElementById('topBooksChart');
    
    if (!ctx) {
        console.warn('Top books chart canvas not found');
        return;
    }
    
    // Get top books data from template (if available)
    const topBooksElement = document.querySelector('.books-table tbody');
    let bookLabels = [];
    let bookCounts = [];
    
    if (topBooksElement) {
        const rows = topBooksElement.querySelectorAll('tr');
        rows.forEach(row => {
            const titleCell = row.querySelector('td:first-child');
            const countCell = row.querySelector('td:nth-child(3)');
            
            if (titleCell && countCell) {
                let title = titleCell.textContent.trim();
                // Truncate long titles
                if (title.length > 25) {
                    title = title.substring(0, 22) + '...';
                }
                bookLabels.push(title);
                bookCounts.push(parseInt(countCell.textContent, 10));
            }
        });
    }
    
    // Generate colors for bars
    const barColors = [
        '#4b7bec',
        '#3498db',
        '#5b5fc7',
        '#2980b9',
        '#1a5f8f'
    ];
    
    topBooksChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: bookLabels.length > 0 ? bookLabels : ['No data'],
            datasets: [{
                label: 'Times Issued',
                data: bookCounts.length > 0 ? bookCounts : [0],
                backgroundColor: barColors.slice(0, bookLabels.length || 1),
                borderColor: barColors.map(color => color),
                borderWidth: 2,
                borderRadius: 5,
                hoverBackgroundColor: '#3498db',
                hoverBorderColor: '#2980b9'
            }]
        },
        options: {
            indexAxis: 'x',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        font: {
                            family: "'Poppins', sans-serif",
                            size: 12,
                            weight: '600'
                        },
                        padding: 20,
                        color: '#2c2c2c'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        family: "'Poppins', sans-serif",
                        size: 13,
                        weight: '700'
                    },
                    bodyFont: {
                        family: "'Poppins', sans-serif",
                        size: 12
                    },
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                    borderWidth: 1,
                    callbacks: {
                        label: function (context) {
                            return `Issues: ${context.parsed.y}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(200, 200, 200, 0.1)',
                        drawBorder: false
                    },
                    ticks: {
                        font: {
                            family: "'Poppins', sans-serif",
                            size: 11
                        },
                        color: '#7f8c8d',
                        stepSize: 1
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            family: "'Poppins', sans-serif",
                            size: 11
                        },
                        color: '#7f8c8d'
                    }
                }
            }
        }
    });
}

/**
 * Initialize Category Distribution Pie Chart
 */
function initializeCategoryChart() {
    const ctx = document.getElementById('categoryChart');
    
    if (!ctx) {
        console.warn('Category chart canvas not found');
        return;
    }
    
    // Generate colors for categories
    const categoryColors = [
        '#4b7bec',
        '#27ae60',
        '#f39c12',
        '#e74c3c',
        '#9b59b6',
        '#1abc9c',
        '#34495e'
    ];
    
    // Note: Category data should be passed from Django template
    // For now, we'll create a placeholder
    categoryChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Education', 'History', 'Novel', 'Fiction', 'Thriller', 'Romance', 'Sci-Fi'],
            datasets: [{
                data: [20, 15, 12, 10, 8, 5, 3],
                backgroundColor: categoryColors,
                borderColor: '#ffffff',
                borderWidth: 3,
                hoverOffset: 10,
                borderRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: {
                            family: "'Poppins', sans-serif",
                            size: 12,
                            weight: '600'
                        },
                        padding: 15,
                        color: '#2c2c2c',
                        usePointStyle: true
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        family: "'Poppins', sans-serif",
                        size: 13,
                        weight: '700'
                    },
                    bodyFont: {
                        family: "'Poppins', sans-serif",
                        size: 12
                    },
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                    borderWidth: 1
                }
            }
        }
    });
}

/**
 * Setup interactions and event listeners
 */
function setupInteractions() {
    // Add smooth scroll behavior to action buttons
    const quickActionButtons = document.querySelectorAll('.quick-action-btn');
    
    quickActionButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            // Add ripple effect
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
    
    // Add keyboard navigation
    document.addEventListener('keydown', function (e) {
        if (e.key === 'r' && (e.ctrlKey || e.metaKey)) {
            e.preventDefault();
            location.reload();
        }
    });
    
    // Intersection Observer for fade-in animations
    observeElements();
}

/**
 * Observe elements for intersection and animate them
 */
function observeElements() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeIn 0.6s ease-out forwards';
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    const elementsToObserve = document.querySelectorAll('.stat-card, .chart-card, .activity-item, .low-stock-item');
    
    elementsToObserve.forEach(element => {
        observer.observe(element);
    });
}

/**
 * Helper function to format numbers with commas
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/**
 * Helper function to format dates
 */
function formatDate(date) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(date).toLocaleDateString(undefined, options);
}

/**
 * Update dashboard data via AJAX (optional enhancement)
 */
function refreshDashboardData() {
    // This function can be extended to fetch fresh data without page reload
    console.log('Refreshing dashboard data...');
    // Example: fetch('/api/dashboard-stats/')
}

// Add ripple effect CSS dynamically
const style = document.createElement('style');
style.textContent = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
