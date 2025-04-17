# LoRA-Chem

This project utilizes [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) to perform LoRA fine-tuning. It provides a complete dataset and scripts for both training and evaluation.

## 📁 Dataset

All datasets are located in the `dataset/` directory and come in two formats:

- **JSON format**: Ready to use directly for fine-tuning.
- **CSV format**: Requires conversion to JSON before use.

### 🔧 Converting CSV to JSON

To convert CSV files into JSON format, use the provided scripts:

- `description.py`: Prepares field descriptions or structures the data.
- `csv_to_json.py`: Converts CSV files into the required JSON format for training.

## 🧠 Fine-Tuning & Evaluation

The fine-tuning process is carried out using [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory), with LoRA as the tuning method.

All relevant scripts are located in the `scripts/` directory, including:

- `*_train.sh`: Shell scripts for training.
- `*_eval.sh`: Shell scripts for evaluation.

Feel free to modify the scripts to suit your specific training and evaluation needs.
