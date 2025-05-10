from sklearn.metrics import (
    accuracy_score, f1_score, hamming_loss,
    precision_score, recall_score, jaccard_score
)
from sklearn.preprocessing import MultiLabelBinarizer

# Example data
y_true = [['barang'], ['nama_barang', 'stok'], ['stok', 'barang'], ['harga', 'barang'],
          ['pemasok', 'alamat'], ['pemasok', 'id'], ['stok'], ['nama_barang', 'nama_kategori']]
y_pred = [['barang'], ['stok'], ['stok'], ['barang'], 
          ['pemasok'], ['pemasok', 'id'], ['stok'], ['nama_barang']]  # Replace with your model's predictions

# Binarize the labels
mlb = MultiLabelBinarizer()
y_true_bin = mlb.fit_transform(y_true)
y_pred_bin = mlb.transform(y_pred)

# Exact Match Ratio
exact_match = accuracy_score(y_true_bin, y_pred_bin)

# Micro/Macro Precision, Recall, F1
precision_micro = precision_score(y_true_bin, y_pred_bin, average='micro')
recall_micro = recall_score(y_true_bin, y_pred_bin, average='micro')
f1_micro = f1_score(y_true_bin, y_pred_bin, average='micro')

precision_macro = precision_score(y_true_bin, y_pred_bin, average='macro')
recall_macro = recall_score(y_true_bin, y_pred_bin, average='macro')
f1_macro = f1_score(y_true_bin, y_pred_bin, average='macro')

# Hamming Loss
hamming = hamming_loss(y_true_bin, y_pred_bin)

# Jaccard Similarity (average='samples' gives per-sample similarity)
jaccard = jaccard_score(y_true_bin, y_pred_bin, average='samples')

# Print results
print(f"Exact Match Ratio: {exact_match:.2f}")
print(f"Micro Precision: {precision_micro:.2f}, Recall: {recall_micro:.2f}, F1: {f1_micro:.2f}")
print(f"Macro Precision: {precision_macro:.2f}, Recall: {recall_macro:.2f}, F1: {f1_macro:.2f}")
print(f"Hamming Loss: {hamming:.2f}")
print(f"Jaccard Similarity: {jaccard:.2f}")
