"""
Quick Setup & Validation Script
Run this to ensure all components are working correctly
"""
import sys
import os

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"✗ Python version too old: {version.major}.{version.minor}")
        return False

def check_packages():
    """Check if required packages are installed"""
    required = [
        'numpy', 'pandas', 'sklearn', 'matplotlib',
        'seaborn', 'PIL', 'joblib'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} (MISSING)")
            missing.append(package)
    
    return len(missing) == 0, missing

def check_files():
    """Check if all required files exist"""
    files = [
        'requirements.txt',
        'data_handler.py',
        'models.py',
        'gui_app.py',
        'comprehensive_sales_prediction.ipynb',
        'README.md'
    ]
    
    all_exist = True
    for file in files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} (MISSING)")
            all_exist = False
    
    return all_exist

def test_imports():
    """Test if modules can be imported"""
    try:
        import data_handler
        print("✓ data_handler module")
    except Exception as e:
        print(f"✗ data_handler module: {e}")
        return False
    
    try:
        import models
        print("✓ models module")
    except Exception as e:
        print(f"✗ models module: {e}")
        return False
    
    return True

def generate_sample_data():
    """Generate and test sample data"""
    try:
        from data_handler import generate_sales_data, prepare_data
        
        print("\nGenerating sample data...")
        data = generate_sales_data(n_samples=100)
        prepared = prepare_data(data)
        
        print(f"✓ Generated {len(data)} records")
        print(f"✓ Features: {prepared['feature_names']}")
        return True
    except Exception as e:
        print(f"✗ Error generating data: {e}")
        return False

def train_sample_models():
    """Train and test sample models"""
    try:
        from data_handler import generate_sales_data, prepare_data
        from models import SalesPredictionModels
        
        print("\nTraining sample models...")
        data = generate_sales_data(n_samples=100)
        prepared = prepare_data(data)
        
        manager = SalesPredictionModels()
        manager.train_linear_regression(
            prepared['X_train'],
            prepared['y_train'],
            prepared['X_test'],
            prepared['y_test']
        )
        print("✓ Linear Regression")
        
        manager.train_random_forest(
            prepared['X_train'],
            prepared['y_train'],
            prepared['X_test'],
            prepared['y_test']
        )
        print("✓ Random Forest")
        
        manager.train_gradient_boosting(
            prepared['X_train'],
            prepared['y_train'],
            prepared['X_test'],
            prepared['y_test']
        )
        print("✓ Gradient Boosting")
        
        best_model, metrics = manager.get_best_model()
        print(f"✓ Best model: {best_model} (R² = {metrics['test_r2']:.4f})")
        
        return True
    except Exception as e:
        print(f"✗ Error training models: {e}")
        return False

def main():
    """Run all checks"""
    print("\n" + "="*60)
    print("SALES PREDICTION SYSTEM - SETUP VALIDATION")
    print("="*60)
    
    print("\n1. CHECKING PYTHON VERSION...")
    print("-"*60)
    python_ok = check_python_version()
    
    print("\n2. CHECKING REQUIRED PACKAGES...")
    print("-"*60)
    packages_ok, missing = check_packages()
    if not packages_ok:
        print(f"\nInstall missing packages with:")
        print(f"pip install {' '.join(missing)}")
    
    print("\n3. CHECKING PROJECT FILES...")
    print("-"*60)
    files_ok = check_files()
    
    print("\n4. TESTING MODULE IMPORTS...")
    print("-"*60)
    imports_ok = test_imports()
    
    print("\n5. TESTING DATA GENERATION...")
    print("-"*60)
    data_ok = generate_sample_data()
    
    print("\n6. TESTING MODEL TRAINING...")
    print("-"*60)
    models_ok = train_sample_models()
    
    # Summary
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    
    all_ok = python_ok and packages_ok and files_ok and imports_ok and data_ok and models_ok
    
    if all_ok:
        print("✓ All checks passed! System is ready.")
        print("\nNEXT STEPS:")
        print("1. Run the GUI: python gui_app.py")
        print("2. Or run Jupyter: jupyter notebook comprehensive_sales_prediction.ipynb")
        print("3. Or train models: python models.py")
    else:
        print("✗ Some checks failed. Please review the output above.")
    
    print("="*60 + "\n")
    
    return all_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
