"""
Machine Learning models for sales prediction
"""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib

class SalesPredictionModels:
    """Manager for multiple sales prediction models"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.results = {}
        
    def train_linear_regression(self, X_train, y_train, X_test, y_test):
        """Train simple linear regression model"""
        # Validate inputs
        if X_train.shape[0] == 0 or X_test.shape[0] == 0:\n            raise ValueError(\"Empty training or test set\")\n        if X_train.shape[1] != X_test.shape[1]:\n            raise ValueError(\"Feature dimension mismatch between train and test\")\n        \n        model = LinearRegression()\n        model.fit(X_train, y_train)
        
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        
        results = self._calculate_metrics(y_train, y_pred_train, y_test, y_pred_test)
        
        self.models['linear'] = model
        self.results['linear'] = results
        return model, results
    
    def train_polynomial_regression(self, X_train, y_train, X_test, y_test, degree=2):
        """Train polynomial regression model"""
        # Create polynomial features
        poly = PolynomialFeatures(degree=degree)
        X_train_poly = poly.fit_transform(X_train)
        X_test_poly = poly.transform(X_test)
        
        model = LinearRegression()
        model.fit(X_train_poly, y_train)
        
        y_pred_train = model.predict(X_train_poly)
        y_pred_test = model.predict(X_test_poly)
        
        results = self._calculate_metrics(y_train, y_pred_train, y_test, y_pred_test)
        
        self.models['polynomial'] = {
            'model': model,
            'poly_features': poly
        }
        self.results['polynomial'] = results
        return model, results
    
    def train_random_forest(self, X_train, y_train, X_test, y_test, n_estimators=100):
        """Train random forest model"""
        model = RandomForestRegressor(
            n_estimators=n_estimators,
            random_state=42,
            max_depth=10,
            min_samples_split=5
        )
        model.fit(X_train, y_train)
        
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        
        results = self._calculate_metrics(y_train, y_pred_train, y_test, y_pred_test)
        
        self.models['random_forest'] = model
        self.results['random_forest'] = results
        return model, results
    
    def train_gradient_boosting(self, X_train, y_train, X_test, y_test, n_estimators=100):
        """Train gradient boosting model"""
        model = GradientBoostingRegressor(
            n_estimators=n_estimators,
            learning_rate=0.1,
            random_state=42,
            max_depth=5
        )
        model.fit(X_train, y_train)
        
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        
        results = self._calculate_metrics(y_train, y_pred_train, y_test, y_pred_test)
        
        self.models['gradient_boosting'] = model
        self.results['gradient_boosting'] = results
        return model, results
    
    def _calculate_metrics(self, y_train, y_pred_train, y_test, y_pred_test):
        """Calculate performance metrics"""
        return {
            'train_mse': mean_squared_error(y_train, y_pred_train),
            'test_mse': mean_squared_error(y_test, y_pred_test),
            'train_rmse': np.sqrt(mean_squared_error(y_train, y_pred_train)),
            'test_rmse': np.sqrt(mean_squared_error(y_test, y_pred_test)),
            'train_mae': mean_absolute_error(y_train, y_pred_train),
            'test_mae': mean_absolute_error(y_test, y_pred_test),
            'train_r2': r2_score(y_train, y_pred_train),
            'test_r2': r2_score(y_test, y_pred_test)
        }
    
    def get_best_model(self):
        """Get model with best test R² score"""
        best_model_name = max(
            self.results.keys(),
            key=lambda x: self.results[x]['test_r2']
        )
        return best_model_name, self.results[best_model_name]
    
    def predict(self, model_name, X):
        """Make predictions using specified model"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not trained yet")
        if model_name == 'polynomial':
            poly = self.models[model_name]['poly_features']
            X_poly = poly.transform(X)
            predictions = self.models[model_name]['model'].predict(X_poly)
        else:
            predictions = self.models[model_name].predict(X)
        return predictions
    
    def get_feature_importance(self, model_name):
        """Get feature importance for tree-based models"""
        if model_name not in self.models:
            return None
        model = self.models[model_name]
        if hasattr(model, 'feature_importances_'):
            importance = model.feature_importances_
            if importance is not None and len(importance) > 0:
                return importance
        return None
    
    def save_model(self, model_name, filepath):
        """Save model to file"""
        joblib.dump(self.models[model_name], filepath)
    
    def load_model(self, model_name, filepath):
        """Load model from file"""
        self.models[model_name] = joblib.load(filepath)

if __name__ == "__main__":
    from data_handler import generate_sales_data, prepare_data
    
    # Generate and prepare data
    data = generate_sales_data(n_samples=300)
    prepared_data = prepare_data(data)
    
    # Train models
    models_manager = SalesPredictionModels()
    
    print("Training models...")
    models_manager.train_linear_regression(
        prepared_data['X_train'],
        prepared_data['y_train'],
        prepared_data['X_test'],
        prepared_data['y_test']
    )
    print("✓ Linear Regression trained")
    
    models_manager.train_polynomial_regression(
        prepared_data['X_train'],
        prepared_data['y_train'],
        prepared_data['X_test'],
        prepared_data['y_test']
    )
    print("✓ Polynomial Regression trained")
    
    models_manager.train_random_forest(
        prepared_data['X_train'],
        prepared_data['y_train'],
        prepared_data['X_test'],
        prepared_data['y_test']
    )
    print("✓ Random Forest trained")
    
    models_manager.train_gradient_boosting(
        prepared_data['X_train'],
        prepared_data['y_train'],
        prepared_data['X_test'],
        prepared_data['y_test']
    )
    print("✓ Gradient Boosting trained")
    
    # Display results
    print("\n" + "="*60)
    print("MODEL PERFORMANCE COMPARISON")
    print("="*60)
    for model_name, metrics in models_manager.results.items():
        print(f"\n{model_name.upper().replace('_', ' ')}")
        print(f"  Train R²: {metrics['train_r2']:.4f}")
        print(f"  Test R²:  {metrics['test_r2']:.4f}")
        print(f"  Test RMSE: {metrics['test_rmse']:.4f}")
        print(f"  Test MAE:  {metrics['test_mae']:.4f}")
    
    best_model, best_results = models_manager.get_best_model()
    print(f"\n{'='*60}")
    print(f"BEST MODEL: {best_model.upper().replace('_', ' ')}")
    print(f"Test R² Score: {best_results['test_r2']:.4f}")
    print(f"{'='*60}")
