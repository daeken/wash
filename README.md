What is it?
===========

W|ASH is an interactive terminal for Wolfram|Alpha.  Some of the features:

- Query history
- Partial statefulness
- Clean output format

Installation
============

Installing is as easy as:

    pip install wash


Statefulness
============

The last `Result` pod will always be stored as `$$`.  So you can do:

    W|A> 4 + 5
      Result
        9
      [...]
    W|A> 10 + $$
      Result
        19

It will automatically be parenthesized, so you don't have to worry about symbols colliding.

In addition, the Result pod is often suffixed with extraneous details.  Where possible, we will remove this to ensure seamless functionality.

Saving Workbooks
================

The history of the commands you run (and their results) in a given session is called a workbook.  These can be output as either HTML or Markdown using the `save` command.

- `save <filename>.html` will always save HTML format
- Any other extension will save as Markdown

Credits
=======

Code and initial design by Cody Brocious (Daeken).  Huge thanks to John Trainer (NightMiles) for help with design of HTML workbooks.
