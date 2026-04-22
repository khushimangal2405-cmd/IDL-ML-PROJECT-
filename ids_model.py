import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
df = pd.read_csv(
"KDDTest+.txt",
sep=",",header=None
)
pd.set_option("display.max_columns",None)
df.head()
Output:

38 39 40

0.0 1.00 1.00

0.0 1.00 1.00

41 42

neptune 21

28201829303132 33 34 35 34 3

02 000 13 13 304 304 030100 00001

neptune 21

nommal 21

saint 15

0.0 0.83 0.71

mscan 11

df.describe()

Output:

df.info()df
.columns = 
[
"duration"
,
"protocol_type"
,
"service"
,
"flag"
,
"src_bytes"
,
"dst_bytes"
,
"land"
,
"wrong_fragment"
,
"urgent"
,
"hot"
,
"num_failed_logins"
,
"logged_in"
,
"num_compromised"
,
"root_shell"
,
"su_attempted"
,
"num_root"
  
,"num_file_creations",
"num_shells",
"num_access_files",
"num_outbound_cmds",
"is_host_login",
"is_guest_login",
"count",
"srv_count",
"serror_rate",
"srv_serror_rate",
"rerror_rate",
"srv_rerror_rate",
"same_srv_rate",
"diff_srv_rate",
"srv_diff_host_rate",
"dst_host_count",
"dst_host_srv_count",
"dst_host_same_srv_rate",
"dst_host_diff_srv_rate",
"dst_host_same_src_port_rate",
"dst_host_srv_diff_host_rate",
"dst_host_serror_rate",
"dst_host_srv_serror_rate",
"dst_host_rerror_rate",
"dst_host_srv_rerror_rate",
"class",
"difficulty"
]
attack_mapping = {
# normal
"normal": "normal",
# DoS
"neptune": "dos",
"smurf": "dos",
"back": "dos",
"teardrop": "dos",
"pod": "dos",
"land": "dos",
# Probe
"satan": "probe",
"ipsweep": "probe",
"portsweep": "probe",
  "nmap": "probe",
# R2L
"guess_passwd": "r2l",
"warezclient": "r2l",
"warezmaster": "r2l",
"ftp_write": "r2l",
"imap": "r2l",
"multihop": "r2l",
"phf": "r2l",
"spy": "r2l",
# U2R
"buffer_overflow": "u2r",
"loadmodule": "u2r",
"rootkit": "u2r",
"perl": "u2r",
}
df["class"] = df["class"].map(attack_mapping)
df['class'].value_counts()
Output:-
 
#Splitting X and Y for Simplification
oh = OneHotEncoder(sparse_output=False)
X = df.drop(['class'],axis = 1)
y = pd.DataFrame(oh.fit_transform(df[['class']]),columns= 
oh.get_feature_names_out(['class']))
#Encoding
df_tcp_trans = pd.DataFrame(oh.fit_transform(X[['protocol_type']]),columns= 
oh.get_feature_names_out(["protocol_type"]))
df_REJ_trans = pd.DataFrame(oh.fit_transform(X[['flag']]),columns= 
oh.get_feature_names_out(["flag"]))
df_private_trans = pd.DataFrame(oh.fit_transform(X[['service']]),columns= 
oh.get_feature_names_out(["service"]))
X = pd.concat([X,df_tcp_trans,df_private_trans,df_REJ_trans],axis= 1)
X.head()
X.head()

davion protocol type flag bytes dit bytes land

wrong frapunt urgent hot cum failed fugin

logged in nan compromised not shell sattrepted sam root

1630

00

0

090

00

1

0

1

1

G

09

1

000

me fie auton

mehnam outbound ands is host ingin is gant ingin count un court sorte sv umor rale rotor rals ave

076

ODO

000

600

0

0

0

225 10

000

10

10

0

0

0

1000

10

13

১০

0

4

41

1

000

10

03

0

4

61

1000

10

02

1

02

012

10

031

000

10

10

100

1123558

31

to

00

03

20

00

30

00

20

10

30

30

00

30

01

10

10

時

30

30

31

00

03

10

20

03

30

10

y.head()

24

13

class dos

class normal

class probe

class r21

class u2r

class_nan

0

1.0

0.0

0.0

00

00

0.0

1

1.0

0.0

0.0

0.0

0.0

0.0

2

0.0

1.0

0.0

0.0

0.0

0.0

3

0.0

0.0

0.0

0.0

0.0

1.0

4

0.0

0.0

0.0

0.0

0.0

1.0

X.drop(['protocol_type', 'service', 'flag'], axis 1,inplace True)

X.info()

Output:

<class 'pandas.core.frame.DataFrame'>

RangeIndex: 22544 entries, 0 to 22543

Columns: 117 entries, duration to flag SH

dtypes: float64(93), int64(24)

memory usage: 20.1 MB

print(list(y.columns))

  Output:
#Model Training / Validation
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
X_train, X_test, y_train, y_test = train_test_split(
  X, y,
test_size=0.2,
random_state=42,
stratify=y
)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train) 
X_test = scaler.transform(X_test)
y_test.shape
#y_train.shape
Output:
#Random Forest
from sklearn.metrics import classification_report, confusion_matrix
,accuracy_score
from sklearn.ensemble import RandomForestClassifier
rf_clf = RandomForestClassifier(
n_estimators=50,
max_depth=7,
random_state=42,
class_weight='balanced'
)
rf_clf.fit(X_train, y_train)
y_val_pred_rf = rf_clf.predict(X_test)
print("Random Forest (val):")
print(classification_report(y_test, y_val_pred_rf, zero_division=0))
print("Accuracy = ", accuracy_score(y_test,y_val_pred_rf))
y_test_rfc = np.argmax(y_test, axis=1)
y_val_pred_rf = np.argmax(y_val_pred_rf, axis=1)
pd.DataFrame(confusion_matrix(y_test_rfc, y_val_pred_rf))
Output:
#XGBoost
from xgboost import XGBClassifier
xgb = XGBClassifier(n_estimators = 200,
n_jobs=-1
           learning_rate = 0.01,
max_depth = 2
)
xgb.fit(X_train,y_train)
xgb_pred = xgb.predict(X_test)
print("Accuracy:",accuracy_score(xgb_pred,y_test))
print(classification_report(xgb_pred,y_test,zero_division=0))
Output:
#Applying Voting Classifier
y_train_vc = np.argmax(y_train, axis=1)
y_test_vc = np.argmax(y_test, axis=1)
from sklearn.ensemble import VotingClassifier
vc = VotingClassifier(
estimators = [
('rfc',RandomForestClassifier(
n_estimators=50,
  max_depth=7,
random_state=42,
class_weight='balanced'
)),
('xgb',XGBClassifier(n_estimators = 200,
n_jobs=-1,
learning_rate = 0.01,
max_depth = 2
))],
n_jobs = -1,
voting ='soft'
)
y_train.shape
Output:
vc.fit(X_train,y_train_vc)
vc_pred = vc.predict(X_test)
print(accuracy_score(y_test_vc,vc_pred))
print(classification_report(y_test_vc,vc_pred,zero_division=0))
pd.DataFrame(confusion_matrix(y_test_vc, vc_pred))
Output:
#Applying ANN
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
num_classes = len(set(y))
model = keras.Sequential([
keras.Input(shape=(X_train.shape[1],)), 
layers.Dense(256, activation='relu'),
layers.Dense(128, activation='relu'),
layers.Dense(64, activation='relu'),
layers.Dense(32, activation='relu'),
layers.Dense(num_classes, activation='softmax')
])
model.summary()
Output:
from tensorflow.keras.optimizers import Adam
model.compile(
optimizer=Adam(learning_rate=0.01),
loss='categorical_crossentropy',
metrics=['accuracy']
)
from tensorflow.keras.callbacks import EarlyStopping
early_stop = EarlyStopping(
monitor='val_loss',
patience=5,
restore_best_weights=True
)
history = model.fit(
X_train, y_train,
validation_split=0.2,
epochs=100,
callbacks=[early_stop],
batch_size=512
)
Output:
import matplotlib.pyplot as plt
plt.figure(figsize=(10,5))
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title("Model Accuracy")
plt.legend(['Train', 'Validation'])
plt.grid(True)
plt.show()
plt.figure(figsize=(10,5))
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title("Model Loss")
plt.legend(['Train', 'Validation'])
plt.grid(True)
plt.show()
import numpy as np
from sklearn.metrics import classification_report, 
accuracy_score,f1_score,confusion_matrix
test_loss, test_acc = model.evaluate(X_test, y_test)
print("Test Accuracy:", test_acc)
y_pred = np.argmax(model.predict(X_test), axis=1)
y_test_labels = np.argmax(y_test, axis=1)
print(classification_report(y_test_labels, y_pred))
print("Accuracy:", accuracy_score(y_test_labels, y_pred))
Output
pd.DataFrame(confusion_matrix(y_test_labels, y_pred))




