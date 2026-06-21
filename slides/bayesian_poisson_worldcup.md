# Model Bayesian Poisson untuk Gol Piala Dunia

Posisi materi:

> Presentasi ini berangkat dari draft teman sebagai dasar riset, lalu dipoles menjadi studi kasus Bayesian Poisson yang lebih fokus untuk data jumlah gol Piala Dunia.

Gagasan utama:

> Tujuan utama bukan membuat AI prediksi sepak bola. Tujuan utama adalah menjelaskan inferensi Bayesian untuk data hitungan.

---

# Motivasi

Gol sepak bola adalah data hitungan:

- 0 gol
- 1 gol
- 2 gol
- 3 gol
- dan seterusnya

Karena jumlah gol berbentuk bilangan bulat tidak negatif, distribusi Poisson cocok sebagai model awal.

Dataset Piala Dunia memberi contoh nyata untuk menjelaskan konsep matematisnya.

---

# Pertanyaan Penelitian

Pertanyaan utama:

> Bagaimana model Bayesian Poisson dapat digunakan untuk memodelkan jumlah gol dalam satu pertandingan Piala Dunia?

Demonstrasi tambahan:

> Jika model belajar dari Piala Dunia 2010, 2014, dan 2018, apakah jumlah gol pada Piala Dunia 2022 masih masuk akal menurut model?

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

Peluang mengamati tepat \( y \) gol adalah:

$$
P(Y = y \mid \lambda) =
\frac{e^{-\lambda}\lambda^y}{y!}
$$

Keterangan:

- \( y \): jumlah gol yang diamati
- \( \lambda \): rata-rata gol yang diharapkan per pertandingan
- \( \lambda > 0 \)

Jika \( \lambda = 2.5 \), model mengharapkan sekitar 2.5 gol per pertandingan.

---

# Apa yang Ditambahkan Bayesian?

Dalam model Poisson biasa, \( \lambda \) dipandang sebagai nilai tetap yang tidak diketahui.

Dalam inferensi Bayesian, \( \lambda \) dipandang sebagai sesuatu yang tidak pasti.

Kita tidak hanya bertanya:

> Berapa satu estimasi terbaik untuk \( \lambda \)?

Tetapi bertanya:

> Setelah melihat data, seberapa kuat keyakinan kita terhadap berbagai nilai \( \lambda \)?

---

# Teorema Bayes

Inferensi Bayesian didasarkan pada:

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

Sebelum melihat data Piala Dunia, kita memberikan keyakinan awal terhadap \( \lambda \).

Karena \( \lambda \) harus bernilai positif, kita menggunakan prior Gamma:

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

Ini membuat perhitungan matematis menjadi bersih dan cocok untuk mata kuliah Mathematical and Statistical Foundations.

---

# Mengapa Prior Ini?

Di notebook, prior yang digunakan adalah:

$$
\lambda \sim \text{Gamma}(5, 2)
$$

Rata-rata prior:

$$
E[\lambda] = \frac{5}{2} = 2.5
$$

Alasannya:

- Piala Dunia modern biasanya memiliki rata-rata sekitar 2 sampai 3 gol per pertandingan
- 2.5 adalah keyakinan awal yang masuk akal sebelum melihat data training
- prior ini lemah dibandingkan 192 pertandingan training dari 2010-2018

Jadi prior memberi arah awal, tetapi posterior tetap didominasi oleh data.

---

# Likelihood dari Data Pertandingan

Misalkan kita mengamati \( n \) pertandingan:

$$
y_1, y_2, ..., y_n
$$

Setiap jumlah gol pertandingan diasumsikan mengikuti:

$$
Y_i \sim \text{Poisson}(\lambda)
$$

Ringkasan data yang penting:

- total gol: \( \sum y_i \)
- jumlah pertandingan: \( n \)

---

# Distribusi Posterior

Dengan prior Gamma dan likelihood Poisson:

$$
\lambda \mid data
\sim
\text{Gamma}(\alpha + \sum y_i, \beta + n)
$$

Sehingga:

$$
\alpha_{post} = \alpha + \sum y_i
$$

$$
\beta_{post} = \beta + n
$$

Rata-rata posterior:

$$
E[\lambda \mid data] =
\frac{\alpha_{post}}{\beta_{post}}
$$

---

# Prediktif Posterior

Setelah posterior diperoleh, kita dapat memprediksi jumlah gol pertandingan berikutnya.

Prediksi Bayesian menghasilkan distribusi peluang:

```text
P(pertandingan berikutnya memiliki 0 gol)
P(pertandingan berikutnya memiliki 1 gol)
P(pertandingan berikutnya memiliki 2 gol)
P(pertandingan berikutnya memiliki 3 gol)
...
```

Ini disebut distribusi prediktif posterior.

Keunggulannya: model tidak hanya memberi satu angka prediksi, tetapi juga ketidakpastian prediksi.

---

# Rencana Dataset

Data training:

```text
Piala Dunia 2010
Piala Dunia 2014
Piala Dunia 2018
```

Data evaluasi:

```text
Piala Dunia 2022
```

Alasan:

- 2022 sudah lengkap
- Piala Dunia modern memiliki pola skor yang relatif lebih mirip
- turnamen lama memiliki format dan pola gol yang berbeda

---

# Evaluasi

Karena model memprediksi data hitungan, evaluasi utama juga sebaiknya berbasis hitungan.

Pemeriksaan yang digunakan:

- membandingkan rata-rata prediksi dengan rata-rata aktual 2022
- menghitung mean absolute error
- menghitung root mean squared error
- mengecek apakah gol aktual 2022 masuk akal dalam distribusi prediktif posterior

Klasifikasi opsional:

```text
positif = lebih dari 2.5 gol
negatif = 2 gol atau kurang
```

Dari sini kita dapat menghitung true positive, false positive, true negative, dan false negative.

---

# Aktual 2022 vs Prediksi Model

Notebook membandingkan frekuensi gol aktual 2022 dengan probabilitas prediksi dari distribusi prediktif posterior.

Contoh interpretasi:

```text
Jika model memberi probabilitas tinggi untuk 2 atau 3 gol,
maka banyak pertandingan 2022 dengan 2 atau 3 gol masih masuk akal.
```

Kita juga membandingkan dua pilihan training:

```text
Model modern: 2010-2018
Model historis: 1930-2018
```

Perbandingan ini menjelaskan mengapa data Piala Dunia yang sangat lama belum tentu menjadi acuan terbaik untuk sepak bola modern.

---

# Kekuatan dan Keterbatasan

Kekuatan:

- struktur matematis sederhana
- cocok untuk data hitungan
- menunjukkan prior, likelihood, posterior, dan prediksi
- mudah direproduksi di Jupyter

Keterbatasan:

- semua pertandingan memakai satu rata-rata gol yang sama
- kekuatan tim tidak dimodelkan
- kekuatan lawan diabaikan
- fase grup dan knockout diperlakukan sama
- kejadian gol mungkin tidak sepenuhnya independen

---

# Kesimpulan

Model Bayesian Poisson cocok untuk menjelaskan pemodelan data hitungan.

Dalam tugas ini:

- Poisson memodelkan total gol per pertandingan
- Bayesian inference memperbarui ketidakpastian tentang \( \lambda \)
- prior Gamma menghasilkan posterior konjugat yang rapi
- data Piala Dunia menjadi demonstrasi nyata
- Jupyter menunjukkan perhitungan end-to-end

Framing akhir:

> Kita memoles draft teman menjadi penjelasan statistik yang fokus, lalu mendukungnya dengan notebook Piala Dunia yang reproducible.
