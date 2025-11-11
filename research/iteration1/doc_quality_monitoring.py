#!/usr/bin/env python3
"""
Documentation Quality Monitoring and Alerting System
Provides continuous monitoring, trend analysis, and alerting for documentation quality.
"""

import os
import json
import logging
import smtplib
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yaml

logger = logging.getLogger(__name__)


class Alert:
    """Represents an alert to be sent."""
    
    def __init__(self, name: str, severity: str, message: str, details: Dict):
        self.name = name
        self.severity = severity
        self.message = message
        self.details = details
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'severity': self.severity,
            'message': self.message,
            'details': self.details,
            'timestamp': self.timestamp
        }


class EmailAlerter:
    """Sends alerts via email."""
    
    def __init__(self, config: Dict):
        self.enabled = config.get('enabled', False)
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender = os.getenv('ALERT_EMAIL_SENDER')
        self.password = os.getenv('ALERT_EMAIL_PASSWORD')
        self.recipients = config.get('recipients', [])
    
    def send(self, alert: Alert) -> bool:
        """Send alert via email."""
        if not self.enabled or not all([self.sender, self.password, self.recipients]):
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender
            msg['To'] = ', '.join(self.recipients)
            msg['Subject'] = f"[{alert.severity.upper()}] {alert.name}"
            
            body = f"""
Documentation Quality Alert

Alert: {alert.name}
Severity: {alert.severity.upper()}
Time: {alert.timestamp}

{alert.message}

Details:
{json.dumps(alert.details, indent=2)}

---
Automated alert from Documentation Quality System
"""
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender, self.password)
                server.send_message(msg)
            
            logger.info(f"Email alert sent: {alert.name}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
            return False


class SlackAlerter:
    """Sends alerts to Slack."""
    
    def __init__(self, config: Dict):
        self.enabled = config.get('enabled', False)
        webhook_url = config.get('webhook_url', '')
        self.webhook_url = os.path.expandvars(webhook_url)  # Expand env vars
    
    def send(self, alert: Alert) -> bool:
        """Send alert to Slack."""
        if not self.enabled or not self.webhook_url:
            return False
        
        try:
            # Map severity to Slack colors
            colors = {
                'critical': '#ff0000',
                'high': '#ff6600',
                'medium': '#ffcc00',
                'low': '#00cc00'
            }
            
            payload = {
                'attachments': [{
                    'color': colors.get(alert.severity, '#cccccc'),
                    'title': alert.name,
                    'text': alert.message,
                    'fields': [
                        {'title': 'Severity', 'value': alert.severity.upper(), 'short': True},
                        {'title': 'Time', 'value': alert.timestamp, 'short': True}
                    ],
                    'footer': 'Documentation Quality System'
                }]
            }
            
            # Add detail fields
            for key, value in alert.details.items():
                payload['attachments'][0]['fields'].append({
                    'title': key.replace('_', ' ').title(),
                    'value': str(value),
                    'short': True
                })
            
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            
            logger.info(f"Slack alert sent: {alert.name}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send Slack alert: {e}")
            return False


class FileAlerter:
    """Logs alerts to a file."""
    
    def __init__(self, config: Dict):
        self.enabled = config.get('enabled', True)
        self.path = config.get('path', 'alerts.log')
    
    def send(self, alert: Alert) -> bool:
        """Log alert to file."""
        if not self.enabled:
            return False
        
        try:
            with open(self.path, 'a') as f:
                f.write(f"\n{'='*80}\n")
                f.write(f"[{alert.timestamp}] {alert.severity.upper()}: {alert.name}\n")
                f.write(f"{alert.message}\n")
                f.write(f"Details: {json.dumps(alert.details)}\n")
            
            logger.info(f"File alert logged: {alert.name}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to log alert to file: {e}")
            return False


class AlertManager:
    """Manages alerting across multiple channels."""
    
    def __init__(self, config: Dict):
        self.enabled = config.get('enabled', True)
        self.rules = config.get('rules', [])
        
        # Initialize alerters
        self.alerters = []
        for channel_config in config.get('channels', []):
            channel_type = channel_config.get('type')
            
            if channel_type == 'email':
                self.alerters.append(EmailAlerter(channel_config))
            elif channel_type == 'slack':
                self.alerters.append(SlackAlerter(channel_config))
            elif channel_type == 'file':
                self.alerters.append(FileAlerter(channel_config))
    
    def evaluate_rules(self, metrics: Dict[str, float]) -> List[Alert]:
        """Evaluate alert rules against current metrics."""
        if not self.enabled:
            return []
        
        alerts = []
        
        for rule in self.rules:
            name = rule.get('name')
            condition = rule.get('condition')
            severity = rule.get('severity', 'medium')
            message = rule.get('message', '')
            
            try:
                # Evaluate condition
                if self._evaluate_condition(condition, metrics):
                    alert = Alert(
                        name=name,
                        severity=severity,
                        message=message,
                        details=self._get_relevant_metrics(condition, metrics)
                    )
                    alerts.append(alert)
            
            except Exception as e:
                logger.error(f"Error evaluating rule '{name}': {e}")
        
        return alerts
    
    def send_alerts(self, alerts: List[Alert]):
        """Send alerts through all configured channels."""
        if not alerts:
            return
        
        logger.info(f"Sending {len(alerts)} alerts")
        
        for alert in alerts:
            for alerter in self.alerters:
                try:
                    alerter.send(alert)
                except Exception as e:
                    logger.error(f"Alert sending failed: {e}")
    
    @staticmethod
    def _evaluate_condition(condition: str, metrics: Dict[str, float]) -> bool:
        """Safely evaluate a condition string."""
        # Create safe evaluation context with only metrics
        safe_dict = {'__builtins__': {}}
        safe_dict.update(metrics)
        
        try:
            return eval(condition, safe_dict)
        except Exception as e:
            logger.error(f"Condition evaluation error: {e}")
            return False
    
    @staticmethod
    def _get_relevant_metrics(condition: str, metrics: Dict[str, float]) -> Dict:
        """Extract metrics mentioned in condition."""
        relevant = {}
        for key, value in metrics.items():
            if key in condition:
                relevant[key] = value
        return relevant


class DashboardGenerator:
    """Generates HTML dashboard for documentation quality metrics."""
    
    def __init__(self, config: Dict):
        self.enabled = config.get('enabled', True)
        self.output_path = config.get('output_path', 'dashboard.html')
    
    def generate(self, metrics: Dict, trends: Dict, issues: List) -> str:
        """Generate HTML dashboard."""
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentation Quality Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        header {{ 
            background: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #333; margin-bottom: 10px; }}
        .timestamp {{ color: #666; font-size: 14px; }}
        .grid {{ 
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .card h2 {{ 
            color: #333;
            font-size: 18px;
            margin-bottom: 15px;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }}
        .metric {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }}
        .metric:last-child {{ border-bottom: none; }}
        .metric-name {{ color: #666; }}
        .metric-value {{ 
            font-weight: bold;
            color: #333;
        }}
        .metric-value.good {{ color: #00cc00; }}
        .metric-value.warning {{ color: #ffcc00; }}
        .metric-value.danger {{ color: #ff0000; }}
        .trend {{
            display: inline-block;
            margin-left: 10px;
            font-size: 12px;
        }}
        .trend.improving {{ color: #00cc00; }}
        .trend.degrading {{ color: #ff0000; }}
        .issue {{
            padding: 15px;
            margin-bottom: 10px;
            border-left: 4px solid #ddd;
            background: #f9f9f9;
            border-radius: 4px;
        }}
        .issue.critical {{ border-left-color: #ff0000; }}
        .issue.high {{ border-left-color: #ff6600; }}
        .issue.medium {{ border-left-color: #ffcc00; }}
        .issue.low {{ border-left-color: #00cc00; }}
        .issue-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
        }}
        .issue-severity {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .issue-severity.critical {{ background: #ff0000; color: white; }}
        .issue-severity.high {{ background: #ff6600; color: white; }}
        .issue-severity.medium {{ background: #ffcc00; color: black; }}
        .issue-severity.low {{ background: #00cc00; color: white; }}
        .issue-description {{ color: #333; margin-top: 5px; }}
        .issue-file {{ color: #666; font-size: 13px; font-family: monospace; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Documentation Quality Dashboard</h1>
            <div class="timestamp">Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </header>
        
        <div class="grid">
            <div class="card">
                <h2>📈 Key Metrics</h2>
                {self._render_metrics(metrics)}
            </div>
            
            <div class="card">
                <h2>📉 Trends (30 days)</h2>
                {self._render_trends(trends)}
            </div>
            
            <div class="card">
                <h2>🎯 Quality Gates</h2>
                {self._render_quality_gates(metrics)}
            </div>
        </div>
        
        <div class="card">
            <h2>🚨 Open Issues ({len(issues)})</h2>
            {self._render_issues(issues)}
        </div>
    </div>
</body>
</html>
"""
        
        with open(self.output_path, 'w') as f:
            f.write(html)
        
        return self.output_path
    
    def _render_metrics(self, metrics: Dict) -> str:
        """Render metrics as HTML."""
        html_parts = []
        
        key_metrics = [
            ('total_issues', 'Total Issues'),
            ('critical_issues', 'Critical Issues'),
            ('auto_fixable_rate', 'Auto-fixable Rate'),
            ('issues_per_file', 'Issues per File')
        ]
        
        for key, label in key_metrics:
            if key in metrics:
                value = metrics[key]
                
                # Format value
                if key == 'auto_fixable_rate':
                    display_value = f"{value*100:.1f}%"
                else:
                    display_value = f"{value:.1f}"
                
                # Determine color class
                css_class = ""
                if key == 'critical_issues':
                    css_class = "good" if value == 0 else "danger"
                elif key == 'auto_fixable_rate':
                    css_class = "good" if value > 0.5 else "warning"
                
                html_parts.append(f"""
                <div class="metric">
                    <span class="metric-name">{label}</span>
                    <span class="metric-value {css_class}">{display_value}</span>
                </div>
                """)
        
        return ''.join(html_parts)
    
    def _render_trends(self, trends: Dict) -> str:
        """Render trends as HTML."""
        html_parts = []
        
        for metric_name, trend_data in trends.items():
            if isinstance(trend_data, dict) and 'trend' in trend_data:
                trend = trend_data['trend']
                change = trend_data.get('percent_change', 0)
                
                icon = "↓" if trend == 'improving' else "↑" if trend == 'degrading' else "→"
                css_class = 'improving' if trend == 'improving' else 'degrading'
                
                html_parts.append(f"""
                <div class="metric">
                    <span class="metric-name">{metric_name.replace('_', ' ').title()}</span>
                    <span class="trend {css_class}">{icon} {abs(change):.1f}%</span>
                </div>
                """)
        
        return ''.join(html_parts) if html_parts else "<p>Insufficient data</p>"
    
    def _render_quality_gates(self, metrics: Dict) -> str:
        """Render quality gate status."""
        gates = [
            ('critical_issues', 'No Critical Issues', 0),
            ('documentation_debt', 'Documentation Debt', 2),
            ('content_consistency_score', 'Consistency Score', 0.95)
        ]
        
        html_parts = []
        for key, label, target in gates:
            value = metrics.get(key, 0)
            
            if key == 'content_consistency_score':
                passing = value >= target
                display = f"{value:.2f} / {target:.2f}"
            else:
                passing = value <= target
                display = f"{value:.0f} / {target:.0f}"
            
            status = "✅ PASS" if passing else "❌ FAIL"
            css_class = "good" if passing else "danger"
            
            html_parts.append(f"""
            <div class="metric">
                <span class="metric-name">{label}</span>
                <span class="metric-value {css_class}">{status} ({display})</span>
            </div>
            """)
        
        return ''.join(html_parts)
    
    def _render_issues(self, issues: List) -> str:
        """Render issues list as HTML."""
        if not issues:
            return "<p>No open issues! 🎉</p>"
        
        # Sort by severity
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        sorted_issues = sorted(issues, key=lambda x: severity_order.get(x.severity, 999))
        
        html_parts = []
        for issue in sorted_issues[:20]:  # Show top 20
            html_parts.append(f"""
            <div class="issue {issue.severity}">
                <div class="issue-header">
                    <span class="issue-severity {issue.severity}">{issue.severity}</span>
                    <span class="issue-file">{issue.file_path}</span>
                </div>
                <div class="issue-description">{issue.description}</div>
            </div>
            """)
        
        if len(issues) > 20:
            html_parts.append(f"<p><em>...and {len(issues) - 20} more issues</em></p>")
        
        return ''.join(html_parts)


class MonitoringSystem:
    """Main monitoring and alerting orchestrator."""
    
    def __init__(self, config_path: str = "quality_config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        alert_config = self.config.get('alerts', {})
        self.alert_manager = AlertManager(alert_config)
        
        dashboard_config = self.config.get('reporting', {}).get('dashboard', {})
        self.dashboard = DashboardGenerator(dashboard_config)
    
    def monitor(self, metrics: Dict, trends: Dict, issues: List):
        """Run monitoring cycle."""
        logger.info("Running monitoring cycle")
        
        # Evaluate alert rules
        alerts = self.alert_manager.evaluate_rules(metrics)
        
        # Send any triggered alerts
        if alerts:
            self.alert_manager.send_alerts(alerts)
        
        # Generate dashboard
        if self.dashboard.enabled:
            dashboard_path = self.dashboard.generate(metrics, trends, issues)
            logger.info(f"Dashboard generated: {dashboard_path}")
        
        logger.info(f"Monitoring complete. {len(alerts)} alerts triggered.")


def main():
    """Run monitoring system."""
    import sys
    from doc_quality_automation import DocumentationQualityEngine, MetricsCollector
    
    config_path = sys.argv[1] if len(sys.argv) > 1 else "quality_config.yaml"
    
    # Initialize systems
    engine = DocumentationQualityEngine(config_path)
    monitoring = MonitoringSystem(config_path)
    
    try:
        # Collect current state
        issues = engine.db.get_open_issues()
        metrics = engine.collect_metrics()
        
        # Calculate trends
        trends = {}
        for metric_name in ['total_issues', 'critical_issues', 'high_issues']:
            trends[metric_name] = engine.metrics_collector.calculate_trends(metric_name)
        
        # Run monitoring
        monitoring.monitor(metrics, trends, issues)
        
        print("✅ Monitoring cycle complete")
    
    finally:
        engine.close()


if __name__ == '__main__':
    main()
