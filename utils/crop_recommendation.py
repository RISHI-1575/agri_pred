import pandas as pd

def recommend_crops(region, soil, land_area):
    """
    Rule-based Crop Recommendation System.
    Inputs:
        region (str): Region name
        soil (str): Soil type
        land_area (float): Land area in acres
    Output:
        List of recommended crops with expected return, suitability score, and market demand level.
    """

    # Load historical data
    data = pd.read_csv('data/soil_data.csv')  # Ensure this file exists in the data directory

    # Filter by region and soil type
    filtered_data = data[(data['Region'] == region) & (data['Soil'] == soil)]

    # Calculate suitability score and expected return
    filtered_data['SuitabilityScore'] = filtered_data['Suitability'].map({'High': 3, 'Medium': 2, 'Low': 1})
    filtered_data['ExpectedReturn'] = filtered_data['ExpectedYield'] * 100  # Example conversion rate

    # Add market demand level
    demand_mapping = {
        'Wheat': 'High',
        'Rice': 'Medium',
        'Maize': 'High'
    }
    filtered_data['MarketDemand'] = filtered_data['Crop'].map(demand_mapping)

    # Sort crops by suitability score and expected return
    recommended_crops = filtered_data.sort_values(by=['SuitabilityScore', 'ExpectedReturn'], ascending=False)

    # Prepare output
    output = recommended_crops[['Crop', 'ExpectedReturn', 'SuitabilityScore', 'MarketDemand']].to_dict(orient='records')
    return output
