# Sample CJK font

The two `STM-Sans-SC-*.ttf` files are small, renamed subsets of Google's [Noto Sans SC variable font](https://github.com/google/fonts/tree/main/ofl/notosanssc). They cover only the glyphs used by `examples/pulse-atlas-zh`, so the included Chinese example renders consistently without requiring a system font.

- Upstream commit: `5e8a3ba899557829a76cfdac30fa512bda91d7ca`
- Upstream file: `ofl/notosanssc/NotoSansSC[wght].ttf`
- Original SHA-256: `a3041811a78c361b1de50f953c805e0244951c21c5bd412f7232ef0d899af0da`
- Modification: instantiate weights 400 and 700, subset to example glyphs, rename family to STM Sans SC.
- Font license: [SIL Open Font License 1.1](OFL.txt). The repository's MIT license does not replace the font's OFL license.

For a new Chinese-language scene, install or provide a full CJK font with the needed glyphs. Do not assume these example subsets cover new product text.
