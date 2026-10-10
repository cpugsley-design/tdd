import argparse
import sys
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
from fire_gdp import get_fire_gdp_year_data

matplotlib.use("Agg")


def create_scatterplot(co2_file, gdp_file, country, output):
    """
    Generate a scatterplot of forest-fire emissions versus GDP.

    Parameters
    ----------
    co2_file : str
        Path to the CO2 emissions CSV file.
    gdp_file : str
        Path to the GDP CSV file.
    country : str
        Country to analyze.
    output : str
        Path where the plot should be saved.

    Returns
    -------
    int
        0 if successful, 1 if an error occurs.
    """

    try:
        data = get_fire_gdp_year_data(
            co2_file, gdp_file, country
        )

    except (FileNotFoundError, OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    # Verify that matching observations were found.
    if not data:
        print(
            f"Error: no matching data found for '{country}'.",
            file=sys.stderr
        )
        return 1

    # Separate the results into plotting variables.
    years = [row[0] for row in data]
    fires = [row[1] for row in data]
    gdp = [row[2] for row in data]

    # Create the figure.
    fig, ax = plt.subplots(figsize=(7, 5))

    ax.scatter(gdp, fires, alpha=0.7)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.set_xlabel("GDP (millions of local currency units)")
    ax.set_ylabel("Forest-fire emissions")
    ax.set_title(
        f"{country}: Forest-fire emissions vs. GDP"
    )

    ax.grid(alpha=0.2)

    # Indicate the number of matched observations.
    ax.text(
        0.98, 0.02,
        f"n = {len(years)}",
        transform=ax.transAxes,
        ha="right",
        va="bottom"
    )

    # Create the output directory if necessary.
    output_path = Path(output)
    output_path.parent.mkdir(
        parents=True, exist_ok=True
    )

    try:
        fig.savefig(
            output_path,
            dpi=300,
            bbox_inches="tight"
        )

    except (OSError, ValueError) as error:
        print(f"Error saving plot: {error}", file=sys.stderr)
        return 1

    finally:
        plt.close(fig)

    print(
        f"Saved {len(data)} observations for "
        f"{country} to {output_path}"
    )

    return 0


def main():
    """Parse command-line arguments and generate the plot."""

    parser = argparse.ArgumentParser(
        description=(
            "Plot forest-fire emissions versus GDP "
            "for a selected country."
        )
    )

    parser.add_argument(
        "--co2_file",
        type=str,
        required=True,
        help="Path to the CO2 emissions CSV file."
    )

    parser.add_argument(
        "--gdp_file",
        type=str,
        required=True,
        help="Path to the GDP CSV file."
    )

    parser.add_argument(
        "--country",
        type=str,
        required=True,
        help="Country to analyze."
    )

    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output image path."
    )

    args = parser.parse_args()

    return create_scatterplot(
        args.co2_file,
        args.gdp_file,
        args.country,
        args.output
    )


if __name__ == "__main__":
    sys.exit(main())
