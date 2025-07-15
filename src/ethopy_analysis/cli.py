"""
Command-line interface for Ethopy analysis.
"""

import click
import logging
from pathlib import Path
from typing import Optional, List

# Import our modules
from .db.schemas import test_connection
from .data.loaders import load_animal_data, load_session_data, load_animals_list
from .plots.animal import plot_animal_performance, plot_sessions_over_time
from ...temp_old_files.session_olf import plot_trial_performance, plot_session_summary
from .plots.comparison import plot_animals_comparison
from .config.settings import load_config, get_config_summary, save_config


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


@click.group()
@click.version_option(version="0.1.0", prog_name="ethopy-analysis")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
@click.pass_context
def main(ctx, verbose):
    """Ethopy Analysis - Behavioral data analysis and visualization."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    setup_logging(verbose)


@main.command()
@click.option("--animal-id", type=int, required=True, help="Animal ID to analyze")
@click.option(
    "--output-dir",
    type=click.Path(),
    default="./output",
    help="Output directory for plots",
)
@click.option("--from-date", type=str, help="Start date (YYYY-MM-DD)")
@click.option("--to-date", type=str, help="End date (YYYY-MM-DD)")
@click.option(
    "--metric", type=str, default="correct_rate", help="Performance metric to plot"
)
@click.option("--save-plots", is_flag=True, help="Save plots to files")
def analyze_animal(animal_id, output_dir, from_date, to_date, metric, save_plots):
    """Analyze data for a specific animal."""
    click.echo(f"Analyzing animal {animal_id}...")

    try:
        # Load animal data
        data = load_animal_data(
            animal_id=animal_id,
            from_date=from_date or "",
            to_date=to_date or "",
        )

        if not data:
            click.echo(f"No data found for animal {animal_id}")
            return

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Generate plots
        if "performance" in data and not data["performance"].empty:
            save_path = (
                str(output_path / f"animal_{animal_id}_performance")
                if save_plots
                else None
            )
            fig, ax = plot_animal_performance(
                data["performance"],
                animal_id=animal_id,
                metric=metric,
                save_path=save_path,
            )
            click.echo(f"Created performance plot for animal {animal_id}")

        if "sessions" in data and not data["sessions"].empty:
            save_path = (
                str(output_path / f"animal_{animal_id}_sessions")
                if save_plots
                else None
            )
            fig, ax = plot_sessions_over_time(
                data["sessions"], animal_id=animal_id, save_path=save_path
            )
            click.echo(f"Created sessions timeline for animal {animal_id}")

        click.echo(f"Analysis complete. Results in: {output_dir}")

    except Exception as e:
        click.echo(f"Error analyzing animal {animal_id}: {e}")
        raise click.ClickException(str(e))


@main.command()
@click.option("--animal-id", type=int, required=True, help="Animal ID")
@click.option("--session-id", type=str, required=True, help="Session ID to analyze")
@click.option(
    "--output-dir",
    type=click.Path(),
    default="./output",
    help="Output directory for plots",
)
@click.option("--include-licking", is_flag=True, help="Include licking data")
@click.option("--include-proximity", is_flag=True, help="Include proximity sensor data")
@click.option("--save-plots", is_flag=True, help="Save plots to files")
def analyze_session(
    animal_id, session_id, output_dir, include_licking, include_proximity, save_plots
):
    """Analyze data for a specific session."""
    click.echo(f"Analyzing session {session_id} for animal {animal_id}...")

    try:
        # Load session data
        data = load_session_data(
            animal_id=animal_id,
            session=session_id,
            include_licking=include_licking,
            include_proximity=include_proximity,
        )

        if not data:
            click.echo(f"No data found for session {session_id}")
            return

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Generate session summary plot
        if data:
            save_path = (
                str(output_path / f"session_{session_id}_summary")
                if save_plots
                else None
            )
            fig, axes = plot_session_summary(
                data, session_id=session_id, save_path=save_path
            )
            click.echo(f"Created session summary for session {session_id}")

        # Generate trial performance plot
        if "trials" in data and not data["trials"].empty:
            save_path = (
                str(output_path / f"session_{session_id}_trials")
                if save_plots
                else None
            )
            fig, ax = plot_trial_performance(
                data["trials"], session_id=session_id, save_path=save_path
            )
            click.echo(f"Created trial performance plot for session {session_id}")

        click.echo(f"Session analysis complete. Results in: {output_dir}")

    except Exception as e:
        click.echo(f"Error analyzing session {session_id}: {e}")
        raise click.ClickException(str(e))


@main.command()
@click.option(
    "--animal-ids", type=str, help="Comma-separated list of animal IDs (optional)"
)
@click.option(
    "--output-dir",
    type=click.Path(),
    default="./output",
    help="Output directory for plots",
)
@click.option(
    "--metric", type=str, default="correct_rate", help="Performance metric to compare"
)
@click.option(
    "--comparison-type",
    type=str,
    default="boxplot",
    help="Comparison type (boxplot, violin, timeline)",
)
@click.option("--save-plots", is_flag=True, help="Save plots to files")
def compare_animals(animal_ids, output_dir, metric, comparison_type, save_plots):
    """Compare performance across multiple animals."""
    click.echo("Comparing animals...")

    try:
        # Parse animal IDs if provided
        ids_list = None
        if animal_ids:
            ids_list = [int(x.strip()) for x in animal_ids.split(",")]

        # Load performance data
        from .data.loaders import load_performance_data

        if ids_list:
            performance_df = load_performance_data(animal_ids=ids_list)
        else:
            # Get all animals
            animals_df = load_animals_list()
            if animals_df.empty:
                click.echo("No animals found in database")
                return

            all_ids = animals_df["animal_id"].tolist()
            performance_df = load_performance_data(animal_ids=all_ids)

        if performance_df.empty:
            click.echo("No performance data found")
            return

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Generate comparison plot
        save_path = (
            str(output_path / f"animals_comparison_{metric}") if save_plots else None
        )
        fig, ax = plot_animals_comparison(
            performance_df,
            animal_ids=ids_list,
            metric=metric,
            comparison_type=comparison_type,
            save_path=save_path,
        )

        click.echo(f"Created animal comparison plot. Results in: {output_dir}")

    except Exception as e:
        click.echo(f"Error comparing animals: {e}")
        raise click.ClickException(str(e))


@main.command()
def list_animals():
    """List available animals in the database."""
    click.echo("Available animals:")

    try:
        animals_df = load_animals_list()

        if animals_df.empty:
            click.echo("No animals found in database")
            return

        # Display animal information
        for _, animal in animals_df.iterrows():
            animal_id = animal.get("animal_id", "Unknown")
            # Add more fields if available in the animal table
            click.echo(f"  Animal ID: {animal_id}")

        click.echo(f"\nTotal animals: {len(animals_df)}")

    except Exception as e:
        click.echo(f"Error listing animals: {e}")
        raise click.ClickException(str(e))


@main.command()
@click.option(
    "--config-path", type=click.Path(exists=True), help="Path to configuration file"
)
def test_db_connection(config_path):
    """Test database connection."""
    click.echo("Testing database connection...")

    try:
        if config_path:
            click.echo(f"Using config file: {config_path}")

        # Test connection
        success = test_connection()

        if success:
            click.echo("✓ Database connection successful!")
        else:
            click.echo("✗ Database connection failed!")

    except Exception as e:
        click.echo(f"✗ Connection test failed: {e}")
        raise click.ClickException(str(e))


@main.command()
def config_info():
    """Show current configuration information."""
    try:
        config_summary = get_config_summary()
        click.echo(config_summary)
    except Exception as e:
        click.echo(f"Error loading configuration: {e}")
        raise click.ClickException(str(e))


@main.command()
@click.option(
    "--output-path", type=click.Path(), required=True, help="Path to save config file"
)
def create_config(output_path):
    """Create a default configuration file."""
    try:
        config = load_config()
        save_config(config, output_path)
        click.echo(f"Configuration file created at: {output_path}")
        click.echo("Edit this file to customize your settings.")
    except Exception as e:
        click.echo(f"Error creating config file: {e}")
        raise click.ClickException(str(e))


@main.command()
@click.option(
    "--animal-id", type=int, required=True, help="Animal ID to create report for"
)
@click.option(
    "--output-dir",
    type=click.Path(),
    default="./reports",
    help="Output directory for report",
)
@click.option("--from-date", type=str, help="Start date (YYYY-MM-DD)")
@click.option("--to-date", type=str, help="End date (YYYY-MM-DD)")
def generate_report(animal_id, output_dir, from_date, to_date):
    """Generate a comprehensive analysis report for an animal."""
    click.echo(f"Generating comprehensive report for animal {animal_id}...")

    try:
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Load all animal data
        data = load_animal_data(
            animal_id=animal_id,
            from_date=from_date or "",
            to_date=to_date or "",
        )

        if not data:
            click.echo(f"No data found for animal {animal_id}")
            return

        report_dir = output_path / f"animal_{animal_id}_report"
        report_dir.mkdir(exist_ok=True)

        # Generate all available plots
        plots_created = 0

        if "performance" in data and not data["performance"].empty:
            plot_animal_performance(
                data["performance"],
                animal_id=animal_id,
                save_path=str(report_dir / "performance"),
            )
            plots_created += 1

        if "sessions" in data and not data["sessions"].empty:
            plot_sessions_over_time(
                data["sessions"],
                animal_id=animal_id,
                save_path=str(report_dir / "sessions_timeline"),
            )
            plots_created += 1

        # Create summary text file
        summary_file = report_dir / "summary.txt"
        with open(summary_file, "w") as f:
            f.write(f"Ethopy Analysis Report - Animal {animal_id}\n")
            f.write("=" * 50 + "\n\n")

            if "performance" in data:
                perf_df = data["performance"]
                f.write(f"Total sessions analyzed: {len(perf_df)}\n")
                if not perf_df.empty:
                    f.write(
                        f"Average correct rate: {perf_df['correct_rate'].mean():.3f}\n"
                    )
                    f.write(
                        f"Best session performance: {perf_df['correct_rate'].max():.3f}\n"
                    )

            f.write(f"\nPlots generated: {plots_created}\n")
            f.write(f"Report location: {report_dir}\n")

        click.echo(f"Report generated successfully!")
        click.echo(f"Location: {report_dir}")
        click.echo(f"Plots created: {plots_created}")

    except Exception as e:
        click.echo(f"Error generating report: {e}")
        raise click.ClickException(str(e))


if __name__ == "__main__":
    main()
