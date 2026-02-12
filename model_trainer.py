import os
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, callbacks
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import argparse

# Configuration
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
INITIAL_EPOCHS = 10
FINE_TUNE_EPOCHS = 20
NUM_CLASSES = 8

# Use relative paths for portability
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "Variant-a(Multiclass Classification)")
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "val")
MODELS_DIR = os.path.join(BASE_DIR, "models")

def build_cnn():
    """Build a CNN model using MobileNetV2 for transfer learning."""
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(*IMG_SIZE, 3), include_top=False, weights="imagenet"
    )
    base_model.trainable = False  # Freeze base model initially

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Dense(256, activation="relu"),
        layers.Dropout(0.5),  # Increased dropout for regularization
        layers.Dense(NUM_CLASSES, activation="softmax")
    ])
    
    # Compile with higher LR for head training
    model.compile(optimizer=optimizers.Adam(learning_rate=1e-3),
                  loss="categorical_crossentropy",
                  metrics=["accuracy"])
    return model, base_model

def train_model():
    print(f"\n--- Starting Advanced Training (CNN) ---")
    
    if not os.path.exists(TRAIN_DIR):
        print(f"Error: Training directory not found at {TRAIN_DIR}")
        return

    # 1. Advanced Data Augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    val_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        TRAIN_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode="categorical"
    )
    val_generator = val_datagen.flow_from_directory(
        VAL_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode="categorical"
    )

    # 2. Build Model
    model, base_model = build_cnn()
    save_path = os.path.join(MODELS_DIR, "disease_model.h5")
    os.makedirs(MODELS_DIR, exist_ok=True)

    # 3. Callbacks
    checkpoint = callbacks.ModelCheckpoint(
        save_path, monitor='val_accuracy', save_best_only=True, mode='max', verbose=1
    )
    reduce_lr = callbacks.ReduceLROnPlateau(
        monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6, verbose=1
    )
    early_stop = callbacks.EarlyStopping(
        monitor='val_loss', patience=8, restore_best_weights=True, verbose=1
    )

    # 4. Phase 1: Train Head (Frozen Base)
    print("\n[Phase 1] Training Top Layers...")
    history_phase1 = model.fit(
        train_generator,
        epochs=INITIAL_EPOCHS,
        validation_data=val_generator,
        callbacks=[checkpoint]
    )

    # 5. Phase 2: Fine-Tuning (Unfreeze Top Layers)
    print("\n[Phase 2] Fine-Tuning Base Model...")
    base_model.trainable = True
    
    # Freeze all layers except the last 30
    for layer in base_model.layers[:-30]:
        layer.trainable = False

    # Recompile with very low learning rate
    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-5),  # Lower LR for fine-tuning
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    history_phase2 = model.fit(
        train_generator,
        epochs=FINE_TUNE_EPOCHS,
        validation_data=val_generator,
        callbacks=[checkpoint, reduce_lr, early_stop]
    )

    print(f"\nTraining Complete. Best model saved to {save_path}")

if __name__ == "__main__":
    # Removed argument parser since we only support CNN now
    train_model()
