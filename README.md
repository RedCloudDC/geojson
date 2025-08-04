# ARTCC Boundaries GeoJSON Converter

This project converts CSV data containing coordinate points into GeoJSON format, specifically designed for processing Air Route Traffic Control Center (ARTCC) boundary data.

## Overview

The script processes CSV files containing coordinate points and groups them by location, altitude, and type to create polygon features in GeoJSON format. It includes validation features to ensure the generated polygons are geometrically valid.

## Project Structure

```
.
├── README.md                    # This file
├── requirements.txt            # Python dependencies
├── scripts/
│   └── csv_to_geojson.py      # Main conversion script
└── data/
    └── artcc_boundaries.geojson # Generated output file
```

## Features

- **CSV to GeoJSON Conversion**: Converts coordinate points from CSV to polygon features in GeoJSON
- **Automatic Grouping**: Groups points by LOCATION_ID, ALTITUDE, and TYPE
- **Polygon Validation**: Uses Shapely to validate polygon geometry
- **Data Type Handling**: Properly converts pandas/numpy data types to JSON-serializable formats
- **Comprehensive Reporting**: Provides detailed conversion summaries and validation results

## Requirements

The script requires Python 3.6+ and the following dependencies:

- geojson==3.2.0
- numpy==2.3.2
- pandas==2.3.1
- shapely==2.1.1
- python-dateutil==2.9.0.post0
- pytz==2025.2
- six==1.17.0
- tzdata==2025.2

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd geojson
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```bash
python scripts/csv_to_geojson.py <input_csv> <output_geojson>
```

### Example

```bash
python scripts/csv_to_geojson.py input_data.csv data/artcc_boundaries.geojson
```

### Input CSV Format

The input CSV file should contain the following columns:

- **LOCATION_ID**: Identifier for the location/boundary
- **LOCATION_NAME**: Human-readable name for the location
- **ALTITUDE**: Altitude information for the boundary
- **TYPE**: Type classification of the boundary
- **LAT_DECIMAL**: Latitude in decimal degrees
- **LONG_DECIMAL**: Longitude in decimal degrees
- **POINT_SEQ**: Sequential point number for ordering coordinates

Additional columns will be preserved as properties in the output GeoJSON.

### Output Format

The script generates a GeoJSON FeatureCollection where each feature represents a polygon boundary with:

- **Geometry**: Polygon coordinates (automatically closed if not already)
- **Properties**: All non-coordinate columns from the input CSV

### Validation Features

The script includes comprehensive validation:

- **Polygon Closure**: Automatically closes polygons if the first and last points don't match
- **Shapely Validation**: Uses Shapely library to validate polygon geometry
- **GeoJSON Validation**: Ensures output can be properly serialized as GeoJSON
- **Error Reporting**: Provides detailed warnings for invalid geometries

### Output Summary

After conversion, the script provides:

- Total number of features processed
- Count of valid vs invalid features
- Sample coordinate information from the first few features
- Validation status of the entire FeatureCollection

## Example Output Summary

```
=== CONVERSION SUMMARY ===
Input CSV: input_data.csv
Output GeoJSON: data/artcc_boundaries.geojson
Total features: 125
Valid features: 123
Invalid features: 2
FeatureCollection valid: True

=== SAMPLE COORDINATES ===
Feature 1 (Boston ARTCC):
  First coordinate: [-71.234567, 42.123456]
  Last coordinate: [-71.234567, 42.123456]
  Total points: 45
...
```

## Troubleshooting

### Common Issues

1. **Invalid Polygons**: If you see validation warnings, check that your coordinate points form valid closed polygons.

2. **Missing Dependencies**: Ensure all required packages are installed with `pip install -r requirements.txt`.

3. **Data Type Errors**: The script handles pandas/numpy data types automatically, but ensure your CSV has proper numeric values for coordinates.

### File Path Issues

Make sure to use the correct paths when running the script. The script accepts both relative and absolute paths for input and output files.

## Contributing

When contributing to this project:

1. Ensure your code follows the existing style
2. Add appropriate error handling and validation
3. Update this README if you add new features
4. Test with various CSV formats to ensure compatibility

## License

[Add your license information here]
