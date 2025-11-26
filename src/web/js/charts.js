/**
 * charts.js
 */

class ChartsManager {
    constructor() {
        this.charts = {};
    }

    /**
     * Remove all existing charts
     */
    destroyAll() {
        Object.values(this.charts).forEach(chart => {
            if (chart) chart.destroy();
        });
        this.charts = {};
    }

    /**
     * Regenerate all charts (useful when changing language)
     */
    updateAll(data) {
        this.destroyAll();
        this.createAll(data);
    }

    /**
     * Create all charts
     */
    createAll(data) {
        this.charts.monthlyRevenue = this.createMonthlyRevenueChart(data);
        this.charts.occupancy = this.createOccupancyChart(data);
        this.charts.seasonal = this.createSeasonalChart(data);
        this.charts.channels = this.createChannelsChart(data);
        this.charts.guestTypes = this.createGuestTypesChart(data);
        this.charts.cancellation = this.createCancellationChart(data);
    }

    /**
     * Monthly Revenue Chart
     */
    createMonthlyRevenueChart(data) {
        const ctx = document.getElementById('monthlyRevenueChart').getContext('2d');
        const monthNames = i18n.getMonthNames();
        
        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.monthly_trends.map(d => monthNames[d.month - 1]),
                datasets: [{
                    label: i18n.t('chart_labels.revenue'),
                    data: data.monthly_trends.map(d => d.avg_revenue),
                    backgroundColor: 'rgba(102, 126, 234, 0.8)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: true }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        ticks: {
                            callback: function(value) {
                                return value.toLocaleString('fr-FR') + '€';
                            }
                        }
                    }
                }
            }
        });
    }

    /**
     * Occupancy Rate Chart
     */
    createOccupancyChart(data) {
        const ctx = document.getElementById('occupancyChart').getContext('2d');
        const monthNames = i18n.getMonthNames();
        
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.monthly_trends.map(d => monthNames[d.month - 1]),
                datasets: [{
                    label: i18n.t('chart_labels.occupancy'),
                    data: data.monthly_trends.map(d => d.avg_occupancy),
                    backgroundColor: 'rgba(23, 162, 184, 0.2)',
                    borderColor: 'rgba(23, 162, 184, 1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: true }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        min: 75,
                        max: 80,
                        ticks: {
                            callback: function(value) {
                                return value.toFixed(1) + '%';
                            }
                        }
                    }
                }
            }
        });
    }

    /**
     * Season Chart
     */
    createSeasonalChart(data) {
        const ctx = document.getElementById('seasonalChart').getContext('2d');
        
        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.seasonal_performance.map(d => d.season),
                datasets: [
                    {
                        label: i18n.t('chart_labels.revenue'),
                        data: data.seasonal_performance.map(d => d.avg_revenue),
                        backgroundColor: 'rgba(102, 126, 234, 0.8)',
                        yAxisID: 'y'
                    },
                    {
                        label: i18n.t('chart_labels.profit'),
                        data: data.seasonal_performance.map(d => d.avg_profit),
                        backgroundColor: 'rgba(40, 167, 69, 0.8)',
                        yAxisID: 'y'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        type: 'linear',
                        position: 'left',
                        ticks: {
                            callback: function(value) {
                                return value.toLocaleString('fr-FR') + '€';
                            }
                        }
                    }
                }
            }
        });
    }

    /**
     * Booking channels chart
     */
    createChannelsChart(data) {
        const ctx = document.getElementById('channelsChart').getContext('2d');
        
        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.booking_channels.map(d => d.channel),
                datasets: [
                    {
                        label: i18n.t('chart_labels.revenue'),
                        data: data.booking_channels.map(d => d.avg_revenue),
                        backgroundColor: 'rgba(102, 126, 234, 0.8)',
                        yAxisID: 'y'
                    },
                    {
                        label: i18n.t('chart_labels.bookings'),
                        data: data.booking_channels.map(d => d.total_bookings),
                        backgroundColor: 'rgba(255, 193, 7, 0.8)',
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        type: 'linear',
                        position: 'left'
                    },
                    y1: {
                        type: 'linear',
                        position: 'right',
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }
        });
    }

    /**
     * Guest types chart
     */
    createGuestTypesChart(data) {
        const ctx = document.getElementById('guestTypesChart').getContext('2d');
        
        return new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.guest_types.map(d => d.guest_type),
                datasets: [{
                    label: i18n.t('chart_labels.bookings'),
                    data: data.guest_types.map(d => d.total_bookings),
                    backgroundColor: [
                        'rgba(102, 126, 234, 0.8)',
                        'rgba(118, 75, 162, 0.8)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    /**
     * Cancellations chart
     */
    createCancellationChart(data) {
        const ctx = document.getElementById('cancellationChart').getContext('2d');
        
        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.booking_channels.map(d => d.channel),
                datasets: [{
                    label: i18n.t('chart_labels.cancellation'),
                    data: data.booking_channels.map(d => d.avg_cancellation_rate),
                    backgroundColor: [
                        'rgba(220, 53, 69, 0.8)',
                        'rgba(40, 167, 69, 0.8)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                indexAxis: 'y',
                scales: {
                    x: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    }
}

const chartsManager = new ChartsManager();