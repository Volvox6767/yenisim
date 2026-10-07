#!/usr/bin/env python3
"""
yenisim - Bulk file renamer. Offline, one file, zero dependencies.

EN: "Rename 300 photos in order", "clean these ugly spaces from filenames",
    "lowercase everything" - one command, preview first, nothing renamed
    until you say --apply.
TR: "300 fotorafi sirala", "dosya adlarindaki bosluklari temizle",
    "hepsini kucuk harf yap" - tek komut, once onizleme, --apply deyince uygular.

by Ahmet Gedik - instagram.com/ahmetgedik67
"""

import argparse
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

AUTHOR = "Ahmet Gedik"
INSTAGRAM = "https://www.instagram.com/ahmetgedik67"
VERSION = "1.0.0"

TRANSIENT = {".crdownload", ".part", ".tmp", ".download"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", "_duplicates"}


def collect(folder, recursive):
    files = []
    if recursive:
        for root, dirs, names in os.walk(folder):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
            for n in names:
                files.append(os.path.join(root, n))
    else:
        for n in sorted(os.listdir(folder)):
            p = os.path.join(folder, n)
            if os.path.isfile(p):
                files.append(p)
    return [f for f in files
            if os.path.splitext(f)[1].lower() not in TRANSIENT
            and not os.path.basename(f).startswith(".")]


def build_plan(files, args):
    """Return [(old, new)] for files whose name actually changes."""
    plan = []
    counters = {}
    for idx, path in enumerate(files):
        folder = os.path.dirname(path)
        stem, ext = os.path.splitext(os.path.basename(path))
        orig_stem = stem

        if args.lower:
            stem = stem.lower()
            ext = ext.lower()
        if args.spaces:
            stem = re.sub(r"\s+", args.spaces_char if args.spaces_char != "-" else "_", stem)
            stem = re.sub(r"_{2,}", "_", stem).strip("_")
        if args.clean:
            stem = re.sub(r"[^\w\-]+", "_", stem, flags=re.UNICODE)
            stem = re.sub(r"_{2,}", "_", stem).strip("_")
        if args.prefix:
            stem = args.prefix + stem
        if args.suffix:
            stem = stem + args.suffix
        if args.find is not None:
            stem = stem.replace(args.find, args.replace or "")
        if args.pattern is not None:
            try:
                stem = re.sub(args.pattern, args.replace or "", stem)
            except re.error as e:
                print(f"ERROR: bad regex --pattern: {e}")
                sys.exit(1)
        if args.start is not None:
            i = args.start + idx
            num = str(i).zfill(args.digits)
            if args.name:
                stem = f"{args.name}-{num}"
            else:
                stem = f"{orig_stem}-{num}" if not args.name else f"{args.name}-{num}"

        new = os.path.join(folder, stem + ext)
        if os.path.abspath(new) != os.path.abspath(path):
            plan.append((path, new))
    return plan


def dedupe(plan):
    """Ensure no two renames target the same path; ensure target doesn't collide with an untouched file."""
    seen = {}
    final = []
    taken = {os.path.abspath(old) for old, _ in plan}
    # count existing files not being renamed (potential collision targets)
    existing = set()
    for old, new in plan:
        folder = os.path.dirname(new)
        try:
            for n in os.listdir(folder):
                existing.add(os.path.abspath(os.path.join(folder, n)))
        except OSError:
            pass
    for old, new in plan:
        root, ext = os.path.splitext(new)
        cand = new
        k = 2
        while (os.path.abspath(cand) in seen
               or (os.path.exists(cand) and os.path.abspath(cand) not in taken
                   and os.path.abspath(cand) != os.path.abspath(old))):
            cand = f"{root} ({k}){ext}"
            k += 1
        seen[os.path.abspath(cand)] = old
        final.append((old, cand))
    return final


def main():
    ap = argparse.ArgumentParser(
        prog="yenisim",
        description="Bulk file renamer - preview first, rename on --apply. / "
                    "Toplu dosya adlandirici - once onizleme, --apply ile uygula.",
        epilog=f"Made with \u2764 by {AUTHOR} - {INSTAGRAM}\nVersion {VERSION} (MIT)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("folder", nargs="?", default=".", help="folder to process (default: current) / islenecek klasor")
    ap.add_argument("-r", "--recursive", action="store_true", help="include subfolders / alt klasorler de")
    ap.add_argument("--lower", action="store_true", help="lowercase everything / tumunu kucuk harf yap")
    ap.add_argument("--spaces", action="store_true", help="replace spaces with underscore / bosluklari _ yap")
    ap.add_argument("--clean", action="store_true", help="remove weird chars (keep A-z 0-9 - _) / tuhaf karakterleri sil")
    ap.add_argument("--prefix", metavar="TXT", help="add prefix / onek ekle")
    ap.add_argument("--suffix", metavar="TXT", help="add suffix before extension / uzanti onceki son ek")
    ap.add_argument("--find", metavar="TXT", help="find & replace (plain text) / bul ve degistir")
    ap.add_argument("--replace", metavar="TXT", default="", help="replacement text / yerine konacak metin")
    ap.add_argument("--pattern", metavar="REGEX", help="find & replace with regex / duzenli ifade ile degistir")
    ap.add_argument("--start", metavar="N", type=int, help="number files starting from N / dosyalari N'den numaralandir")
    ap.add_argument("--name", metavar="TXT", help="base name when numbering (default: keep original + -N) / numaralama adi")
    ap.add_argument("--digits", metavar="N", type=int, default=3, help="padding for numbers (default 3) / sifir doldurma")
    ap.add_argument("--apply", action="store_true", help="really rename (default: preview) / gerceklestir (varsayilan: onizleme)")
    ap.add_argument("--version", action="version", version=f"yenisim {VERSION}")
    args = ap.parse_args()

    folder = os.path.abspath(args.folder)
    if not os.path.isdir(folder):
        print(f"ERROR: not a folder / klasor degil: {folder}")
        sys.exit(1)

    files = collect(folder, args.recursive)
    if not files:
        print("No files found / dosya bulunamadi.")
        sys.exit(0)

    plan = build_plan(files, args)
    plan = dedupe(plan)

    if not plan:
        print("Nothing to rename - all names already clean. / Degisecek isim yok.")
        sys.exit(0)

    if not args.apply:
        print(f"PREVIEW: {len(plan)} file(s) would be renamed / {len(plan)} dosya yeniden adlandirilacak:\n")
        for old, new in plan:
            o, n = os.path.basename(old), os.path.basename(new)
            rel = os.path.relpath(os.path.dirname(old), folder)
            loc = "" if rel == "." else rel + os.sep
            print(f"  [dry] {loc}{o}  ->  {n}")
        print("\nDRY-RUN: nothing renamed. Hicbir sey degistirilmedi.")
        print("Uygulamak icin / to apply:  --apply")
        sys.exit(0)

    ok = fail = 0
    for old, new in plan:
        try:
            os.rename(old, new)
            ok += 1
            print(f"  \u2714 {os.path.basename(old)}  ->  {os.path.basename(new)}")
        except OSError as e:
            fail += 1
            print(f"  \u2718 {os.path.basename(old)}: {e}")
    print(f"\nDone: {ok} renamed, {fail} failed. / {ok} adlandirildi, {fail} hata.")
    if fail:
        sys.exit(2)
    print(f"\nMade with \u2764 by {AUTHOR} - {INSTAGRAM}")


if __name__ == "__main__":
    main()
