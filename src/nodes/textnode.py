from enum import Enum
from src.nodes.htmlnode import LeafNode
import re



class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url


    def __eq__(self, other):
        res = False
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            res = True
        return res


    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"




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



def split_nodes_delimeter(old_nodes, delimeter, text_type):
    res = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            res.append(node)
            continue
        
        new_texts = node.text.split(delimeter)

        if len(new_texts) % 2 == 0:
            raise Exception(f"invalid markdown sintax, only one delimeter:{delimeter} found")
        
        text = True
        for new_t in new_texts:
            if new_t == '':
                break
            if text:
                res.append(TextNode(new_t, TextType.TEXT))
                text = False
            else:
                res.append(TextNode(new_t, text_type))
                text = True

    return res


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)


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



def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = [node]
    nodes = split_nodes_delimeter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimeter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimeter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes



def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    res = []
    for block in blocks:
        if block != "":
            res.append(block.strip())
    return res



class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def block_to_block_type(block):
    res = BlockType.PARAGRAPH
    
    if is_heading(block):
        res = BlockType.HEADING
    
    elif is_code(block):
        res = BlockType.CODE
    
    elif is_quote(block):
        res = BlockType.QUOTE
    
    elif is_unordered_list(block):
        res = BlockType.UNORDERED_LIST
    
    elif is_ordered_list(block):
        res = BlockType.ORDERED_LIST
    
    return res

def is_heading(block):
    cant_numerales = 0
    block_len = len(block)
    for i in range(block_len):
        char = block[i]
        if char == '#':
            cant_numerales += 1
            if cant_numerales > 6:
                return False
        else:
            break
    if char != " ":
        return False
    if i == block_len:
        return False
    return True

def is_code(block):
    cant_backticks = 0
    block_len = len(block)
    if block_len <= 6:
        return False
    for i in range(block_len):
        char = block[i]
        if char =='`':
            cant_backticks += 1
            if cant_backticks > 3:
                return False
        else:
            break
    if cant_backticks != 3 or char != '\n':
        return False
    for j in range(1,4):
        if block[block_len-j] == '`':
            cant_backticks -= 1
    if cant_backticks != 0:
        return False
    return True

def is_quote(block):
    if block[0] == '>':
        return True
    return False

def is_unordered_list(block):
    lines = block.split('\n')
    for line in lines:
        if line == '':
            continue
        if len(line) < 2:
            return False
        if line[0] != '-':
            return False
        if line[1] != ' ':
            return False
    return True

def is_ordered_list(block):
    lines = block.split('\n')
    index = 1
    for line in lines:
        if line == '':
            continue
        if len(line) < 3:
            return False
        if line[0] != f"{index}":
            return False
        if line[1] != '.':
            return False
        if line[2] != ' ':
            return False
        index += 1
    return True
