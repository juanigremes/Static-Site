



class HTMLNode():

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html no esta implementado en HTMLNode")

    def props_to_html(self):
        res = ""
        if self.props != None:
            for clave in self.props:
                valor = self.props[clave]
                res += f" {clave}=\"{valor}\""
        return res

    def __repr__(self):
        return(f"tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props_to_html()}")


class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        if value == None:
            raise ValueError("LeafNode must have a value != None")
        super().__init__(tag, value, None, props)

    def to_html(self):
        res = self.value
        if self.tag != None:
            res = f"<{self.tag}{self.props_to_html()}>{res}</{self.tag}>"
        return res

    def __repr__(self):
        return(f"tag = {self.tag}, value = {self.value}, props = {self.props_to_html()}")


class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        if tag == None:
            raise ValueError("ParentNode must have a tag")
        if children == None:
            raise ValueError("ParentNode must have children")
        super().__init__(tag, None, children, props)

    def to_html(self):
        res = ""
        for child in self.children:
            res += child.to_html()
        res = f"""<{self.tag}{self.props_to_html()}>{res}</{self.tag}>"""
        return res
