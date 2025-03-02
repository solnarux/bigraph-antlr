grammar SimpleLang;

// Reglas de producción
program      : (statement)* EOF;
statement    : varDecl | assignStmt | funcDecl | returnStmt | exprStmt;
varDecl      : 'let' ID ':' type '=' expr ';';
assignStmt   : ID '=' expr ';';
returnStmt   : 'return' expr ';';
exprStmt     : expr ';';

funcDecl     : 'fn' ID '(' paramList? ')' '->' type block;
paramList    : param (',' param)*;
param        : ID ':' type;

block        : '{' (statement)* '}';

expr         : expr ('+' | '-') expr 
             | expr ('*' | '/') expr 
             | '(' expr ')' 
             | NUMBER 
             | ID;

type         : 'int' | 'float' | 'void';

// Tokens
ID           : [a-zA-Z_][a-zA-Z0-9_]*;
NUMBER       : [0-9]+ ('.' [0-9]+)?;
WS           : [ \t\r\n]+ -> skip;
