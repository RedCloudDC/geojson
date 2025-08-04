import sys
import pandas as pd
import geojson
from shapely.geometry import Polygon
from shapely.validation import explain_validity

def main():
    if len(sys.argv) != 3:
        print("Usage: python csv_to_geojson.py <input_csv> <output_geojson>")
        sys.exit(1)
    
    input_csv = sys.argv[1]
    output_geojson = sys.argv[2]
    
    # Read CSV file
    df = pd.read_csv(input_csv)
    
    # Calculate grouping key
    df['group_key'] = df['LOCATION_ID'].astype(str) + '_' + df['ALTITUDE'].astype(str) + '_' + df['TYPE'].astype(str)
    
    # Group by the key and sort by POINT_SEQ
    grouped = df.groupby('group_key')
    
    features = []
    valid_features = 0
    invalid_features = 0
    
    for name, group in grouped:
        sorted_group = group.sort_values('POINT_SEQ')
        
        # Extract lat/lon as list of [lon, lat]
        coordinates = [list(coord) for coord in sorted_group[['LONG_DECIMAL', 'LAT_DECIMAL']].to_numpy()]
        
        # Ensure the polygon is closed
        if coordinates[0] != coordinates[-1]:
            coordinates.append(coordinates[0])
    
        # Helper function to convert pandas/numpy types to native Python types
        def convert_to_native(value):
            if pd.isna(value):
                return None
            elif hasattr(value, 'item'):  # numpy scalar
                return value.item()
            else:
                return value
        
        # Build GeoJSON Feature
        properties = {
            "LOCATION_ID": convert_to_native(sorted_group.iloc[0]['LOCATION_ID']),
            "LOCATION_NAME": convert_to_native(sorted_group.iloc[0]['LOCATION_NAME']),
            "ALTITUDE": convert_to_native(sorted_group.iloc[0]['ALTITUDE']),
            "TYPE": convert_to_native(sorted_group.iloc[0]['TYPE'])
        }
        
        # Add all other columns
        for col in df.columns:
            if col not in properties and col not in ['LONG_DECIMAL', 'LAT_DECIMAL', 'POINT_SEQ', 'group_key']:
                properties[col] = convert_to_native(sorted_group.iloc[0][col])
    
        feature = geojson.Feature(geometry=geojson.Polygon([coordinates]), properties=properties)
        
        # Validate the feature using shapely
        is_valid_feature = True
        try:
            # Test if the GeoJSON feature can be serialized (basic validity check)
            geojson.dumps(feature)
            
            # Validate using shapely
            shapely_polygon = Polygon(coordinates)
            is_valid_shapely = shapely_polygon.is_valid
            if not is_valid_shapely:
                print(f"Warning: Invalid polygon for {name}: {explain_validity(shapely_polygon)}")
                is_valid_feature = False
        except Exception as e:
            print(f"Warning: Could not validate feature for {name}: {e}")
            is_valid_feature = False
        
        if is_valid_feature:
            valid_features += 1
        else:
            invalid_features += 1
        
        features.append(feature)
    
    # Build FeatureCollection
    feature_collection = geojson.FeatureCollection(features)
    
    # Validate the entire FeatureCollection
    try:
        geojson.dumps(feature_collection)
        is_valid_collection = True
    except Exception as e:
        print(f"Warning: Invalid FeatureCollection: {e}")
        is_valid_collection = False
    
    # Write to GeoJSON file
    with open(output_geojson, 'w') as f:
        geojson.dump(feature_collection, f, indent=2)
    
    # Print summary
    print(f"\n=== CONVERSION SUMMARY ===")
    print(f"Input CSV: {input_csv}")
    print(f"Output GeoJSON: {output_geojson}")
    print(f"Total features: {len(features)}")
    print(f"Valid features: {valid_features}")
    print(f"Invalid features: {invalid_features}")
    print(f"FeatureCollection valid: {is_valid_collection}")
    
    # Print sample coordinates from first few features
    print(f"\n=== SAMPLE COORDINATES ===")
    for i, feature in enumerate(features[:3]):
        coords = feature['geometry']['coordinates'][0]  # First ring of polygon
        print(f"Feature {i+1} ({feature['properties'].get('LOCATION_NAME', 'Unknown')}):")  
        print(f"  First coordinate: [{coords[0][0]:.6f}, {coords[0][1]:.6f}]")
        print(f"  Last coordinate: [{coords[-1][0]:.6f}, {coords[-1][1]:.6f}]")
        print(f"  Total points: {len(coords)}")
    
    if len(features) > 3:
        print(f"  ... and {len(features) - 3} more features")

if __name__ == "__main__":
    main()
