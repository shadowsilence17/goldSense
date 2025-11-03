// Gold Price Prediction App JavaScript

let weekChart = null;
let monthChart = null;

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    loadCurrentPrice();
});

// Load current gold price
async function loadCurrentPrice() {
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ type: 'day' })
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('current-price').innerHTML = 
                `$${data.current_price.toFixed(2)}`;
            document.getElementById('last-updated').textContent = 
                `Last updated: ${new Date(data.timestamp).toLocaleString()}`;
        }
    } catch (error) {
        console.error('Error loading current price:', error);
        document.getElementById('current-price').innerHTML = 
            '<span class="error">Error loading price</span>';
    }
}

// Get prediction
async function getPrediction(type) {
    // Hide all results
    hideAllResults();
    
    // Show loading
    showLoading();
    
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ type: type })
        });
        
        const data = await response.json();
        
        hideLoading();
        
        if (data.success) {
            // Show results container
            document.getElementById('results-container').style.display = 'block';
            
            // Display based on type
            if (type === 'day') {
                showDayResults(data.prediction);
            } else if (type === 'week') {
                showWeekResults(data.prediction);
            } else if (type === 'month') {
                showMonthResults(data.prediction);
            }
        } else {
            showError(data.error || 'Prediction failed');
        }
        
    } catch (error) {
        hideLoading();
        showError('Network error. Please try again.');
        console.error('Error:', error);
    }
}

// Show day results
function showDayResults(prediction) {
    const dayResults = document.getElementById('day-results');
    dayResults.style.display = 'block';
    
    document.getElementById('next-day-price').textContent = 
        prediction.next_day.toFixed(2);
    
    const change = prediction.change;
    const changePercent = prediction.change_percent;
    
    const changeAmount = document.getElementById('change-amount');
    const changePercentElem = document.getElementById('change-percent');
    const changeDiv = document.querySelector('.pred-change');
    
    changeAmount.textContent = (change >= 0 ? '+' : '') + change.toFixed(2);
    changePercentElem.textContent = (changePercent >= 0 ? '+' : '') + changePercent.toFixed(2);
    
    // Color based on change
    changeDiv.className = 'pred-change ' + (change >= 0 ? 'positive' : 'negative');
}

// Show week results
function showWeekResults(prediction) {
    const weekResults = document.getElementById('week-results');
    weekResults.style.display = 'block';
    
    document.getElementById('week-min').textContent = prediction.min.toFixed(2);
    document.getElementById('week-avg').textContent = prediction.avg.toFixed(2);
    document.getElementById('week-max').textContent = prediction.max.toFixed(2);
    
    // Create chart
    const ctx = document.getElementById('week-chart').getContext('2d');
    
    // Destroy previous chart if exists
    if (weekChart) {
        weekChart.destroy();
    }
    
    weekChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'],
            datasets: [{
                label: 'Predicted Price ($)',
                data: prediction.daily,
                borderColor: 'rgb(255, 215, 0)',
                backgroundColor: 'rgba(255, 215, 0, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: '7-Day Price Forecast'
                },
                legend: {
                    display: true
                }
            },
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

// Show month results
function showMonthResults(prediction) {
    const monthResults = document.getElementById('month-results');
    monthResults.style.display = 'block';
    
    document.getElementById('month-min').textContent = prediction.min.toFixed(2);
    document.getElementById('month-avg').textContent = prediction.avg.toFixed(2);
    document.getElementById('month-max').textContent = prediction.max.toFixed(2);
    
    // Create chart
    const ctx = document.getElementById('month-chart').getContext('2d');
    
    // Destroy previous chart if exists
    if (monthChart) {
        monthChart.destroy();
    }
    
    monthChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            datasets: [{
                label: 'Average Weekly Price ($)',
                data: prediction.weekly_avg,
                borderColor: 'rgb(255, 140, 0)',
                backgroundColor: 'rgba(255, 140, 0, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Monthly Price Trend (Weekly Averages)'
                },
                legend: {
                    display: true
                }
            },
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

// Hide all results
function hideAllResults() {
    document.getElementById('day-results').style.display = 'none';
    document.getElementById('week-results').style.display = 'none';
    document.getElementById('month-results').style.display = 'none';
    document.getElementById('error-message').style.display = 'none';
}

// Show/hide loading
function showLoading() {
    document.getElementById('loading').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

// Show error
function showError(message) {
    const errorDiv = document.getElementById('error-message');
    document.getElementById('error-text').textContent = message;
    errorDiv.style.display = 'block';
    
    // Hide after 5 seconds
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}
