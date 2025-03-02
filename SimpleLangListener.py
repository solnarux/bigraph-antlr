# Generated from SimpleLang.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SimpleLangParser import SimpleLangParser
else:
    from SimpleLangParser import SimpleLangParser

# This class defines a complete listener for a parse tree produced by SimpleLangParser.
class SimpleLangListener(ParseTreeListener):

    # Enter a parse tree produced by SimpleLangParser#program.
    def enterProgram(self, ctx:SimpleLangParser.ProgramContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#program.
    def exitProgram(self, ctx:SimpleLangParser.ProgramContext):
        pass


    # Enter a parse tree produced by SimpleLangParser#statement.
    def enterStatement(self, ctx:SimpleLangParser.StatementContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#statement.
    def exitStatement(self, ctx:SimpleLangParser.StatementContext):
        pass


    # Enter a parse tree produced by SimpleLangParser#varDecl.
    def enterVarDecl(self, ctx:SimpleLangParser.VarDeclContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#varDecl.
    def exitVarDecl(self, ctx:SimpleLangParser.VarDeclContext):
        pass


    # Enter a parse tree produced by SimpleLangParser#assignStmt.
    def enterAssignStmt(self, ctx:SimpleLangParser.AssignStmtContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#assignStmt.
    def exitAssignStmt(self, ctx:SimpleLangParser.AssignStmtContext):
        pass


    # Enter a parse tree produced by SimpleLangParser#returnStmt.
    def enterReturnStmt(self, ctx:SimpleLangParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#returnStmt.
    def exitReturnStmt(self, ctx:SimpleLangParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by SimpleLangParser#exprStmt.
    def enterExprStmt(self, ctx:SimpleLangParser.ExprStmtContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#exprStmt.
    def exitExprStmt(self, ctx:SimpleLangParser.ExprStmtContext):
        pass


    # Enter a parse tree produced by SimpleLangParser#funcDecl.
    def enterFuncDecl(self, ctx:SimpleLangParser.FuncDeclContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#funcDecl.
    def exitFuncDecl(self, ctx:SimpleLangParser.FuncDeclContext):
        pass


    # Enter a parse tree produced by SimpleLangParser#paramList.
    def enterParamList(self, ctx:SimpleLangParser.ParamListContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#paramList.
    def exitParamList(self, ctx:SimpleLangParser.ParamListContext):
        pass


    # Enter a parse tree produced by SimpleLangParser#param.
    def enterParam(self, ctx:SimpleLangParser.ParamContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#param.
    def exitParam(self, ctx:SimpleLangParser.ParamContext):
        pass


    # Enter a parse tree produced by SimpleLangParser#block.
    def enterBlock(self, ctx:SimpleLangParser.BlockContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#block.
    def exitBlock(self, ctx:SimpleLangParser.BlockContext):
        pass


    # Enter a parse tree produced by SimpleLangParser#expr.
    def enterExpr(self, ctx:SimpleLangParser.ExprContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#expr.
    def exitExpr(self, ctx:SimpleLangParser.ExprContext):
        pass


    # Enter a parse tree produced by SimpleLangParser#type.
    def enterType(self, ctx:SimpleLangParser.TypeContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#type.
    def exitType(self, ctx:SimpleLangParser.TypeContext):
        pass


    # Enter a parse tree produced by SimpleLangParser#argList.
    def enterArgList(self, ctx:SimpleLangParser.ArgListContext):
        pass

    # Exit a parse tree produced by SimpleLangParser#argList.
    def exitArgList(self, ctx:SimpleLangParser.ArgListContext):
        pass



del SimpleLangParser