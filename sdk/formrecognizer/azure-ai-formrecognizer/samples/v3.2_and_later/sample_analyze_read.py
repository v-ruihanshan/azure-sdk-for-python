"""
This code sample shows the adds on functionality of Prebuilt Read operations with the Azure Form Recognizer client library.
The async versions of the samples require Python 3.6 or later.
"""

    with open(path_to_sample_documents, "rb") as f:
        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-read", document=f,
            features=
            [AnalysisFeature.STYLE_FONT],
            [AnalysisFeature.FORMULAS],
            [AnalysisFeature.BARCODES],
            [AnalysisFeature.OCR_HIGH_RESOLUTION],
            [AnalysisFeature.LANGUAGES]
        )
    result = poller.result()


    print("----Barcode detected in the document----")
    for page in result.pages:
        for barcode in page.barcodes:
            print(f"Barcode value: '{barcode.value}' with confidence {barcode.confidence}")

    print("----Formulas detected in the document----")
    for page in result.pages:
        if page.formulas:
            print(f"----Formulas on page #{page.page_number}----")
            for formula in page.formulas:
                print(f"Formula '{formula}'")
