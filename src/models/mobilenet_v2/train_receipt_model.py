import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
from tchau_preguica import create_model

def train_model(dataset_dir):
    """Treina o modelo com um conjunto de dados fornecido."""
    train_dir = os.path.join(dataset_dir, 'train')
    validation_dir = os.path.join(dataset_dir, 'validation')

    train_datagen = ImageDataGenerator(rescale=1.0/255.0, rotation_range=40, width_shift_range=0.2, height_shift_range=0.2, shear_range=0.2, zoom_range=0.2, horizontal_flip=True, fill_mode='nearest')
    validation_datagen = ImageDataGenerator(rescale=1.0/255.0)

    train_generator = train_datagen.flow_from_directory(train_dir, target_size=(150, 150), batch_size=20, class_mode='binary')
    validation_generator = validation_datagen.flow_from_directory(validation_dir, target_size=(150, 150), batch_size=20, class_mode='binary')

    model = create_model()

    early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

    model.fit(train_generator, epochs=20, validation_data=validation_generator, callbacks=[early_stopping])

    model_save_path = '/src/models/mobilenet_v2/saved_model/receipt_detection_model_v1.h5.py'
    
    model.save(model_save_path)

    print(f'Modelo salvo em: {model_save_path}')

train_model('./dataset')