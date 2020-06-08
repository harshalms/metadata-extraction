training= ../Training_data
validation=../Validation_Data
label=../TrainingTestSet.csv

echo "Data annotation file is executing..."
python data_annotation.py --folder_path=$training --label_file_path=$label
python data_annotation.py --folder_path=$validation --label_file_path=$label
echo "Data annotation is done successfully."
echo "Model is under training..."
python train_spacy_ner.py
echo "Training completed successfullt"

echo "Model accuracy: Precision, Recall, F score"
python check_accuracy.py


