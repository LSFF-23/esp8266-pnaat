import os
import time
import numpy as np
import tensorflow as tf
from keras import layers, models

print("TensorFlow Version:", tf.__version__)

# 1. Load and Prepare Data
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# Normalize to [0,1] and add channel dimension (N, 28, 28, 1)
x_train = (x_train.astype("float32") / 255.0)[..., None]
x_test = (x_test.astype("float32") / 255.0)[..., None]

print("x_train shape:", x_train.shape, x_train.dtype)
print("x_test shape :", x_test.shape, x_test.dtype)

# 2. Build and Train Model
model = models.Sequential([
    layers.Input(shape=(28, 28, 1)), 
    layers.Flatten(), 
    layers.Dense(64, activation="relu"), 
    layers.Dense(10, activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

history = model.fit(
    x_train, y_train,
    validation_split=0.1,
    epochs=2,
    batch_size=256,
    verbose=1
)

test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
print(f"\n[Keras] Test Accuracy: {test_acc:.3f}")

# 3. Save Models
os.makedirs("export", exist_ok=True)

keras_path = "export/mnist_teste.keras"
model.save(keras_path)
print("Saved (Keras v3):", keras_path)

h5_path = "export/mnist_teste.h5"
model.save(h5_path)
print("Saved (Legacy HDF5):", h5_path)

# 4. TFLite Conversions (Fixed for Keras 3 Compatibility)
# Generate a concrete function from the Keras model using its input shape
run_model = tf.function(lambda x: model(x))
concrete_func = run_model.get_concrete_function(
    tf.TensorSpec(shape=[None, 28, 28, 1], dtype=tf.float32)
)

# (A) Float32 Conversion
converter = tf.lite.TFLiteConverter.from_concrete_functions([concrete_func], model)
tflite_float32 = converter.convert()
tfl_float_path = "export/mnist_teste_float32.tflite"
with open(tfl_float_path, "wb") as f:
    f.write(tflite_float32)

# (B) Dynamic Range Quantization Conversion
converter = tf.lite.TFLiteConverter.from_concrete_functions([concrete_func], model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_dynamic = converter.convert()
tfl_dyn_path = "export/mnist_teste_dynamic.tflite"
with open(tfl_dyn_path, "wb") as f:
    f.write(tflite_dynamic)

# 5. Handle LiteRT / TFLite Interpreter Import Safely
try:
    from ai_edge_litert.interpreter import Interpreter
    print("\nUsing LiteRT (ai-edge-litert).")
except ImportError:
    from tensorflow.lite import Interpreter
    print("\nUsing tf.lite.Interpreter (fallback).")

# 6. Helper Functions for Inference & Benchmarking
def create_interpreter(tflite_path):
    interp = Interpreter(model_path=tflite_path)
    interp.allocate_tensors()
    input_details = interp.get_input_details()[0]
    output_details = interp.get_output_details()[0]
    return interp, input_details, output_details

def run_inference(interp_info, img):
    interp, in_details, out_details = interp_info
    interp.set_tensor(in_details["index"], img)
    interp.invoke()
    probs = interp.get_tensor(out_details["index"])[0]
    pred = int(np.argmax(probs))
    return probs, pred

# Initialize interpreters once to avoid overhead reload
interp_f32_info = create_interpreter(tfl_float_path)
interp_dyn_info = create_interpreter(tfl_dyn_path)

# Single Test Image Selection
i = 0
img = x_test[i:i+1] # Keeps shape (1, 28, 28, 1)

probs_keras = model.predict(img, verbose=0)[0]
pred_keras = int(np.argmax(probs_keras))

probs_f32, pred_f32 = run_inference(interp_f32_info, img)
probs_dyn, pred_dyn = run_inference(interp_dyn_info, img)

print("\nPrediction Results")
print("=" * 40)
print(f"Ground Truth Label: {y_test[i]}")
print(f"Keras             : {pred_keras}")
print(f"LiteRT f32        : {pred_f32}")
print(f"LiteRT dyn        : {pred_dyn}")
print("-" * 40)
print("Probabilities (First 5 classes):")
print("Keras   :", np.round(probs_keras[:5], 3))
print("float32 :", np.round(probs_f32[:5], 3))
print("dynamic :", np.round(probs_dyn[:5], 3))

# 7. File Size Evaluation
def size_mb(p):
    return os.path.getsize(p) / (1024 * 1024) 

print("\nApproximate File Sizes:")
print(f" - {keras_path}: {size_mb(keras_path):.2f} MB (Keras v3)")
print(f" - {h5_path}:     {size_mb(h5_path):.2f} MB (Legacy HDF5)")
print(f" - {tfl_float_path}:   {size_mb(tfl_float_path):.2f} MB (TFLite float32)")
print(f" - {tfl_dyn_path}:     {size_mb(tfl_dyn_path):.2f} MB (TFLite dynamic)")

# 8. Latency Benchmark
def warmup(interp, in_det, out_det, img, runs=5):
    for _ in range(runs):
        interp.set_tensor(in_det["index"], img)
        interp.invoke()
        _ = interp.get_tensor(out_det["index"]) 

def benchmark(interp, in_det, out_det, img, runs=100):
    start = time.perf_counter()
    for _ in range(runs):
        interp.set_tensor(in_det["index"], img)
        interp.invoke()
        _ = interp.get_tensor(out_det["index"])
    end = time.perf_counter()
    return ((end - start) * 1000.0) / runs  # Average ms per run

# Unpack for benchmarking
interp_f32, in_f32, out_f32 = interp_f32_info
interp_dyn, in_dyn, out_dyn = interp_dyn_info

warmup(interp_f32, in_f32, out_f32, img, runs=10)
lat_f32_ms = benchmark(interp_f32, in_f32, out_f32, img, runs=100)

warmup(interp_dyn, in_dyn, out_dyn, img, runs=10)
lat_dyn_ms = benchmark(interp_dyn, in_dyn, out_dyn, img, runs=100)

print(f"\nAverage Latency (100 runs):")
print(f" - float32 : {lat_f32_ms:.3f} ms")
print(f" - dynamic : {lat_dyn_ms:.3f} ms")
print("Note: Results vary based on your local system hardware.")