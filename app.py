
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import time
import json
from pydantic import BaseModel

from tools.extractor_tool import Extractor_Tool
from tools.fetcher_tool import Fetcher_Tool
from tools.analyzer_tool import Analyzer_Tool
from tools.predictor_tool import Predictor_Tool


# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="ProductPulse AI",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
<style>
    .success-box {
        background: #d4edda;
        border: 2px solid #c3e6cb;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .danger-box {
        background: #f8d7da;
        border: 2px solid #f5c6cb;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .wait-box {
        background: #C9A185;
        border: 2px solid #ffeaa7;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .info-box {
        background: #3F704D;
        border: 2px solid #bee5eb;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .step-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border: 1px solid #667eea30;
        padding: 1rem;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def safe_get(obj, key, default=None):
    """Safely get attribute from Pydantic model or dict"""
    if isinstance(obj, BaseModel):
        return getattr(obj, key, default)
    elif isinstance(obj, dict):
        return obj.get(key, default)
    else:
        return default


def format_price(price):
    """Format price with currency symbol"""
    if price is None:
        return "N/A"
    return f"${price:,.2f}"


def format_percentage(value):
    """Format percentage value"""
    if value is None:
        return "N/A"
    return f"{value:.1f}%"


# ============================================================================
# PIPELINE EXECUTION
# ============================================================================

def run_analysis_pipeline(product_input: str):
    """Run all tools sequentially"""
    
    # Step 1: Extract
    extractor = Extractor_Tool()
    extractor_output = extractor.run(product_input)
    
    # Step 2: Fetch (ensure required fields)
    required_fields = {
        'product_name': None, 'brand': None, 'model': None, 'category': None,
        'attributes': {}, 'condition': None, 'market_region': None,
        'currency': 'USD', 'additional_context': None,
        'search_keywords': [], 'input_confidence': 0.0
    }
    complete_product_info = {**required_fields, **extractor_output}
    
    fetcher = Fetcher_Tool()
    fetcher_output = fetcher.run({"product_info": complete_product_info})
    
    # Step 3: Analyze
    analyzer = Analyzer_Tool()
    analyzer_output = analyzer.run({"fetched_product_info": fetcher_output})
    
    # Step 4: Predict
    predictor = Predictor_Tool()
    predictor_output = predictor.run({"analyzer_output": analyzer_output})
    
    return {
        "extractor": extractor_output,
        "fetcher": fetcher_output,
        "analyzer": analyzer_output,
        "predictor": predictor_output
    }


# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def create_price_chart(fetcher_data):
    """Price comparison bar chart"""
    prices = [
        safe_get(fetcher_data, 'lowest_price', 0),
        safe_get(fetcher_data, 'current_price', 0),
        safe_get(fetcher_data, 'average_price', 0),
        safe_get(fetcher_data, 'highest_price', 0)
    ]
    labels = ['Lowest', 'Current', 'Average', 'Highest']
    colors = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444']
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=labels, y=prices, marker_color=colors,
        text=[f'${p:,.2f}' for p in prices],
        textposition='outside',
        textfont=dict(size=14, color='black', family='Arial Black')
    ))
    
    fig.update_layout(
        title={'text': 'Price Comparison Analysis', 'x': 0.5, 'xanchor': 'center'},
        yaxis_title='Price (USD)', height=450, showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig


def create_distribution_chart(fetcher_data):
    """Price distribution chart"""
    price_dist = safe_get(fetcher_data, 'price_distribution', [])
    if not price_dist:
        return None
    
    sellers = [safe_get(d, 'seller', 'Unknown') for d in price_dist]
    prices = [safe_get(d, 'price', 0) for d in price_dist]
    
    fig = go.Figure(data=[go.Bar(
        x=sellers, y=prices, marker_color='#667eea',
        text=[f'${p:,.2f}' for p in prices],
        textposition='outside'
    )])
    
    fig.update_layout(
        title={'text': 'Price Distribution Across Sellers', 'x': 0.5},
        xaxis_title='Seller', yaxis_title='Price (USD)', height=450,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig


def create_gauge_chart(confidence):
    """Confidence gauge"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence * 100,
        title={'text': "Confidence Score", 'font': {'size': 24}},
        number={'suffix': "%", 'font': {'size': 40}},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "#667eea"},
            'steps': [
                {'range': [0, 50], 'color': '#fee2e2'},
                {'range': [50, 75], 'color': '#fef3c7'},
                {'range': [75, 100], 'color': '#d1fae5'}
            ]
        }
    ))
    fig.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20))
    return fig


# ============================================================================
# MAIN APP
# ============================================================================

if "show_balloons" not in st.session_state:
    st.session_state.show_balloons = False


def main():
    # Session state
    if 'results' not in st.session_state:
        st.session_state.results = None
    
    # Header
    st.markdown("""
        <h1 style='text-align:center; font-weight:700;'>🛒 ProductPulse AI</h1>
        <p style='text-align:center; color:#9aa0a6; font-size:1.1rem;'>
        AI-powered market intelligence for confident buying decisions
        </p>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ System Info")
        st.info("This system uses multiple AI-powered tools to analyze products and deliver data-driven buying recommendations.")
        
        st.markdown("---")
        st.header("📊 Pipeline Steps")
        st.markdown("""
        **Step 1: Extractor** 🔍  
        Parse product details from natural language
        
        **Step 2: Fetcher** 📊  
        Gather real-time market pricing data
        
        **Step 3: Analyzer** 🧠  
        Comprehensive market trend analysis
        
        **Step 4: Predictor** 🎯  
        ML-based buy/no-buy prediction
        """)
        
        st.markdown("---")
        if st.button("🗑️ Clear Results", use_container_width=True):
            st.session_state.results = None
            st.rerun()
    
    # Input Section
    st.markdown("## 🔍 Product Information")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.markdown("**Quick Examples:**")
        examples = {
            "📱 iPhone": "iPhone 15 Pro 256GB new, US market",
            "💻 Laptop": "HP Pavilion 15 laptop with Ryzen 5, 8GB RAM, 512GB SSD, new condition, buying in India",
            "🎧 Headphones": "Bose QuietComfort Ultra headphones, wireless, active noise cancellation, new, buying in the US market"

        }
        selected = st.selectbox("Choose:", ["Custom"] + list(examples.keys()), label_visibility="collapsed")
    
    with col1:
        default = examples.get(selected, "") if selected != "Custom" else ""
        product_input = st.text_area(
            "**Describe the product:**",
            value=default,
            placeholder="e.g., iPhone 15 Pro 256GB in good condition, US market",
            height=100
        )
    
    # Analyze button
    if st.button("🚀 Analyze Product", type="primary", disabled=not product_input):
        st.markdown("---")
        st.markdown("## 📈 Analysis Progress")
        
        progress_bar = st.progress(0)
        status = st.empty()
        
        steps = [
            ("🔍 Extractor", "Parsing...", 0.25),
            ("📊 Fetcher", "Gathering data...", 0.50),
            ("🧠 Analyzer", "Analyzing...", 0.75),
            ("🎯 Predictor", "Predicting...", 1.0)
        ]
        
        try:
            for icon, desc, prog in steps:
                status.markdown(f'<div class="step-container"><h3>{icon} {desc}</h3></div>', unsafe_allow_html=True)
                progress_bar.progress(prog)
                time.sleep(0.3)
            
            with st.spinner("🤖 Running analysis..."):
                results = run_analysis_pipeline(product_input)
            
            status.success("✅ Analysis complete!")
            st.session_state.results = results
            st.session_state.show_balloons = True
            st.rerun()

            
        except Exception as e:
            status.error(f"❌ Failed: {str(e)}")
            st.exception(e)
            return
    
    if st.session_state.get("show_balloons", False):
        st.balloons()
        st.session_state.show_balloons = False
    
    # Display Results
    if st.session_state.results:
        results = st.session_state.results
        extractor = results['extractor']
        fetcher = results['fetcher']
        analyzer = results['analyzer']
        predictor = results['predictor']
        
        st.markdown("---")
        st.markdown("## 📊 Analysis Results")
        
        # Product Info
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📦 Product", safe_get(extractor, 'product_name', 'N/A'))
        col2.metric("🏷️ Brand", safe_get(extractor, 'brand', 'N/A'))
        col3.metric("✨ Condition", safe_get(extractor, 'condition', 'N/A'))
   
        
        st.markdown("---")
        
        # Pricing
        st.markdown("### 💰 Market Pricing")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        current = safe_get(fetcher, 'current_price', 0)
        average = safe_get(fetcher, 'average_price', 0)
        
        col1.metric("💵 Current", format_price(current))
        col2.metric("📊 Average", format_price(average), f"{current-average:,.2f}", delta_color="inverse")
        col3.metric("⬇️ Lowest", format_price(safe_get(fetcher, 'lowest_price', 0)))
        col4.metric("⬆️ Highest", format_price(safe_get(fetcher, 'highest_price', 0)))
        col5.metric("🏪 Sellers", safe_get(fetcher, 'seller_count', 0))
        
        # Charts
        st.markdown("---")
        st.markdown("### 📈 Visual Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_price_chart(fetcher), use_container_width=True)
        with col2:
            chart = create_distribution_chart(fetcher)
            if chart:
                st.plotly_chart(chart, use_container_width=True)
            else:
                st.info("📊 Distribution data unavailable")
        
        st.markdown("---")
        
        # Analysis Summary
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📝 Analysis Summary")
            summary = safe_get(analyzer, 'summary', None)
            if summary:
                st.markdown(f"**{safe_get(summary, 'headline', 'N/A')}**")
                st.markdown(f"*{safe_get(summary, 'short_explanation', '')}*")
                
                points = safe_get(summary, 'key_points', [])
                if points:
                    st.markdown("**Key Points:**")
                    for i, p in enumerate(points, 1):
                        st.markdown(f"{i}. {p}")
            
            st.markdown("---")
            
            # Best Offer
            st.markdown("### 🏆 Best Offer")
            best = safe_get(analyzer, 'best_offer', None)
            if best:
                st.success(f"""
                **💰 Price:** {format_price(safe_get(best, 'price', 0))}  
                **🏪 Seller:** {safe_get(best, 'seller', 'N/A')}  
                **✨ Condition:** {safe_get(best, 'condition', 'N/A')}  
                **⭐ Confidence:** {safe_get(best, 'seller_confidence', 0):.0%}
                """)
        
        with col2:
            conf = safe_get(predictor, 'confidence', 0)
            st.plotly_chart(create_gauge_chart(conf), use_container_width=True)
            
            st.markdown("**Price Evaluation:**")
            price_eval = safe_get(analyzer, 'price_evaluation', None)
            if price_eval:
                st.metric("Gap", format_percentage(safe_get(price_eval, 'price_gap_percent', 0)))
                st.metric("Position", safe_get(price_eval, 'price_position', 'N/A'))
        
        st.markdown("---")
        
        # Final Decision
        decision = safe_get(predictor, 'final_decision', 'UNKNOWN')
        conf = safe_get(predictor, 'confidence', 0)
        reasoning = safe_get(predictor, 'llm_reasoning', ['No reasoning'])
        
        st.markdown("### 🎯 Final Recommendation")
        
        if decision == "BUY":
            st.markdown(f"""
            <div class="success-box">
                <h2 style="color: #155724; margin: 0;">✅ RECOMMENDATION: BUY</h2>
                <h3 style="color: #155724;">Confidence: {conf*100:.1f}%</h3>
                <p><strong>Reasoning:</strong></p>
                <ul>{''.join([f'<li>{r}</li>' for r in reasoning])}</ul>
            </div>
            """, unsafe_allow_html=True)
        elif decision == "WAIT":
            st.markdown(f"""
            <div class="wait-box">
                <h2 style="color: #856404; margin: 0;">⏳ RECOMMENDATION: WAIT</h2>
                <h3 style="color: #856404;">Confidence: {conf*100:.1f}%</h3>
                <p><strong>Reasoning:</strong></p>
                <ul>{''.join([f'<li>{r}</li>' for r in reasoning])}</ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="danger-box">
                <h2 style="color: #721c24; margin: 0;">❌ RECOMMENDATION: DON'T BUY</h2>
                <h3 style="color: #721c24;">Confidence: {conf*100:.1f}%</h3>
                <p><strong>Reasoning:</strong></p>
                <ul>{''.join([f'<li>{r}</li>' for r in reasoning])}</ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Features
        st.markdown("---")
        st.markdown("### 📊 Feature Analysis")
        features = safe_get(predictor, 'feature_snapshot', {})
        
        col1, col2, col3 = st.columns(3)
        col1.metric("💹 Price Gap", format_percentage(safe_get(features, 'price_gap_percent', 0)))
        col1.metric("📉 Volatility", f"{safe_get(features, 'volatility_score', 0):.2f}")
        col2.metric("📊 Spread", format_percentage(safe_get(features, 'price_spread_percent', 0)))
        col2.metric("🏪 Competition", f"{safe_get(features, 'competition_score', 0):.2f}")
        col3.metric("🔢 Sellers", safe_get(features, 'seller_count', 0))
        col3.metric("🎯 Confidence", f"{safe_get(features, 'confidence_score', 0):.2f}")
        
        # Risks
        risks = safe_get(analyzer, 'risks_and_warnings', [])
        if risks:
            st.markdown("---")
            st.markdown("### ⚠️ Risks & Warnings")
            for i, risk in enumerate(risks, 1):
                st.warning(f"**{i}.** {risk}")
        
        # Market Analysis
        st.markdown("---")
        st.markdown("### 📈 Market Analysis")
        market = safe_get(analyzer, 'market_analysis', None)
        
        if market:
            col1, col2, col3, col4 = st.columns(4)
            col1.markdown(f"""<div class="info-box"><h4>🏪 Competition</h4><h3>{safe_get(market, 'competition_level', 'N/A')}</h3></div>""", unsafe_allow_html=True)
            col2.markdown(f"""<div class="info-box"><h4>📊 Pricing</h4><h3>{safe_get(market, 'pricing_health', 'N/A')}</h3></div>""", unsafe_allow_html=True)
            col3.markdown(f"""<div class="info-box"><h4>📈 Spread</h4><h3>{format_percentage(safe_get(market, 'price_spread_percent', 0))}</h3></div>""", unsafe_allow_html=True)
            col4.markdown(f"""<div class="info-box"><h4>🔢 Sellers</h4><h3>{safe_get(market, 'seller_count', 0)}</h3></div>""", unsafe_allow_html=True)
        
        # Download
        st.markdown("---")
        json_str = json.dumps(results, indent=2, default=str)
        st.download_button(
            "📥 Download Full Report (JSON)",
            json_str,
            f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "application/json"
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>Powered by AI | Made with ❤️ for smart shopping</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()