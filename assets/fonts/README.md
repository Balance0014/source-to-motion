# Sample CJK font

The two `STM-Sans-SC-*.ttf` files are small, renamed subsets of Google's [Noto Sans SC variable font](https://github.com/google/fonts/tree/main/ofl/notosanssc). They cover only the glyphs used by `examples/pulse-atlas-zh`, so the included Chinese example renders consistently without requiring a system font.

- Upstream commit: `5e8a3ba899557829a76cfdac30fa512bda91d7ca`
- Upstream file: `ofl/notosanssc/NotoSansSC[wght].ttf`
- Original SHA-256: `a3041811a78c361b1de50f953c805e0244951c21c5bd412f7232ef0d899af0da`
- Modification: instantiate weights 400 and 700, subset to example glyphs, rename family to STM Sans SC.
- Font license: [SIL Open Font License 1.1](OFL.txt). The repository's MIT license does not replace the font's OFL license.

For a new Chinese-language scene, install or provide a full CJK font with the needed glyphs. Do not assume these example subsets cover new product text.

## GapMine Latin sample font

`SpaceGrotesk-Variable.ttf` is the unmodified [Space Grotesk variable font](https://github.com/google/fonts/tree/main/ofl/spacegrotesk) from Google Fonts, used by the GapMine example. It is covered by its separate [SIL Open Font License 1.1](SpaceGrotesk-OFL.txt).

- Upstream file: `ofl/spacegrotesk/SpaceGrotesk[wght].ttf`
- Upstream font commit: `2861cb7b12f90c0a294a12ed666e381e2211872f`
- Bundled file SHA-256: `acad6de1fc93436f5c0f1f4137751ef04f1aea3063e7036535970ffcfbd79f72`
