"Minimalist XML library for reading, writing, creating and editing an element tree."

__all__ = ["Element", "read", "parse"]

import copy
import io
import xml.sax
import xml.sax.saxutils


class Element:
    "XML element. Contains a reference to superelement and subelements (if any)."

    repr_indent = 2
    xml_decl = True

    def __init__(self, tag, *subelements, **attrs):
        self.tag = tag
        self.attrs = {}
        for name, value in attrs.items():
            self[name] = value
        self.superelement = None
        self.subelements = []
        for subelement in subelements:
            self.append(subelement)

    def __str__(self):
        "Return the string representation of the element's starting tag."
        outfile = io.StringIO()
        outfile.write(f"<{self.tag}")
        for name, value in self.attrs.items():
            outfile.write(f" {name}={xml.sax.saxutils.quoteattr(value)}")
        if len(self):
            outfile.write(">")
        else:
            outfile.write("/>")
        return outfile.getvalue()

    def __repr__(self):
        "Return the string representation of the element and its subelements."
        outfile = io.StringIO()
        self.write(
            outfile, indent=self.repr_indent, xml_decl=self.xml_decl and self.depth == 0
        )
        return outfile.getvalue()

    def __getitem__(self, key):
        "Get the value of the attribute in this element."
        try:
            return self.attrs[key]
        except KeyError:
            raise KeyError(f"no such attribute '{key}' in element")

    def __setitem__(self, key, value):
        "Set the value of the attribute in this element."
        if not isinstance(value, str):
            value = str(value)
        self.attrs[key] = value

    def __delitem__(self, key):
        "Delete the attribute in this element."
        try:
            del self.attrs[key]
        except KeyError:
            raise KeyError(f"no such attribute '{key}' in element")

    def __contains__(self, key):
        "Does this element have the given attribute?"
        return key in self.attrs

    def __iter__(self):
        "Iterate over the subelements of this element."
        yield from self.subelements

    def __len__(self):
        "Return the number of subelements of this element."
        return len(self.subelements)

    def __eq__(self, other):
        "Are the element and its subelements equal? Ignores the superelement."
        if not isinstance(other, Element):
            return False
        if self.tag != other.tag:
            return False
        if self.attrs != other.attrs:
            return False
        if len(self) != len(other):
            return False
        for subelement1, subelement2 in zip(self.subelements, other.subelements):
            if subelement1 != subelement2:
                return False
        return True

    def __iadd__(self, other):
        self.append(other)
        return self

    def get(self, key, default=None):
        "Return the value of the given attribute in this element, or the default."
        try:
            return self[key]
        except KeyError:
            return default

    def set(self, key, value):
        "Set the value of the attribute in this element."
        self[key] = value

    @property
    def text(self):
        "Return the text content of this element. All non-blank texts are concatenated."
        result = []
        for subelement in self:
            if isinstance(subelement, str) and subelement.strip():
                result.append(subelement)
        return "".join(result)

    @property
    def superelements(self):
        "List of superelements, most immediate first."
        result = []
        elem = self
        while elem.superelement is not None:
            result.append(elem.superelement)
            elem = elem.superelement
        return result

    @property
    def depth(self):
        "Depth of hierarchy for this element; number of superelements to root."
        result = 0
        elem = self
        while elem.superelement is not None:
            result += 1
            elem = elem.superelement
        return result

    def insert(self, i, elem):
        "Insert the element at position i in the list of subelements of this element."
        assert isinstance(elem, (Element, str))
        if isinstance(elem, Element) and elem.superelement:
            raise ValueError("given element has not been freed from its superelement")
        self.subelements.insert(i, elem)
        if isinstance(elem, Element):
            elem.superelement = self

    def append(self, elem):
        "Append the element last in the subelements of this element."
        assert isinstance(elem, (Element, str))
        if isinstance(elem, Element) and elem.superelement:
            raise ValueError("given element has not been freed from its superelement")
        self.subelements.append(elem)
        if isinstance(elem, Element):
            elem.superelement = self

    def free(self):
        "Remove this element from its superelement, if any."
        self.superelement = None

    def create(self, tag, **attrs):
        """Create an element with the given tag and attributes,
        and append to the subelements of this element.
        Return the created element.
        """
        elem = Element(tag, **attrs)
        self.append(elem)
        return elem

    def copy(self):
        """Make a copy of this element and its subelements (i.e. deepcopy).
        The returned element has no superelement.
        """
        result = copy.deepcopy(self)
        result.superelement = None
        return result

    def walk(self, test=None):
        """Walk over this element and all its subelements recursively,
        yielding those elements that match the given test function.
        If no test function given, yield all.
        """
        if test is None or test(self):
            yield self
        for subelement in self:
            if not isinstance(subelement, Element):
                continue
            yield from subelement.walk(test=test)

    def write(self, outfile, indent=None, xml_decl=False):
        "Write the XML of the element and its subelements into the open file object."
        if xml_decl:
            outfile.write(f'<?xml version="1.0"?>\n')
        if indent is None:
            padding = ""
        else:
            padding = " " * indent * self.depth
        outfile.write(padding)
        outfile.write(f"<{self.tag}")
        for name, value in self.attrs.items():
            outfile.write(f" {name}={xml.sax.saxutils.quoteattr(value)}")
        if len(self):
            outfile.write(">")
            newline = False
            for elem in self:
                if isinstance(elem, Element):
                    if indent:
                        outfile.write("\n")
                    elem.write(outfile, indent=indent)
                    newline = True
                elif isinstance(elem, str):
                    outfile.write(xml.sax.saxutils.escape(elem))
                    newline = False
                else:
                    outfile.write(xml.sax.saxutils.escape(str(elem)))
                    newline = False
            if newline:
                if indent:
                    outfile.write("\n")
                outfile.write(padding)
            outfile.write(f"</{self.tag}>")
        else:
            outfile.write(" />")


class ContentHandler(xml.sax.ContentHandler):
    "Parse XML read events into Element tree."

    def __init__(self):
        self.stack = []
        self.root = None

    def startElement(self, tag, attrs):
        elem = Element(tag, **dict(attrs))
        if self.stack:
            self.stack[-1].subelements.append(elem)
            elem.superelement = self.stack[-1]
        else:
            self.root = elem
        self.stack.append(elem)

    def endElement(self, tag: str):
        self.stack.pop()

    def characters(self, content: str):
        if content.strip():
            self.stack[-1].subelements.append(xml.sax.saxutils.unescape(content))


def read(filepath_or_stream):
    """Read and parse the file given by its path, or an open file object.
    Returns the root XML element.
    """
    try:
        xml.sax.parse(filepath_or_stream, ContentHandler())
    except xml.sax.SAXException as error:
        raise ValueError(f"XML parse error: {error}")
    return content_handler.root


def parse(content):
    "Parse the given XML content. Return the root XML element."
    return read(io.StringIO(content))
