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
    animateCounters();
    initializeCharts();
    setupInteractions();
});

/* ==================== COUNTER ANIMATION ==================== */
function animateCounters() {
    const counterElements = document.querySelectorAll('.stat-number');
    
    counterElements.forEach(element => {
        const finalCount = parseInt(element.getAttribute('data-count'), 10);
        let currentCount = 0;
        const increment = Math.max(1, Math.ceil(finalCount / 50));
        const duration = 1000;
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

/* ==================== CHART INITIALIZATION ==================== */
function initializeCharts() {
    initializeStatusChart();
    initializeTrendChart();
    initializeTopBooksChart();
    initializeCategoryChart();
}

/* ==================== BOOKS STATUS CHART (Doughnut) ==================== */
function initializeStatusChart() {
    const ctx = document.getElementById('statusChart');
    if (!ctx) {
        console.warn('Status chart canvas not found');
        return;
    }
    
    const colors = ['#27ae60', '#f39c12', '#e74c3c'];
    
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

/* ==================== MONTHLY TREND CHART (Line) ==================== */
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
                    pointHoverRadius: 7
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
                    pointHoverRadius: 7
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

/* ==================== TOP BOOKS CHART (Bar) ==================== */
function initializeTopBooksChart() {
    const ctx = document.getElementById('topBooksChart');
    if (!ctx) {
        console.warn('Top books chart canvas not found');
        return;
    }
    
    // Extract data from table
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
                if (title.length > 25) {
                    title = title.substring(0, 22) + '...';
                }
                bookLabels.push(title);
                bookCounts.push(parseInt(countCell.textContent, 10));
            }
        });
    }
    
    const barColors = ['#4b7bec', '#3498db', '#5b5fc7', '#2980b9', '#1a5f8f'];
    
    topBooksChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: bookLabels.length > 0 ? bookLabels : ['No data'],
            datasets: [{
                label: 'Times Issued',
                data: bookCounts.length > 0 ? bookCounts : [0],
                backgroundColor: barColors.slice(0, bookLabels.length || 1),
                borderColor: barColors.map(color => color),
                borderWidth: 1,
                borderRadius: 3,
                hoverBackgroundColor: '#3498db',
                hoverBorderColor: '#2980b9'
            }]
        },
        options: {
            indexAxis: 'x',
            responsive: true,
            maintainAspectRatio: false,
            barPercentage: 0.5,
            categoryPercentage: 0.7,
            plugins: {
                legend: {
                    display: false
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
                        stepSize: 1,
                        padding: 5
                    },
                    border: {
                        display: true,
                        color: 'rgba(200, 200, 200, 0.3)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            family: "'Poppins', sans-serif",
                            size: 10,
                            weight: '500'
                        },
                        color: '#7f8c8d',
                        maxRotation: 45,
                        minRotation: 0
                    },
                    border: {
                        display: true,
                        color: 'rgba(200, 200, 200, 0.3)'
                    }
                }
            },
            layout: {
                padding: {
                    top: 15,
                    right: 15,
                    bottom: 15,
                    left: 10
                }
            }
        }
    });
}

/* ==================== CATEGORY CHART (Pie) ==================== */
function initializeCategoryChart() {
    const ctx = document.getElementById('categoryChart');
    if (!ctx) {
        console.warn('Category chart canvas not found');
        return;
    }
    
    const categoryColors = [
        '#4b7bec', '#27ae60', '#f39c12', '#e74c3c', '#9b59b6',
        '#1abc9c', '#34495e', '#3498db', '#e67e22', '#95a5a6'
    ];
    
    // Extract from backend data
    const categoryLabels = dashboardData.categoryDistribution.map(item => item.category);
    const categoryCounts = dashboardData.categoryDistribution.map(item => item.count);
    
    categoryChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: categoryLabels,
            datasets: [{
                data: categoryCounts,
                backgroundColor: categoryColors.slice(0, categoryLabels.length),
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
                    borderWidth: 1,
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

/* ==================== INTERACTIONS ==================== */
function setupInteractions() {
    // Ripple effect on quick action buttons
    const quickActionButtons = document.querySelectorAll('.quick-action-btn');
    quickActionButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function (e) {
        if (e.key === 'r' && (e.ctrlKey || e.metaKey)) {
            e.preventDefault();
            location.reload();
        }
    });
    
    // Intersection Observer for animations
    observeElements();
}

/* ==================== INTERSECTION OBSERVER ==================== */
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
    elementsToObserve.forEach(element => observer.observe(element));
}