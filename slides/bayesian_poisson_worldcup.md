# Model Bayesian Poisson untuk Gol Piala Dunia

Posisi materi:

> Materi ini melanjutkan draft teman sebagai dasar riset, lalu merapikannya menjadi studi kasus Bayesian Poisson untuk jumlah gol Piala Dunia.

Tujuan utama:

> Menjelaskan inferensi Bayesian untuk data hitungan, bukan membuat sistem prediksi sepak bola yang kompleks.

---

# Motivasi

Gol sepak bola adalah data hitungan:

- 0 gol
- 1 gol
- 2 gol
- 3 gol
- dan seterusnya

Karena nilainya berupa bilangan bulat tidak negatif, distribusi Poisson cocok sebagai model awal.

Dataset Piala Dunia memberi contoh nyata untuk menjelaskan konsep matematisnya.

---

# Pertanyaan Penelitian

Pertanyaan utama:

> Bagaimana model Bayesian Poisson dapat digunakan untuk memodelkan jumlah gol dalam satu pertandingan Piala Dunia?

Pertanyaan lanjutan:

> Berdasarkan Piala Dunia 2014, 2018, dan 2022, seperti apa distribusi prediktif posterior untuk jumlah gol pada satu pertandingan Piala Dunia 2026?

---

# Mengapa Poisson?

Distribusi Poisson digunakan untuk memodelkan jumlah kejadian dalam satu interval tetap.

Dalam proyek ini:

- kejadian: gol
- interval: satu pertandingan sepak bola
- variabel acak: total gol dalam satu pertandingan

Misalkan:

$$
Y = \text{total gol dalam satu pertandingan}
$$

Maka:

$$
Y \sim \text{Poisson}(\lambda)
$$

---

# Distribusi Poisson

Peluang untuk mendapatkan tepat \( y \) gol adalah:

$$
P(Y = y \mid \lambda) =
\frac{e^{-\lambda}\lambda^y}{y!}
$$

Keterangan:

- \( y \): jumlah gol yang diamati
- \( \lambda \): rata-rata gol per pertandingan
- \( \lambda > 0 \)

Jika \( \lambda \) besar, pertandingan dengan banyak gol menjadi lebih mungkin. Jika \( \lambda \) kecil, pertandingan dengan sedikit gol menjadi lebih mungkin.

---

# Apa yang Ditambahkan Bayes?

Dalam model Poisson biasa, \( \lambda \) sering dipandang sebagai satu nilai tetap yang tidak diketahui.

Dalam inferensi Bayes, \( \lambda \) dipandang sebagai parameter yang masih tidak pasti.

Kita tidak hanya bertanya:

> Berapa estimasi terbaik untuk \( \lambda \)?

Tetapi juga:

> Setelah melihat data, seberapa besar keyakinan kita terhadap berbagai nilai \( \lambda \)?

---

# Teorema Bayes

Inferensi Bayes didasarkan pada:

$$
P(\theta \mid data) =
\frac{P(data \mid \theta)P(\theta)}{P(data)}
$$

Untuk proyek ini:

$$
P(\lambda \mid data)
\propto
P(data \mid \lambda)P(\lambda)
$$

Secara sederhana:

```text
posterior = likelihood dari data x prior
```

---

# Distribusi Prior

Sebelum melihat data, kita memberi keyakinan awal terhadap \( \lambda \).

Karena \( \lambda \) harus bernilai positif, prior yang dipakai adalah Gamma:

$$
\lambda \sim \text{Gamma}(\alpha, \beta)
$$

Keterangan:

- \( \alpha \): parameter shape
- \( \beta \): parameter rate
- rata-rata prior:

$$
E[\lambda] = \frac{\alpha}{\beta}
$$

---

# Mengapa Prior Gamma?

Distribusi Gamma berguna karena:

- hanya menghasilkan nilai positif
- bentuknya fleksibel
- konjugat terhadap likelihood Poisson

Konjugat berarti:

> Jika prior adalah Gamma dan likelihood adalah Poisson, maka posterior juga berbentuk Gamma.

Ini membuat perhitungan matematis bersih dan cocok untuk mata kuliah Mathematical and Statistical Foundations.

---

# Mengapa Prior Ini?

Sesuai draft, prior utama yang dipakai adalah:

$$
\lambda \sim \text{Gamma}(1,1)
$$

Rata-rata prior:

$$
E[\lambda] = \frac{1}{1} = 1
$$

Interpretasi:

- prior ini lemah dan sederhana
- prior tidak memaksa rata-rata gol harus dekat nilai tertentu
- setelah 192 pertandingan diamati, posterior lebih banyak dipengaruhi data

---

# Data yang Dipakai

Data utama mengikuti draft:

```text
Piala Dunia 2014
Piala Dunia 2018
Piala Dunia 2022
```

Ringkasan data:

| Edisi | Pertandingan | Total gol | Rata-rata |
|---|---:|---:|---:|
| 2014 | 64 | 171 | 2.672 |
| 2018 | 64 | 169 | 2.641 |
| 2022 | 64 | 172 | 2.688 |

Total: 192 pertandingan dan 512 gol.

---

# Likelihood dari Data

Misalkan kita mengamati \( n \) pertandingan:

$$
y_1, y_2, ..., y_n
$$

Setiap jumlah gol pertandingan diasumsikan mengikuti:

$$
Y_i \mid \lambda \sim \text{Poisson}(\lambda)
$$

Ringkasan data yang penting:

- total gol: \( \sum y_i = 512 \)
- jumlah pertandingan: \( n = 192 \)

---

# Distribusi Posterior

Dengan prior Gamma dan likelihood Poisson:

$$
\lambda \mid data
\sim
\text{Gamma}(\alpha + \sum y_i, \beta + n)
$$

Karena priornya \( \text{Gamma}(1,1) \), maka:

$$
\lambda \mid data
\sim
\text{Gamma}(1 + 512, 1 + 192)
$$

Jadi:

$$
\lambda \mid data
\sim
\text{Gamma}(513,193)
$$

Rata-rata posterior:

$$
E[\lambda \mid data] = \frac{513}{193} = 2.658
$$

---

# Goodness-of-Fit

Notebook tidak hanya menghitung posterior. Notebook juga mengecek apakah pola frekuensi gol terlihat wajar untuk model Poisson.

Langkahnya:

- hitung frekuensi aktual untuk 0 gol, 1 gol, 2 gol, dan seterusnya
- hitung frekuensi yang diharapkan dari Poisson dengan rata-rata posterior
- bandingkan keduanya secara tabel dan grafik
- hitung statistik chi-square deskriptif

Bagian ini membantu menjawab apakah Poisson cukup masuk akal sebagai model agregat.

---

# Prediktif Posterior

Setelah posterior diperoleh, kita dapat memprediksi jumlah gol pada pertandingan baru.

Prediksi Bayes menghasilkan distribusi peluang:

```text
P(pertandingan baru memiliki 0 gol)
P(pertandingan baru memiliki 1 gol)
P(pertandingan baru memiliki 2 gol)
P(pertandingan baru memiliki 3 gol)
...
```

Ini disebut distribusi prediktif posterior.

Keunggulannya: model tidak hanya memberi satu angka prediksi, tetapi juga memperlihatkan ketidakpastian prediksi.

---

# Prediksi untuk 2026

Dengan posterior \( \text{Gamma}(513,193) \), prediksi untuk satu pertandingan Piala Dunia 2026 dihitung dengan distribusi prediktif posterior Gamma-Poisson.

Probabilitas prediksi diringkas sebagai peluang beberapa rentang jumlah gol.

Contoh hasil notebook:

- peluang 0 sampai 1 gol: sekitar 0.257
- peluang 2 sampai 3 gol: sekitar 0.466
- peluang 4 gol atau lebih: sekitar 0.277
- interval prediktif 90%: 0 sampai 6 gol

Interpretasi:

> Model memperkirakan pertandingan dengan 2 atau 3 gol paling umum, tetapi pertandingan dengan skor rendah atau tinggi tetap mungkin.

---

# Kekuatan dan Keterbatasan

Kekuatan:

- struktur matematis sederhana
- cocok untuk data hitungan
- menunjukkan prior, likelihood, posterior, dan prediksi
- mudah dijalankan di Jupyter

Keterbatasan:

- semua pertandingan memakai satu rata-rata gol yang sama
- kekuatan tim belum dimodelkan
- fase grup dan fase gugur belum dibedakan
- skor rendah dapat membutuhkan koreksi khusus
- model hierarkis dapat menjadi pengembangan lanjutan

---

# Kesimpulan

Model Bayesian Poisson cocok untuk menjelaskan pemodelan data hitungan.

Dalam tugas ini:

- Poisson memodelkan total gol per pertandingan
- Bayes memperbarui ketidakpastian tentang \( \lambda \)
- prior Gamma menghasilkan posterior konjugat yang rapi
- data 2014, 2018, dan 2022 menghasilkan posterior \( \text{Gamma}(513,193) \)
- distribusi prediktif posterior memberi prediksi probabilistik untuk 2026

Framing akhir:

> Draft teman tetap menjadi arah utama, lalu notebook menambahkan perhitungan, visualisasi, goodness-of-fit, dan prediksi 2026 secara konsisten.
