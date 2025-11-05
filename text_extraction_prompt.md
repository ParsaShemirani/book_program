# Book Page Extraction Instructions
If there is main text, extract the markdown representation of it in this field. This is the running text and does not include elements like the header, footer, chapter names and numbers, etc. It does not include any non text elements either like figures, images. It is what a narrator would read out loud. 

## General rules
- Do not add, take away, or modify any content. 
- Do not complete cut-off sentences. Only extract exactly what is visible.
- Extract the content exactly as is and in its full.
- Do not include any content besides the text extraction of the page.

## Markdown formatting rules you must follow
- Use `#`, `##`, `###` for section headings if they are visually distinguishable as titles, subtitles, or numbered sections.
- Convert all bulleted lists into proper Markdown lists using `- ` or `* ` instead of OCR bullet characters like `•`.
- Preserve all paragraphs as plain text (separated by a blank line).
- If there are quotations or dialogue, wrap them in Markdown blockquotes using `>`.
- If text is emphasized (italics, bold, underlined in the book), convert it into Markdown emphasis (`*italic*`, `**bold**`).