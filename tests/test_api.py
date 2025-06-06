# SPDX-FileCopyrightText: 2022 James R. Barlow
# SPDX-License-Identifier: MPL-2.0

from __future__ import annotations

import pickle
from io import BytesIO
from pathlib import Path

import pytest
from pdfminer.high_level import extract_text

import ocrmypdf
import ocrmypdf._pipelines
import ocrmypdf.api


def test_language_list():
    with pytest.raises(
        (ocrmypdf.exceptions.InputFileError, ocrmypdf.exceptions.MissingDependencyError)
    ):
        ocrmypdf.ocr('doesnotexist.pdf', '_.pdf', language=['eng', 'deu'])


def test_stream_api(resources: Path):
    in_ = (resources / 'graph.pdf').open('rb')
    out = BytesIO()

    ocrmypdf.ocr(in_, out)
    out.seek(0)
    assert b'%PDF' in out.read(1024)




def test_hocr_result_json():
    result = ocrmypdf._pipelines._common.HOCRResult(
        pageno=1,
        pdf_page_from_image=Path('a'),
        hocr=Path('b'),
        textpdf=Path('c'),
        orientation_correction=180,
    )
    assert (
        result.to_json()
        == '{"pageno": 1, "pdf_page_from_image": {"Path": "a"}, "hocr": {"Path": "b"}, '
        '"textpdf": {"Path": "c"}, "orientation_correction": 180}'
    )
    assert ocrmypdf._pipelines._common.HOCRResult.from_json(result.to_json()) == result


def test_hocr_result_pickle():
    result = ocrmypdf._pipelines._common.HOCRResult(
        pageno=1,
        pdf_page_from_image=Path('a'),
        hocr=Path('b'),
        textpdf=Path('c'),
        orientation_correction=180,
    )
    assert result == pickle.loads(pickle.dumps(result))
