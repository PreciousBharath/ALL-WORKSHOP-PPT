"""
Prompt Engineering Studio - Plotly Visualization Engine
Generates interactive charts, radar graphs, bar charts, and treemaps
formatted with dark glassmorphism styling.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

class PromptVisualizer:
    """
    Renders high-quality Plotly visual charts for prompt analysis.
    """

    COLOR_PALETTE = {
        "primary": "#6366f1",
        "secondary": "#a855f7",
        "accent_pink": "#ec4899",
        "accent_cyan": "#06b6d4",
        "green": "#10b981",
        "red": "#ef4444",
        "amber": "#f59e0b",
        "bg": "#0f172a",
        "card_bg": "#1e293b",
        "text": "#f8fafc"
    }

    def __init__(self):
        pass

    def create_radar_chart(self, orig_metrics: dict, imp_metrics: dict) -> go.Figure:
        """Generates side-by-side radar (spider) chart comparing scores."""
        categories = ['Complexity', 'Specificity', 'Clarity', 'Quality']
        
        orig_values = [
            orig_metrics.get('complexity_score', 0),
            orig_metrics.get('specificity_score', 0),
            orig_metrics.get('clarity_score', 0),
            orig_metrics.get('quality_score', 0)
        ]
        
        imp_values = [
            imp_metrics.get('complexity_score', 0),
            imp_metrics.get('specificity_score', 0),
            imp_metrics.get('clarity_score', 0),
            imp_metrics.get('quality_score', 0)
        ]

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=orig_values + [orig_values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='Original Prompt',
            line_color=self.COLOR_PALETTE['red'],
            fillcolor='rgba(239, 68, 68, 0.25)'
        ))

        fig.add_trace(go.Scatterpolar(
            r=imp_values + [imp_values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='Improved Prompt',
            line_color=self.COLOR_PALETTE['green'],
            fillcolor='rgba(16, 185, 129, 0.35)'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], color=self.COLOR_PALETTE['text']),
                angularaxis=dict(color=self.COLOR_PALETTE['text']),
                bgcolor='rgba(15, 23, 42, 0.6)'
            ),
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=self.COLOR_PALETTE['text'], family="Outfit, sans-serif"),
            margin=dict(l=40, r=40, t=30, b=30),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        return fig

    def create_comparison_bar(self, orig_metrics: dict, imp_metrics: dict) -> go.Figure:
        """Generates grouped bar chart for words, characters, and tokens."""
        metrics_list = ['Words', 'Characters', 'Estimated Tokens']
        
        orig_vals = [
            orig_metrics.get('word_count', 0),
            orig_metrics.get('char_count', 0),
            orig_metrics.get('estimated_tokens', 0)
        ]
        
        imp_vals = [
            imp_metrics.get('word_count', 0),
            imp_metrics.get('char_count', 0),
            imp_metrics.get('estimated_tokens', 0)
        ]

        fig = go.Figure(data=[
            go.Bar(name='Original', x=metrics_list, y=orig_vals, marker_color=self.COLOR_PALETTE['accent_pink']),
            go.Bar(name='Improved', x=metrics_list, y=imp_vals, marker_color=self.COLOR_PALETTE['primary'])
        ])

        fig.update_layout(
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(15, 23, 42, 0.4)',
            font=dict(color=self.COLOR_PALETTE['text'], family="Inter, sans-serif"),
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        return fig

    def create_ascii_distribution(self, ascii_df: pd.DataFrame) -> go.Figure:
        """Generates histogram of ASCII decimal values."""
        if ascii_df.empty:
            return go.Figure()

        fig = px.histogram(
            ascii_df, 
            x="ASCII (Dec)", 
            color="Category",
            nbins=30,
            color_discrete_sequence=[
                self.COLOR_PALETTE['primary'],
                self.COLOR_PALETTE['secondary'],
                self.COLOR_PALETTE['accent_pink'],
                self.COLOR_PALETTE['green'],
                self.COLOR_PALETTE['amber']
            ]
        )

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(15, 23, 42, 0.4)',
            font=dict(color=self.COLOR_PALETTE['text'], family="Inter, sans-serif"),
            xaxis_title="ASCII Decimal Value",
            yaxis_title="Character Count",
            margin=dict(l=20, r=20, t=30, b=20)
        )
        return fig

    def create_token_length_distribution(self, token_df: pd.DataFrame) -> go.Figure:
        """Generates bar chart of token length distribution."""
        if token_df.empty or "Length" not in token_df.columns:
            return go.Figure()

        counts = token_df["Length"].value_counts().sort_index().reset_index()
        counts.columns = ["Length", "Count"]

        fig = px.bar(
            counts,
            x="Length",
            y="Count",
            labels={"Length": "Token Character Length", "Count": "Frequency"},
            color_discrete_sequence=[self.COLOR_PALETTE['accent_cyan']]
        )

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(15, 23, 42, 0.4)',
            font=dict(color=self.COLOR_PALETTE['text'], family="Inter, sans-serif"),
            margin=dict(l=20, r=20, t=30, b=20)
        )
        return fig

    def create_word_freq_treemap(self, text: str) -> go.Figure:
        """Generates a word frequency treemap."""
        import re
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        if not words:
            return go.Figure()

        freq_df = pd.Series(words).value_counts().head(20).reset_index()
        freq_df.columns = ["Word", "Frequency"]

        fig = px.treemap(
            freq_df,
            path=["Word"],
            values="Frequency",
            color="Frequency",
            color_continuous_scale="Purples"
        )

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=self.COLOR_PALETTE['text'], family="Outfit, sans-serif"),
            margin=dict(l=10, r=10, t=10, b=10)
        )
        return fig
