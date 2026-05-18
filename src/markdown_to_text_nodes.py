from logic.textnode import *
from logic.htmlnode import *
from logic.blocks import *
import re



#recibo un texto en markdown y lo transformo en bloques de texto en markdown
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    res = []
    for block in blocks:
        if block != "":
            res.append(block.strip())
    return res



#recibo texto en markdown y lo transformo en TextNodes
def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = [node]
    nodes = split_nodes_delimeter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimeter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimeter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

#recibo una lista de nodos y los separo mejor en nodos de tipos bold, italic y code
def split_nodes_delimeter(old_nodes, delimeter, text_type):
    res = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            res.append(node)
            continue
        
        new_texts = node.text.split(delimeter)

        if len(new_texts) % 2 == 0:
            raise Exception(f"invalid markdown sintax, only one delimeter:{delimeter} found")
        
        text = False
        for new_t in new_texts:
            text = not text
            if new_t == '':
                continue
            if text:
                res.append(TextNode(new_t, TextType.TEXT))
            else:
                res.append(TextNode(new_t, text_type))

    return res

#recibo una lista de nodos y los separo en nodos de tipo image
def split_nodes_image(old_nodes):
    res = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            res.append(node)
            continue

        markdown_images = extract_markdown_images(node.text)
        if markdown_images == []:
            res.append(node)
            continue

        rest_of_text = node.text
        for img in markdown_images:
            alt_txt = img[0]
            link = img[1]

            parts = rest_of_text.split(f"![{alt_txt}]({link})", 1)
            rest_of_text = parts[1]

            res.append(TextNode(parts[0], TextType.TEXT))
            res.append(TextNode(alt_txt, TextType.IMAGE, link))

        if parts[1] != "":
            res.append(TextNode(rest_of_text, TextType.TEXT))
    return res

#recibo una lista de nodos y los separo en nodos de tipo link
def split_nodes_link(old_nodes):
    res = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            res.append(node)
            continue

        markdown_images = extract_markdown_links(node.text)
        if markdown_images == []:
            res.append(node)
            continue 

        rest_of_text = node.text
        for link in markdown_images:
            alt_txt = link[0]
            txt_link = link[1]

            parts = rest_of_text.split(f"[{alt_txt}]({txt_link})", 1)
            rest_of_text = parts[1]

            res.append(TextNode(parts[0], TextType.TEXT))
            res.append(TextNode(alt_txt, TextType.LINK, txt_link))

        if parts[1] != "":
            res.append(TextNode(rest_of_text, TextType.TEXT))
    return res

#funciones para extraer imagenes y links de un texto en markdown
def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)


