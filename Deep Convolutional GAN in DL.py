import tensorflow as tf
from keras import layers, models
import numpy as np
import matplotlib.pyplot as plt

# 1. Load and Preprocess the Dataset
(x_train, _), (_, _) = tf.keras.datasets.mnist.load_data()
# Normalize images to the range [-1, 1] (crucial for GANs using 'tanh' activation)
x_train = (x_train.astype(np.float32) - 127.5) / 127.5
x_train = np.expand_dims(x_train, axis=-1)  # Reshape to (60000, 28, 28, 1)

# Training configuration
LATENT_DIM = 100
BATCH_SIZE = 64
EPOCHS = 10
dataset = tf.data.Dataset.from_tensor_slices(x_train).shuffle(60000).batch(BATCH_SIZE)

# 2. Build the Generator
def build_generator():
    model = models.Sequential([
        # Foundation for 7x7 image maps
        layers.Dense(7 * 7 * 128, input_dim=LATENT_DIM),
        layers.Reshape((7, 7, 128)),
        layers.BatchNormalization(),
        layers.ReLU(),
        
        # Upsample to 14x14
        layers.Conv2DTranspose(64, kernel_size=5, strides=2, padding='same'),
        layers.BatchNormalization(),
        layers.ReLU(),
        
        # Upsample to 28x28 (Matching MNIST dimensions)
        layers.Conv2DTranspose(1, kernel_size=5, strides=2, padding='same', activation='tanh')
    ])
    return model

# 3. Build the Discriminator
def build_discriminator():
    model = models.Sequential([
        # Downsample to 14x14
        layers.Conv2D(64, kernel_size=5, strides=2, padding='same', input_shape=(28, 28, 1)),
        layers.LeakyReLU(alpha=0.2),
        layers.Dropout(0.3),
        
        # Downsample to 7x7
        layers.Conv2D(128, kernel_size=5, strides=2, padding='same'),
        layers.LeakyReLU(alpha=0.2),
        layers.Dropout(0.3),
        
        layers.Flatten(),
        layers.Dense(1, activation='sigmoid')  # Binary classification: Real (1) or Fake (0)
    ])
    return model

# Initialize and compile models
discriminator = build_discriminator()
discriminator.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0002, beta_1=0.5), 
                      loss='binary_crossentropy', metrics=['accuracy'])

generator = build_generator()

# 4. Build the Combined GAN Model
# Freeze discriminator weights during generator training
discriminator.trainable = False

gan_input = layers.Input(shape=(LATENT_DIM,))
fake_image = generator(gan_input)
gan_output = discriminator(fake_image)

gan = models.Model(gan_input, gan_output)
gan.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0002, beta_1=0.5), loss='binary_crossentropy')

# Helper function to plot and save generated images
def plot_generated_images(generator, epoch, examples=16, dim=(4, 4), figsize=(4, 4)):
    noise = np.random.normal(0, 1, size=[examples, LATENT_DIM])
    generated_images = generator.predict(noise)
    generated_images = generated_images.reshape(examples, 28, 28)

    plt.figure(figsize=figsize)
    for i in range(generated_images.shape[0]):
        plt.subplot(dim[0], dim[1], i+1)
        plt.imshow(generated_images[i], cmap='gray_r')
        plt.axis('off')
    plt.tight_layout()
    plt.suptitle(f"Epoch {epoch}", y=1.02)
    plt.show()

# 5. The Training Loop
for epoch in range(1, EPOCHS + 1):
    print(f"--- Starting Epoch {epoch} ---")
    
    for real_images in dataset:
        current_batch_size = real_images.shape[0]
        
        # --- Train Discriminator ---
        # Generate fake images from random noise
        noise = np.random.normal(0, 1, size=[current_batch_size, LATENT_DIM])
        fake_images = generator.predict(noise, verbose=0)
        
        # Create labels (one-sided label smoothing can be added here, but keeping it simple)
        real_labels = np.ones((current_batch_size, 1))
        fake_labels = np.zeros((current_batch_size, 1))
        
        # Train on real and fake data separately
        d_loss_real = discriminator.train_on_batch(real_images, real_labels)
        d_loss_fake = discriminator.train_on_batch(fake_images, fake_labels)
        d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
        
        # --- Train Generator ---
        # We want the discriminator to mistake fake images for real ones (label = 1)
        noise = np.random.normal(0, 1, size=[current_batch_size, LATENT_DIM])
        misleading_labels = np.ones((current_batch_size, 1))
        
        g_loss = gan.train_on_batch(noise, misleading_labels)
        
    # Print progress and plot sample images at the end of each epoch
    print(f"Discriminator Loss: {d_loss[0]:.4f}, Accuracy: {100 * d_loss[1]:.2f}% | Generator Loss: {g_loss:.4f}")
    plot_generated_images(generator, epoch)