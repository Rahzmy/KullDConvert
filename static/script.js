// static/script.js
const form = document.getElementById('convForm');
const msg = document.getElementById('msg');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  msg.textContent = 'Mengunggah...';

  const f = document.getElementById('file').files[0];
  if (!f) {
    msg.textContent = 'Pilih file dahulu.';
    return;
  }

  // warning: file size limit on Vercel Functions ~4.5MB
  if (f.size > 4.5 * 1024 * 1024) {
    msg.innerHTML = 'File terlalu besar untuk dikirim langsung ke function (batas ≈ 4.5MB). Gunakan direct upload ke blob/S3.';
    return;
  }

  const formData = new FormData();
  formData.append('file', f);
  formData.append('to_format', document.getElementById('to_format').value);

  try {
    const resp = await fetch('/api/convert', {
      method: 'POST',
      body: formData
    });

    if (!resp.ok) {
      const data = await resp.json().catch(()=>null);
      msg.textContent = data && data.error ? 'Error: '+data.error : 'Server error';
      return;
    }

    const blob = await resp.blob();
    const cd = resp.headers.get('Content-Disposition') || '';
    let filename = 'converted';
    const m = cd.match(/filename="(.+)"/);
    if (m) filename = m[1];

    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);

    msg.textContent = 'Selesai — file diunduh.';
  } catch (err) {
    console.error(err);
    msg.textContent = 'Terjadi kesalahan: ' + err.message;
  }
});
