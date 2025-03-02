# Generated from SimpleLang.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SimpleLangParser import SimpleLangParser
else:
    from SimpleLangParser import SimpleLangParser

# This class defines a complete generic visitor for a parse tree produced by SimpleLangParser.

class SimpleLangVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SimpleLangParser#program.
    def visitProgram(self, ctx:SimpleLangParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleLangParser#statement.
    def visitStatement(self, ctx:SimpleLangParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleLangParser#varDecl.
    def visitVarDecl(self, ctx:SimpleLangParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleLangParser#assignStmt.
    def visitAssignStmt(self, ctx:SimpleLangParser.AssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleLangParser#returnStmt.
    def visitReturnStmt(self, ctx:SimpleLangParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleLangParser#exprStmt.
    def visitExprStmt(self, ctx:SimpleLangParser.ExprStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleLangParser#funcDecl.
    def visitFuncDecl(self, ctx:SimpleLangParser.FuncDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleLangParser#paramList.
    def visitParamList(self, ctx:SimpleLangParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleLangParser#param.
    def visitParam(self, ctx:SimpleLangParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleLangParser#block.
    def visitBlock(self, ctx:SimpleLangParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleLangParser#expr.
    def visitExpr(self, ctx:SimpleLangParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleLangParser#type.
    def visitType(self, ctx:SimpleLangParser.TypeContext):
        return self.visitChildren(ctx)



del SimpleLangParser