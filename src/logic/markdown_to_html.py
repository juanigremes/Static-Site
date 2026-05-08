from src.logic.markdown_to_text_nodes import *
from src.logic.textnode import *
from src.logic.htmlnode import *
from src.logic.blocks import *



def markdown_to_html_node(markdown):
    bloques_de_md = markdown_to_blocks(markdown)
    
    bloques_en_html = []
    for bloque in bloques_de_md:
        
        tipo_del_bloque = block_to_block_type(bloque)
        if tipo_del_bloque == BlockType.CODE:
            bloque = bloque.strip("```").replace("\n", '', 1)

            code_text_node = TextNode(bloque, TextType.CODE)
            contenido_en_html = [text_node_to_html_node(code_text_node)]

        elif tipo_del_bloque == BlockType.UNORDERED_LIST or tipo_del_bloque == BlockType.ORDERED_LIST:
            contenido_en_html = block_list_to_html_nodes(bloque, tipo_del_bloque)

        else:
            bloque = bloque.replace('\n', ' ')
            contenido_en_text_nodes = text_to_textnodes(bloque)    
                
            contenido_en_html = []
            for t_node in contenido_en_text_nodes:
                html_node = text_node_to_html_node(t_node)
                contenido_en_html.append(html_node)


        parent = create_parent_node(tipo_del_bloque, contenido_en_html, bloque)
        bloques_en_html.append(parent)

    div = ParentNode("div", bloques_en_html)

    return div


def create_parent_node(block_type, children, block):
    #paragraph, heading, code, quote, u_list, o_list
    if block_type == BlockType.PARAGRAPH:
        return ParentNode("p", children)
    elif block_type == BlockType.HEADING:
        number = heading_type(block)
        return ParentNode(f"h{number}", children)
    elif block_type == BlockType.CODE:
        return ParentNode("pre", children)
    elif block_type == BlockType.QUOTE:
        return ParentNode("blockquote", children)
    elif block_type == BlockType.UNORDERED_LIST:
        return ParentNode("ul", children)
    elif block_type == BlockType.ORDERED_LIST:
        return ParentNode("ol", children)

def heading_type(block):
    for i in range(0,7):
        if block[i] != '#':
            return i


#recibo un TextNode y lo transformo en HTMLNode
def text_node_to_html_node(text_node):
    
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_type.url, "alt":"alternative text"})

def block_list_to_html_nodes(block, block_type):
    res = []
    list_items = block.split("\n")

    for item in list_items:
        if block_type == BlockType.ORDERED_LIST:
            item = item[3:]
        else:
            item = item[2:]
        html_li = LeafNode("li", item)
        res.append(html_li)

    return res
