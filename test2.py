import tensorflow as tf
import numpy as np
NoofHource=12
NoofData=3

print("TensorFlow version:", tf.__version__)
physical_devices = tf.config.list_physical_devices('GPU')
print("Num GPUs :", len(physical_devices))

MainF=np.load(f"{NoofHource}_{NoofData}_F.npy",allow_pickle=True)
LMain=len(MainF)
print(int(LMain*0.8))
np.random.shuffle(MainF)
trainingI,trainingO, testI,testO = MainF[:int(LMain*0.8),0:-1],MainF[:int(LMain*0.8),-1],MainF[int(LMain*0.8):,0:-1] ,MainF[int(LMain*0.8):,-1]

print(len(trainingI))
print(len(trainingO))
print(len(testI))
print(len(testI))
print(len(MainF))





NtrainingI=np.zeros((len(trainingI),NoofHource,NoofData,7),dtype=float)

for i in range(len(NtrainingI)):
    for j in range(len(NtrainingI[i])):
        length=trainingI[i][NoofHource][0][0]

        for k in range(len(NtrainingI[i][j])):
            for z in range(len(NtrainingI[i][j][k])):
                if j==NoofHource-1:
                    NtrainingI[i][j][k][z] = float(trainingI[i][j][k][z+1])/100
                else:
                    if z==2 or z==3:
                        NtrainingI[i][j][k][z]=float(trainingI[i][j][k][z+1])*5
                    elif z==1:
                        NtrainingI[i][j][k][z] = float(trainingI[i][j][k][z + 1]) / int(length)
                    elif z==4 :
                        NtrainingI[i][j][k][z] = float(trainingI[i][j][k][z + 1]) / 100
                    elif z==6 :
                        NtrainingI[i][j][k][z] = float(trainingI[i][j][k][z + 1]) / 10000
                    elif z==5:
                        NtrainingI[i][j][k][z] = float(trainingI[i][j][k][z + 1]) / 1000
                    elif z==0:
                        NtrainingI[i][j][k][z] =float(1/abs(trainingI[i][j][k][z + 1]+1))*10
                    else:
                        NtrainingI[i][j][k][z] = float(trainingI[i][j][k][z + 1])


print(NtrainingI.shape)
NtrainingO=np.zeros((len(trainingO),1),dtype=float)
print(NtrainingO.shape)
for i in range(len(NtrainingO)):
    for j in range(len(NtrainingO[i])):
        NtrainingO[i][j]=trainingO[i][j]
print(NtrainingO.shape)

print()
NtestI=np.zeros((len(testI),NoofHource,NoofData,7),dtype=float)
for i in range(len(NtestI)):
    for j in range(len(NtestI[i])):
        length = trainingI[i][NoofHource][0][0]
        for k in range(len(NtestI[i][j])):
            for z in range(len(NtestI[i][j][k])):
                if j == NoofHource - 1:
                    NtestI[i][j][k][z] = float(testI[i][j][k][z + 1]) / 100
                else:
                    if z == 2 or z == 3:
                        NtestI[i][j][k][z] = float(testI[i][j][k][z + 1]) * 5
                    elif z == 1:
                        NtestI[i][j][k][z] = float(testI[i][j][k][z + 1]) / int(length)
                    elif z == 4:
                        NtestI[i][j][k][z] = float(testI[i][j][k][z + 1]) / 100
                    elif z == 6:
                        NtestI[i][j][k][z] = float(testI[i][j][k][z + 1]) / 10000
                    elif z == 5:
                        NtestI[i][j][k][z] = float(testI[i][j][k][z + 1]) / 1000
                    elif z == 0:
                        NtestI[i][j][k][z] = float(1 / abs(testI[i][j][k][z + 1] + 1)) * 10
                    else:
                        NtestI[i][j][k][z] = float(testI[i][j][k][z + 1])
print(NtestI.shape)
NtestO=np.zeros((len(testO),1),dtype=float)

for i in range(len(NtestO)):
    for j in range(len(NtestO[i])):
        NtestO[i][j]=testO[i][j]
print(NtestO.shape)

train_dataset = tf.data.Dataset.from_tensor_slices((NtrainingI, NtrainingO))
test_dataset = tf.data.Dataset.from_tensor_slices((NtestI, NtestO))

BATCH_SIZE = 40
SHUFFLE_BUFFER_SIZE = 100

train_dataset = train_dataset.shuffle(SHUFFLE_BUFFER_SIZE).batch(BATCH_SIZE)
test_dataset = test_dataset.batch(BATCH_SIZE)


model = tf.keras.Sequential([
    tf.keras.layers.Input(NtrainingI[0].shape),

    tf.keras.layers.Dense(7),tf.keras.layers.Dense(7),
    tf.keras.layers.Dense(1,activation="relu"),
    tf.keras.layers.Reshape((NoofHource, NoofData)),

    tf.keras.layers.Dense(NoofHource),
    tf.keras.layers.Dense(NoofHource),


    tf.keras.layers.Dense(1),

    tf.keras.layers.Dense(1,activation="relu"),
    tf.keras.layers.Reshape((NoofHource,)),
    tf.keras.layers.Dense(NoofHource),

    tf.keras.layers.Dense(NoofHource),
    tf.keras.layers.Dense(NoofHource,activation="softmax")
])

model.compile(optimizer=tf.keras.optimizers.Adam()#//RMSprop().SGD()
              ,
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['sparse_categorical_accuracy'])
print(model.summary())
assert True
model.fit(train_dataset, epochs=300)

# Evaluate the model on the test data using `evaluate`
print("Evaluate on test data")
results = model.evaluate(test_dataset, batch_size=128)
print("test loss, test acc:", results)

# Generate predictions (probabilities -- the output of the last layer)
# on new data using `predict`
print("Generate predictions for  samples")
predictions = model.predict(NtestI)
print("predictions shape:", predictions.shape)
print(predictions)
output=[np.argmax(x) for x in predictions]
print(output)
print([output.count(x) for x in range(12)])
print(sum(predictions[1]))

print(sum(predictions[2]))

model.save(f"{NoofHource}_{NoofData}_test2.h5")



