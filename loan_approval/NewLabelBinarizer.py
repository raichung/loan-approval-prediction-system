from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder, LabelBinarizer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelBinarizer
class NewLabelBinarizer(LabelBinarizer):
    def fit_transform(self, X, y=None):
        return super(NewLabelBinarizer,self).fit_transform(X)