#!/usr/bin/env python3
"""
===================================================================================
analyze_results.py - Drone SAR Simulation Results Analyzer
===================================================================================
Analyzes OMNeT++ simulation results (.sca and .vec files) and generates
comprehensive visualizations for Bat Algorithm routing performance.

Usage:
    python3 analyze_results.py
    python3 analyze_results.py --config DroneSwarm5km
    python3 analyze_results.py --all
"""

import os
import sys
import re
import argparse
from pathlib import Path
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

# Configuration
RESULTS_DIR = "simulations/results"
OUTPUT_DIR = "analysis"
FIGURE_DPI = 300
FIGURE_SIZE = (12, 8)

class SimulationAnalyzer:
    """Analyzes OMNeT++ simulation scalar (.sca) results"""
    
    def __init__(self, results_dir):
        self.results_dir = Path(results_dir)
        self.data = defaultdict(lambda: defaultdict(list))
        
    def load_sca_file(self, filepath):
        """Parse OMNeT++ .sca (scalar) file"""
        print(f"Loading {filepath.name}...")
        
        current_module = None
        current_scalar = None
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                
                # Module declaration: scalar ModuleName.submodule
                if line.startswith('scalar'):
                    parts = line.split()
                    if len(parts) >= 3:
                        current_module = parts[1]  # e.g., "DroneSwarmNetwork.drone[0].batRouting"
                        current_scalar = parts[2]   # e.g., "routeDiscovered:count"
                        
                        # Extract value (last part)
                        try:
                            value = float(parts[3])
                            
                            # Extract drone ID from module name
                            match = re.search(r'drone\[(\d+)\]', current_module)
                            if match:
                                drone_id = int(match.group(1))
                                self.data[current_scalar][drone_id].append(value)
                        except (ValueError, IndexError):
                            pass
    
    def load_all_sca_files(self, pattern="*.sca"):
        """Load all .sca files matching pattern"""
        files = sorted(self.results_dir.glob(pattern))
        
        if not files:
            print(f"⚠️  No .sca files found in {self.results_dir}")
            return False
        
        for filepath in files:
            self.load_sca_file(filepath)
        
        print(f"✅ Loaded {len(files)} result file(s)")
        return True
    
    def get_metric_stats(self, metric_name):
        """Calculate statistics for a given metric across all drones"""
        if metric_name not in self.data:
            return None
        
        values = []
        for drone_id, runs in self.data[metric_name].items():
            values.extend(runs)
        
        if not values:
            return None
        
        return {
            'mean': np.mean(values),
            'std': np.std(values),
            'min': np.min(values),
            'max': np.max(values),
            'median': np.median(values),
            'total': np.sum(values)
        }
    
    def print_summary(self):
        """Print statistical summary of all metrics"""
        print("\n" + "="*80)
        print("SIMULATION RESULTS SUMMARY")
        print("="*80)
        
        metrics = [
            ('routeDiscovered:count', 'Routes Discovered'),
            ('packetRouted:count', 'Packets Routed'),
            ('routeDiscovered:sum', 'Total Route Discoveries'),
            ('packetRouted:sum', 'Total Packets Routed')
        ]
        
        for metric_key, metric_label in metrics:
            stats = self.get_metric_stats(metric_key)
            if stats:
                print(f"\n📊 {metric_label}:")
                print(f"   Mean:   {stats['mean']:.2f}")
                print(f"   Median: {stats['median']:.2f}")
                print(f"   Std:    {stats['std']:.2f}")
                print(f"   Range:  [{stats['min']:.0f}, {stats['max']:.0f}]")
                print(f"   Total:  {stats['total']:.0f}")
        
        print("\n" + "="*80)


class GraphGenerator:
    """Generates comprehensive visualization graphs"""
    
    def __init__(self, analyzer, output_dir):
        self.analyzer = analyzer
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set publication-quality style
        plt.style.use('seaborn-v0_8-darkgrid')
        plt.rcParams['figure.figsize'] = FIGURE_SIZE
        plt.rcParams['font.size'] = 11
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['legend.fontsize'] = 10
    
    def plot_routes_per_drone(self):
        """Bar chart: Routes discovered per drone in SAR mission"""
        data = self.analyzer.data.get('routeDiscovered:count')
        if not data:
            print("⚠️  No route discovery data available")
            return
        
        # Calculate average routes per drone across all runs
        drone_ids = sorted(data.keys())
        avg_routes = [np.mean(data[drone_id]) for drone_id in drone_ids]
        std_routes = [np.std(data[drone_id]) if len(data[drone_id]) > 1 else 0 
                      for drone_id in drone_ids]
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Color bars by performance (gradient)
        colors = plt.cm.YlOrRd(np.linspace(0.3, 0.9, len(drone_ids)))
        bars = ax.bar(drone_ids, avg_routes, yerr=std_routes, 
                      capsize=5, alpha=0.85, color=colors, edgecolor='black', linewidth=1.2)
        
        # Add value labels on bars
        for i, (bar, val, std) in enumerate(zip(bars, avg_routes, std_routes)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + std + 2,
                   f'{val:.1f}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_xlabel('UAV ID (Drone Index)', fontweight='bold', fontsize=13)
        ax.set_ylabel('Routes Discovered (count)', fontweight='bold', fontsize=13)
        ax.set_title('Bat Algorithm Route Discovery Performance in SAR Mission\n' + 
                    'Multi-hop Route Identification over 300s Simulation',
                    fontweight='bold', fontsize=15, pad=20)
        ax.grid(axis='y', alpha=0.4, linestyle='--')
        ax.set_axisbelow(True)
        
        # Add statistical reference lines
        mean_val = np.mean(avg_routes)
        ax.axhline(y=mean_val, color='darkred', linestyle='--', 
                  label=f'Mean: {mean_val:.1f} routes', linewidth=2.5, alpha=0.8)
        
        # Add legend with context
        legend_text = [
            f'Mean: {mean_val:.1f} routes',
            f'Total UAVs: {len(drone_ids)}',
            f'Std Dev: {np.std(avg_routes):.1f}'
        ]
        ax.legend(['\n'.join(legend_text)], loc='upper right', 
                 frameon=True, shadow=True, fontsize=10)
        
        # Add footer with methodology
        fig.text(0.5, 0.02, 
                'Bio-inspired routing using Bat Algorithm with loudness adaptation and pulse rate control\n' +
                'Error bars represent standard deviation across simulation runs',
                ha='center', fontsize=9, style='italic', color='gray')
        
        plt.tight_layout(rect=[0, 0.05, 1, 0.98])
        output_path = self.output_dir / 'bat_routes_per_drone.png'
        plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches='tight', facecolor='white')
        print(f"✅ Saved: {output_path}")
        plt.close()
    
    def plot_route_distribution(self):
        """Histogram: Distribution of Bat Algorithm route discoveries"""
        data = self.analyzer.data.get('routeDiscovered:count')
        if not data:
            return
        
        all_values = []
        for runs in data.values():
            all_values.extend(runs)
        
        fig, ax = plt.subplots(figsize=(13, 8))
        
        # Create histogram with custom styling
        n, bins, patches = ax.hist(all_values, bins=25, alpha=0.8, 
                                   color='#2E86AB', edgecolor='#1A5276', linewidth=1.5)
        
        # Color bars by frequency (gradient)
        cm = plt.cm.Blues
        norm = plt.Normalize(vmin=n.min(), vmax=n.max())
        for count, patch in zip(n, patches):
            patch.set_facecolor(cm(norm(count)))
        
        ax.set_xlabel('Routes Discovered (count)', fontweight='bold', fontsize=13)
        ax.set_ylabel('Frequency (UAV count)', fontweight='bold', fontsize=13)
        ax.set_title('Statistical Distribution of Bat Algorithm Route Discovery\n' +
                    'FANET Multi-hop Routing Performance in SAR Operations',
                    fontweight='bold', fontsize=15, pad=20)
        ax.grid(axis='y', alpha=0.4, linestyle='--')
        ax.set_axisbelow(True)
        
        # Add statistical markers
        mean_val = np.mean(all_values)
        median_val = np.median(all_values)
        std_val = np.std(all_values)
        
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=2.5, 
                  label=f'Mean: {mean_val:.1f}', alpha=0.8)
        ax.axvline(median_val, color='orange', linestyle='-.', linewidth=2.5,
                  label=f'Median: {median_val:.1f}', alpha=0.8)
        
        # Enhanced statistics box
        stats_text = (
            f'Statistical Summary:\n'
            f'━━━━━━━━━━━━━━━━\n'
            f'Mean:     {mean_val:.2f} routes\n'
            f'Median:   {median_val:.2f} routes\n'
            f'Std Dev:  {std_val:.2f}\n'
            f'Min:      {np.min(all_values):.0f} routes\n'
            f'Max:      {np.max(all_values):.0f} routes\n'
            f'Sample:   {len(all_values)} UAVs'
        )
        ax.text(0.98, 0.97, stats_text, transform=ax.transAxes,
               fontsize=10, verticalalignment='top', horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='lightyellow', 
                        alpha=0.9, edgecolor='black', linewidth=1.5),
               family='monospace')
        
        ax.legend(loc='upper left', frameon=True, shadow=True, fontsize=11)
        
        # Add footer
        fig.text(0.5, 0.02,
                'Bat Algorithm parameters: loudness α=0.9→0.1, pulse rate β=0.5→0.95, frequency [0-2 Hz]',
                ha='center', fontsize=9, style='italic', color='gray')
        
        plt.tight_layout(rect=[0, 0.05, 1, 0.98])
        output_path = self.output_dir / 'bat_distribution.png'
        plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches='tight', facecolor='white')
        print(f"✅ Saved: {output_path}")
        plt.close()
    
    def plot_variability_across_runs(self):
        """Box plot: Bat Algorithm consistency across simulation runs"""
        data = self.analyzer.data.get('routeDiscovered:count')
        if not data:
            return
        
        drone_ids = sorted(data.keys())
        runs_data = [data[drone_id] for drone_id in drone_ids]
        
        max_runs = max(len(runs) for runs in runs_data)
        if max_runs < 2:
            print("⚠️  Only one run available, skipping variability plot")
            return
        
        fig, ax = plt.subplots(figsize=(15, 8))
        
        bp = ax.boxplot(runs_data, tick_labels=drone_ids, patch_artist=True,
                       showmeans=True, meanline=True, widths=0.6)
        
        # Enhanced box plot styling with gradient
        colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(drone_ids)))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
            patch.set_edgecolor('black')
            patch.set_linewidth(1.5)
        
        # Style median lines
        for median in bp['medians']:
            median.set_color('darkred')
            median.set_linewidth(3)
        
        # Style mean lines
        for mean in bp['means']:
            mean.set_color('darkblue')
            mean.set_linewidth(3)
            mean.set_linestyle('--')
        
        # Style whiskers and caps
        for whisker in bp['whiskers']:
            whisker.set_linewidth(1.5)
            whisker.set_linestyle('-')
        for cap in bp['caps']:
            cap.set_linewidth(1.5)
        
        ax.set_xlabel('UAV Index (Drone ID)', fontweight='bold', fontsize=13)
        ax.set_ylabel('Routes Discovered (count)', fontweight='bold', fontsize=13)
        ax.set_title('Bat Algorithm Consistency Analysis\n' +
                    'Route Discovery Variability Across Multiple Simulation Runs',
                    fontweight='bold', fontsize=15, pad=20)
        ax.grid(axis='y', alpha=0.4, linestyle='--')
        ax.set_axisbelow(True)
        
        # Enhanced legend
        legend_elements = [
            plt.Line2D([0], [0], color='darkred', linewidth=3, label='Median'),
            plt.Line2D([0], [0], color='darkblue', linewidth=3, linestyle='--', label='Mean'),
            plt.Rectangle((0, 0), 1, 1, fc='lightgreen', alpha=0.7, label='Interquartile Range (IQR)')
        ]
        ax.legend(handles=legend_elements, loc='upper right', 
                 frameon=True, shadow=True, fontsize=11)
        
        # Add statistics annotation
        all_data = [val for sublist in runs_data for val in sublist]
        overall_mean = np.mean(all_data)
        overall_std = np.std(all_data)
        cv = (overall_std / overall_mean) * 100  # Coefficient of variation
        
        stats_text = (
            f'Swarm Statistics:\n'
            f'━━━━━━━━━━━━━━\n'
            f'Overall Mean: {overall_mean:.2f}\n'
            f'Overall Std:  {overall_std:.2f}\n'
            f'Coef. Var:    {cv:.1f}%\n'
            f'Total Runs:   {max_runs}'
        )
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
               fontsize=10, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='lightyellow', 
                        alpha=0.9, edgecolor='black', linewidth=1.5),
               family='monospace')
        
        # Add footer
        fig.text(0.5, 0.02,
                'Box: Q1-Q3 | Whiskers: 1.5×IQR | Lower variability indicates more consistent routing performance',
                ha='center', fontsize=9, style='italic', color='gray')
        
        plt.tight_layout(rect=[0, 0.05, 1, 0.98])
        output_path = self.output_dir / 'bat_consistency.png'
        plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches='tight', facecolor='white')
        print(f"✅ Saved: {output_path}")
        plt.close()
    
    def plot_swarm_efficiency(self):
        """Efficiency analysis: Route discovery rate and network coverage"""
        data = self.analyzer.data.get('routeDiscovered:count')
        if not data:
            print("⚠️  Not enough data for efficiency analysis")
            return
        
        drone_ids = sorted(data.keys())
        avg_routes = np.array([np.mean(data[drone_id]) for drone_id in drone_ids])
        
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
        
        # Left plot: Cumulative route discovery
        cumulative = np.cumsum(sorted(avg_routes, reverse=True))
        percentage = (cumulative / cumulative[-1]) * 100
        
        ax1.plot(range(1, len(cumulative) + 1), cumulative, 
                marker='o', linewidth=3, markersize=8, color='#2E86AB')
        ax1.fill_between(range(1, len(cumulative) + 1), cumulative, 
                         alpha=0.3, color='#2E86AB')
        
        ax1.set_xlabel('Number of UAVs', fontweight='bold', fontsize=12)
        ax1.set_ylabel('Cumulative Routes Discovered', fontweight='bold', fontsize=12)
        ax1.set_title('Swarm Route Discovery Accumulation\n(Ordered by Performance)',
                     fontweight='bold', fontsize=13)
        ax1.grid(True, alpha=0.4, linestyle='--')
        ax1.set_axisbelow(True)
        
        # Add percentage annotations
        for i in [2, 4, 6, 9]:
            if i < len(percentage):
                ax1.annotate(f'{percentage[i]:.0f}%',
                           xy=(i+1, cumulative[i]),
                           xytext=(10, -10), textcoords='offset points',
                           fontsize=9, bbox=dict(boxstyle='round', 
                           facecolor='yellow', alpha=0.7))
        
        # Right plot: Individual contribution
        colors = ['#27AE60' if r >= np.mean(avg_routes) else '#E74C3C' 
                 for r in avg_routes]
        bars = ax2.barh(drone_ids, avg_routes, color=colors, alpha=0.8, edgecolor='black')
        
        ax2.axvline(np.mean(avg_routes), color='blue', linestyle='--', 
                   linewidth=2.5, label=f'Swarm Mean: {np.mean(avg_routes):.1f}')
        
        ax2.set_xlabel('Routes Discovered (count)', fontweight='bold', fontsize=12)
        ax2.set_ylabel('UAV Index', fontweight='bold', fontsize=12)
        ax2.set_title('Individual UAV Contribution to Network\n(Green: Above Mean | Red: Below Mean)',
                     fontweight='bold', fontsize=13)
        ax2.legend(loc='lower right', fontsize=10)
        ax2.grid(axis='x', alpha=0.4, linestyle='--')
        ax2.set_axisbelow(True)
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, avg_routes)):
            ax2.text(val + 2, bar.get_y() + bar.get_height()/2, 
                    f'{val:.1f}',
                    va='center', fontsize=9, fontweight='bold')
        
        # Overall title
        fig.suptitle('Bat Algorithm FANET Routing: Swarm Efficiency Analysis',
                    fontsize=16, fontweight='bold', y=0.98)
        
        # Add footer
        fig.text(0.5, 0.02,
                'Left: Cumulative network capacity | Right: Individual UAV performance relative to swarm average',
                ha='center', fontsize=9, style='italic', color='gray')
        
        plt.tight_layout(rect=[0, 0.05, 1, 0.96])
        output_path = self.output_dir / 'bat_efficiency.png'
        plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches='tight', facecolor='white')
        print(f"✅ Saved: {output_path}")
        plt.close()
    
    def plot_performance_heatmap(self):
        """Heatmap: Bat Algorithm performance across UAVs and simulation runs"""
        data = self.analyzer.data.get('routeDiscovered:count')
        if not data:
            return
        
        drone_ids = sorted(data.keys())
        max_runs = max(len(data[drone_id]) for drone_id in drone_ids)
        
        if max_runs < 2:
            print("⚠️  Only one run available, skipping heatmap")
            return
        
        # Create matrix
        matrix = np.zeros((len(drone_ids), max_runs))
        for i, drone_id in enumerate(drone_ids):
            for j, value in enumerate(data[drone_id]):
                matrix[i, j] = value
        
        fig, ax = plt.subplots(figsize=(12, 9))
        
        # Use red-yellow colormap for intensity
        im = ax.imshow(matrix, cmap='RdYlGn', aspect='auto', interpolation='nearest')
        
        ax.set_xticks(np.arange(max_runs))
        ax.set_yticks(np.arange(len(drone_ids)))
        ax.set_xticklabels([f'Run #{i}' for i in range(max_runs)], fontsize=11)
        ax.set_yticklabels([f'UAV {i}' for i in drone_ids], fontsize=11)
        
        # Add colorbar with enhanced label
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Routes Discovered\n(Bio-inspired Optimization)', 
                      rotation=270, labelpad=30, fontweight='bold', fontsize=11)
        
        # Add text annotations with contrasting colors
        for i in range(len(drone_ids)):
            for j in range(max_runs):
                if matrix[i, j] > 0:
                    # Choose text color based on background intensity
                    text_color = 'white' if matrix[i, j] > np.mean(matrix) else 'black'
                    text = ax.text(j, i, f'{int(matrix[i, j])}',
                                 ha="center", va="center", color=text_color, 
                                 fontsize=9, fontweight='bold')
        
        ax.set_title('Bat Algorithm Performance Heatmap: UAV Swarm Route Discovery\n' +
                    'Spatial-Temporal Analysis of Multi-hop FANET Routing',
                    fontweight='bold', fontsize=14, pad=20)
        ax.set_xlabel('Simulation Run (300s each)', fontweight='bold', fontsize=12)
        ax.set_ylabel('UAV Index (Swarm Member)', fontweight='bold', fontsize=12)
        
        # Add grid for clarity
        ax.set_xticks(np.arange(max_runs) - 0.5, minor=True)
        ax.set_yticks(np.arange(len(drone_ids)) - 0.5, minor=True)
        ax.grid(which="minor", color="gray", linestyle='-', linewidth=0.5, alpha=0.3)
        
        # Add performance statistics
        stats_text = (
            f'Swarm Performance:\n'
            f'Average: {np.mean(matrix):.1f} routes/UAV\n'
            f'Best: {np.max(matrix):.0f} routes\n'
            f'Worst: {np.min(matrix[matrix>0]):.0f} routes'
        )
        ax.text(1.15, 0.5, stats_text, transform=ax.transAxes,
               fontsize=10, verticalalignment='center',
               bbox=dict(boxstyle='round', facecolor='lightblue', 
                        alpha=0.8, edgecolor='black', linewidth=1.5))
        
        # Add footer
        fig.text(0.5, 0.02,
                'Color intensity indicates routing efficiency | Darker = Higher route discovery | SAR Mission Context',
                ha='center', fontsize=9, style='italic', color='gray')
        
        plt.tight_layout(rect=[0, 0.05, 1, 0.98])
        output_path = self.output_dir / 'bat_heatmap.png'
        plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches='tight', facecolor='white')
        print(f"✅ Saved: {output_path}")
        plt.close()
    
    def generate_all_plots(self):
        """Generate all available visualizations for Bat Algorithm analysis"""
        print("\n" + "="*80)
        print("GENERATING BAT ALGORITHM PERFORMANCE VISUALIZATIONS")
        print("="*80 + "\n")
        
        self.plot_routes_per_drone()
        self.plot_route_distribution()
        self.plot_variability_across_runs()
        self.plot_swarm_efficiency()
        self.plot_performance_heatmap()
        
        print(f"\n✅ All graphs saved to: {self.output_dir.absolute()}")
        print("📊 5 publication-ready figures generated for FANET routing analysis")


def main():
    parser = argparse.ArgumentParser(
        description='Analyze Drone SAR simulation results and generate graphs',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--config', type=str, default='*',
                       help='Configuration name (e.g., DroneSwarm5km) or * for all')
    parser.add_argument('--all', action='store_true',
                       help='Analyze all configurations')
    parser.add_argument('--output', type=str, default=OUTPUT_DIR,
                       help='Output directory for graphs')
    
    args = parser.parse_args()
    
    print("\n" + "="*80)
    print("DRONE SAR SIMULATION ANALYZER")
    print("="*80)
    
    # Check if results directory exists
    results_path = Path(RESULTS_DIR)
    if not results_path.exists():
        print(f"❌ Error: Results directory not found: {results_path}")
        print("   Please run simulations first!")
        sys.exit(1)
    
    # Determine file pattern
    if args.all or args.config == '*':
        pattern = "*.sca"
        print(f"📂 Analyzing all configurations in {RESULTS_DIR}")
    else:
        pattern = f"{args.config}-*.sca"
        print(f"📂 Analyzing configuration: {args.config}")
    
    # Create analyzer and load data
    analyzer = SimulationAnalyzer(RESULTS_DIR)
    
    if not analyzer.load_all_sca_files(pattern):
        print("❌ No data loaded. Exiting.")
        sys.exit(1)
    
    # Print summary
    analyzer.print_summary()
    
    # Generate graphs
    output_path = Path(args.output)
    # Only append config name if user didn't already specify it in the path
    if args.config != '*' and not args.all and args.config not in str(output_path):
        output_path = output_path / args.config
    
    generator = GraphGenerator(analyzer, output_path)
    generator.generate_all_plots()
    
    print("\n" + "="*80)
    print("✅ ANALYSIS COMPLETE")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
