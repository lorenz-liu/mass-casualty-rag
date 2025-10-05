from docling.document_converter import DocumentConverter


class FormatConverter:
    _converter = DocumentConverter()

    @classmethod
    def _get_document(cls, source):
        return cls._converter.convert(source).document

    @classmethod
    def convert(cls, source):
        raise NotImplementedError("Subclasses must implement convert method")


class MarkdownConverter(FormatConverter):
    @classmethod
    def convert(cls, source):
        return cls._get_document(source).export_to_markdown()


class JSONConverter(FormatConverter):
    @classmethod
    def convert(cls, source):
        return cls._get_document(source).export_to_dict()


class TextConverter(FormatConverter):
    @classmethod
    def convert(cls, source):
        return cls._get_document(source).export_to_text()


class HTMLConverter(FormatConverter):
    @classmethod
    def convert(cls, source):
        return cls._get_document(source).export_to_html()
