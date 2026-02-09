import os
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import argparse

# Configuration
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 3
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
    base_model.trainable = False  # Freeze base model

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.2),
        layers.Dense(NUM_CLASSES, activation="softmax")
    ])
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    return model

def build_vit():
    """Build a simplified Vision Transformer (ViT) model compatible with Keras 3."""
    input_shape = (*IMG_SIZE, 3)
    patch_size = 32
    num_patches = (IMG_SIZE[0] // patch_size) ** 2
    projection_dim = 64
    num_heads = 4
    transformer_layers = 4
    mlp_head_units = [128, 64]

    inputs = layers.Input(shape=input_shape)
    
    # 1. Patch Creation & Embedding
    patches = layers.Conv2D(projection_dim, kernel_size=patch_size, strides=patch_size)(inputs)
    patches = layers.Reshape((num_patches, projection_dim))(patches)
    
    # 2. Positional Embedding (Stable Functional API Way)
    # We use a trainable parameter by using an Embedding layer on a constant input
    # This avoids the tf.range broadcasting issues in Keras 3 Functional API
    pos_embed = layers.Embedding(input_dim=1, output_dim=num_patches * projection_dim)(tf.zeros((1,), dtype="int32"))
    pos_embed = layers.Reshape((num_patches, projection_dim))(pos_embed)
    encoded_patches = layers.Add()([patches, pos_embed])

    # 3. Transformer Layers
    for _ in range(transformer_layers):
        x1 = layers.LayerNormalization(epsilon=1e-6)(encoded_patches)
        # Call with 1 arg for self-attention. Keras 3 handles it.
        # Or explicitly pass query/value/key. Let's use 1 arg for simplicity.
        attention_output = layers.MultiHeadAttention(
            num_heads=num_heads, key_dim=projection_dim, dropout=0.1
        )(x1, x1)
        x2 = layers.Add()([attention_output, encoded_patches])
        x3 = layers.LayerNormalization(epsilon=1e-6)(x2)
        x3 = layers.Dense(projection_dim, activation="gelu")(x3)
        x3 = layers.Dropout(0.1)(x3)
        encoded_patches = layers.Add()([x3, x2])

    # 4. Classification Head
    representation = layers.LayerNormalization(epsilon=1e-6)(encoded_patches)
    representation = layers.GlobalAveragePooling1D()(representation)
    for units in mlp_head_units:
        representation = layers.Dense(units, activation="gelu")(representation)
        representation = layers.Dropout(0.1)(representation)
    
    outputs = layers.Dense(NUM_CLASSES, activation="softmax")(representation)
    
    model = models.Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    return model

def train_model(model_type):
    print(f"\n--- Starting Training for {model_type} ---")
    
    if not os.path.exists(TRAIN_DIR):
        print(f"Error: Training directory not found at {TRAIN_DIR}")
        return

    train_datagen = ImageDataGenerator(rescale=1./255, rotation_range=20, horizontal_flip=True)
    val_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        TRAIN_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode="categorical"
    )
    val_generator = val_datagen.flow_from_directory(
        VAL_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode="categorical"
    )

    if model_type == "CNN":
        model = build_cnn()
        save_path = os.path.join(MODELS_DIR, "disease_model.h5")
    else:
        model = build_vit()
        save_path = os.path.join(MODELS_DIR, "disease_vit_model.h5")

    os.makedirs(MODELS_DIR, exist_ok=True)

    print(f"Epochs: {EPOCHS}, Classes: {NUM_CLASSES}")
    model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=val_generator
    )

    model.save(save_path)
    print(f"Model saved to {save_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, choices=["CNN", "ViT"], required=True)
    args = parser.parse_args()
    
    train_model(args.model)
