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
    pass

