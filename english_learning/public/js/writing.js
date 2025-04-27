function nopBai() {
    const text = document.getElementById('baiViet').value.trim();
    const preview = document.getElementById('previewContent');
    
    if (text === '') {
      alert('Vui lòng nhập bài viết trước khi nộp!');
    } else {
      preview.innerText = text;
      alert('✅ Bài viết đã được nộp!');
    }
  }