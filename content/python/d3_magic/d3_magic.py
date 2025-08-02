from urllib.parse import quote

from IPython.core.magic import register_cell_magic
from IPython.core.magic_arguments import (
    argument,
    magic_arguments,
    parse_argstring,
)
from IPython.display import HTML


@magic_arguments()
@argument("-h", "--height", default="350px", help="Height of the output area")
@argument("-w", "--width", default="100%", help="Width of the output area")
@argument(
    "-s", "--style", default="border: none", help="Style of the output area"
)
@argument("-v", "--version", default="4.13.0", help="D3.js version")
@argument(
    "-i",
    "--integrity",
    default=None,
    help="Integrity hash for d3.js; when changing version provide one for security",
)
@argument(
    "-c",
    "--cdn",
    default="https://cdnjs.cloudflare.com/ajax/libs/d3",
    help="CDN address",
)
@register_cell_magic
def d3(line, cell):
    args = parse_argstring(d3, line)
    known_versions = {
        "4.13.0": "sha512-RJJ1NNC88QhN7dwpCY8rm/6OxI+YdQP48DrLGe/eSAd+n+s1PXwQkkpzzAgoJe4cZFW2GALQoxox61gSY2yQfg=="
    }
    if not args.integrity:
        args.integrity = known_versions.get(args.version, "")
    integrity = (
        'integrity="{}"'.format(args.integrity) if args.integrity else ""
    )

    content = quote(
        """
        <html>
            <body>
            <script src='{args.cdn}/{args.version}/d3.min.js' {integrity} crossorigin="anonymous"></script>
            <script>document.body.onload = function () {{ {code} }}</script>
            </body>
        </html>
        """.format(
            code=cell, args=args, integrity=integrity
        ),
        safe="",
    )
    html = """
    <iframe
        style="{args.style}"
        width="{args.width}"
        height="{args.height}"
        sandbox="allow-scripts allow-modals"
        referrerpolicy="no-referrer"
        src="data:text/html;charset=UTF-8,{content}"
    ></iframe>
    """.format(
        content=content, args=args
    )
    return HTML(html)
