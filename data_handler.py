"""
Data generation and preprocessing for sales prediction
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

def generate_sales_data(n_samples=200, random_state=42):
    """
    Generate synthetic sales data with realistic relationships
    
    Features:
    - TV: Advertising expenditure on TV (in thousands of dollars)
    - Radio: Advertising expenditure on Radio (in thousands of dollars)
    - Social Media: Advertising expenditure on Social Media (in thousands of dollars)
    - Target: Sales (in thousands of units)
    """
    np.random.seed(random_state)
    
    # Generate features
    tv = np.random.uniform(0, 300, n_samples)
    radio = np.random.uniform(0, 40, n_samples)
    social_media = np.random.uniform(0, 60, n_samples)
    
    # Generate realistic sales with non-linear relationships
    sales = (
        0.05 * tv +
        1.1 * radio +
        0.9 * social_media +
        0.03 * tv * radio +  # interaction effect
        np.random.normal(0, 3, n_samples)  # noise
    )
    
    sales = np.maximum(sales, 0)  # ensure non-negative
    
    # Create DataFrame
    data = pd.DataFrame({
        'TV': tv,
        'Radio': radio,
        'Social Media': social_media,
        'Sales': sales
    })
    
    return data

def load_or_create_data(filepath='sales_data.csv', create=True):
    """Load existing data or create new data"""
    import os
    try:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File {filepath} not found")
        data = pd.read_csv(filepath)
        if data.empty:
            raise ValueError(f"Data file {filepath} is empty")
        # Validate required columns
        required_cols = ['TV', 'Radio', 'Social Media', 'Sales']
        if not all(col in data.columns for col in required_cols):
            raise ValueError(f"Missing required columns. Need: {required_cols}")
        print(f"Loaded data from {filepath}")
        return data
    except (FileNotFoundError, ValueError, pd.errors.EmptyDataError) as e:
        if create:
            print(f"Creating new synthetic data... ({str(e)})")
            data = generate_sales_data()
            try:
                data.to_csv(filepath, index=False)
                print(f"Data saved to {filepath}")
            except IOError as io_err:
                print(f"Warning: Could not save data to file: {io_err}")
            return data
        else:
            raise

def prepare_data(data, test_size=0.2, random_state=42):
    """Prepare data for modeling"""
    X = data[['TV', 'Radio', 'Social Media']]
    y = data['Sales']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return {
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'X_train_scaled': X_train_scaled,
        'X_test_scaled': X_test_scaled,
        'scaler': scaler,
        'feature_names': ['TV', 'Radio', 'Social Media']
    }

def get_data_statistics(data):
    """Get descriptive statistics"""
    return data.describe().to_dict()

if __name__ == "__main__":
    # Test data generation
    data = generate_sales_data(n_samples=300)
    print("Generated Sales Data:")
    print(data.head())
    print("\nStatistics:")
    print(data.describe())
    
    # Test preparation
    prepared = prepare_data(data)
    print(f"\nTraining set size: {len(prepared['X_train'])}")
    print(f"Test set size: {len(prepared['X_test'])}")
