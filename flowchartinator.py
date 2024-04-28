from pycparser.c_parser import CParser
from pycparser.c_generator import CGenerator
from pycparser.c_ast import *
from pycparser import parse_file
from sys import argv
import random

pool = []
def random_color():
    global pool
    if not pool:
        pool = ["#ff595e","#ff924c","#ffca3a","#c5ca30","#8ac926","#52a675","#1982c4","#4267ac","#6a4c93","#b5a6c9"]
    color = random.choice(pool)
    pool.remove(color)
    return color

def html_template(body):
    return f''' 
<html>
  <head>
    <link rel="stylesheet" type="text/css" href="style.css" />
  </head>
  <body>
      {body}
  </body>
</html>
    '''

def html(node):
    if isinstance(node, EmptyStatement):
        return f''
    if isinstance(node, Break):
        return f'<div class="block" style="background-color:{random_color()}"> BREAK </div>'
    if isinstance(node, Return):
        return f'<div class="block" style="background-color:{random_color()}"> RETURN {CGenerator().visit(node.expr)} </div>'
    if isinstance(node, FuncDef):
        return html_template(f'<h1> {CGenerator().visit(node.decl)} </h1> {html(node.body)} ')
    if isinstance(node, Compound):
        return f'<div class="column"> {"".join(html(item) for item in node.block_items)} </div>'
    if isinstance(node, If):
        return f'''
<div class="column">
    {html(node.cond)}
    <div class="row">
        <div class="column">
            <div class="yes"> YES </div> {html(node.iftrue)}
        </div>
        <div class="column">
            <div class="no"> NO </div> {html(node.iffalse) if node.iffalse else ''}
        </div>
    </div>
</div>
'''
    if isinstance(node, While):
        return f'''
<div class="row">
    <div class="strip"> LOOP </div>
    <div class="column">
        {html(node.cond)}
        <div class="row">
            <div class="column" style="border-bottom: 8px solid white;">
                <div class="yes"> YES </div>
                {html(node.stmt)}
            </div>
            <div class="column">
                <div class="no"> NO </div>
            </div>
        </div>
    </div>
</div>
'''
    if isinstance(node, For):
        return f'''
<div class="column">
    {html(node.init)}
    <div class="row">
        <div class="strip"> LOOP </div>
        <div class="column">
            {html(node.cond)} 
            <div class="row">
                <div class="column" style="border-bottom: 8px solid white;">
                    <div class="yes"> YES </div>
                    {html(node.stmt)}
                    {html(node.next)}
                </div>
                <div class="column">
                    <div class="no"> NO </div>
                </div>
            </div>
        </div>
    </div>
</div>
'''
    if isinstance(node, DoWhile):
        return f'''
<div class="row">
    <div class="strip"> LOOP </div>
    <div class="column">
        {html(node.stmt)}
        {html(node.cond)} 
        <div class="row">
            <div class="column" style="border-bottom: 8px solid white;">
                <div class="yes"> YES </div>
            </div>
            <div class="column">
                <div class="no"> NO </div>
            </div>
        </div>
    </div>
</div>
'''
    return f'<div class="block" style="background-color:{random_color()}"> {CGenerator().visit(node)} </div>'

declarations = parse_file(argv[1]).ext
for declaration in declarations:
    print(html(declaration))
