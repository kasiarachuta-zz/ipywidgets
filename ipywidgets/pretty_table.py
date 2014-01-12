import pandas

class TableStyle(object):
    """
    Keep track of styles for cells/headers in PrettyTable
    """
    def __init__(self, theme=None):
        self.row_head_style = CellStyle()
        self.col_head_style = CellStyle()
        self.cell_style = CellStyle()
        self.corner_style = CellStyle()

        # add themes as needed
        if theme == "basic":
            self.cell_style.border = "1px solid black"
            self.col_head_style.font_weight = "bold"
            self.row_head_style.font_weight = "bold"

        if theme == "theme1":
            self.cell_style.border = "1px solid black"
            self.cell_style.color = "black"
            self.col_head_style.color = "black"
            self.row_head_style.color = "black"
            self.col_head_style.font_weight = "bold"
            self.row_head_style.font_weight = "bold"
            self.col_head_style.background_color = "gray"
            self.row_head_style.background_color = "gray"
            self.corner_style.background_color = "red"

class CellStyle(object):
    """
    Styles for cells PrettyTable
    """
    
    def __init__(self):
        # add CSS features as needed
        self.background_color = None
        self.border_collapse = None
        self.border_color = None
        self.border_style = None
        self.border = None
        self.color = None
        self.font_family = None
        self.font_size = None
        self.font_style = None
        self.font_weight = None
        self.font = None

    def css(self):
        style = ""
        if self.background_color is not None:
            style += "background-color: %s;"%self.background_color
        if self.border_collapse is not None:
            style += "border-collapse: %s;"%self.border_collapse
        if self.border_color is not None:
            style += "border-color: %s;"%self.border_color
        if self.border_style is not None:
            style += "border-style: %s;"%self.border_style
        if self.border is not None:
            style += "border: %s;"%self.border
        if self.color is not None:
            style += "color: %s;"%self.color
        if self.font_family is not None:
            style += "font-family: %s;"%self.font_family
        if self.font_size is not None:
            style += "font-size: %s;"%self.font_size
        if self.font_style is not None:
            style += "font-style: %s;"%self.font_style
        if self.font_weight is not None:
            style += "font-weight: %s;"%self.font_weight
        if self.font is not None:
            style += "font: %s;"%self.font
        return style

    # Individual elements, may override later
    def table_css(self):
        return self.css()

    def row_css(self):
        return self.css()

    def column_css(self):
        return self.css()

    def column_format(self, x):
        return str(x)

class PrettyTable(object):
    """
    Formatted tables for display in IPython notebooks
    """

    def __init__(self, df, style=None, header_row=False, header_col=False):
        """
        df: pandas.DataFrame
        style: TableStyle
        header_row: include row headers
        header_col: include column headers
        """
        self.df = df
        self.num_rows = df.shape[0]
        self.num_cols = df.shape[1]
        self.header_row = header_row
        self.header_col = header_col
        self.style = style

        # overall table style
        if style is None:
            self.cell_style = CellStyle()
            self.corner_style = CellStyle()
            self.header_row_styles = [None for i in range(len(self.num_rows))]
            self.header_col_styles = [None for i in range(len(self.num_cols))]
        else:
            self.cell_style = style.cell_style
            self.corner_style = style.corner_style
            self.header_row_styles = [style.row_head_style for i in range(self.num_rows)]
            self.header_col_styles = [style.col_head_style for i in range(self.num_cols)]

        # Individual cell styles, overrides overall style
        self.cell_styles = [[None for i in range(self.num_cols)]\
                            for j in range(self.num_rows)]

    def set_cell_style(self, style, rows=None, cols=None):
        """
        Apply cell style to rows and columns specified
        """
        if rows is None: rows = range(self.num_rows)
        if cols is None: cols = range(self.num_cols)
        for i in rows:
            for j in cols:
                self.cell_styles[i][j] = style
    
    def set_row_header_style(self, style, index=None):
        """
        Apply style to header at specific index
        If index is None, apply to all headings
        """
        if index is not None:
            self.header_row_styles[index] = style
        else:
            self.header_row_styles = [style for i in range(self.num_rows)]

    def set_col_header_style(self, style, index=None):
        """
        Apply style to header at specific index
        If index is None, apply to all headings
        """
        if index is not None:
            self.header_col_styles[index] = style
        else:
            self.header_col_styles = [style for i in range(self.num_cols)]

    def _repr_html_(self):
        """
        IPython display protocol calls this method to get the
        HTML representation of the object
        """
        html = "<table style=\"%s\">"%self.cell_style.table_css()
        if self.header_col:
            html += "<tr style=\"%s\">"%self.cell_style.row_css()
            if self.header_row:
                # need to add an extra empty cell
                html += "<td style=\"%s\"></td>"%self.corner_style.css()
            for j in range(self.num_cols):
                if self.header_col_styles is not None:
                    header_style = self.header_col_styles[j].column_css()
                else: header_style = self.cell_style.column_css()
                html += "<td style=\"%s\">"%header_style
                html += self.df.columns[j]
                html += "</td>"
            html += "</tr>"
        for i in range(self.num_rows):
            html += "<tr style=\"%s\">"%self.cell_style.row_css()
            if self.header_row:
                if self.header_row_styles is not None:
                    header_style = self.header_row_styles[i].column_css()
                else: header_style = self.cell_style.column_css()
                html += "<td style=\"%s\">"%header_style
                html += str(self.df.index.values[i])
                html += "</td>"
            for j in range(self.num_cols):
                if self.cell_styles[i][j] is not None:
                    col_style = self.cell_styles[i][j].column_css()
                    col_data = self.cell_styles[i][j].column_format(self.df.iloc[i,j])
                else:
                    col_style = self.cell_style.column_css()
                    col_data = self.cell_style.column_format(self.df.iloc[i,j])
                html += "<td style=\"%s\">"%col_style
                html += col_data
                html += "</td>"
            html += "</tr>"
        html += "</table>"
        return html

    def copy(self):
        p = PrettyTable(self.df, self.style, self.header_row, self.header_col)
        p.header_row_styles = list(self.header_row_styles)
        p.header_col_styles = list(self.header_col_styles)
        p.cell_styles = [list(item) for item in self.cell_styles]
        return p

