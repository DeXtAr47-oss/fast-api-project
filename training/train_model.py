import pandas as pd
import joblib
import os 
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error, mean_absolute_error
from .train_utils import DATA_FILE_PATH, MODEL_DIR, MODEL_PATH

df = (pd
      .read_csv(DATA_FILE_PATH)
      .drop_duplicates()
      .drop(columns=['name', 'model', 'edition'])
    )

X = df.drop(columns='selling_price')
y = df['selling_price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

numeric_cols = X_train.select_dtypes(include='number').columns.tolist()
categorical_cols = X_train.select_dtypes(include='object').columns.tolist()

num_pipe = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

cat_pipe = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(transformers=
                                 [('num', num_pipe, numeric_cols),
                                 ('cat', cat_pipe, categorical_cols)]
                                 )

rf = RandomForestRegressor(
    n_estimators=10, max_depth=5, random_state=42
)

rf_model = Pipeline(steps=[
    ('pre', preprocessor),
    ('reg', rf)
])

rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)
print(f'MAE testing error: {mean_absolute_error(y_test, y_pred): .3f}')
print(f'Root mean squared testing error: {root_mean_squared_error(y_test, y_pred): .3f}')

os.makedirs(MODEL_DIR, exist_ok=True)
joblib.dump(rf_model, MODEL_PATH)
