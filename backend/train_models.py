import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from collections import Counter
from app.model_classes import RandomForest

# Get the absolute path to the backend directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'app', 'models')

def create_feature_plots(df, output_dir):
    """Create and save feature distribution plots."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Numerical features
    features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    fig, axes = plt.subplots(3, 3, figsize=(15, 15))
    axes = axes.ravel()
    
    for idx, feature in enumerate(features):
        sns.histplot(data=df, x=feature, ax=axes[idx])
        axes[idx].set_title(f'{feature} Distribution')
    
    # Add crop distribution
    sns.countplot(data=df, y='label', ax=axes[-2])
    axes[-2].set_title('Crop Distribution')
    axes[-1].remove()  # Remove extra subplot
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'feature_distributions.png'))
    plt.close()

class DecisionTree:
    def __init__(self, max_depth=None, min_samples_split=2):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.tree = None

    def _entropy(self, y):
        """Calculate entropy of the target variable."""
        classes, counts = np.unique(y, return_counts=True)
        probabilities = counts / len(y)
        return -np.sum(probabilities * np.log2(probabilities))

    def _information_gain(self, X, y, feature_idx, threshold):
        """Calculate information gain for a split."""
        parent_entropy = self._entropy(y)
        
        # Split the data
        left_mask = X[:, feature_idx] <= threshold
        right_mask = ~left_mask
        
        if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
            return 0
        
        # Calculate weighted entropy of children
        left_entropy = self._entropy(y[left_mask])
        right_entropy = self._entropy(y[right_mask])
        
        left_weight = np.sum(left_mask) / len(y)
        right_weight = np.sum(right_mask) / len(y)
        
        weighted_child_entropy = (left_weight * left_entropy + 
                                right_weight * right_entropy)
        
        return parent_entropy - weighted_child_entropy

    def _best_split(self, X, y):
        """Find the best split for a node."""
        best_gain = -1
        best_feature = None
        best_threshold = None
        
        n_features = X.shape[1]
        
        for feature_idx in range(n_features):
            thresholds = np.unique(X[:, feature_idx])
            for threshold in thresholds:
                gain = self._information_gain(X, y, feature_idx, threshold)
                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature_idx
                    best_threshold = threshold
                    
        return best_feature, best_threshold

    def _build_tree(self, X, y, depth=0):
        n_samples = len(y)
        n_classes = len(np.unique(y))
        
        # Check stopping criteria
        if (self.max_depth is not None and depth >= self.max_depth) or \
           n_samples < self.min_samples_split or \
           n_classes == 1:
            return {'type': 'leaf', 'prediction': Counter(y).most_common(1)[0][0]}
        
        # Find best split
        feature_idx, threshold = self._best_split(X, y)
        
        if feature_idx is None:
            return {'type': 'leaf', 'prediction': Counter(y).most_common(1)[0][0]}
        
        # Split the data
        left_mask = X[:, feature_idx] <= threshold
        right_mask = ~left_mask
        
        # Build child trees
        left_tree = self._build_tree(X[left_mask], y[left_mask], depth + 1)
        right_tree = self._build_tree(X[right_mask], y[right_mask], depth + 1)
        
        return {
            'type': 'node',
            'feature_idx': feature_idx,
            'threshold': threshold,
            'left': left_tree,
            'right': right_tree
        }

    def fit(self, X, y):
        """Build the decision tree."""
        self.tree = self._build_tree(X, y)
        return self

    def _predict_single(self, x, tree):
        """Make prediction for a single sample."""
        if tree['type'] == 'leaf':
            return tree['prediction']
        
        if x[tree['feature_idx']] <= tree['threshold']:
            return self._predict_single(x, tree['left'])
        return self._predict_single(x, tree['right'])

    def predict(self, X):
        """Make predictions for multiple samples."""
        return np.array([self._predict_single(x, self.tree) for x in X])

class RandomForest:
    def __init__(self, n_trees=10, max_depth=None, min_samples_split=2, sample_ratio=0.8):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.sample_ratio = sample_ratio
        self.trees = []

    def _bootstrap_sample(self, X, y):
        """Create a bootstrap sample of the data."""
        n_samples = int(len(X) * self.sample_ratio)
        indices = np.random.choice(len(X), size=n_samples, replace=True)
        return X[indices], y[indices]

    def fit(self, X, y):
        """Build the random forest."""
        self.trees = []
        for _ in range(self.n_trees):
            # Create bootstrap sample
            X_sample, y_sample = self._bootstrap_sample(X, y)
            
            # Train decision tree
            tree = DecisionTree(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split
            )
            tree.fit(X_sample, y_sample)
            self.trees.append(tree)
        return self

    def predict(self, X):
        """Make predictions using majority voting."""
        predictions = np.array([tree.predict(X) for tree in self.trees])
        return np.array([Counter(pred).most_common(1)[0][0] 
                        for pred in predictions.T])

def prepare_data():
    """Prepare the crop recommendation dataset."""
    try:
        # Load data
        df = pd.read_csv('Crop_recommendation.csv')
        
        # Separate features and target
        X = df.drop('label', axis=1).values
        y = df['label'].values
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test, scaler
    except Exception as e:
        print(f"Error in prepare_data: {str(e)}")
        raise

def train_model():
    """Train the random forest model."""
    try:
        # Create models directory if it doesn't exist
        os.makedirs(MODELS_DIR, exist_ok=True)
        
        # Prepare data
        print("Preparing data...")
        X_train, X_test, y_train, y_test, scaler = prepare_data()
        
        # Initialize and train the model
        print("Training Random Forest model...")
        rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            random_state=42
        )
        rf_model.fit(X_train, y_train)
        
        # Save all components in a single file
        print("\nSaving model components...")
        model_components = {
            'model': rf_model,
            'scaler': scaler,
            'labels': np.unique(y_train)
        }
        
        model_path = os.path.join(MODELS_DIR, 'crop_model.joblib')
        joblib.dump(model_components, model_path)
        print("File saved to:", model_path)
        
    except Exception as e:
        print(f"Error in train_model: {str(e)}")
        raise

if __name__ == "__main__":
    train_model()