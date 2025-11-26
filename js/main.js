/**
 * Load data from JSON file
 */
async function loadData() {
    try {
        const response = await fetch('./data/hotel_analysis_results.json');
        const data = await response.json();
        return data;
    } catch (error) {
        console.warn('Données JSON non disponibles, utilisation des données mockées');
        return {};
    }
}

/**
 * Display KPIs
 */
function displayKPIs(data) {
    const container = document.getElementById('kpiContainer');
    container.innerHTML = '';
    
    const profitMargin = ((data.overview.avg_profit / data.overview.avg_revenue) * 100).toFixed(1);
    
    const kpis = [
        {
            label: i18n.t('kpis.revenue.label'),
            value: `${data.overview.avg_revenue.toLocaleString('fr-FR')}€`,
            subtext: i18n.t('kpis.revenue.subtext')
        },
        {
            label: i18n.t('kpis.profit.label'),
            value: `${data.overview.avg_profit.toLocaleString('fr-FR')}€`,
            subtext: `${profitMargin}% ${i18n.t('kpis.profit.subtext')}`
        },
        {
            label: i18n.createTooltip(i18n.t('kpis.occupancy.label'), 'tooltips.occupancy'),
            value: `${data.overview.avg_occupancy.toFixed(1)}%`,
            subtext: i18n.t('kpis.occupancy.subtext')
        },
        {
            label: i18n.createTooltip(i18n.t('kpis.adr.label'), 'tooltips.adr'),
            value: `${data.overview.avg_adr.toFixed(2)}€`,
            subtext: i18n.t('kpis.adr.subtext')
        },
        {
            label: i18n.createTooltip(i18n.t('kpis.revpar.label'), 'tooltips.revpar'),
            value: `${data.overview.avg_revpar.toFixed(2)}€`,
            subtext: i18n.t('kpis.revpar.subtext')
        },
        {
            label: i18n.t('kpis.cancellation.label'),
            value: `${data.overview.avg_cancellation_rate.toFixed(1)}%`,
            subtext: i18n.t('kpis.cancellation.subtext')
        }
    ];
    
    kpis.forEach(kpi => {
        const card = document.createElement('div');
        card.className = 'kpi-card';
        card.innerHTML = `
            <div class="kpi-label">${kpi.label}</div>
            <div class="kpi-value">${kpi.value}</div>
            <div class="kpi-subtext">${kpi.subtext}</div>
        `;
        container.appendChild(card);
    });
}

/**
 * Display Business Insights 
 */
function displayInsights(data) {
    const container = document.getElementById('insightsContainer');
    container.innerHTML = '';
    
    const profitMargin = ((data.overview.avg_profit / data.overview.avg_revenue) * 100).toFixed(1);
    const bestSeason = data.seasonal_performance[0];
    const bestChannel = data.booking_channels[0];
    
    const insights = [
        {
            type: 'success',
            title: i18n.t('insights.performance.title'),
            message: i18n.t('insights.performance.message', {
                revenue: data.overview.avg_revenue.toLocaleString('fr-FR'),
                profit: data.overview.avg_profit.toLocaleString('fr-FR')
            }),
            metric: i18n.t('insights.performance.metric', { margin: profitMargin })
        },
        {
            type: 'info',
            title: i18n.t('insights.occupancy.title'),
            message: i18n.t('insights.occupancy.message', {
                rate: data.overview.avg_occupancy.toFixed(1)
            }),
            metric: i18n.t('insights.occupancy.metric')
        },
        {
            type: 'success',
            title: i18n.t('insights.seasonality.title'),
            message: i18n.t('insights.seasonality.message', {
                season: bestSeason.season,
                revenue: bestSeason.avg_revenue.toLocaleString('fr-FR')
            }),
            metric: i18n.t('insights.seasonality.metric', {
                profit: bestSeason.avg_profit.toLocaleString('fr-FR')
            })
        },
        {
            type: 'info',
            title: i18n.t('insights.channel.title'),
            message: i18n.t('insights.channel.message', {
                channel: bestChannel.channel,
                rate: bestChannel.avg_cancellation_rate.toFixed(1)
            }),
            metric: i18n.t('insights.channel.metric', {
                bookings: bestChannel.total_bookings
            })
        },
        {
            type: 'warning',
            title: i18n.t('insights.segment.title'),
            message: i18n.t('insights.segment.message', {
                rate: data.guest_types[0].avg_cancellation_rate.toFixed(1)
            }),
            metric: i18n.t('insights.segment.metric')
        }
    ];
    
    insights.forEach(insight => {
        const card = document.createElement('div');
        card.className = `insight-card ${insight.type}`;
        card.innerHTML = `
            <div class="insight-title">${insight.title}</div>
            <div class="insight-message">${insight.message}</div>
            <span class="insight-metric">${insight.metric}</span>
        `;
        container.appendChild(card);
    });
}

/**
 * Display recommandations
 */
function displayRecommendations() {
    const container = document.getElementById('recommendationsContainer');
    container.innerHTML = '';
    
    const recommendations = [
        {
            priority: 'high',
            category: i18n.t('recommendations.categories.revenue_management'),
            title: i18n.t('recommendations.items.dynamic_pricing.title'),
            impact: i18n.t('recommendations.items.dynamic_pricing.impact'),
            actions: i18n.t('recommendations.items.dynamic_pricing.actions')
        },
        {
            priority: 'high',
            category: i18n.t('recommendations.categories.cancellation'),
            title: i18n.t('recommendations.items.reduce_cancellation.title'),
            impact: i18n.t('recommendations.items.reduce_cancellation.impact'),
            actions: i18n.t('recommendations.items.reduce_cancellation.actions')
        },
        {
            priority: 'medium',
            category: i18n.t('recommendations.categories.marketing'),
            title: i18n.t('recommendations.items.optimize_marketing.title'),
            impact: i18n.t('recommendations.items.optimize_marketing.impact'),
            actions: i18n.t('recommendations.items.optimize_marketing.actions')
        },
        {
            priority: 'medium',
            category: i18n.t('recommendations.categories.mix'),
            title: i18n.t('recommendations.items.rebalance_mix.title'),
            impact: i18n.t('recommendations.items.rebalance_mix.impact'),
            actions: i18n.t('recommendations.items.rebalance_mix.actions')
        }
    ];
    
    recommendations.forEach(rec => {
        const card = document.createElement('div');
        card.className = 'recommendation-card';
        
        const actionsHTML = Array.isArray(rec.actions) 
            ? rec.actions.map(action => `<li>${action}</li>`).join('')
            : '';
        
        const priorityLabel = i18n.t(`recommendations.priority.${rec.priority}`);
        
        card.innerHTML = `
            <span class="rec-priority ${rec.priority}">${priorityLabel}</span>
            <div class="rec-category">${rec.category}</div>
            <div class="rec-title">${rec.title}</div>
            <div class="rec-impact">💰 ${rec.impact}</div>
            <div class="rec-actions">
                <strong>${i18n.getCurrentLang() === 'fr' ? 'Actions recommandées:' : 'Recommended actions:'}</strong>
                <ul>${actionsHTML}</ul>
            </div>
        `;
        container.appendChild(card);
    });
}

/**
 * Switch language
 */
function switchLanguage(lang) {
    i18n.setLanguage(lang);
    displayKPIs(analysisData);
    displayInsights(analysisData);
    displayRecommendations();
    chartsManager.updateAll(analysisData);
}


async function init() {
    console.log('🏨 Dashboard Initialization...');
    

    await i18n.loadTranslations();
    console.log('✓ Translations loaded');
    
    const data = await loadData();
    
    i18n.updateUI();
    displayKPIs(data);
    chartsManager.createAll(data);
    displayInsights(data);
    displayRecommendations();
    
    console.log('✓ Dashboard initialized successfully!');
}

document.addEventListener('DOMContentLoaded', init);