# Source and facts

`source.json` contains `source`, `locator`, `kind`, `ocr`, and `text`. Keep source text local; do not commit private customer inputs. A fact manifest has:

```json
{
  "source": "https://example.com/product",
  "facts": [
    {
      "id": "speed",
      "display": "10–100×",
      "evidence": "10-100x faster",
      "locator": "README.md > Highlights; publisher benchmark"
    }
  ]
}
```

Evidence is an exact excerpt from the source, not a paraphrase. The display may shorten wording if it preserves meaning and qualifiers. A product's self-reported performance must say so on screen or in the accompanying description. Keep units, time periods, sample sizes, baselines, and ranges. Use source dates when material. When sources conflict, resolve from the latest authoritative material or omit the claim.

For a dashboard, collect concrete product facts for every peripheral panel: supported inputs, actual commands or API paths, transformations, and outputs. Do not fill the frame with feature labels and unlabeled decorative charts. If you add mutable GitHub stars or forks, record the API response values and capture timestamp in `source.json`, cite the API endpoint in each fact, and label the on-screen card as a dated GitHub snapshot. Those counts describe the repository, not product results. Never substitute them for missing performance or usage data.

For cross-language output, set `source_language` and `output_language` in the manifest. Keep `evidence` in the source language and `display` in the video language. Review the translation beside the original sentence; see `localization.md`.

The local verifier checks that evidence occurs in extracted text and that all numbers shown in a fact's display occur in its evidence. It does not verify the truth of a publisher claim or the accuracy of a translation. Inspect those manually. If a fact comes from a linked source, extract that linked page into a second source file and cite it in the locator; a single-source checker cannot automatically follow links.
