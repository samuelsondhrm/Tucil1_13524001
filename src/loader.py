import os
from PIL import Image, UnidentifiedImageError

def read_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError("File tidak ditemukan.")
    
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == '.txt':
        return read_txt_file(file_path)
    elif ext in ['.png', '.jpg', '.jpeg', '.bmp']:
        return read_image_file(file_path)
    else:
        raise ValueError(f"Format file '{ext}' tidak didukung.")
    
def read_txt_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        raise ValueError("File korup atau bukan file teks valid (mungkin file gambar yang di-rename?).")

    lines = [line.strip() for line in lines if line.strip()]
    if not lines:
        raise ValueError("File teks kosong.")
    
    matriks_warna = []
    N = len(lines)

    for i, line in enumerate(lines):
        if len(line) != N:
            raise ValueError(f"Baris {i+1} tidak valid. Panjang harus {N}, tapi ditemukan {len(line)}.")
        
        if not line.isprintable():
            raise ValueError(f"Baris {i+1} mengandung karakter tidak valid/binary.")
        
        matriks_warna.append(list(line))

    all_colors = [char for row in matriks_warna for char in row]
    unique_colors = set(all_colors)

    if len(unique_colors) != N:
        raise ValueError(f"Konfigurasi puzzle tidak valid."
                         f"Ukuran papan {N}x{N} harus memiliki tepat {N} wilayah warna berbeda. "
                         f"Ditemukan: {len(unique_colors)} warna ({', '.join(sorted(unique_colors))}).")
    
    return matriks_warna, N

def read_image_file(file_path):
    try:
        with Image.open(file_path) as img:
            img = img.convert('RGB')
            return img, -1
    except (UnidentifiedImageError, IOError):
        raise ValueError("File bukan gambar valid atau korup.")
    
def image_to_grid(image, N):
    width, height = image.size

    cell_w = width / N
    cell_h = height / N

    matriks_warna = []

    for r in range(N):
        row = []
        for c in range(N):
            center_x = int((c * cell_w) + (cell_w / 2))
            center_y = int((r * cell_h) + (cell_h / 2))

            pixel = image.getpixel((center_x, center_y))

            row.append(pixel)
        matriks_warna.append(row)

    return rgb_to_chars(matriks_warna)

def rgb_to_chars(matriks_rgb):
    color_map = {}
    next = 'A'
    matriks_char = []

    for row in matriks_rgb:
        char_row = []
        for pixel in row:
            if pixel not in color_map:
                color_map[pixel] = next
                next = chr(ord(next)+1)
            
            char_row.append(color_map[pixel])
        matriks_char.append(char_row)

    return matriks_char