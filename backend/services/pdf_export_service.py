"""
Professional PDF Export Service for ILUMINATI SYSTEM
Bank-grade report templates with executive summaries and risk analysis
"""

import logging
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from jinja2 import Template, Environment, FileSystemLoader
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch
from weasyprint.text.fonts import FontConfiguration

from services.export_service import export_to_excel

logger = logging.getLogger(__name__)

class PDFExportService:
    """Professional PDF export service with bank-grade templates."""
    
    def __init__(self, template_dir: str = "templates/pdf"):
        self.template_dir = template_dir
        self.font_config = FontConfiguration()
        self.templates = self._load_templates()
        self.css_styles = self._get_professional_css()
    
    def _load_templates(self) -> Dict[str, Template]:
        """Load HTML templates for PDF generation."""
        try:
            env = Environment(loader=FileSystemLoader(self.template_dir))
            
            templates = {
                'executive_summary': env.get_template('executive_summary.html'),
                'company_profile': env.get_template('company_profile.html'),
                'network_analysis': env.get_template('network_analysis.html'),
                'risk_assessment': env.get_template('risk_assessment.html'),
                'comparative_analysis': env.get_template('comparative_analysis.html'),
                'dashboard_report': env.get_template('dashboard_report.html'),
            }
            
            logger.info(f"Loaded {len(templates)} PDF templates")
            return templates
            
        except Exception as e:
            logger.error(f"Failed to load templates: {e}")
            # Fallback to basic templates
            return self._create_fallback_templates()
    
    def _create_fallback_templates(self) -> Dict[str, Template]:
        """Create basic fallback templates."""
        basic_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{{ title }}</title>
        </head>
        <body>
            <h1>{{ title }}</h1>
            <p>Generated: {{ generated_at }}</p>
            <div>{{ content|safe }}</div>
        </body>
        </html>
        """
        
        return {
            'executive_summary': Template(basic_template),
            'company_profile': Template(basic_template),
            'network_analysis': Template(basic_template),
            'risk_assessment': Template(basic_template),
            'comparative_analysis': Template(basic_template),
            'dashboard_report': Template(basic_template),
        }
    
    def _get_professional_css(self) -> str:
        """Return professional CSS styling for PDF documents."""
        return """
            @page {
                size: A4;
                margin: 2cm;
                @top-center {
                    content: "ILUMINATI SYSTEM - Executive Intelligence";
                    font-family: "Playfair Display", serif;
                    font-size: 12pt;
                    color: #D4AF37;
                    border-bottom: 1px solid #D4AF37;
                    padding-bottom: 5px;
                }
                @bottom-center {
                    content: "Confidential - For Authorized Use Only | Page " counter(page) " of " counter(pages);
                    font-family: "Inter", sans-serif;
                    font-size: 8pt;
                    color: #666;
                }
            }
            
            body {
                font-family: "Inter", sans-serif;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 0;
                background: #ffffff;
            }
            
            h1, h2, h3, h4, h5, h6 {
                font-family: "Playfair Display", serif;
                color: #0B4EA2;
                margin-top: 0;
                margin-bottom: 1rem;
                line-height: 1.2;
            }
            
            h1 {
                font-size: 28pt;
                color: #D4AF37;
                border-bottom: 3px solid #D4AF37;
                padding-bottom: 15px;
                margin-bottom: 2rem;
            }
            
            h2 {
                font-size: 20pt;
                color: #0B4EA2;
                border-left: 4px solid #D4AF37;
                padding-left: 20px;
                margin-bottom: 1.5rem;
            }
            
            h3 {
                font-size: 16pt;
                color: #333;
                margin-bottom: 1rem;
            }
            
            .header {
                text-align: center;
                margin-bottom: 3rem;
                padding: 2rem;
                background: linear-gradient(135deg, #0A0A0A, #1A1A2E);
                color: white;
                border-radius: 8px;
                position: relative;
                overflow: hidden;
            }
            
            .header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: radial-gradient(circle, rgba(212, 175, 55, 0.1) 0%, transparent 70%);
                pointer-events: none;
            }
            
            .company-name {
                font-size: 32pt;
                font-weight: bold;
                color: #D4AF37;
                margin-bottom: 0.5rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            
            .report-meta {
                font-size: 12pt;
                color: #D1D5DB;
                margin-top: 1rem;
            }
            
            .risk-score {
                font-size: 60pt;
                font-weight: bold;
                color: #EF4444;
                margin: 1rem 0;
                text-align: center;
                background: #fff;
                padding: 1rem;
                border-radius: 50%;
                width: 120px;
                height: 120px;
                line-height: 120px;
                margin: 2rem auto;
                border: 4px solid #EF4444;
                box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
            }
            
            .risk-indicator {
                display: inline-block;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                background-color: #EF4444;
                margin-right: 8px;
            }
            
            .risk-level {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 10pt;
                font-weight: bold;
                text-transform: uppercase;
            }
            
            .risk-high { background: #fee2e2; color: #dc2626; }
            .risk-medium { background: #fef3c7; color: #d97706; }
            .risk-low { background: #ecfdf5; color: #059669; }
            
            .table-container {
                margin: 2rem 0;
                border: 1px solid #ddd;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .table {
                width: 100%;
                border-collapse: collapse;
                margin: 0;
            }
            
            .table th, .table td {
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
                vertical-align: top;
            }
            
            .table th {
                background-color: #f8fafc;
                font-weight: 600;
                color: #1e293b;
                font-family: "Inter", sans-serif;
            }
            
            .table tr:nth-child(even) {
                background-color: #f8fafc;
            }
            
            .table tr:hover {
                background-color: #e2e8f0;
            }
            
            .chart-container {
                width: 100%;
                height: 400px;
                margin: 2rem 0;
                border: 1px solid #ddd;
                border-radius: 8px;
                background: #fff;
                position: relative;
            }
            
            .summary-box {
                background: #f1f5f9;
                border-left: 4px solid #D4AF37;
                padding: 1.5rem;
                margin: 1.5rem 0;
                border-radius: 0 8px 8px 0;
            }
            
            .key-metrics {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
                margin: 2rem 0;
            }
            
            .metric-card {
                background: #fff;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 1.5rem;
                text-align: center;
            }
            
            .metric-value {
                font-size: 24pt;
                font-weight: bold;
                color: #1e293b;
                margin-bottom: 0.5rem;
            }
            
            .metric-label {
                font-size: 10pt;
                color: #64748b;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
            
            .footer-note {
                font-size: 8pt;
                color: #666;
                margin-top: 3rem;
                font-style: italic;
                border-top: 1px solid #ddd;
                padding-top: 1rem;
            }
            
            .signature {
                margin-top: 4rem;
                text-align: right;
                padding: 2rem;
                border-top: 1px solid #ddd;
            }
            
            .signature-line {
                width: 300px;
                height: 1px;
                background: #333;
                margin: 2rem auto 1rem;
            }
            
            .watermark {
                position: fixed;
                bottom: 0;
                right: 0;
                opacity: 0.05;
                font-size: 160pt;
                font-weight: bold;
                color: #D4AF37;
                transform: rotate(-45deg);
                pointer-events: none;
                z-index: -1;
            }
            
            .highlight {
                background: linear-gradient(120deg, #D4AF37, #E5E4E2);
                background-size: 100%;
                background-clip: text;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: bold;
            }
            
            .network-graph {
                width: 100%;
                height: 500px;
                border: 1px solid #ddd;
                border-radius: 8px;
                background: #f8fafc;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #64748b;
                font-style: italic;
            }
            
            .company-details {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1.5rem;
                margin: 2rem 0;
            }
            
            .detail-card {
                background: #fff;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 1.5rem;
            }
            
            .detail-label {
                font-size: 10pt;
                color: #64748b;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 0.5rem;
            }
            
            .detail-value {
                font-size: 14pt;
                font-weight: 600;
                color: #1e293b;
            }
        """
    
    def generate_executive_summary(
        self, 
        companies: List[Dict], 
        metadata: Dict,
        include_risk_analysis: bool = True,
        include_financials: bool = True
    ) -> bytes:
        """Generate executive summary PDF."""
        try:
            # Calculate summary statistics
            summary_stats = self._calculate_summary_statistics(companies)
            
            # Generate insights
            insights = self._generate_executive_insights(companies, summary_stats)
            
            html_content = self.templates['executive_summary'].render(
                companies=companies,
                metadata=metadata,
                summary_stats=summary_stats,
                insights=insights,
                generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                include_risk_analysis=include_risk_analysis,
                include_financials=include_financials
            )
            
            return self._render_pdf(html_content, 'executive_summary')
            
        except Exception as e:
            logger.error(f"Executive summary generation failed: {e}")
            raise
    
    def generate_company_profile(
        self, 
        company_data: Dict, 
        relationships: List[Dict],
        include_financials: bool = True,
        include_risk_factors: bool = True
    ) -> bytes:
        """Generate detailed company profile PDF."""
        try:
            # Calculate company risk factors
            risk_factors = self._calculate_company_risk_factors(company_data)
            
            # Generate company insights
            insights = self._generate_company_insights(company_data, relationships)
            
            html_content = self.templates['company_profile'].render(
                company=company_data,
                relationships=relationships,
                risk_factors=risk_factors,
                insights=insights,
                generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                include_financials=include_financials,
                include_risk_factors=include_risk_factors
            )
            
            return self._render_pdf(html_content, 'company_profile')
            
        except Exception as e:
            logger.error(f"Company profile generation failed: {e}")
            raise
    
    def generate_network_analysis(
        self, 
        graph_data: Dict, 
        insights: Dict,
        include_visualization: bool = True
    ) -> bytes:
        """Generate network analysis PDF with embedded graph."""
        try:
            # Analyze network topology
            network_analysis = self._analyze_network_topology(graph_data)
            
            html_content = self.templates['network_analysis'].render(
                graph_data=graph_data,
                insights=insights,
                network_analysis=network_analysis,
                generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                include_visualization=include_visualization
            )
            
            return self._render_pdf(html_content, 'network_analysis')
            
        except Exception as e:
            logger.error(f"Network analysis generation failed: {e}")
            raise
    
    def generate_risk_assessment(
        self, 
        companies: List[Dict], 
        risk_factors: Dict,
        include_recommendations: bool = True
    ) -> bytes:
        """Generate professional risk assessment PDF."""
        try:
            # Calculate comprehensive risk scores
            risk_scores = self._calculate_comprehensive_risk_scores(companies, risk_factors)
            
            # Generate risk recommendations
            recommendations = self._generate_risk_recommendations(risk_scores)
            
            html_content = self.templates['risk_assessment'].render(
                companies=companies,
                risk_factors=risk_factors,
                risk_scores=risk_scores,
                recommendations=recommendations,
                generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                include_recommendations=include_recommendations
            )
            
            return self._render_pdf(html_content, 'risk_assessment')
            
        except Exception as e:
            logger.error(f"Risk assessment generation failed: {e}")
            raise
    
    def generate_comparative_analysis(
        self, 
        companies: List[Dict],
        comparison_metrics: List[str],
        include_rankings: bool = True
    ) -> bytes:
        """Generate comparative analysis PDF."""
        try:
            # Perform comparative analysis
            comparison_results = self._perform_comparative_analysis(companies, comparison_metrics)
            
            html_content = self.templates['comparative_analysis'].render(
                companies=companies,
                comparison_results=comparison_results,
                comparison_metrics=comparison_metrics,
                generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                include_rankings=include_rankings
            )
            
            return self._render_pdf(html_content, 'comparative_analysis')
            
        except Exception as e:
            logger.error(f"Comparative analysis generation failed: {e}")
            raise
    
    def generate_dashboard_report(
        self,
        dashboard_data: Dict,
        include_charts: bool = True,
        include_tables: bool = True
    ) -> bytes:
        """Generate dashboard report PDF."""
        try:
            html_content = self.templates['dashboard_report'].render(
                dashboard_data=dashboard_data,
                generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                include_charts=include_charts,
                include_tables=include_tables
            )
            
            return self._render_pdf(html_content, 'dashboard_report')
            
        except Exception as e:
            logger.error(f"Dashboard report generation failed: {e}")
            raise
    
    def _render_pdf(self, html_content: str, document_type: str) -> bytes:
        """Render HTML content to PDF with professional styling."""
        try:
            # Create HTML document
            html = HTML(string=html_content, base_url='.')
            
            # Professional CSS styling
            css = CSS(string=self.css_styles, font_config=self.font_config)
            
            # Render PDF
            pdf_bytes = html.write_pdf(stylesheets=[css], font_config=self.font_config)
            
            logger.info(f"Generated {document_type} PDF: {len(pdf_bytes)} bytes")
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"PDF rendering failed: {e}")
            raise
    
    def _calculate_summary_statistics(self, companies: List[Dict]) -> Dict:
        """Calculate summary statistics for executive summary."""
        if not companies:
            return {
                'total_companies': 0,
                'average_risk_score': 0,
                'high_risk_companies': 0,
                'medium_risk_companies': 0,
                'low_risk_companies': 0,
                'countries': {},
                'legal_forms': {}
            }
        
        total_companies = len(companies)
        risk_scores = [c.get('risk_score', 0) for c in companies]
        average_risk = sum(risk_scores) / total_companies
        
        high_risk = len([c for c in companies if c.get('risk_score', 0) > 7])
        medium_risk = len([c for c in companies if 4 < c.get('risk_score', 0) <= 7])
        low_risk = len([c for c in companies if c.get('risk_score', 0) <= 4])
        
        # Country distribution
        countries = {}
        for company in companies:
            country = company.get('country', 'Unknown')
            countries[country] = countries.get(country, 0) + 1
        
        # Legal form distribution
        legal_forms = {}
        for company in companies:
            legal_form = company.get('legal_form', 'Unknown')
            legal_forms[legal_form] = legal_forms.get(legal_form, 0) + 1
        
        return {
            'total_companies': total_companies,
            'average_risk_score': round(average_risk, 2),
            'high_risk_companies': high_risk,
            'medium_risk_companies': medium_risk,
            'low_risk_companies': low_risk,
            'countries': countries,
            'legal_forms': legal_forms,
            'risk_distribution': {
                'high': round((high_risk / total_companies) * 100, 1),
                'medium': round((medium_risk / total_companies) * 100, 1),
                'low': round((low_risk / total_companies) * 100, 1)
            }
        }
    
    def _generate_executive_insights(self, companies: List[Dict], summary_stats: Dict) -> List[str]:
        """Generate executive insights based on data."""
        insights = []
        
        if summary_stats['average_risk_score'] > 6:
            insights.append("⚠️ High average risk score detected. Recommend immediate review of high-risk companies.")
        
        if summary_stats['risk_distribution']['high'] > 30:
            insights.append("📈 Elevated concentration of high-risk companies. Consider portfolio diversification.")
        
        if len(summary_stats['countries']) > 3:
            insights.append("🌍 Diversified geographic exposure across multiple countries.")
        
        # Add more insights based on data patterns
        return insights
    
    def _calculate_company_risk_factors(self, company_data: Dict) -> Dict:
        """Calculate detailed risk factors for a company."""
        risk_factors = {
            'financial_health': 'Unknown',
            'legal_risks': [],
            'operational_risks': [],
            'market_risks': [],
            'overall_risk_level': 'Unknown'
        }
        
        # Analyze financial data if available
        financial_data = company_data.get('financial_data', {})
        if financial_data:
            revenue = financial_data.get('revenue', 0)
            if revenue < 100000:
                risk_factors['financial_health'] = 'High Risk'
                risk_factors['financial_risks'] = ['Low revenue', 'Potential liquidity issues']
            elif revenue > 10000000:
                risk_factors['financial_health'] = 'Low Risk'
        
        # Analyze company status
        status = company_data.get('status', '').lower()
        if 'liquidation' in status or 'bankruptcy' in status:
            risk_factors['legal_risks'].append('Company in liquidation/bankruptcy')
            risk_factors['overall_risk_level'] = 'High Risk'
        
        # Analyze virtual seat
        if company_data.get('virtual_seat', False):
            risk_factors['operational_risks'].append('Virtual office address')
        
        return risk_factors
    
    def _generate_company_insights(self, company_data: Dict, relationships: List[Dict]) -> List[str]:
        """Generate insights for a specific company."""
        insights = []
        
        # Analyze relationships
        if len(relationships) > 10:
            insights.append("🔗 Extensive network connections. High influence in business ecosystem.")
        
        # Analyze risk score
        risk_score = company_data.get('risk_score', 0)
        if risk_score > 8:
            insights.append("⚠️ Very high risk score. Recommend thorough due diligence.")
        elif risk_score < 3:
            insights.append("✅ Low risk profile. Suitable for conservative investment strategies.")
        
        return insights
    
    def _analyze_network_topology(self, graph_data: Dict) -> Dict:
        """Analyze network topology and characteristics."""
        nodes = graph_data.get('nodes', [])
        edges = graph_data.get('edges', [])
        
        # Calculate basic metrics
        total_nodes = len(nodes)
        total_edges = len(edges)
        
        # Calculate connectivity
        if total_nodes > 0:
            avg_connectivity = total_edges / total_nodes
        else:
            avg_connectivity = 0
        
        # Identify central nodes
        node_connections = {}
        for edge in edges:
            source = edge.get('source')
            target = edge.get('target')
            node_connections[source] = node_connections.get(source, 0) + 1
            node_connections[target] = node_connections.get(target, 0) + 1
        
        # Find most connected nodes
        sorted_connections = sorted(node_connections.items(), key=lambda x: x[1], reverse=True)
        most_connected = sorted_connections[:5] if sorted_connections else []
        
        return {
            'total_nodes': total_nodes,
            'total_edges': total_edges,
            'avg_connectivity': round(avg_connectivity, 2),
            'most_connected_nodes': most_connected,
            'network_density': total_edges / (total_nodes * (total_nodes - 1) / 2) if total_nodes > 1 else 0,
            'centralization': 'High' if avg_connectivity > 5 else 'Medium' if avg_connectivity > 2 else 'Low'
        }
    
    def _calculate_comprehensive_risk_scores(self, companies: List[Dict], risk_factors: Dict) -> Dict:
        """Calculate comprehensive risk scores."""
        risk_scores = {}
        
        for company in companies:
            base_score = company.get('risk_score', 0)
            
            # Adjust based on risk factors
            adjustments = 0
            if risk_factors.get('financial_health') == 'High Risk':
                adjustments += 2
            if risk_factors.get('legal_risks'):
                adjustments += len(risk_factors['legal_risks'])
            if risk_factors.get('operational_risks'):
                adjustments += len(risk_factors['operational_risks']) * 0.5
            
            final_score = min(10, base_score + adjustments)
            risk_scores[company.get('identifier', '')] = {
                'base_score': base_score,
                'adjusted_score': round(final_score, 1),
                'risk_level': self._get_risk_level(final_score)
            }
        
        return risk_scores
    
    def _get_risk_level(self, score: float) -> str:
        """Get risk level based on score."""
        if score >= 8:
            return 'High Risk'
        elif score >= 5:
            return 'Medium Risk'
        else:
            return 'Low Risk'
    
    def _generate_risk_recommendations(self, risk_scores: Dict) -> List[str]:
        """Generate risk-based recommendations."""
        recommendations = []
        
        high_risk_count = len([score for score in risk_scores.values() if score['adjusted_score'] >= 8])
        medium_risk_count = len([score for score in risk_scores.values() if 5 <= score['adjusted_score'] < 8])
        
        if high_risk_count > 0:
            recommendations.append(f"🚨 {high_risk_count} companies classified as High Risk. Immediate review required.")
        
        if medium_risk_count > 5:
            recommendations.append("⚠️ Significant number of Medium Risk companies. Consider enhanced monitoring.")
        
        if high_risk_count == 0 and medium_risk_count == 0:
            recommendations.append("✅ Portfolio shows low risk profile. Continue standard monitoring.")
        
        return recommendations
    
    def _perform_comparative_analysis(self, companies: List[Dict], metrics: List[str]) -> Dict:
        """Perform comparative analysis across companies."""
        comparison_results = {}
        
        for metric in metrics:
            values = []
            for company in companies:
                value = company.get(metric)
                if value is not None:
                    values.append((company.get('name', ''), value))
            
            # Sort by value
            sorted_values = sorted(values, key=lambda x: x[1], reverse=True)
            comparison_results[metric] = sorted_values
        
        return comparison_results

# Global instance
_pdf_service = None

def get_pdf_service() -> PDFExportService:
    """Get singleton instance of PDFExportService."""
    global _pdf_service
    if _pdf_service is None:
        _pdf_service = PDFExportService()
    return _pdf_service