# Plotext-Prometheus

A command-line tool that combines [plotext](https://github.com/piccolomo/plotext) and Prometheus to graph metrics from a Prometheus server directly in your terminal.

## Features

- 📊 Graph Prometheus metrics in your terminal using ASCII charts
- 🔄 Support for both instant and range queries
- ⏱️ Watch mode for continuous monitoring
- 🎨 Customizable graph dimensions
- 📄 YAML configuration file support
- 🚀 Easy to use command-line interface

## Installation

1. Clone this repository:
```bash
git clone <repo-url>
cd plotext-prom
```

2. Install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Make the script executable (optional):
```bash
chmod +x plotext_prom.py
```

## Usage

### Basic Examples

#### Instant Query (Current Values)
```bash
python plotext_prom.py -q "up"
python plotext_prom.py -q "cpu_usage_percent" --url http://localhost:9090
```

#### Range Query (Time Series)
```bash
$ python plotext_prom.py -q 'scrape_duration_seconds' -r 5m
                                           Query: scrape_duration_seconds (last 5m)
      ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
0.0108┤ ▞▞ scrape_duration_seconds{app=prometheus,instance=127.0.0.1:9090,job=prometheus}            ▗▌                │
      │                                                                                              ▌▌                │
      │▌                                                                                            ▞ ▐                │
      │▌                                                                                           ▗▘ ▝▖               │
0.0099┤▐                                                                       ▗▄▄▄▄▄▌             ▌   ▌               │
      │▝▖                                                                      ▌     ▌            ▐    ▐         ▖     │
      │ ▌                                                                     ▐      ▐           ▗▘    ▐        ▐▝▚▄   │
      │ ▐                                          ▟                          ▌      ▝▖          ▞      ▌       ▌   ▀▚▄│
0.0089┤ ▐                                          ▛▖                        ▐        ▌         ▐       ▚      ▐       │
      │  ▌                                        ▐ ▚                        ▌        ▐         ▌       ▐      ▌       │
      │  ▚                                        ▞ ▐                       ▐         ▐        ▐         ▌    ▗▘       │
      │  ▐                                        ▌  ▌                      ▌          ▌       ▌         ▚    ▞        │
0.0080┤   ▌                                      ▐   ▐                     ▐           ▚      ▐          ▐   ▗▘        │
      │   ▚                                      ▞    ▌                    ▌           ▐      ▌          ▝▖  ▞         │
      │   ▐                                      ▌    ▚                   ▐             ▌    ▗▘           ▌  ▌         │
      │   ▝▖                                    ▐     ▝▖                  ▌             ▚    ▞            ▐ ▐          │
0.0070┤    ▌                                    ▐      ▚                 ▄▘             ▐   ▗▘            ▝▖▌          │
      │    ▐                                    ▌      ▐              ▄▞▀               ▝▖  ▞              █           │
      │    ▝▖                                  ▗▘       ▌           ▞▀                   ▌  ▌              ▝           │
      │     ▌        ▄▄▞▄                      ▐        ▐          ▞                     ▐ ▐                           │
0.0060┤     ▝▀▀▀▀▀▀▀▀    ▀▄                    ▌         ▚        ▞                      ▝▖▌                           │
      │                    ▀▄                 ▗▘          ▚▖     ▐                        █                            │
      │                      ▀▄        ▗▞▄    ▐            ▝▖   ▗▘                        ▝                            │
      │                        ▀▚▄  ▗▄▀▘  ▀▄  ▌             ▝▚ ▗▘                                                      │
0.0051┤                           ▀▀▘       ▀▄▌               ▚▌                                                       │
      └──────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────┘
09:56:29  09:56:59  09:57:29   09:57:59   09:58:29   09:58:59   09:59:29   09:59:59   10:00:29   10:00:59   10:01:29
Value                                                        Time
```

#### Range Query with Custom Step Size
```bash
python plotext_prom.py -q "process_cpu_seconds_total" -r "30m" -s "30s"
                                         Query: process_cpu_seconds_total (last 30m)
    ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
1.86┤ ▞▞ process_cpu_seconds_total{app=prometheus,instance=127.0.0.1:9090,job=prometheus}                           ▗▄▞│
    │                                                                                                         ▄▄▄▄▀▀▘  │
    │                                                                                                    ▗▄▄▀▀         │
    │                                                                                           ▗▄▄▄▄▀▀▀▀▘             │
1.68┤                                                                                         ▄▞▘                      │
    │                                                                                 ▄▄▀▀▀▀▀▀                         │
    │                                                                            ▗▄▞▀▀                                 │
    │                                                                      ▄▄▄▄▀▀▘                                     │
1.50┤                                                                 ▗▄▄▀▀                                            │
    │                                                             ▄▄▞▀▘                                                │
    │                                                  ▗▄▞▀▀▀▀▀▀▀▀                                                     │
    │                                           ▗▄▄▄▄▀▀▘                                                               │
1.32┤                                     ▗▄▞▀▀▀▘                                                                      │
    │                                  ▗▀▀▘                                                                            │
    │                                 ▞▘                                                                               │
    │                               ▗▀                                                                                 │
1.14┤                            ▗▄▞▘                                                                                  │
    │                      ▄▄▄▄▀▀▘                                                                                     │
    │                 ▗▄▄▀▀                                                                                            │
    │             ▄▄▞▀▘                                                                                                │
0.96┤          ▄▞▀                                                                                                     │
    │       ▗▞▀                                                                                                        │
    │    ▗▄▀▘                                                                                                          │
    │  ▗▞▘                                                                                                             │
0.78┤▄▞▘                                                                                                               │
    └─────────┬────────────┬────────────┬────────────┬────────────┬────────────┬────────────┬────────────┬─────────────┘
09:50:55   09:52:25    09:53:55     09:55:25     09:56:55     09:58:25     09:59:55     10:01:25     10:02:55
Value                                                       Time
```

#### Watch Mode (Continuous Monitoring)
```bash
$ python plotext_prom.py -q "process_cpu_seconds_total" -r "10m" --watch --interval 15
Watching query: process_cpu_seconds_total
Refresh interval: 15s
Press Ctrl+C to stop

                                         Query: process_cpu_seconds_total (last 10m)
    ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
2.02┤ ▞▞ process_cpu_seconds_total{app=prometheus,instance=127.0.0.1:9090,job=prometheus}                          ▗▄▄▞│
    │                                                                                                      ▄▄▄▀▀▀▀▀▘   │
    │                                                                                                  ▄▞▀▀            │
    │                                                                                             ▗▄▄▞▀                │
1.92┤                                                                                           ▄▞▘                    │
    │                                                                                  ▗▄▄▀▀▀▀▀▀                       │
    │                                                                               ▗▄▀▘                               │
    │                                                                           ▗▞▀▀▘                                  │
1.82┤                                                                        ▗▄▀▘                                      │
    │                                                                 ▗▄▄▀▀▀▀▘                                         │
    │                                                               ▗▞▘                                                │
    │                                                         ▄▄▞▀▀▀▘                                                  │
1.71┤                                                    ▗▄▀▀▀                                                         │
    │                                                 ▗▄▀▘                                                             │
    │                                               ▄▀▘                                                                │
    │                                       ▗▄▄▄▄▄▞▀                                                                   │
1.61┤                                     ▄▞▘                                                                          │
    │                                ▗▄▀▀▀                                                                             │
    │                              ▄▀▘                                                                                 │
    │                         ▗▄▄▞▀                                                                                    │
1.51┤                     ▗▞▀▀▘                                                                                        │
    │                 ▄▄▄▀▘                                                                                            │
    │              ▄▞▀                                                                                                 │
    │     ▗▄▄▄▄▄▞▀▀                                                                                                    │
1.41┤▄▄▄▀▀▘                                                                                                            │
    └───────────┬─────────────┬──────────────┬─────────────┬─────────────┬─────────────┬─────────────┬─────────────┬───┘
 09:57:06   09:58:21      09:59:36       10:00:51      10:02:06      10:03:21      10:04:36      10:05:51    10:07:06
Value                                                       Time
^C
Stopped watching.
```

### Command Line Options

```
Options:
  -u, --url TEXT       Prometheus server URL [default: http://localhost:9090]
  -q, --query TEXT     Prometheus query to execute [required]
  -r, --range TEXT     Time range for query (e.g., 1h, 30m, 24h)
  -s, --step TEXT      Query step size for range queries [default: 15s]
  -t, --title TEXT     Custom title for the graph
  -w, --width INTEGER  Graph width [default: 120]
  -h, --height INTEGER Graph height [default: 30]
  -c, --config TEXT    Configuration file path
  --watch              Continuously refresh the graph
  --interval INTEGER   Refresh interval in seconds (for --watch) [default: 30]
  --help               Show this message and exit.
```

### Configuration File

Create a YAML configuration file to avoid repeating common settings:

```yaml
prometheus_url: "http://localhost:9090"
width: 140
height: 40
```

Use with:
```bash
python plotext_prom.py -q "up" -c config.yaml
```

## Example Queries

Here are some common Prometheus queries you can visualize:

### System Metrics
```bash
# CPU usage
python plotext_prom.py -q "process_cpu_seconds_total" -r "1h"

# Memory usage
python plotext_prom.py -q "process_resident_memory_bytes" -r "2h"
```

### Application Metrics
```bash
# HTTP requests per second
python plotext_prom.py -q "sum(rate(prometheus_http_requests_total[5m]))" -r "1h"

# Response times
python plotext_prom.py -q "histogram_quantile(0.95, sum(rate(prometheus_http_request_duration_seconds_bucket{handler="/metrics"}[5m])) by (le))" -r "30m"

# Number of currently active appender transactions
python plotext_prom.py -q "prometheus_tsdb_head_active_appenders" -r "2h"
```

### Container Metrics (if using cAdvisor)
```bash
# Container CPU usage
python plotext_prom.py -q "rate(container_cpu_usage_seconds_total[5m])" -r "1h"

# Container memory usage
python plotext_prom.py -q "container_memory_usage_bytes" -r "30m"
```

## Output Examples

### Time Series Graph
```
                        Query: cpu_usage_percent (last 1h)                         
    ┌─────────────────────────────────────────────────────────────────────────────┐
 90 │                                                              ▗▄▖             │
    │                                                            ▄▀  ▚▄           │
 80 │                                          ▗▖                █     ▀▄          │
    │                                        ▄▀ ▝▄             ▗▀       ▚▖        │
 70 │                              ▄▄▖      █    ▀▄           ▄▀         ▝▄       │
    │                            ▄▀   ▀▄   ▗▀      ▚▄        ▄▀            ▀▖     │
 60 │                 ▄▄▖        █      ▀▄ ▄▀        ▀▄      ▗▀              ▝▄    │
    │               ▄▀   ▀▄     ▗▀        ▀▀           ▀▄   ▄▀                 ▚▄  │
 50 │         ▄▄▖  ▄▀      ▀▄  ▄▀                       ▀▄▄▀                   ▝▀▄│
    │       ▄▀   ▀▀          ▀▀                                                    │
 40 │▄▄▄▄▄▀                                                                        │
    └─────────────────────────────────────────────────────────────────────────────┘
    10:30:00        11:00:00        11:30:00        12:00:00        12:30:00
                                          Time
```

### Instant Values Bar Chart
```
                             Current Metrics                              
    ┌─────────────────────────────────────────────────────────────────┐
  1 │██████████████████████████████████████████████████████████████  │
    │                                                                 │
0.8 │                                                                 │
    │                                                                 │
0.6 │                    ███████████████                             │
    │                                                                 │
0.4 │                                        ████████                │
    │                                                                 │
0.2 │         ███████                                   ████          │
    │                                                                 │
  0 └─────────────────────────────────────────────────────────────────┘
    up{job="prometheus"}  up{job="node"}  up{job="app1"}  up{job="app2"}
                                    Metrics
```

## Troubleshooting

### Connection Issues
- Ensure your Prometheus server is running and accessible
- Check the URL format (include `http://` or `https://`)
- Verify network connectivity and firewall settings

### Query Issues
- Test your queries in the Prometheus web UI first
- Ensure metric names and labels are correct
- Check that the time range contains data

### Display Issues
- Adjust terminal size or graph dimensions with `-w` and `-h`
- Some terminals may not support all Unicode characters used in graphs
- Try different step sizes for range queries if graphs appear too dense

## Requirements

- Python 3.7+
- plotext >= 5.2.8
- requests >= 2.28.0
- click >= 8.0.0
- PyYAML >= 6.0

## License

MIT License - feel free to use and modify as needed!
