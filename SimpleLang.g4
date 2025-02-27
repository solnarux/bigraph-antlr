grammar SimpleLang;

// Reglas de producción
program     : (statement)* EOF;
statement   : varDecl | assignStmt | exprStmt;
varDecl     : 'let' ID '=' expr ';';
assignStmt  : ID '=' expr ';';
exprStmt    : expr ';';
expr        : expr ('+' | '-') expr 
            | expr ('*' | '/') expr 
            | '(' expr ')' 
            | NUMBER 
            | ID;

// Tokens
ID          : [a-zA-Z_][a-zA-Z0-9_]*;
NUMBER      : [0-9]+;
WS          : [ \t\r\n]+ -> skip;
