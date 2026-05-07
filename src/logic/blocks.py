from enum import Enum

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


