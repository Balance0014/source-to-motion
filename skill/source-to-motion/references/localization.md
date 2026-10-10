# Language and translation

Use the user's requested output language. If none is given, use the source's main language. Produce one clean language per video; bilingual captions need a deliberate two-language layout and a direct user request.

For a translated video, retain the exact original quote in each fact's `evidence`, put the screen wording in `display`, and add `source_language` and `output_language` to the manifest. Keep product names as styled by their owner unless the source supplies a localized name. Translate the meaning, not the typography; shorten only if the comparison, unit, time period, qualifier, and attribution survive.

The numeric verifier catches added numbers. It cannot certify that a translation preserves meaning. Read every translated card beside the source sentence. A claim like "median response was 12 minutes in the last 30 days" must not become "average response is 12 minutes" or lose the time period.

Choose fonts before layout. Check glyph coverage for Chinese and other non-Latin scripts, then inspect full-size video frames for tofu boxes, awkward line breaks, punctuation, and illegible captions. `examples/pulse-atlas-zh` demonstrates an English brief rendered as a Chinese video, with an original-language evidence manifest.
