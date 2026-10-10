import csv

def get_data(file_name,
             query_column=None,
             query_value=None,
             return_header=False):
    
    """
    Read a CSV file and optionally filter rows by a query.

    Parameters:
    ----------
    file_name : str or Path
        Path to the input CSV file.
    query_column : str or int, optional
        Column name or zero-based column index.
    query_value : str, optional
        Exact value to match in the query column.
    return_header : bool, optional
        Whether to include the header in the output.

    Returns:
    -------
    list
        CSV rows as lists of strings. If return_header
        is True, the header is the first returned row.

    Raises:
    ------
    SystemExit
        Code 1 for an empty file.
        Code 2 for incomplete or invalid queries.
    """

    # Check whether exactly one query argument is missing.
    if (query_column is None) != (query_value is None):
        raise SystemExit(2)

    # Read the CSV file.
    with open(file_name, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        data = list(reader)

    # Check for an empty file or a header-only file.
    if len(data) <= 1:
        raise SystemExit(1)

    # Separate header and data rows.
    header = data[0]
    rows = data[1:]

    # Filter rows if a complete query was provided.
    if query_column is not None:

        # Identify the column index.
        if isinstance(query_column, int):
            column_index = query_column

        elif isinstance(query_column, str):
            try:
                column_index = header.index(query_column)
            except ValueError:
                raise SystemExit(2)

        else:
            raise SystemExit(2)

        # Verify that the index is valid.
        if not 0 <= column_index < len(header):
            raise SystemExit(2)

        # Select matching rows.
        rows = [row for row in rows if row[column_index] == query_value]

    # Optionally include the header.
    if return_header:
        return [header] + rows

    return rows
    pass

def get_column_index(header, column_name):
    """
    Return the index of a specified column in a header.

    Parameters:
    ----------
    header : list
        List of column names.
    column_name : str
        Name of the column to locate.

    Returns:
    -------
    int or None
        Zero-based index of the column if found,
        otherwise None.
    """

    try:
        return header.index(column_name)

    except ValueError:
        return None
    
    pass


def get_fire_gdp_year_data(co2_file, gdp_file, country):
    """
    Combine forest-fire emissions and GDP by country and year.

    Parameters
    ----------
    co2_file : str or Path
        Path to the forest-fire emissions CSV file.
    gdp_file : str or Path
        Path to the GDP CSV file.
    country : str
        Country name to query.

    Returns
    -------
    list
        List of [year, forest_fires, gdp] entries.
        Years are integers; emissions and GDP are floats.
        Years with missing values are excluded.
    """

    # Retrieve CO2 data for the selected country.
    co2_data = get_data(
        co2_file,
        query_column="Area",
        query_value=country,
        return_header=True
    )

    # Retrieve GDP data for the selected country.
    gdp_data = get_data(
        gdp_file,
        query_column="Country",
        query_value=country,
        return_header=True
    )

    # Separate headers and data.
    co2_header = co2_data[0]
    co2_rows = co2_data[1:]

    gdp_header = gdp_data[0]
    gdp_rows = gdp_data[1:]

    # Return an empty list if the country was not found.
    if not co2_rows or not gdp_rows:
        return []

    # GDP file has one row per country.
    gdp_row = gdp_rows[0]

    # Locate necessary CO2 columns.
    fires_index = get_column_index(
        co2_header, "Forest fires"
    )

    year_index = get_column_index(
        co2_header, "Year"
    )

    # Check that required columns exist.
    if fires_index is None or year_index is None:
        return []

    # Store matching observations.
    result = []

    for row in co2_rows:

        # Extract year and forest-fire emissions.
        year = row[year_index]
        fires = row[fires_index]

        # Locate the corresponding GDP year column.
        gdp_index = get_column_index(
            gdp_header, year
        )

        # Skip years absent from the GDP dataset.
        if gdp_index is None:
            continue

        # Retrieve GDP for that year.
        gdp = gdp_row[gdp_index]

        # Skip incomplete observations.
        if fires.strip() == "" or gdp.strip() == "":
            continue

        # Convert to numerical values.
        year = int(year)
        fires = float(fires)
        gdp = float(gdp)

        # Append the matching observation.
        result.append([year, fires, gdp])

    return result
    pass

