"""
This code sample shows Prebuilt Read operations with the Azure Form Recognizer client library.
The async versions of the samples require Python 3.6 or later.

To learn more, please visit the documentation - Quickstart: Form Recognizer Python client library SDKs
https://docs.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/quickstarts/try-v3-python-sdk
"""

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

"""
Remember to remove the key from your code when you're done, and never post it publicly. For production, use
secure methods to store and access your credentials. For more information, see 
https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-security?tabs=command-line%2Ccsharp#environment-variables-and-application-configuration
"""
endpoint = "YOUR_FORM_RECOGNIZER_ENDPOINT"
key = "YOUR_FORM_RECOGNIZER_KEY"

def format_bounding_region(bounding_regions):
    if not bounding_regions:
        return "N/A"
    return ", ".join(
        f"Page #{region.page_number}: {format_polygon(region.polygon)}"
        for region in bounding_regions
    )


def format_polygon(polygon):
    if not polygon:
        return "N/A"
    return ", ".join([f"[{p.x}, {p.y}]" for p in polygon])


def analyze_read():
    # sample document
    formUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/sample-layout.pdf"

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    poller = document_analysis_client.begin_analyze_document_from_url(
        "prebuilt-read", formUrl)
    result = poller.result()

    print("----Languages detected in the document----")
    for language in result.languages:
        print(
            f"Language code: '{language.locale}' with confidence {language.confidence}"
        )

    print("----Styles detected in the document----")
    for style in result.styles:
        if style.is_handwritten:
            print("Found the following handwritten content: ")
            print(
                ",".join(
                    [
                        result.content[span.offset : span.offset + span.length]
                        for span in style.spans
                    ]
                )
            )
        if style.font_style:
            print(
                f"The document contains '{style.font_style}' font style, applied to the following text: "
            )
            print(
                ",".join(
                    [
                        result.content[span.offset : span.offset + span.length]
                        for span in style.spans
                    ]
                )
            )

    for page in result.pages:
        print(f"----Analyzing document from page #{page.page_number}----")
        print(
            f"Page has width: {page.width} and height: {page.height}, measured with unit: {page.unit}"
        )

        for line_idx, line in enumerate(page.lines):
            words = line.get_words()
            print(
                f"...Line # {line_idx} has {len(words)} words and text '{line.content}' within bounding polygon '{format_polygon(line.polygon)}'"
            )

            for word in words:
                print(
                    f"......Word '{word.content}' has a confidence of {word.confidence}"
                )

        for selection_mark in page.selection_marks:
            print(
                f"...Selection mark is '{selection_mark.state}' within bounding polygon "
                f"'{format_polygon(selection_mark.polygon)}' and has a confidence of {selection_mark.confidence}"
            )


    if len(result.paragraphs) > 0:
        print(f"----Detected #{len(result.paragraphs)} paragraphs in the document----")
        for paragraph in result.paragraphs:
            print(
                f"Found paragraph with role: '{paragraph.role}' within {format_bounding_region(paragraph.bounding_regions)} bounding region"
            )
            print(f"...with content: '{paragraph.content}'")

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

    print("----------------------------------------")


if __name__ == "__main__":
    import sys
    from azure.core.exceptions import HttpResponseError

    try:
        analyze_read()
    except HttpResponseError as error:
        print(
            "For more information about troubleshooting errors, see the following guide: "
            "https://aka.ms/azsdk/python/formrecognizer/troubleshooting"
        )
        # Examples of how to check an HttpResponseError
        # Check by error code:
        if error.error is not None:
            if error.error.code == "InvalidImage":
                print(f"Received an invalid image error: {error.error}")
            if error.error.code == "InvalidRequest":
                print(f"Received an invalid request error: {error.error}")
            # Raise the error again after printing it
            raise
        # If the inner error is None and then it is possible to check the message to get more information:
        if "Invalid request".casefold() in error.message.casefold():
            print(f"Uh-oh! Seems there was an invalid request: {error}")
        # Raise the error again
        raise

