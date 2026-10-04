
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
)

# Load the prepared dataset
df = pd.read_csv("powerbi/review_prediction_data.csv")

# Features available after delivery and target
feature_columns = [
    "delivery_duration_days",
    "delay_days",
    "total_price",
    "total_freight",
    "payment_type",
]

X = df[feature_columns]
y = df["low_review"]

numeric_features = [
    "delivery_duration_days",
    "delay_days",
    "total_price",
    "total_freight",
]

categorical_features = ["payment_type"]

# Split before fitting preprocessing to avoid data leakage
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore")),
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_transformer, numeric_features),
    ("categorical", categorical_transformer, categorical_features),
])

models = {
    "Logistic Regression": LogisticRegression(
        class_weight="balanced",
        max_iter=1000,
        random_state=42,
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    ),
}

results = []

for model_name, model in models.items():
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", model),
    ])

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)
    probabilities = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "Model": model_name,
        "Accuracy": accuracy_score(y_test, predictions),
        "Precision": precision_score(
            y_test, predictions, zero_division=0
        ),
        "Recall": recall_score(
            y_test, predictions, zero_division=0
        ),
        "F1-score": f1_score(
            y_test, predictions, zero_division=0
        ),
        "ROC-AUC": roc_auc_score(y_test, probabilities),
    }
    results.append(metrics)

    print("\n" + "=" * 55)
    print(model_name)
    print("=" * 55)

    for metric, value in metrics.items():
        if metric != "Model":
            print(f"{metric}: {value:.4f}")

    print("\nConfusion matrix:")
    print(confusion_matrix(y_test, predictions))

    print("\nClassification report:")
    print(classification_report(
        y_test,
        predictions,
        target_names=["Other reviews", "Low reviews"],
        zero_division=0,
    ))

    # Show feature importance for Random Forest
    if model_name == "Random Forest":
        feature_names = (
            pipeline.named_steps["preprocessor"]
            .get_feature_names_out()
        )
        importances = (
            pipeline.named_steps["model"].feature_importances_
        )

        importance_df = pd.DataFrame({
            "Feature": feature_names,
            "Importance": importances,
        }).sort_values("Importance", ascending=False)

        print("\nTop 10 encoded feature importances:")
        print(importance_df.head(10).to_string(index=False))

        # Aggregate encoded payment categories into one feature
        importance_df["Feature_Group"] = (
            importance_df["Feature"]
            .str.replace(
                "numeric__", "", regex=False
            )
            .str.replace(
                "categorical__payment_type_", "", regex=False
            )
            .where(
                ~importance_df["Feature"].str.startswith(
                    "categorical__payment_type_"
                ),
                "payment_type",
            )
        )

        grouped_importance = (
            importance_df.groupby("Feature_Group")["Importance"]
            .sum()
            .sort_values(ascending=False)
        )

        print("\nGrouped feature importance:")
        print(grouped_importance.to_string())

# Compare both models
results_df = pd.DataFrame(results).sort_values(
    "F1-score", ascending=False
)

print("\n" + "=" * 55)
print("MODEL COMPARISON")
print("=" * 55)
print(results_df.to_string(index=False, float_format="%.4f".__mod__))

results_df.to_csv(
    "powerbi/review_model_comparison.csv",
    index=False,
)

print("\nSaved comparison to powerbi/review_model_comparison.csv")
