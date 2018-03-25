# Turing Script? Tasm? TsCode?
___

As of right now, this compiler tarets a pure standard turing machine. This is
likely to change in the future.

Instructions:
 * Ignore instructions: These move the tape head without writing
    * IRU(char) -> Ignore Right Until Char. This by default will put the tape
      head one to the right of the char
    * IRC(int) -> Ignore Right for exactly int characters
    * IRU and IRC have left-moving variants, ILU and ILC

* WRT(string) -> Writes the string char by char to the tape at the current position, moving
  to the right

This code also implements branching:
```
if (char) {
    ...
}
else 
{
    ...
}
```
It's worth noting that as of right now, the if statement implicitly moves to
the right, as standard turing machines must  move in some direction on reading
a character.


