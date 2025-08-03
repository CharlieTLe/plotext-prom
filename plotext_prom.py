#!/usr/bin/env python3
"""
Plotext-Prometheus: Graph Prometheus metrics in your terminal using plotext
"""

import time
import sys
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional, Tuple
import requests
import plotext as plt
import click
import yaml
import json


class PrometheusClient:
    """Client for querying Prometheus metrics"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        
    def query(self, query: str) -> Dict[str, Any]:
        """Execute a Prometheus query and return results"""
        url = f"{self.base_url}/api/v1/query"
        params = {'query': query}
        
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to query Prometheus: {e}")
    
    def query_range(self, query: str, start: str, end: str, step: str = '15s') -> Dict[str, Any]:
        """Execute a Prometheus range query"""
        url = f"{self.base_url}/api/v1/query_range"
        params = {
            'query': query,
            'start': start,
            'end': end,
            'step': step
        }
        
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to query Prometheus range: {e}")


class MetricVisualizer:
    """Visualize Prometheus metrics using plotext"""
    
    def __init__(self, width: int = 120, height: int = 30):
        self.width = width
        self.height = height
        
    def plot_time_series(self, data: Dict[str, Any], title: str = "Prometheus Metrics"):
        """Plot time series data from Prometheus"""
        plt.clear_figure()
        plt.plotsize(self.width, self.height)
        
        if data['status'] != 'success':
            print(f"Error: {data.get('error', 'Unknown error')}")
            return
            
        result = data['data']['result']
        if not result:
            print("No data returned from query")
            return
            
        # Plot each series
        for i, series in enumerate(result):
            values = series['values']
            if not values:
                continue
                
            # Extract timestamps and values
            timestamps = [float(val[0]) for val in values]
            metric_values = [float(val[1]) for val in values]
            
            # Generate series label from metric
            metric_name = series['metric'].get('__name__', 'metric')
            label_parts = [f"{k}={v}" for k, v in series['metric'].items() if k != '__name__']
            series_label = f"{metric_name}{{{','.join(label_parts)}}}" if label_parts else metric_name
            
            # Plot the series using numeric indices
            plt.plot(metric_values, label=series_label)
        
        plt.title(title)
        plt.xlabel("Time")
        plt.ylabel("Value")
        
        # Set custom x-axis labels if we have timestamps
        if result:
            first_series = result[0]
            if first_series.get('values'):
                timestamps = [float(val[0]) for val in first_series['values']]
                # Create time labels for key points
                time_labels = []
                indices = []
                step_size = max(1, len(timestamps) // 8)  # Show up to 8 time labels
                for i in range(0, len(timestamps), step_size):
                    time_labels.append(datetime.fromtimestamp(timestamps[i]).strftime('%H:%M:%S'))
                    indices.append(i)
                plt.xticks(indices, time_labels)
        
        plt.show()
        
    def plot_instant(self, data: Dict[str, Any], title: str = "Current Metrics"):
        """Plot instant metric values as a bar chart"""
        plt.clear_figure()
        plt.plotsize(self.width, self.height)
        
        if data['status'] != 'success':
            print(f"Error: {data.get('error', 'Unknown error')}")
            return
            
        result = data['data']['result']
        if not result:
            print("No data returned from query")
            return
            
        # Extract metric names and values
        labels = []
        values = []
        
        for series in result:
            metric_name = series['metric'].get('__name__', 'metric')
            label_parts = [f"{k}={v}" for k, v in series['metric'].items() if k != '__name__']
            label = f"{metric_name}{{{','.join(label_parts[:2])}}}" if label_parts else metric_name
            
            # Truncate long labels
            if len(label) > 20:
                label = label[:17] + "..."
            
            labels.append(label)
            values.append(float(series['value'][1]))
        
        plt.bar(labels, values)
        plt.title(title)
        plt.xlabel("Metrics")
        plt.ylabel("Value")
        plt.show()


class PrometheusGrapher:
    """Main class that combines Prometheus querying with plotext visualization"""
    
    def __init__(self, prometheus_url: str, width: int = 120, height: int = 30):
        self.client = PrometheusClient(prometheus_url)
        self.visualizer = MetricVisualizer(width, height)
    
    def graph_query(self, query: str, title: str = None):
        """Graph an instant Prometheus query"""
        if title is None:
            title = f"Query: {query}"
        
        data = self.client.query(query)
        self.visualizer.plot_instant(data, title)
    
    def graph_range(self, query: str, duration: str = "1h", step: str = "15s", title: str = None):
        """Graph a Prometheus range query"""
        if title is None:
            title = f"Query: {query} (last {duration})"
        
        end_time = datetime.now(timezone.utc)
        start_time = end_time - self._parse_duration(duration)
        
        # Convert to Unix timestamps (what Prometheus expects)
        start_str = str(int(start_time.timestamp()))
        end_str = str(int(end_time.timestamp()))
        
        data = self.client.query_range(query, start_str, end_str, step)
        self.visualizer.plot_time_series(data, title)
    
    def _parse_duration(self, duration: str) -> timedelta:
        """Parse duration string like '1h', '30m', '24h' into timedelta"""
        if duration.endswith('s'):
            return timedelta(seconds=int(duration[:-1]))
        elif duration.endswith('m'):
            return timedelta(minutes=int(duration[:-1]))
        elif duration.endswith('h'):
            return timedelta(hours=int(duration[:-1]))
        elif duration.endswith('d'):
            return timedelta(days=int(duration[:-1]))
        else:
            raise ValueError(f"Invalid duration format: {duration}")


@click.command()
@click.option('--url', '-u', default='http://localhost:9090', help='Prometheus server URL')
@click.option('--query', '-q', required=True, help='Prometheus query to execute')
@click.option('--range', '-r', 'query_range', help='Time range for query (e.g., 1h, 30m)')
@click.option('--step', '-s', default='15s', help='Query step size for range queries')
@click.option('--title', '-t', help='Custom title for the graph')
@click.option('--width', '-w', default=120, help='Graph width')
@click.option('--height', '-h', default=30, help='Graph height')
@click.option('--config', '-c', help='Configuration file path')
@click.option('--watch', is_flag=True, help='Continuously refresh the graph')
@click.option('--interval', default=30, help='Refresh interval in seconds (for --watch)')
def main(url, query, query_range, step, title, width, height, config, watch, interval):
    """Plotext-Prometheus: Graph Prometheus metrics in your terminal"""
    
    # Load configuration if provided
    if config:
        try:
            with open(config, 'r') as f:
                config_data = yaml.safe_load(f)
                url = config_data.get('prometheus_url', url)
                width = config_data.get('width', width)
                height = config_data.get('height', height)
        except Exception as e:
            click.echo(f"Error loading config: {e}", err=True)
            sys.exit(1)
    
    try:
        grapher = PrometheusGrapher(url, width, height)
        
        def plot_once():
            if query_range:
                grapher.graph_range(query, query_range, step, title)
            else:
                grapher.graph_query(query, title)
        
        if watch:
            click.echo(f"Watching query: {query}")
            click.echo(f"Refresh interval: {interval}s")
            click.echo("Press Ctrl+C to stop\n")
            
            try:
                while True:
                    plot_once()
                    time.sleep(interval)
            except KeyboardInterrupt:
                click.echo("\nStopped watching.")
        else:
            plot_once()
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()