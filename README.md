# yenisim 📝🔁

**EN | Bulk file renamer — preview first, rename on --apply. One file, zero dependencies.**
**TR | Toplu dosya yeniden adlandırıcı — önce önizleme, --apply ile uygula. Tek dosya, sıfır bağımlılık.**

"Rename 300 photos in order", "clean spaces from filenames", "lowercase
everything" — PowerRename feels like overkill, online tools want uploads.
`yenisim` is one Python file that previews exactly what will happen, then
renames only when you say so.

"300 fotoğrafı sırayla adlandır", "dosya adlarındaki boşlukları temizle",
"hepsini küçük harf yap" — PowerRename gereğinden ağır, online araçlar yükleme
istiyor. `yenisim` tek Python dosyasıdır: önce tam olarak ne olacağını
gösterir, sen deyince uygular.

```
PREVIEW: 6 file(s) would be renamed:

  [dry] Foto (1).JPG  ->  tatil-001.jpg
  [dry] Foto (2).JPG  ->  tatil-002.jpg
  [dry] yeni  design final v2.PNG  ->  tatil-006.png

DRY-RUN: nothing renamed.
Uygulamak icin / to apply:  --apply
```

---

## 🇬🇧 English

### Operations

| Flag | What it does |
|---|---|
| `--start 1 --name tatil` | Number files: `tatil-001.jpg`, `tatil-002.jpg`, ... |
| `--lower` | Lowercase everything (extension too) |
| `--spaces` | Spaces → underscores (`my file.txt` → `my_file.txt`) |
| `--clean` | Remove weird characters (keeps letters, digits, `-`, `_`) |
| `--prefix TXT` / `--suffix TXT` | Add text before / after the name |
| `--find TXT --replace TXT` | Plain find & replace |
| `--pattern REGEX --replace TXT` | Regex find & replace |
| `-r` | Include subfolders (skips `.git`, `node_modules`, ...) |

### Safety

- **Dry-run by default** — you see the full list before anything happens
- Never overwrites: if a target name exists, it becomes `name (2).ext`
- Skips partial downloads (`.crdownload .part .tmp`) and hidden files
- Numbering, prefix and clean can be combined in one pass

### Install

Python 3.8+ — that's all:

```bash
curl -LO https://raw.githubusercontent.com/Volvox6767/yenisim/main/yenisim.py
```

### Examples

```bash
python yenisim.py ./Photos --start 1 --name tatil --lower --apply
python yenisim.py ./Docs --spaces --lower --apply
python yenisim.py . --find "IMG_" --replace "2026_" --apply
python yenisim.py . --pattern "copy|backup" --replace "" --apply
```

### FAQ

**Can it rename folders too?** Files only — safer.

**Collision with an existing file?** Auto-renamed to `name (2).ext`. Never overwritten.

**Turkish characters?** `--clean` keeps Unicode letters (`ç`, `ğ`, `ş` stay); combine with `--lower` for `İstanbul → istanbul`.

---

## 🇹🇷 Türkçe

### İşlemler

| Bayrak | Ne yapar? |
|---|---|
| `--start 1 --name tatil` | Dosyaları numaralandırır: `tatil-001.jpg`, `tatil-002.jpg`, ... |
| `--lower` | Hepsini küçük harf yapar (uzantı dahil) |
| `--spaces` | Boşlukları alt çizgi yapar (`benim dosya.txt` → `benim_dosya.txt`) |
| `--clean` | Tuhaf karakterleri siler (harf, rakam, `-`, `_` kalır) |
| `--prefix TXT` / `--suffix TXT` | İsimden önce / sonra metin ekler |
| `--find TXT --replace TXT` | Düz metin bul ve değiştir |
| `--pattern REGEX --replace TXT` | Düzenli ifade ile bul ve değiştir |
| `-r` | Alt klasörleri de işler (`.git`, `node_modules` atlanır) |

### Güvenlik

- **Varsayılan dry-run** — bir şey olmadan önce listeyi tam görürsün
- Asla üzerine yazmaz: hedef isim varsa `isim (2).ext` olur
- Yarım indirmeleri (`.crdownload .part .tmp`) ve gizli dosyaları atlar
- Numaralandırma + önek + temizlik tek seferde birleştirilebilir

### Kurulum

Python 3.8+ — hepsi bu:

```bash
curl -LO https://raw.githubusercontent.com/Volvox6767/yenisim/main/yenisim.py
```

### Örnekler

```bash
python yenisim.py ./Fotolar --start 1 --name tatil --lower --apply
python yenisim.py ./Belgeler --spaces --lower --apply
python yenisim.py . --find "IMG_" --replace "2026_" --apply
python yenisim.py . --pattern "kopya|yedek" --replace "" --apply
```

### SSS

**Klasörleri de adlandırır mı?** Sadece dosyaları — daha güvenli.

**Var olan dosyayla çakışırsa?** Otomatik `isim (2).ext` olur. Asla üzerine yazılmaz.

**Türkçe karakterler?** `--clean` Unicode harfleri korur (`ç`, `ğ`, `ş` kalır); `--lower` ile birleştirince `İstanbul → istanbul`.

---

Made with ❤ by **Ahmet Gedik** — [instagram.com/ahmetgedik67](https://www.instagram.com/ahmetgedik67)
Follow on Instagram for more free everyday tools.
Daha fazla ücretsiz günlük araç için Instagram'da takip edin.

License / Lisans: [MIT](LICENSE)
