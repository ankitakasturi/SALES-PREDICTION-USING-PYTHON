"""
Professional GUI Application for Sales Prediction
"""
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Check for required third-party packages and provide a helpful error if missing
try:
    import numpy as np
    import pandas as pd
    from data_handler import generate_sales_data, prepare_data, load_or_create_data
    from models import SalesPredictionModels
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
except ModuleNotFoundError as e:
    missing = getattr(e, 'name', str(e))
    root = tk.Tk()
    root.withdraw()
    message = (
        f"Required Python package '{missing}' is not installed.\n\n"
        "Install dependencies with:\n    pip install -r requirements.txt\n\n"
        "Then re-run this application."
    )
    messagebox.showerror("Missing dependency", message)
    sys.exit(1)

class SalesPredictionGUI:
    """Professional GUI for sales prediction"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sales Prediction System - Machine Learning")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('Title.TLabel', background='#f0f0f0', font=('Arial', 14, 'bold'))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TNotebook', background='#f0f0f0')
        self.style.map('TButton', background=[('active', '#0078d4')])
        
        # Initialize data and models
        self.data = None
        self.prepared_data = None
        self.models_manager = None
        self.best_model = None
        
        # Create UI
        self.create_widgets()
        self.load_data_and_models()
        
    def create_widgets(self):
        """Create GUI widgets"""
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        header_label = ttk.Label(
            header_frame,
            text="🚀 Sales Prediction System",
            style='Title.TLabel'
        )
        header_label.pack(side=tk.LEFT)
        
        subtitle = ttk.Label(
            header_frame,
            text="Predict sales based on advertising expenditure",
            font=('Arial', 10),
            foreground='#666'
        )
        subtitle.pack(side=tk.LEFT, padx=20)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Prediction
        self.create_prediction_tab()
        
        # Tab 2: Model Comparison
        self.create_comparison_tab()
        
        # Tab 3: Analytics
        self.create_analytics_tab()
        
        # Tab 4: About
        self.create_about_tab()
        
    def create_prediction_tab(self):
        """Create prediction tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Prediction")
        
        # Left side: Input
        left_frame = ttk.Frame(frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(left_frame, text="Enter Advertising Expenditure", style='Title.TLabel').pack(pady=10)
        
        # TV Input
        ttk.Label(left_frame, text="TV Advertising (in $1000s):").pack(anchor=tk.W, pady=(10, 5))
        self.tv_var = tk.DoubleVar(value=100)
        tv_scale = ttk.Scale(
            left_frame, from_=0, to=300, variable=self.tv_var,
            orient=tk.HORIZONTAL, command=self.update_prediction
        )
        tv_scale.pack(fill=tk.X, pady=(0, 5))
        self.tv_label = ttk.Label(left_frame, text="$100k")
        self.tv_label.pack(anchor=tk.W)
        
        # Radio Input
        ttk.Label(left_frame, text="Radio Advertising (in $1000s):").pack(anchor=tk.W, pady=(15, 5))
        self.radio_var = tk.DoubleVar(value=20)
        radio_scale = ttk.Scale(
            left_frame, from_=0, to=40, variable=self.radio_var,
            orient=tk.HORIZONTAL, command=self.update_prediction
        )
        radio_scale.pack(fill=tk.X, pady=(0, 5))
        self.radio_label = ttk.Label(left_frame, text="$20k")
        self.radio_label.pack(anchor=tk.W)
        
        # Social Media Input
        ttk.Label(left_frame, text="Social Media Advertising (in $1000s):").pack(anchor=tk.W, pady=(15, 5))
        self.social_media_var = tk.DoubleVar(value=30)
        social_scale = ttk.Scale(
            left_frame, from_=0, to=60, variable=self.social_media_var,
            orient=tk.HORIZONTAL, command=self.update_prediction
        )
        social_scale.pack(fill=tk.X, pady=(0, 5))
        self.social_media_label = ttk.Label(left_frame, text="$30k")
        self.social_media_label.pack(anchor=tk.W)
        
        # Button frame
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(pady=20, fill=tk.X)
        
        ttk.Button(button_frame, text="Predict Sales", command=self.predict_sales).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset_inputs).pack(side=tk.LEFT, padx=5)
        
        # Right side: Results
        right_frame = ttk.Frame(frame, relief=tk.SUNKEN, borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(right_frame, text="Prediction Results", style='Title.TLabel').pack(pady=10)
        
        self.result_text = tk.Text(right_frame, height=20, width=40, font=('Courier', 10))
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(right_frame, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        
    def create_comparison_tab(self):
        """Create model comparison tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Model Comparison")
        
        ttk.Label(frame, text="Model Performance Metrics", style='Title.TLabel').pack(pady=10)
        
        # Table frame
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview
        columns = ('Model', 'Train R²', 'Test R²', 'Test RMSE', 'Test MAE')
        self.comparison_tree = ttk.Treeview(table_frame, columns=columns, height=8, show='headings')
        
        # Define column headings and widths
        for col in columns:
            self.comparison_tree.heading(col, text=col)
            self.comparison_tree.column(col, width=180)
        
        self.comparison_tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, command=self.comparison_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.comparison_tree.config(yscrollcommand=scrollbar.set)
        
        # Refresh button
        ttk.Button(frame, text="Refresh Comparison", command=self.update_comparison).pack(pady=10)
        
    def create_analytics_tab(self):
        """Create analytics tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Analytics")
        
        ttk.Label(frame, text="Data Visualization", style='Title.TLabel').pack(pady=10)
        
        # Create figure with proper cleanup
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.fig.subplots_adjust(hspace=0.3, wspace=0.3)
        
        # Button frame
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Plot Data Distribution", 
                   command=self.plot_distribution).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Plot Correlations",
                   command=self.plot_correlations).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Plot Feature Importance",
                   command=self.plot_feature_importance).pack(side=tk.LEFT, padx=5)
        
    def create_about_tab(self):
        """Create about tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="About")
        
        about_text = """
        📊 SALES PREDICTION SYSTEM
        ═══════════════════════════════════════
        
        Version: 1.0
        
        DESCRIPTION:
        This application uses machine learning algorithms to predict
        sales based on advertising expenditure across multiple channels.
        
        FEATURES:
        • Multiple ML Models (Linear, Polynomial, Random Forest, Gradient Boosting)
        • Real-time Predictions
        • Model Performance Comparison
        • Data Visualization
        • Feature Importance Analysis
        
        MODELS INCLUDED:
        1. Linear Regression - Simple baseline model
        2. Polynomial Regression - Captures non-linear relationships
        3. Random Forest - Ensemble method with feature importance
        4. Gradient Boosting - Advanced ensemble technique
        
        INPUT FEATURES:
        • TV Advertising Expenditure (in $1000s)
        • Radio Advertising Expenditure (in $1000s)
        • Social Media Advertising Expenditure (in $1000s)
        
        OUTPUT:
        • Predicted Sales (in $1000s of units)
        • Confidence Metrics
        • Comparison across all models
        
        HOW TO USE:
        1. Go to 'Prediction' tab
        2. Adjust advertising sliders
        3. Click 'Predict Sales'
        4. View predictions in the results panel
        5. Compare models in 'Model Comparison' tab
        6. Analyze data in 'Analytics' tab
        
        MACHINE LEARNING APPROACH:
        • Data: 300 synthetic samples with realistic relationships
        • Train-Test Split: 80-20
        • Feature Scaling: StandardScaler
        • Hyperparameter Tuning: Grid Search Optimized
        
        © 2024 Sales Prediction System
        """
        
        text_widget = tk.Text(frame, wrap=tk.WORD, font=('Courier', 10), 
                              bg='#f9f9f9', height=30)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(1.0, about_text)
        text_widget.config(state=tk.DISABLED)
        
    def load_data_and_models(self):
        """Load data and train models"""
        try:
            # Load or generate data
            self.data = load_or_create_data('sales_data.csv')
            self.prepared_data = prepare_data(self.data)
            
            # Train models
            self.models_manager = SalesPredictionModels()
            
            self.models_manager.train_linear_regression(
                self.prepared_data['X_train'],
                self.prepared_data['y_train'],
                self.prepared_data['X_test'],
                self.prepared_data['y_test']
            )
            
            self.models_manager.train_polynomial_regression(
                self.prepared_data['X_train'],
                self.prepared_data['y_train'],
                self.prepared_data['X_test'],
                self.prepared_data['y_test']
            )
            
            self.models_manager.train_random_forest(
                self.prepared_data['X_train'],
                self.prepared_data['y_train'],
                self.prepared_data['X_test'],
                self.prepared_data['y_test']
            )
            
            self.models_manager.train_gradient_boosting(
                self.prepared_data['X_train'],
                self.prepared_data['y_train'],
                self.prepared_data['X_test'],
                self.prepared_data['y_test']
            )
            
            self.best_model, _ = self.models_manager.get_best_model()
            
            self.update_comparison()
            messagebox.showinfo("Success", "Models trained successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data/models: {str(e)}")
    
    def update_prediction(self, value=None):
        """Update labels on slider movement"""
        self.tv_label.config(text=f"${self.tv_var.get():.0f}k")
        self.radio_label.config(text=f"${self.radio_var.get():.0f}k")
        self.social_media_label.config(text=f"${self.social_media_var.get():.0f}k")
    
    def predict_sales(self):
        """Make predictions"""
        try:
            if self.models_manager is None or not self.models_manager.models:
                messagebox.showwarning("Warning", "Models not loaded yet")
                return
            
            # Validate input values
            tv = self.tv_var.get()
            radio = self.radio_var.get()
            social_media = self.social_media_var.get()
            
            if tv < 0 or radio < 0 or social_media < 0:
                messagebox.showerror("Error", "Input values cannot be negative")
                return
            
            # Get input values
            input_data = np.array([[
                tv,
                radio,
                social_media
            ]])
            
            # Make predictions
            results = "="*50 + "\n"
            results += "PREDICTION RESULTS\n"
            results += "="*50 + "\n\n"
            
            results += "INPUT:\n"
            results += f"  TV Advertising:          ${self.tv_var.get():.2f}k\n"
            results += f"  Radio Advertising:       ${self.radio_var.get():.2f}k\n"
            results += f"  Social Media Advertising: ${self.social_media_var.get():.2f}k\n\n"
            
            results += "PREDICTIONS:\n"
            results += "-"*50 + "\n"
            
            for model_name in ['linear', 'polynomial', 'random_forest', 'gradient_boosting']:
                pred = self.models_manager.predict(model_name, input_data)[0]
                model_results = self.models_manager.results[model_name]
                
                display_name = model_name.upper().replace('_', ' ')
                results += f"\n{display_name}:\n"
                results += f"  Predicted Sales: ${pred:.2f}k units\n"
                results += f"  Model R² Score:  {model_results['test_r2']:.4f}\n"
            
            results += "\n" + "="*50 + "\n"
            results += f"BEST MODEL: {self.best_model.upper().replace('_', ' ')}\n"
            best_pred = self.models_manager.predict(self.best_model, input_data)[0]
            results += f"RECOMMENDED SALES: ${best_pred:.2f}k units\n"
            results += "="*50
            
            # Display results
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, results)
            self.result_text.config(state=tk.DISABLED)
            
            # Close any open matplotlib figures to prevent memory leak
            plt.close('all')
            
        except Exception as e:
            messagebox.showerror("Error", f"Prediction error: {str(e)}")
    
    def reset_inputs(self):
        """Reset input values"""
        self.tv_var.set(100)
        self.radio_var.set(20)
        self.social_media_var.set(30)
        self.update_prediction()
    
    def update_comparison(self):
        """Update model comparison table"""
        try:
            if self.models_manager is None or not self.models_manager.results:
                messagebox.showwarning("Warning", "Models not trained yet")
                return
            # Clear existing items
            for item in self.comparison_tree.get_children():
                self.comparison_tree.delete(item)
            
            # Add data
            for model_name, metrics in self.models_manager.results.items():
                display_name = model_name.upper().replace('_', ' ')
                self.comparison_tree.insert('', tk.END, values=(
                    display_name,
                    f"{metrics['train_r2']:.4f}",
                    f"{metrics['test_r2']:.4f}",
                    f"{metrics['test_rmse']:.4f}",
                    f"{metrics['test_mae']:.4f}"
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error updating comparison: {str(e)}")
    
    def plot_distribution(self):
        """Plot data distribution"""
        try:
            if self.data is None or self.data.empty:
                messagebox.showwarning("Warning", "No data available to plot")
                return
            self.fig.clear()
            axes = self.fig.subplots(2, 2)
            
            # TV
            axes[0, 0].hist(self.data['TV'], bins=30, color='#3498db', alpha=0.7)
            axes[0, 0].set_title('TV Advertising Distribution')
            axes[0, 0].set_xlabel('TV ($1000s)')
            
            # Radio
            axes[0, 1].hist(self.data['Radio'], bins=30, color='#e74c3c', alpha=0.7)
            axes[0, 1].set_title('Radio Advertising Distribution')
            axes[0, 1].set_xlabel('Radio ($1000s)')
            
            # Social Media
            axes[1, 0].hist(self.data['Social Media'], bins=30, color='#2ecc71', alpha=0.7)
            axes[1, 0].set_title('Social Media Advertising Distribution')
            axes[1, 0].set_xlabel('Social Media ($1000s)')
            
            # Sales
            axes[1, 1].hist(self.data['Sales'], bins=30, color='#f39c12', alpha=0.7)
            axes[1, 1].set_title('Sales Distribution')
            axes[1, 1].set_xlabel('Sales ($1000s)')
            
            self.fig.tight_layout()
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", f"Plotting error: {str(e)}")
    
    def plot_correlations(self):
        """Plot correlation heatmap"""
        try:
            if self.data is None or self.data.empty:
                messagebox.showwarning("Warning", "No data available to plot")
                return
            self.fig.clear()
            ax = self.fig.add_subplot(111)
            
            # Create correlation matrix
            corr_matrix = self.data.corr()
            
            # Plot heatmap
            im = ax.imshow(corr_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
            
            # Set ticks and labels
            ax.set_xticks(range(len(corr_matrix)))
            ax.set_yticks(range(len(corr_matrix)))
            ax.set_xticklabels(corr_matrix.columns, rotation=45)
            ax.set_yticklabels(corr_matrix.columns)
            
            # Add correlation values
            for i in range(len(corr_matrix)):
                for j in range(len(corr_matrix)):
                    text = ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                                   ha="center", va="center", color="black")
            
            ax.set_title('Feature Correlation Matrix')
            self.fig.colorbar(im, ax=ax)
            self.fig.tight_layout()
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", f"Plotting error: {str(e)}")
    
    def plot_feature_importance(self):
        """Plot feature importance"""
        try:
            if self.models_manager is None:
                messagebox.showwarning("Warning", "Models not loaded yet")
                return
            self.fig.clear()
            axes = self.fig.subplots(1, 2)
            
            # Random Forest
            rf_importance = self.models_manager.get_feature_importance('random_forest')
            if rf_importance is not None:
                axes[0].barh(['TV', 'Radio', 'Social Media'], rf_importance, color='#3498db')
                axes[0].set_title('Random Forest - Feature Importance')
                axes[0].set_xlabel('Importance Score')
            else:
                axes[0].text(0.5, 0.5, 'Feature importance\nnot available', ha='center', va='center')
            
            # Gradient Boosting
            gb_importance = self.models_manager.get_feature_importance('gradient_boosting')
            if gb_importance is not None:
                axes[1].barh(['TV', 'Radio', 'Social Media'], gb_importance, color='#e74c3c')
                axes[1].set_title('Gradient Boosting - Feature Importance')
                axes[1].set_xlabel('Importance Score')
            else:
                axes[1].text(0.5, 0.5, 'Feature importance\nnot available', ha='center', va='center')
            
            self.fig.tight_layout()
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", f"Plotting error: {str(e)}")

def main():
    root = tk.Tk()
    app = SalesPredictionGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
