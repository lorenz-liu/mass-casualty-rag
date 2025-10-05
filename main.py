from toolkit.converter import MarkdownConverter

if __name__ == "__main__":
    converter = MarkdownConverter()
    print(converter.convert("https://em.umaryland.edu/files/uploads/ems/salt_2008.pdf"))
