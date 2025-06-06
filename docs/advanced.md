% SPDX-FileCopyrightText: 2022 James R. Barlow
% SPDX-License-Identifier: CC-BY-SA-4.0

# Advanced features

## Control of unpaper

OCRmyPDF uses `unpaper` to provide the implementation of the
`--clean` and `--clean-final` arguments.
[unpaper](https://github.com/Flameeyes/unpaper/blob/main/doc/basic-concepts.md)
provides a variety of image processing filters to improve images.

By default, OCRmyPDF uses only `unpaper` arguments that were found to
be safe to use on almost all files without having to inspect every page
of the file afterwards. This is particularly true when only `--clean`
is used, since that instructs OCRmyPDF to only clean the image before
OCR and not the final image.

However, if you wish to use the more aggressive options in `unpaper`,
you may use `--unpaper-args '...'` to override the OCRmyPDF's defaults
and forward other arguments to unpaper. This option will forward
arguments to `unpaper` without any knowledge of what that program
considers to be valid arguments. The string of arguments must be quoted
as shown in the examples below. No filename arguments may be included.
OCRmyPDF will assume it can append input and output filename of
intermediate images to the `--unpaper-args` string.

In this example, we tell `unpaper` to expect two pages of text on a
sheet (image), such as occurs when two facing pages of a book are
scanned. `unpaper` uses this information to deskew each independently
and clean up the margins of both.

```bash
ocrmypdf --clean --clean-final --unpaper-args '--layout double' input.pdf output.pdf
ocrmypdf --clean --clean-final --unpaper-args '--layout double --no-noisefilter' input.pdf output.pdf
```

:::{warning}
Some `unpaper` features will reposition text within the image.
`--clean-final` is recommended to avoid this issue.
:::

:::{warning}
Some `unpaper` features cause multiple input or output files to be
consumed or produced. OCRmyPDF requires `unpaper` to consume one
file and produce one file; errors will result if this assumption is not
met.
:::

:::{note}
`unpaper` uses uncompressed PBM/PGM/PPM files for its intermediate
files. For large images or documents, it can take a lot of temporary
disk space.
:::

## Changing the PDF renderer

rasterizing

: Converting a PDF to an image for display.

rendering

: Creating a new PDF from other data (such as an existing PDF).

OCRmyPDF has these PDF renderers: `sandwich` and `hocr`. The
renderer may be selected using `--pdf-renderer`. The default is
`auto` which lets OCRmyPDF select the renderer to use. Currently,
`auto` always selects `hocr`.

### The `hocr` renderer

:::{versionchanged} 16.0.0
:::

In both renderers, a text-only layer is rendered and sandwiched (overlaid)
on to either the original PDF page, or newly rasterized version of the
original PDF page (when `--force-ocr` is used). In this way, loss
of PDF information is generally avoided. (You may need to disable PDF/A
conversion and optimization to eliminate all lossy transformations.)

The current approach used by the new hOCR renderer is a re-implementation
of Tesseract's PDF renderer, using the same Glyphless font and general
ideas, but fixing many technical issues that impeded it. The new hocr
provides better text placement accuracy, avoids issues with word
segmentation, and provides better positioning of skewed text.

Using the experimental API, it is also possible to edit the OCR output
from Tesseract, using any tool that is capable of editing hOCR files.

Older versions of this renderer did not support non-Latin languages, but
it is now universal.

### The `sandwich` renderer

The `sandwich` renderer uses Tesseract's text-only PDF feature,
which produces a PDF page that lays out the OCR in invisible text.

Currently some problematic PDF viewers like Mozilla PDF.js and macOS
Preview have problems with segmenting its text output, and
mightrunseveralwordstogether. It also does not implement right to left
fonts (Arabic, Hebrew, Persian). The output of this renderer cannot
be edited. The sandwich renderer is retained for testing.

When image preprocessing features like `--deskew` are used, the
original PDF will be rendered as a full page and the OCR layer will be
placed on top.

## Rendering and rasterizing options

:::{versionadded} 14.3.0
:::

The `--continue-on-soft-render-error` option allows OCRmyPDF to
proceed if a page cannot be rasterized/rendered. This is useful if you are
trying to get the best possible OCR from a PDF that is not well-formed,
and you are willing to accept some pages that may not visually match the
input, and that may not OCR well.

## Color conversion strategy

:::{versionadded} 15.0.0
:::

OCRmyPDF uses Ghostscript to convert PDF to PDF/A. In some cases, this
conversion requires color conversion. The default strategy is to convert
using the `LeaveColorUnchanged` strategy, which preserves the original
color space wherever possible (some rare color spaces might still be
converted).

Usually document scanners produce PDFs in the sRGB color space, and do
not need to be converted, so the default strategy is appropriate.

Suppose that you have a document that was prepared for professional
printing in a Separation or CMYK color space, and text was converted to
curves. In this case, you may want to use a different color conversion
strategy. The `--color-conversion-strategy` option allows you to select a
different strategy, such as `RGB`.

## Return code policy

OCRmyPDF writes all messages to `stderr`. `stdout` is reserved for
piping output files. `stdin` is reserved for piping input files.

The return codes generated by the OCRmyPDF are considered part of the
stable user interface. They may be imported from
`ocrmypdf.exceptions`.

```{eval-rst}
.. list-table:: Return codes
    :widths: 5 35 60
    :header-rows: 1

    *   - Code
        - Name
        - Interpretation
    *   - 0
        - ``ExitCode.ok``
        - Everything worked as expected.
    *   - 1
        - ``ExitCode.bad_args``
        - Invalid arguments, exited with an error.
    *   - 2
        - ``ExitCode.input_file``
        - The input file does not seem to be a valid PDF.
    *   - 3
        - ``ExitCode.missing_dependency``
        - An external program required by OCRmyPDF is missing.
    *   - 4
        - ``ExitCode.invalid_output_pdf``
        - An output file was created, but it does not seem to be a valid PDF. The file will be available.
    *   - 5
        - ``ExitCode.file_access_error``
        - The user running OCRmyPDF does not have sufficient permissions to read the input file and write the output file.
    *   - 6
        - ``ExitCode.already_done_ocr``
        - The file already appears to contain text so it may not need OCR. See output message.
    *   - 7
        - ``ExitCode.child_process_error``
        - An error occurred in an external program (child process) and OCRmyPDF cannot continue.
    *   - 8
        - ``ExitCode.encrypted_pdf``
        - The input PDF is encrypted. OCRmyPDF does not read encrypted PDFs. Use another program such as ``qpdf`` to remove encryption.
    *   - 9
        - ``ExitCode.invalid_config``
        - A custom configuration file was forwarded to Tesseract using ``--tesseract-config``, and Tesseract rejected this file.
    *   - 10
        - ``ExitCode.pdfa_conversion_failed``
        - A valid PDF was created, PDF/A conversion failed. The file will be available.
    *   - 15
        - ``ExitCode.other_error``
        - Some other error occurred.
    *   - 130
        - ``ExitCode.ctrl_c``
        - The program was interrupted by pressing Ctrl+C.

```

(tmpdir)=
## Changing temporary storage location

OCRmyPDF generates many temporary files during processing.

To change where temporary files are stored, change the `TMPDIR`
environment variable for ocrmypdf's environment. (Python's
`tempfile.gettempdir()` returns the root directory in which temporary
files will be stored.) For example, one could redirect `TMPDIR` to a
large RAM disk to avoid wear on HDD/SSD and potentially improve
performance.

On Windows, the `TEMP` environment variable is used instead.

## Debugging the intermediate files

OCRmyPDF normally saves its intermediate results to a temporary folder
and deletes this folder when it exits, whether it succeeded or failed.

If the `--keep-temporary-files` (`-k`) argument is issued on the
command line, OCRmyPDF will keep the temporary folder and print the location,
whether it succeeded or failed. An example message is:

```none
Temporary working files retained at:
/tmp/ocrmypdf.io.u20wpz07
```

When OCRmyPDF is launched as a snap, this corresponds to the snap filesystem, for instance:

> /tmp/snap-private-tmp/snap.ocrmypdf/tmp/ocrmypdf.io.u20wpz07

The organization of this folder is an implementation detail and subject
to change between releases. However the general organization is that
working files on a per page basis have the page number as a prefix
(starting with page 1), an infix indicates the processing stage, and a
suffix indicates the file type. Some important files include:

- `_rasterize.png` - what the input page looks like
- `_ocr.png` - the file that is sent to Tesseract for OCR; depending
  on arguments this may differ from the presentation image
- `_pp_deskew.png` - the image, after deskewing
- `_pp_clean.png` - the image, after cleaning with unpaper
- `_ocr_hocr.pdf` - the OCR file; appears as a blank page with invisible
  text embedded
- `_ocr_hocr.txt` - the OCR text (not necessarily all text on the page,
  if the page is mixed format)
- `fix_docinfo.pdf` - a temporary file created to fix the PDF DocumentInfo
  data structure
- `graft_layers.pdf` - the rendered PDF with OCR layers grafted on
- `pdfa.pdf` - `graft_layers.pdf` after conversion to PDF/A
- `pdfa.ps` - a PostScript file used by Ghostscript for PDF/A conversion
- `optimize.pdf` - the PDF generated before optimization
- `optimize.out.pdf` - the PDF generated by optimization
- `origin` - the input file
- `origin.pdf` - the input file or the input image converted to PDF
- `images/*` - images extracted during the optimization process; here
  the prefix indicates a PDF object ID not a page number
