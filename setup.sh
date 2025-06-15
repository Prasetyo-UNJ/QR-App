#!/bin/bash

# Hentikan jika ada error
set -e

# Cek apakah git sudah terinstal
if ! command -v git &> /dev/null
then
    echo "❌ Git belum terinstal. Silakan instal Git terlebih dahulu."
    exit 1
fi

# Inisialisasi git
echo "🔧 Inisialisasi git repository..."
git init

# Tambah semua file
git add .

# Commit awal
git commit -m "Initial commit"

# Ganti nama branch ke main
git branch -M main

# Tanya user untuk URL GitHub repository
read -p "🔗 Masukkan URL GitHub repository (contoh: https://github.com/username/nama-repo.git): " remote_url

# Tambahkan remote
git remote add origin "$remote_url"

# Push ke GitHub
echo "📤 Push ke GitHub..."
git push -u origin main

echo "✅ Selesai! Repository berhasil dipush ke GitHub."
